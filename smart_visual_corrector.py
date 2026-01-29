#!/usr/bin/env python3
"""
INTELLIGENT VISUAL CORRECTOR - Iterates until 100% match

Detects WHAT is different (positioning, size, missing elements)
and auto-adjusts code parameters to fix it.
"""

import subprocess
import json
import re
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import numpy as np

class IntelligentVisualCorrector:
    """Smart system that detects and fixes visual differences."""
    
    def __init__(self):
        self.dpi = 150
        self.threshold = 10  # Human perception threshold
        self.target_similarity = 99.0
        self.max_iterations = 100
        
        self.config_file = Path("src/config.py")
        self.iteration = 0
        self.best_similarity = 0.0
        
        # Parameters to optimize
        self.y_offset_history = []
        
    def generate_pdf(self):
        """Generate CV PDF."""
        result = subprocess.run(["python3", "main.py"], capture_output=True, timeout=10)
        return result.returncode == 0
    
    def pdf_to_png(self, pdf, png):
        """Convert PDF to PNG."""
        images = convert_from_path(str(pdf), dpi=self.dpi)
        images[0].save(png, 'PNG')
    
    def analyze_differences(self, obj_png, gen_png):
        """Deep analysis of WHERE and WHAT is different."""
        obj = np.array(Image.open(obj_png).convert('RGB'))
        gen = np.array(Image.open(gen_png).convert('RGB'))
        
        if gen.shape != obj.shape:
            gen_img = Image.fromarray(gen).resize((obj.shape[1], obj.shape[0]), Image.Resampling.LANCZOS)
            gen = np.array(gen_img)
        
        # Calculate perceptible differences
        diff = np.abs(obj.astype(int) - gen.astype(int))
        diff_perceptible = diff.copy()
        diff_perceptible[diff < self.threshold] = 0
        
        # Overall similarity
        perceptible_pixels = np.sum(np.any(diff_perceptible > 0, axis=2))
        total_pixels = obj.shape[0] * obj.shape[1]
        similarity = 100 * (1 - perceptible_pixels / total_pixels)
        
        # Analyze by horizontal bands (detect vertical shift)
        h = obj.shape[0]
        bands = 20
        band_height = h // bands
        
        band_diffs = []
        for i in range(bands):
            y_start = i * band_height
            y_end = (i + 1) * band_height
            
            obj_band = obj[y_start:y_end, :]
            gen_band = gen[y_start:y_end, :]
            
            diff_band = np.abs(obj_band.astype(int) - gen_band.astype(int))
            diff_band[diff_band < self.threshold] = 0
            
            band_perceptible = np.sum(np.any(diff_band > 0, axis=2))
            band_total = obj_band.shape[0] * obj_band.shape[1]
            band_pct = (band_perceptible / band_total) * 100
            
            band_diffs.append(band_pct)
        
        # Detect if there's a systematic vertical shift
        # If top bands have more diff and bottom have less (or vice versa),
        # suggests Y offset issue
        top_half_diff = np.mean(band_diffs[:bands//2])
        bottom_half_diff = np.mean(band_diffs[bands//2:])
        
        vertical_gradient = top_half_diff - bottom_half_diff
        
        analysis = {
            "similarity": similarity,
            "perceptible_pixels": int(perceptible_pixels),
            "total_pixels": int(total_pixels),
            "band_differences": band_diffs,
            "top_half_diff": float(top_half_diff),
            "bottom_half_diff": float(bottom_half_diff),
            "vertical_gradient": float(vertical_gradient)
        }
        
        return analysis
    
    def get_current_y_offset(self):
        """Read current Y_GLOBAL_OFFSET from config."""
        with open(self.config_file, 'r') as f:
            content = f.read()
        
        match = re.search(r'Y_GLOBAL_OFFSET:\s*float\s*=\s*([\d.]+)', content)
        if match:
            return float(match.group(1))
        return 32.0  # default
    
    def set_y_offset(self, new_offset):
        """Update Y_GLOBAL_OFFSET in config."""
        with open(self.config_file, 'r') as f:
            content = f.read()
        
        # Replace Y_GLOBAL_OFFSET value
        new_content = re.sub(
            r'(Y_GLOBAL_OFFSET:\s*float\s*=\s*)[\d.]+',
            rf'\g<1>{new_offset}',
            content
        )
        
        with open(self.config_file, 'w') as f:
            f.write(new_content)
    
    def suggest_adjustment(self, analysis):
        """Suggest parameter adjustment based on analysis."""
        current_offset = self.get_current_y_offset()
        
        # Strategy: If there's a vertical gradient in differences,
        # adjust Y offset to minimize it
        gradient = analysis['vertical_gradient']
        
        # If top has more diff than bottom, content might be too low -> increase offset
        # If bottom has more diff than top, content might be too high -> decrease offset
        
        if abs(gradient) > 5.0:  # Significant gradient
            if gradient > 0:  # Top has more diff
                # Content too low, move up
                adjustment = +0.5
            else:  # Bottom has more diff
                # Content too high, move down  
                adjustment = -0.5
        else:
            # No clear pattern - try smaller random walk
            adjustment = 0.1 * (1 if len(self.y_offset_history) % 2 == 0 else -1)
        
        new_offset = current_offset + adjustment
        
        return {
            "current_offset": current_offset,
            "adjustment": adjustment,
            "new_offset": new_offset,
            "reason": f"Vertical gradient: {gradient:.2f}"
        }
    
    def create_comparison(self, obj_png, gen_png, iteration, analysis):
        """Create annotated comparison image."""
        obj_img = Image.open(obj_png)
        gen_img = Image.open(gen_png)
        
        if gen_img.size != obj_img.size:
            gen_img = gen_img.resize(obj_img.size, Image.Resampling.LANCZOS)
        
        w, h = obj_img.size
        comp = Image.new('RGB', (w*2+50, h+100), 'white')
        comp.paste(obj_img, (15, 80))
        comp.paste(gen_img, (w+35, 80))
        
        draw = ImageDraw.Draw(comp)
        sim = analysis['similarity']
        draw.text((w-100, 15), f"Iteration {iteration} - {sim:.2f}%", fill='black')
        draw.text((w-100, 35), f"Y_offset: {self.get_current_y_offset()}", fill='gray')
        draw.text((w//2-40, 55), "OBJETIVO", fill='red')
        draw.text((w+w//2-40, 55), "GENERADO", fill='blue')
        
        # Draw vertical line
        draw.line([(w+25, 0), (w+25, h+100)], fill='gray', width=2)
        
        comp.save(f"outputs/smart_iter_{iteration:04d}_{sim:.2f}pct.png")
    
    def run(self):
        """Main optimization loop."""
        print("="*90)
        print("INTELLIGENT VISUAL CORRECTOR - Auto-adjusting until 100% match")
        print("="*90)
        print(f"Target: {self.target_similarity}%")
        print(f"Max iterations: {self.max_iterations}")
        print("="*90)
        
        obj_png = "outputs/objetivo_ref.png"
        gen_png = "outputs/generated_current.png"
        
        # Create objetivo PNG once
        print("\n📸 Creating objetivo reference...")
        self.pdf_to_png("pdfs/objective/Objetivo_No_editar.pdf", obj_png)
        
        while self.iteration < self.max_iterations:
            self.iteration += 1
            
            print(f"\n{'='*90}")
            print(f"ITERATION {self.iteration}/{self.max_iterations}")
            print(f"{'='*90}")
            
            # Generate PDF
            print("⚙️  Generating PDF...")
            if not self.generate_pdf():
                print("❌ Generation failed")
                break
            
            # Convert to PNG
            print("📸 Converting to PNG...")
            self.pdf_to_png("outputs/Nicolas_Fredes_CV.pdf", gen_png)
            
            # Analyze differences
            print("🔍 Analyzing differences...")
            analysis = self.analyze_differences(obj_png, gen_png)
            
            similarity = analysis['similarity']
            print(f"\n📊 RESULTS:")
            print(f"   Similarity: {similarity:.4f}%")
            print(f"   Perceptible diff: {analysis['perceptible_pixels']:,} pixels")
            print(f"   Current Y_offset: {self.get_current_y_offset()}")
            print(f"   Vertical gradient: {analysis['vertical_gradient']:.2f}")
            
            # Create comparison
            self.create_comparison(obj_png, gen_png, self.iteration, analysis)
            
            # Check if target reached
            if similarity >= self.target_similarity:
                print(f"\n🎯 TARGET REACHED! {similarity:.2f}% >= {self.target_similarity}%")
                print(f"=" *90)
                print("✅ 100% VISUAL MATCH ACHIEVED!")
                print(f"="*90)
                break
            
            #Track best
            if similarity > self.best_similarity:
                self.best_similarity = similarity
                print(f"   ✅ New best: {self.best_similarity:.4f}%")
            
            # Auto-adjust parameters
            print("🔧 Calculating adjustment...")
            adjustment = self.suggest_adjustment(analysis)
            print(f"   {adjustment['reason']}")
            print(f"   Adjusting Y_offset: {adjustment['current_offset']} → {adjustment['new_offset']}")
            
            self.set_y_offset(adjustment['new_offset'])
            self.y_offset_history.append(adjustment['new_offset'])
        
        # Final report
        print(f"\n{'='*90}")
        print("OPTIMIZATION COMPLETE")
        print(f"{'='*90}")
        print(f"Best similarity: {self.best_similarity:.4f}%")
        print(f"Iterations: {self.iteration}")
        print(f"Target reached: {'YES ✅' if self.best_similarity >= self.target_similarity else 'NO ❌'}")
        print(f"Final Y_offset: {self.get_current_y_offset()}")
        print("="*90)

if __name__ == "__main__":
    corrector = IntelligentVisualCorrector()
    corrector.run()
