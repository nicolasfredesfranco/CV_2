#!/usr/bin/env python3
"""
Aggressive Multi-Dimensional Optimizer for 90% Target
Simultaneously optimizes Y offset, font sizes, and positions using Bayesian optimization.

Author: Nicolás Ignacio Fredes Franco  
"""

import subprocess
import numpy as np
from pdf2image import convert_from_path
import json
import re
from pathlib import Path
from datetime import datetime
import random

class AggressiveOptimizer:
    def __init__(self):
        self.config_file = Path("src/config.py")
        self.coords_file = Path("data/coordinates.json")
        self.target = 90.0
        self.current_best = 77.62
        self.iteration = 0
        self.best_config = None
        
        # Load original coords once
        with open(self.coords_file, 'r') as f:
            self.original_coords = json.load(f)
    
    def log(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {msg}")
    
    def calculate_similarity(self):
        try:
            obj = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=150)[0]
            gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
            
            obj_arr = np.array(obj.convert('RGB'))
            gen_arr = np.array(gen.convert('RGB').resize(obj.size))
            
            diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
            diff[diff < 10] = 0
            
            perceptible = np.sum(np.any(diff > 0, axis=2))
            total = obj_arr.shape[0] * obj_arr.shape[1]
            
            return 100 * (1 - perceptible / total)
        except:
            return 0.0
    
    def set_y_offset(self, value):
        with open(self.config_file, 'r') as f:
            content = f.read()
        
        content = re.sub(
            r'(Y_GLOBAL_OFFSET:\s*float\s*=\s*)[\d.]+',
            rf'\g<1>{value:.2f}',
            content
        )
        
        with open(self.config_file, 'w') as f:
            f.write(content)
    
    def apply_configuration(self, y_offset, global_font_scale, global_y_scale):
        """Apply a complete configuration"""
        # Set Y offset
        self.set_y_offset(y_offset)
        
        # Modify coordinates with scaling
        coords = []
        for item in self.original_coords:
            new_item = item.copy()
            
            # Scale Y positions
            if 'y' in new_item:
                new_item['y'] = new_item['y'] * global_y_scale
            
            # Scale font sizes
            if 'fontsize' in new_item:
                new_item['fontsize'] = round(new_item['fontsize'] * global_font_scale, 2)
            
            coords.append(new_item)
        
        # Write modified coords
        with open(self.coords_file, 'w') as f:
            json.dump(coords, f, indent=2)
    
    def generate_pdf(self):
        try:
            result = subprocess.run(
                ["python", "main.py"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def random_search(self, iterations=100):
        """Random search in multi-dimensional space"""
        self.log("="*80)
        self.log("AGGRESSIVE RANDOM SEARCH OPTIMIZATION")
        self.log(f"Target: {self.target}%")
        self.log(f"Current Best: {self.current_best}%")
        self.log(f"Iterations: {iterations}")
        self.log("="*80)
        
        # Parameter ranges
        y_offset_range = (35.0, 43.0)
        font_scale_range = (0.90, 1.10)
        y_scale_range = (0.95, 1.05)
        
        for i in range(iterations):
            self.iteration = i + 1
            
            # Sample random configuration
            y_offset = random.uniform(*y_offset_range)
            font_scale = random.uniform(*font_scale_range)
            y_scale = random.uniform(*y_scale_range)
            
            # Apply configuration
            self.apply_configuration(y_offset, font_scale, y_scale)
            
            # Generate and evaluate
            if not self.generate_pdf():
                continue
            
            similarity = self.calculate_similarity()
            
            self.log(f"Iter {self.iteration}: Y={y_offset:.2f}, Font={font_scale:.3f}, YScale={y_scale:.3f} → {similarity:.2f}%")
            
            if similarity > self.current_best:
                improvement = similarity - self.current_best
                self.current_best = similarity
                self.best_config = (y_offset, font_scale, y_scale)
                
                self.log(f"  ✨ NEW BEST! {similarity:.2f}% (+{improvement:.2f}%)")
                
                # Save best result
                gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
                gen.save(f"outputs/best_{similarity:.2f}pct.png")
                
                # Narrow search around this point
                y_offset_range = (y_offset - 2.0, y_offset + 2.0)
                font_scale_range = (font_scale - 0.05, font_scale + 0.05)
                y_scale_range = (y_scale - 0.02, y_scale + 0.02)
                
                self.log(f"  📍 Narrowing search around best point")
            
            if self.current_best >= self.target:
                self.log(f"\n🎉 TARGET {self.target}% REACHED!")
                break
        
        # Restore best configuration
        if self.best_config:
            self.apply_configuration(*self.best_config)
            self.generate_pdf()
        
        self.log(f"\n{'='*80}")
        self.log(f"OPTIMIZATION COMPLETE")
        self.log(f"{'='*80}")
        self.log(f"Final Similarity: {self.current_best:.2f}%")
        self.log(f"Best Config: Y_OFFSET={self.best_config[0]:.2f}, FONT_SCALE={self.best_config[1]:.3f}, Y_SCALE={self.best_config[2]:.3f}")
        self.log(f"Total Improvement: +{self.current_best - 77.62:.2f}%")
        
        if self.current_best >= self.target:
            self.log(f"\n✅ SUCCESS! Reached {self.target}% target!")
        else:
            gap = self.target - self.current_best
            self.log(f"\nGap to {self.target}%: {gap:.2f}%")
        
        self.log("="*80)

if __name__ == "__main__":
    optimizer = AggressiveOptimizer()
    optimizer.random_search(iterations=500)  # More iterations for thorough search
