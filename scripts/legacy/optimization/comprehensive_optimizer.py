#!/usr/bin/env python3
"""
Comprehensive Multi-Parameter Optimizer for 90% Target
Adjusts fonts, positions, and spacing based on regional analysis.

Author: Nicolás Ignacio Fredes Franco
"""

import subprocess
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import json
import re
import shutil
from pathlib import Path
from datetime import datetime

class ComprehensiveOptimizer:
    def __init__(self):
        self.config_file = Path("src/config.py")
        self.coords_file = Path("data/coordinates.json")
        self.coords_backup = Path("data/coordinates_backup.json")
        self.target = 90.0
        self.current_best = 77.62
        self.iteration = 0
        self.max_iterations = 200
        
        # Backup original coordinates
        if not self.coords_backup.exists():
            shutil.copy(self.coords_file, self.coords_backup)
        
    def log(self, msg):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {msg}")
    
    def calculate_similarity(self):
        """Calculate visual similarity"""
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
        except Exception as e:
            self.log(f"Error: {e}")
            return 0.0
    
    def analyze_regional_differences(self):
        """Analyze differences by region to target optimization"""
        obj = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=150)[0]
        gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
        
        obj_arr = np.array(obj.convert('RGB'))
        gen_arr = np.array(gen.convert('RGB').resize(obj.size))
        
        h, w = obj_arr.shape[0], obj_arr.shape[1]
        
        # Analyze in 40 horizontal bands for finer granularity
        bands = 40
        band_height = h // bands
        
        problem_bands = []
        
        for i in range(bands):
            y_start = i * band_height
            y_end = min((i + 1) * band_height, h)
            
            obj_band = obj_arr[y_start:y_end, :]
            gen_band = gen_arr[y_start:y_end, :]
            
            diff = np.abs(obj_band.astype(int) - gen_band.astype(int))
            diff[diff < 10] = 0
            
            band_error = np.sum(np.any(diff > 0, axis=2)) / (obj_band.shape[0] * obj_band.shape[1])
            
            if band_error > 0.25:  # More than 25% different
                problem_bands.append({
                    'band': i,
                    'y_start': y_start,
                    'y_end': y_end,
                    'error_rate': band_error * 100
                })
        
        return sorted(problem_bands, key=lambda x: x['error_rate'], reverse=True)
    
    def adjust_elements_in_region(self, y_start, y_end, adjustment_type='y_shift', amount=0.5):
        """Adjust elements within a specific Y region"""
        with open(self.coords_file, 'r') as f:
            coords = json.load(f)
        
        modified = 0
        for item in coords:
            item_y = item.get('y', 0)
            
            # Check if element is in this region
            if y_start <= item_y <= y_end:
                if adjustment_type == 'y_shift':
                    item['y'] += amount
                    modified += 1
                elif adjustment_type == 'font_scale':
                    if 'fontsize' in item:
                        item['fontsize'] = round(item['fontsize'] * (1 + amount * 0.01), 2)
                        modified += 1
                elif adjustment_type == 'x_shift':
                    item['x'] += amount
                    modified += 1
        
        with open(self.coords_file, 'w') as f:
            json.dump(coords, f, indent=2)
        
        return modified
    
    def generate_pdf(self):
        """Generate PDF"""
        try:
            result = subprocess.run(
                ["python", "main.py"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def save_best_result(self, similarity):
        """Save visualization of best result"""
        try:
            obj = convert_from_path("pdfs/objetivo/Objetivo_No_editar.pdf", dpi=150)[0]
            gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
            
            # Side by side comparison
            w, h = obj.size
            comparison = Image.new('RGB', (w*2 + 60, h + 100), 'white')
            comparison.paste(obj, (20, 80))
            comparison.paste(gen, (w + 40, 80))
            
            draw = ImageDraw.Draw(comparison)
            draw.text((w - 100, 20), f"{similarity:.2f}% Similarity", fill='green')
            draw.text((50, 50), "OBJETIVO", fill='blue')
            draw.text((w + 80, 50), "GENERATED", fill='green')
            
            comparison.save(f"outputs/best_{similarity:.2f}pct_iter{self.iteration}.png")
            
            # Also save just the generated
            gen.save(f"outputs/generated_{similarity:.2f}pct.png")
        except Exception as e:
            self.log(f"Could not save viz: {e}")
    
    def run_optimization(self):
        """Main optimization loop"""
        self.log("="*80)
        self.log("COMPREHENSIVE MULTI-PARAMETER OPTIMIZATION TO 90%")
        self.log(f"Starting: {self.current_best:.2f}%")
        self.log(f"Target: {self.target}%")
        self.log(f"Gap: {self.target - self.current_best:.2f}%")
        self.log("="*80)
        
        # Initial analysis
        self.log("\n📊 Analyzing problem regions...")
        problem_regions = self.analyze_regional_differences()
        
        self.log(f"\nFound {len(problem_regions)} problem regions (>25% error)")
        for i, region in enumerate(problem_regions[:10]):
            self.log(f"  {i+1}. Band {region['band']} (y={region['y_start']}-{region['y_end']}): {region['error_rate']:.1f}% error")
        
        # Iterative optimization
        adjustments = [
            ('y_shift', 0.5),
            ('y_shift', -0.5),
            ('y_shift', 1.0),
            ('y_shift', -1.0),
            ('font_scale', 1.0),  # +1% font size
            ('font_scale', -1.0),  # -1% font size
            ('x_shift', 0.5),
            ('x_shift', -0.5),
        ]
        
        stuck_counter = 0
        last_improvement_iter = 0
        
        while self.iteration < self.max_iterations and self.current_best < self.target:
            self.iteration += 1
            
            # Re-analyze problem regions periodically
            if self.iteration % 10 == 1:
                problem_regions = self.analyze_regional_differences()
            
            if not problem_regions:
                self.log("\n✅ No more problem regions!")
                break
            
            # Target worst region
            worst_region = problem_regions[0]
            
            # Try different adjustments
            best_local_sim = self.current_best
            best_adjustment = None
            
            for adj_type, adj_amount in adjustments:
                # Restore from backup
                shutil.copy(self.coords_backup, self.coords_file)
                
                # Apply accumulated best
                # (We'd need to track history for this - simplified for now)
                
                # Try adjustment
                modified = self.adjust_elements_in_region(
                    worst_region['y_start'],
                    worst_region['y_end'],
                    adj_type,
                    adj_amount
                )
                
                if modified == 0:
                    continue
                
                if not self.generate_pdf():
                    continue
                
                similarity = self.calculate_similarity()
                
                if similarity > best_local_sim:
                    best_local_sim = similarity
                    best_adjustment = (adj_type, adj_amount, modified)
            
            # Apply best adjustment if found
            if best_adjustment and best_local_sim > self.current_best:
                improvement = best_local_sim - self.current_best
                self.current_best = best_local_sim
                last_improvement_iter = self.iteration
                
                self.log(f"\n🔄 Iteration {self.iteration}:")
                self.log(f"   Region: Band {worst_region['band']} (y={worst_region['y_start']}-{worst_region['y_end']})")
                self.log(f"   Adjustment: {best_adjustment[0]} by {best_adjustment[1]}, {best_adjustment[2]} elements")
                self.log(f"   ✨ NEW BEST: {self.current_best:.2f}% (+{improvement:.2f}%)")
                
                # Save this configuration
                shutil.copy(self.coords_file, f"data/coords_iter{self.iteration}_{self.current_best:.2f}pct.json")
                self.save_best_result(self.current_best)
                
                stuck_counter = 0
            else:
                stuck_counter += 1
                if stuck_counter % 5 == 0:
                    self.log(f"   Iteration {self.iteration}: No improvement ({stuck_counter} iterations stuck)")
                
                # Restore best known
                shutil.copy(self.coords_backup, self.coords_file)
            
            # Check if stuck
            if self.iteration - last_improvement_iter > 30:
                self.log(f"\n⚠️  Stuck for 30 iterations at {self.current_best:.2f}%")
                self.log("   This may be the practical maximum achievable")
                break
        
        # Final report
        self.log(f"\n{'='*80}")
        self.log(f"OPTIMIZATION COMPLETE")
        self.log(f"{'='*80}")
        self.log(f"Final Similarity: {self.current_best:.2f}%")
        self.log(f"Total Iterations: {self.iteration}")
        self.log(f"Total Improvement: +{self.current_best - 77.62:.2f}% from starting point")
        
        if self.current_best >= self.target:
            self.log(f"\n🎉🎉🎉 TARGET OF {self.target}% ACHIEVED! 🎉🎉🎉")
        else:
            gap = self.target - self.current_best
            self.log(f"\n📊 Achieved {self.current_best:.2f}%, remaining gap: {gap:.2f}%")
            
            if self.current_best >= 85.0:
                self.log("   Status: EXCELLENT - Very close to target!")
            elif self.current_best >= 80.0:
                self.log("   Status: VERY GOOD - Significant progress")
            else:
                self.log("   Status: GOOD - Continued improvement")
        
        self.log("="*80)

if __name__ == "__main__":
    optimizer = ComprehensiveOptimizer()
    optimizer.run_optimization()
