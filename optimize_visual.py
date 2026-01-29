#!/usr/bin/env python3
"""
Automated Visual Similarity Optimizer

Iteratively adjusts CV generation parameters to achieve 100% pixel-perfect
similarity with the objective PDF through automated parameter tuning.
"""

import subprocess
import json
import numpy as np
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Tuple, List
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VisualOptimizer:
    """Automated optimizer for achieving pixel-perfect visual similarity."""
    
    def __init__(
        self,
        objective_pdf: str = "pdfs/objective/Objetivo_No_editar.pdf",
        generated_pdf: str = "outputs/Nicolas_Fredes_CV.pdf",
        dpi: int = 300,
        max_iterations: int = 100,
        target_similarity: float = 99.5
    ):
        self.objective_pdf = Path(objective_pdf)
        self.generated_pdf = Path(generated_pdf)
        self.dpi = dpi
        self.max_iterations = max_iterations
        self.target_similarity = target_similarity
        
        self.iteration = 0
        self.history: List[Dict] = []
        
    def generate_pdf(self) -> bool:
        """Generate CV PDF using main.py."""
        try:
            result = subprocess.run(
                ["python3", "main.py"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return False
    
    def load_images(self) -> Tuple[np.ndarray, np.ndarray]:
        """Load both PDFs as high-resolution images."""
        logger.info(f"Loading PDFs at {self.dpi} DPI...")
        
        obj = convert_from_path(str(self.objective_pdf), dpi=self.dpi)[0]
        gen = convert_from_path(str(self.generated_pdf), dpi=self.dpi)[0]
        
        # Ensure same size
        if gen.size != obj.size:
            gen = gen.resize(obj.size, Image.Resampling.LANCZOS)
        
        return np.array(obj), np.array(gen)
    
    def calculate_similarity(self, obj_arr: np.ndarray, gen_arr: np.ndarray) -> float:
        """Calculate pixel-perfect similarity percentage."""
        diff = np.sum(np.abs(obj_arr.astype(int) - gen_arr.astype(int)))
        max_diff = obj_arr.shape[0] * obj_arr.shape[1] * 3 * 255
        similarity = 100 * (1 - diff / max_diff)
        return similarity
    
    def analyze_differences(
        self, 
        obj_arr: np.ndarray, 
        gen_arr: np.ndarray
    ) -> Dict:
        """Analyze pixel differences to identify adjustment areas."""
        diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
        diff_gray = diff.sum(axis=2)
        
        height, width = obj_arr.shape[:2]
        
        # Analyze by regions
        regions = {
            "top_header": (0, int(height * 0.1)),
            "contact_info": (int(height * 0.1), int(height * 0.15)),
            "education": (int(height * 0.15), int(height * 0.35)),
            "experience": (int(height * 0.35), int(height * 0.75)),
            "skills_bottom": (int(height * 0.75), height)
        }
        
        region_analysis = {}
        for name, (y_start, y_end) in regions.items():
            region_diff = np.sum(diff[y_start:y_end, :])
            region_pixels = (y_end - y_start) * width * 3
            region_pct = (region_diff / region_pixels) * 100 if region_pixels > 0 else 0
            region_analysis[name] = {
                "diff_percentage": float(region_pct),
                "y_start_pts": (y_start / height) * 806.0,
                "y_end_pts": (y_end / height) * 806.0
            }
        
        # Find most problematic rows (for Y-offset adjustment)
        row_diffs = diff_gray.sum(axis=1)
        worst_row = int(np.argmax(row_diffs))
        worst_row_pts = (worst_row / height) * 806.0
        
        # Horizontal analysis
        sidebar_width = int(width * 0.25)
        sidebar_diff = np.sum(diff[:, :sidebar_width])
        content_diff = np.sum(diff[:, sidebar_width:])
        
        return {
            "regions": region_analysis,
            "worst_row_pixel": worst_row,
            "worst_row_pts": float(worst_row_pts),
            "sidebar_diff_pct": float((sidebar_diff / (height * sidebar_width * 3)) * 100),
            "content_diff_pct": float((content_diff / (height * (width - sidebar_width) * 3)) * 100),
            "total_diff_pixels": int(np.sum(diff_gray > 0))
        }
    
    def suggest_adjustments(self, analysis: Dict, current_offset: float) -> Dict:
        """Suggest parameter adjustments based on analysis."""
        adjustments = {}
        
        # Analyze which region has most differences
        regions = analysis["regions"]
        max_diff_region = max(regions.items(), key=lambda x: x[1]["diff_percentage"])
        
        logger.info(f"Most problematic region: {max_diff_region[0]} ({max_diff_region[1]['diff_percentage']:.2f}%)")
        
        # Suggest Y offset adjustment if vertical misalignment detected
        worst_row_pts = analysis["worst_row_pts"]
        
        # Simple heuristic: if worst area is in top half, increase offset; if bottom, decrease
        if worst_row_pts < 403.0:  # Top half
            suggested_offset = current_offset + 0.5
        else:  # Bottom half
            suggested_offset = current_offset - 0.5
        
        adjustments["y_global_offset"] = suggested_offset
        
        return adjustments
    
    def apply_adjustments(self, adjustments: Dict) -> bool:
        """Apply parameter adjustments to config.py."""
        config_path = Path("src/config.py")
        
        try:
            with open(config_path, 'r') as f:
                content = f.read()
            
            # Apply Y_GLOBAL_OFFSET adjustment
            if "y_global_offset" in adjustments:
                new_offset = adjustments["y_global_offset"]
                # Replace the Y_GLOBAL_OFFSET line
                import re
                pattern = r'Y_GLOBAL_OFFSET:\s*float\s*=\s*[\d.]+' 
                replacement = f'Y_GLOBAL_OFFSET: float = {new_offset:.1f}'
                content = re.sub(pattern, replacement, content)
                
                logger.info(f"Adjusted Y_GLOBAL_OFFSET to {new_offset:.1f}")
            
            with open(config_path, 'w') as f:
                f.write(content)
            
            return True
        except Exception as e:
            logger.error(f"Failed to apply adjustments: {e}")
            return False
    
    def create_comparison_image(
        self,
        obj_arr: np.ndarray,
        gen_arr: np.ndarray,
        similarity: float,
        iteration: int
    ) -> None:
        """Create visual comparison image for this iteration."""
        height, width = obj_arr.shape[:2]
        
        # Create side-by-side comparison
        comparison = Image.new('RGB', (width * 2 + 40, height + 100), 'white')
        
        obj_img = Image.fromarray(obj_arr)
        gen_img = Image.fromarray(gen_arr)
        
        comparison.paste(obj_img, (0, 80))
        comparison.paste(gen_img, (width + 40, 80))
        
        draw = ImageDraw.Draw(comparison)
        
        # Add labels
        draw.text((width // 2 - 100, 20), f"OBJETIVO", fill='red')
        draw.text((width + width // 2 - 60, 20), f"GENERADO", fill='blue')
        draw.text((width, 50), f"Iteration {iteration} - Similarity: {similarity:.2f}%", fill='black')
        
        # Save
        output_path = f"outputs/iteration_{iteration:04d}_similarity_{similarity:.2f}.png"
        comparison.save(output_path)
        logger.info(f"Saved comparison: {output_path}")
    
    def run_iteration(self) -> Tuple[float, Dict]:
        """Run one optimization iteration."""
        self.iteration += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"ITERATION {self.iteration}/{self.max_iterations}")
        logger.info(f"{'='*60}")
        
        # Generate PDF
        if not self.generate_pdf():
            logger.error("PDF generation failed")
            return 0.0, {}
        
        # Load images
        obj_arr, gen_arr = self.load_images()
        
        # Calculate similarity
        similarity = self.calculate_similarity(obj_arr, gen_arr)
        logger.info(f"📊 Current similarity: {similarity:.4f}%")
        
        # Analyze differences
        analysis = self.analyze_differences(obj_arr, gen_arr)
        
        # Create comparison image
        self.create_comparison_image(obj_arr, gen_arr, similarity, self.iteration)
        
        # Record history
        self.history.append({
            "iteration": self.iteration,
            "similarity": similarity,
            "analysis": analysis
        })
        
        return similarity, analysis
    
    def optimize(self) -> Dict:
        """Run full optimization loop until target similarity reached."""
        logger.info("🚀 Starting automated visual optimization...")
        logger.info(f"Target: {self.target_similarity}% similarity")
        logger.info(f"Max iterations: {self.max_iterations}")
        
        # Read current offset
        with open("src/config.py", 'r') as f:
            content = f.read()
            import re
            match = re.search(r'Y_GLOBAL_OFFSET:\s*float\s*=\s*([\d.]+)', content)
            current_offset = float(match.group(1)) if match else 32.0
        
        best_similarity = 0.0
        best_offset = current_offset
        
        for i in range(self.max_iterations):
            similarity, analysis = self.run_iteration()
            
            # Check if target reached
            if similarity >= self.target_similarity:
                logger.info(f"\n🎯 TARGET REACHED! {similarity:.4f}% >= {self.target_similarity}%")
                break
            
            # Track best
            if similarity > best_similarity:
                best_similarity = similarity
                best_offset = current_offset
                logger.info(f"✅ New best: {best_similarity:.4f}%")
            
            # Suggest and apply adjustments
            adjustments = self.suggest_adjustments(analysis, current_offset)
            
            if not self.apply_adjustments(adjustments):
                logger.error("Failed to apply adjustments")
                break
            
            current_offset = adjustments.get("y_global_offset", current_offset)
            
            # Save progress
            with open("outputs/optimization_history.json", 'w') as f:
                json.dump(self.history, f, indent=2)
        
        # Final report
        logger.info(f"\n{'='*60}")
        logger.info(f"OPTIMIZATION COMPLETE")
        logger.info(f"{'='*60}")
        logger.info(f"Best similarity achieved: {best_similarity:.4f}%")
        logger.info(f"Best Y_GLOBAL_OFFSET: {best_offset:.1f}")
        logger.info(f"Total iterations: {self.iteration}")
        logger.info(f"History saved: outputs/optimization_history.json")
        
        return {
            "best_similarity": best_similarity,
            "best_offset": best_offset,
            "total_iterations": self.iteration,
            "history": self.history
        }


def main():
    """Entry point for automated optimization."""
    optimizer = VisualOptimizer(
        dpi=300,
        max_iterations=100,
        target_similarity=99.5
    )
    
    results = optimizer.optimize()
    
    print(f"\n{'='*60}")
    print(f"FINAL RESULTS")
    print(f"{'='*60}")
    print(f"Best Similarity: {results['best_similarity']:.4f}%")
    print(f"Best Y Offset: {results['best_offset']:.1f} pts")
    print(f"Iterations Run: {results['total_iterations']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
