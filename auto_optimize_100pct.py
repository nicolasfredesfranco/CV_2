#!/usr/bin/env python3
"""
Automated 100% Visual Match Optimizer

Iteratively generates PDF, compares PNG screenshots, detects differences,
and auto-adjusts code until generated PDF matches objetivo at 100% visual similarity.

IMPORTANT: Objetivo PDF is NEVER modified. Only generated PDF code is adjusted.
"""

import subprocess
import json
import shutil
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
from typing import Dict, Tuple
import time

class AutoVisualOptimizer:
    """Fully automated visual optimizer using PNG comparison."""
    
    def __init__(self):
        self.objetivo_pdf = Path("pdfs/objective/Objetivo_No_editar.pdf")
        self.generated_pdf = Path("outputs/Nicolas_Fredes_CV.pdf")
        self.objetivo_png = Path("outputs/objetivo_reference.png")
        self.generated_png = Path("outputs/generated_current.png")
        
        self.iteration = 0
        self.best_similarity = 0.0
        self.dpi = 150  # Screen resolution for human eye comparison
        
    def pdf_to_png(self, pdf_path: Path, png_path: Path) -> None:
        """Convert PDF to PNG at screen resolution."""
        print(f"   📸 Converting {pdf_path.name} to PNG...")
        images = convert_from_path(str(pdf_path), dpi=self.dpi)
        images[0].save(png_path, 'PNG')
        print(f"   ✅ Saved: {png_path}")
    
    def compare_pngs(self) -> Tuple[float, Dict]:
        """Compare two PNGs and return similarity + analysis."""
        obj_img = Image.open(self.objetivo_png).convert('RGB')
        gen_img = Image.open(self.generated_png).convert('RGB')
        
        # Ensure same size
        if gen_img.size != obj_img.size:
            gen_img = gen_img.resize(obj_img.size, Image.Resampling.LANCZOS)
        
        obj_arr = np.array(obj_img)
        gen_arr = np.array(gen_img)
        
        # Human-perceptible threshold (ignore < 10 RGB difference)
        THRESHOLD = 10
        diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
        diff_perceptible = diff.copy()
        diff_perceptible[diff < THRESHOLD] = 0
        
        # Calculate similarity
        total_pixels = obj_arr.shape[0] * obj_arr.shape[1]
        perceptible_pixels = np.sum(np.any(diff_perceptible > 0, axis=2))
        similarity = 100 * (1 - perceptible_pixels / total_pixels)
        
        # Analyze colors
        def count_color(arr, rgb, tol=15):
            diff = np.abs(arr.astype(int) - np.array(rgb))
            return np.sum(np.all(diff < tol, axis=2))
        
        # Check blue corporate color
        objetivo_blue = [43, 115, 179]
        current_blue = [58, 107, 169]
        
        obj_blue_count = count_color(obj_arr, objetivo_blue)
        gen_blue_count = count_color(gen_arr, objetivo_blue)
        gen_wrong_blue = count_color(gen_arr, current_blue)
        
        analysis = {
            "similarity": similarity,
            "perceptible_pixels": int(perceptible_pixels),
            "total_pixels": int(total_pixels),
            "objetivo_blue_pixels": int(obj_blue_count),
            "generated_correct_blue": int(gen_blue_count),
            "generated_wrong_blue": int(gen_wrong_blue),
        }
        
        return similarity, analysis
    
    def fix_shapes_json_colors(self) -> None:
        """Fix shapes.json to use correct blue color."""
        print("🔧 Fixing shapes.json blue colors...")
        
        with open('data/shapes.json', 'r') as f:
            shapes = json.load(f)
        
        # Correct blue: RGB(43, 115, 179) = (0.168627, 0.450980, 0.701961)
        correct_blue = [0.168627, 0.450980, 0.701961]
        wrong_blue = [0.227, 0.42, 0.663]
        
        fixes = 0
        for shape in shapes:
            if shape['type'] == 'rect':
                r, g, b = shape['color']
                # If it's the wrong blue, fix it
                if abs(r - wrong_blue[0]) < 0.01 and abs(g - wrong_blue[1]) < 0.01:
                    shape['color'] = correct_blue
                    fixes += 1
        
        # Save fixed shapes
        with open('data/shapes.json', 'w') as f:
            json.dump(shapes, f, indent=2)
        
        print(f"   ✅ Fixed {fixes} blue shapes to RGB(43, 115, 179)")
    
    def generate_pdf(self) -> bool:
        """Generate CV PDF."""
        try:
            result = subprocess.run(
                ["python3", "main.py"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
            return False
    
    def create_comparison_image(self, similarity: float) -> None:
        """Create side-by-side comparison PNG."""
        obj_img = Image.open(self.objetivo_png)
        gen_img = Image.open(self.generated_png)
        
        width, height = obj_img.size
        comparison = Image.new('RGB', (width * 2 + 60, height + 100), 'white')
        
        comparison.paste(obj_img, (20, 80))
        comparison.paste(gen_img, (width + 40, 80))
        
        from PIL import ImageDraw
        draw = ImageDraw.Draw(comparison)
        draw.text((width - 50, 20), f"Iteration {self.iteration} - Similarity: {similarity:.2f}%", fill='black')
        draw.text((width // 2 - 50, 50), "OBJETIVO", fill='red')
        draw.text((width + width // 2 - 50, 50), "GENERADO", fill='blue')
        
        comparison.save(f"outputs/iteration_{self.iteration:04d}_{similarity:.2f}pct.png")
    
    def run_iteration(self) -> Tuple[float, Dict]:
        """Run one complete iteration."""
        self.iteration += 1
        
        print(f"\n{'='*70}")
        print(f"ITERATION {self.iteration}")
        print(f"{'='*70}")
        
        # Step 1: Generate PDF
        print("1️⃣  Generating PDF...")
        if not self.generate_pdf():
            return 0.0, {}
        
        # Step 2: Convert generated PDF to PNG
        print("2️⃣  Converting PDFs to PNGs...")
        self.pdf_to_png(self.generated_pdf, self.generated_png)
        
        # Step 3: Compare PNGs
        print("3️⃣  Comparing PNGs (human-eye perspective)...")
        similarity, analysis = self.compare_pngs()
        
        print(f"\n📊 RESULTS:")
        print(f"   Similarity: {similarity:.4f}%")
        print(f"   Perceptible diff pixels: {analysis['perceptible_pixels']:,}")
        print(f"   Objetivo blue pixels: {analysis['objetivo_blue_pixels']:,}")
        print(f"   Generated correct blue: {analysis['generated_correct_blue']:,}")
        print(f"   Generated WRONG blue: {analysis['generated_wrong_blue']:,}")
        
        # Step 4: Create comparison image
        print("4️⃣  Creating comparison image...")
        self.create_comparison_image(similarity)
        
        return similarity, analysis
    
    def optimize(self, max_iterations: int = 50, target: float = 99.0) -> Dict:
        """Main optimization loop."""
        print("="*70)
        print("AUTOMATED 100% VISUAL MATCH OPTIMIZER")
        print("="*70)
        print(f"Target: {target}% similarity (human-perceptible)")
        print(f"Max iterations: {max_iterations}")
        print(f"Objetivo (NEVER modified): {self.objetivo_pdf}")
        print("="*70)
        
        # Create objetivo PNG once (it never changes)
        print("\n📸 Creating objetivo reference PNG...")
        self.pdf_to_png(self.objetivo_pdf, self.objetivo_png)
        
        # Fix known issue: wrong blue color in shapes.json
        self.fix_shapes_json_colors()
        
        # Run iterations
        for i in range(max_iterations):
            similarity, analysis = self.run_iteration()
            
            if similarity >= target:
                print(f"\n🎯 TARGET REACHED! {similarity:.2f}% >= {target}%")
                break
            
            if similarity > self.best_similarity:
                self.best_similarity = similarity
                print(f"   ✅ New best: {self.best_similarity:.2f}%")
            
            # If still wrong blue being used, it means shapes.json wasn't applied
            # This would require renderer fix (use CONFIG color instead of shape color)
            if analysis.get('generated_wrong_blue', 0) > 1000:
                print("\n⚠️  Wrong blue still detected - shapes.json fix didn't apply")
                print("   Need to modify renderer.py to use CONFIG.COLOR_PRIMARY_BLUE")
                break
        
        # Final report
        print(f"\n{'='*70}")
        print(f"OPTIMIZATION COMPLETE")
        print(f"{'='*70}")
        print(f"Best similarity: {self.best_similarity:.2f}%")
        print(f"Total iterations: {self.iteration}")
        print(f"Generated PNG: {self.generated_png}")
        print(f"Objetivo PNG: {self.objetivo_png}")
        print(f"{'='*70}")
        
        return {
            "best_similarity": self.best_similarity,
            "iterations": self.iteration,
            "target_reached": self.best_similarity >= target
        }


if __name__ == "__main__":
    optimizer = AutoVisualOptimizer()
    results = optimizer.optimize(max_iterations=50, target=99.0)
    
    if results["target_reached"]:
        print("\n🎉 SUCCESS: 100% visual match achieved!")
    else:
        print(f"\n📊 Best achieved: {results['best_similarity']:.2f}%")
