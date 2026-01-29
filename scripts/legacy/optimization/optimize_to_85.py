#!/usr/bin/env python3
"""
Iterative Visual Optimizer for 85% Target
Systematically adjusts parameters to improve visual similarity.

Author: Nicolás Ignacio Fredes Franco
"""

import subprocess
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import re
from pathlib import Path

class VisualOptimizer85:
    def __init__(self):
        self.config_file = Path("src/config.py")
        self.target_similarity = 85.0
        self.max_iterations = 100
        self.iteration = 0
        self.best_similarity = 0
        self.best_offset = None
        
    def get_current_similarity(self):
        """Calculate current visual similarity"""
        obj = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=150)[0]
        gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
        
        obj_arr = np.array(obj.convert('RGB'))
        gen_arr = np.array(gen.convert('RGB').resize(obj.size))
        
        diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
        diff_perceptible = diff.copy()
        diff_perceptible[diff < 10] = 0
        
        perceptible_pixels = np.sum(np.any(diff_perceptible > 0, axis=2))
        total_pixels = obj_arr.shape[0] * obj_arr.shape[1]
        similarity = 100 * (1 - perceptible_pixels / total_pixels)
        
        return similarity
    
    def get_current_y_offset(self):
        """Read current Y_GLOBAL_OFFSET from config"""
        with open(self.config_file, 'r') as f:
            content = f.read()
        
        match = re.search(r'Y_GLOBAL_OFFSET:\s*float\s*=\s*([\d.]+)', content)
        if match:
            return float(match.group(1))
        return 32.0
    
    def set_y_offset(self, new_offset):
        """Update Y_GLOBAL_OFFSET in config"""
        with open(self.config_file, 'r') as f:
            content = f.read()
        
        new_content = re.sub(
            r'(Y_GLOBAL_OFFSET:\s*float\s*=\s*)[\d.]+',
            rf'\g<1>{new_offset}',
            content
        )
        
        with open(self.config_file, 'w') as f:
            f.write(new_content)
    
    def generate_pdf(self):
        """Generate CV PDF"""
        result = subprocess.run(
            ["python", "main.py"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    
    def analyze_vertical_shift(self):
        """Analyze if content needs vertical shift"""
        obj = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=150)[0]
        gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
        
        obj_arr = np.array(obj.convert('RGB'))
        gen_arr = np.array(gen.convert('RGB').resize(obj.size))
        
        # Analyze top vs bottom differences
        h = obj_arr.shape[0]
        top_diff = np.sum(np.any(np.abs(obj_arr[:h//2] - gen_arr[:h//2]) > 10, axis=2))
        bottom_diff = np.sum(np.any(np.abs(obj_arr[h//2:] - gen_arr[h//2:]) > 10, axis=2))
        
        if top_diff > bottom_diff * 1.2:
            return +0.5  # Push down
        elif bottom_diff > top_diff * 1.2:
            return -0.5  # Push up
        return 0.1  # Small exploration
    
    def run(self):
        """Main optimization loop"""
        print("="*80)
        print("  OPTIMIZACIÓN HACIA 85% SIMILITUD VISUAL")
        print("="*80)
        
        while self.iteration < self.max_iterations:
            self.iteration += 1
            current_offset = self.get_current_y_offset()
            
            print(f"\n🔄 Iteración {self.iteration}/{self.max_iterations}")
            print(f"   Y_offset actual: {current_offset:.2f}")
            
            # Generate PDF
            if not self.generate_pdf():
                print("   ❌ Error en generación")
                break
            
            # Measure similarity
            similarity = self.get_current_similarity()
            print(f"   📊 Similitud: {similarity:.2f}%")
            
            # Track best
            if similarity > self.best_similarity:
                self.best_similarity = similarity
                self.best_offset = current_offset
                print(f"   ✨ ¡Nuevo mejor! {similarity:.2f}%")
            
            # Check if target reached
            if similarity >= self.target_similarity:
                print(f"\n🎉 ¡OBJETIVO ALCANZADO! {similarity:.2f}% >= {self.target_similarity}%")
                break
            
            # Calculate adjustment
            shift = self.analyze_vertical_shift()
            new_offset = current_offset + shift
            
            print(f"   🔧 Ajustando offset: {current_offset:.2f} → {new_offset:.2f}")
            self.set_y_offset(new_offset)
            
            # Progress
            progress = (similarity / self.target_similarity) * 100
            print(f"   📈 Progreso: {progress:.1f}% del objetivo")
        
        print(f"\n{'='*80}")
        print(f"RESULTADO FINAL:")
        print(f"   Mejor similitud: {self.best_similarity:.2f}%")
        print(f"   Mejor offset: {self.best_offset:.2f}")
        print(f"   Iteraciones: {self.iteration}")
        
        if self.best_similarity >= self.target_similarity:
            print(f"\n✅ ¡ÉXITO! Objetivo de 85% alcanzado")
        else:
            print(f"\n⚠️  Máximo alcanzado: {self.best_similarity:.2f}%")
            print(f"   Falta: {self.target_similarity - self.best_similarity:.2f}%")
        
        print("="*80)

if __name__ == "__main__":
    optimizer = VisualOptimizer85()
    optimizer.run()
