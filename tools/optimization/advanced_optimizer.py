#!/usr/bin/env python3
"""
Advanced Visual Optimizer - Grid Search Approach
Systematically tests parameter combinations to achieve 85% similarity.

Author: Nicolás Ignacio Fredes Franco
"""

import subprocess
import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import re
from pathlib import Path
import json
from datetime import datetime

class AdvancedOptimizer:
    def __init__(self):
        self.config_file = Path("src/config.py")
        self.target = 85.0
        self.current_best = 76.14
        self.best_params = {
            'y_offset': 36.7,
            'font_scale': 1.0
        }
        self.iterations = 0
        self.log_file = Path("outputs/optimization_advanced.log")
        
    def log(self, message):
        """Log message to file and console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        with open(self.log_file, 'a') as f:
            f.write(log_msg + "\n")
    
    def calculate_similarity(self):
        """Calculate visual similarity between objective and generated"""
        try:
            obj = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=150)[0]
            gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
            
            obj_arr = np.array(obj.convert('RGB'))
            gen_arr = np.array(gen.convert('RGB').resize(obj.size))
            
            diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
            diff[diff < 10] = 0
            
            perceptible = np.sum(np.any(diff > 0, axis=2))
            total = obj_arr.shape[0] * obj_arr.shape[1]
            similarity = 100 * (1 - perceptible / total)
            
            return similarity
        except Exception as e:
            self.log(f"Error calculating similarity: {e}")
            return 0.0
    
    def set_y_offset(self, value):
        """Update Y_GLOBAL_OFFSET in config"""
        with open(self.config_file, 'r') as f:
            content = f.read()
        
        new_content = re.sub(
            r'(Y_GLOBAL_OFFSET:\s*float\s*=\s*)[\d.]+',
            rf'\g<1>{value}',
            content
        )
        
        with open(self.config_file, 'w') as f:
            f.write(new_content)
    
    def generate_pdf(self):
        """Generate CV PDF"""
        try:
            result = subprocess.run(
                ["python", "main.py"],
                capture_output=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False
    
    def test_configuration(self, y_offset):
        """Test a specific configuration"""
        self.iterations += 1
        
        self.log(f"\n{'='*60}")
        self.log(f"Iteration {self.iterations}: Testing Y_OFFSET = {y_offset:.2f}")
        
        # Apply configuration
        self.set_y_offset(y_offset)
        
        # Generate PDF
        if not self.generate_pdf():
            self.log("  ❌ Generation failed")
            return 0.0
        
        # Measure similarity
        similarity = self.calculate_similarity()
        self.log(f"  📊 Similarity: {similarity:.2f}%")
        
        # Update best if improved
        if similarity > self.current_best:
            improvement = similarity - self.current_best
            self.current_best = similarity
            self.best_params['y_offset'] = y_offset
            self.log(f"  ✨ NEW BEST! +{improvement:.2f}% improvement")
            
            # Save screenshot of best result
            gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
            gen.save(f"outputs/best_{similarity:.2f}pct_iter{self.iterations}.png")
        
        return similarity
    
    def grid_search(self):
        """Systematic grid search of parameter space"""
        self.log("="*60)
        self.log("ADVANCED OPTIMIZATION - GRID SEARCH")
        self.log(f"Target: {self.target}%")
        self.log(f"Current Best: {self.current_best}%")
        self.log(f"Gap: {self.target - self.current_best:.2f}%")
        self.log("="*60)
        
        # Start with current best
        base_offset = self.best_params['y_offset']
        
        # Phase 1: Coarse search around current best (±5 points, step 1.0)
        self.log("\n📍 PHASE 1: Coarse Search (±5 points, step 1.0)")
        for delta in np.arange(-5.0, 5.5, 1.0):
            test_offset = base_offset + delta
            similarity = self.test_configuration(test_offset)
            
            if similarity >= self.target:
                self.log(f"\n🎉 TARGET REACHED! {similarity:.2f}% >= {self.target}%")
                return True
        
        # Phase 2: Fine search around new best (±2 points, step 0.5)
        self.log("\n📍 PHASE 2: Fine Search (±2 points, step 0.5)")
        base_offset = self.best_params['y_offset']
        
        for delta in np.arange(-2.0, 2.5, 0.5):
            test_offset = base_offset + delta
            similarity = self.test_configuration(test_offset)
            
            if similarity >= self.target:
                self.log(f"\n🎉 TARGET REACHED! {similarity:.2f}% >= {self.target}%")
                return True
        
        # Phase 3: Ultra-fine search (±1 point, step 0.1)
        self.log("\n📍 PHASE 3: Ultra-Fine Search (±1 point, step 0.1)")
        base_offset = self.best_params['y_offset']
        
        for delta in np.arange(-1.0, 1.1, 0.1):
            test_offset = base_offset + delta
            similarity = self.test_configuration(test_offset)
            
            if similarity >= self.target:
                self.log(f"\n🎉 TARGET REACHED! {similarity:.2f}% >= {self.target}%")
                return True
        
        # Phase 4: Extreme fine search if close (±0.5 point, step 0.05)
        if self.current_best >= 83.0:
            self.log("\n📍 PHASE 4: Extreme Fine Search (±0.5 points, step 0.05)")
            base_offset = self.best_params['y_offset']
            
            for delta in np.arange(-0.5, 0.55, 0.05):
                test_offset = base_offset + delta
                similarity = self.test_configuration(test_offset)
                
                if similarity >= self.target:
                    self.log(f"\n🎉 TARGET REACHED! {similarity:.2f}% >= {self.target}%")
                    return True
        
        return False
    
    def finalize(self, reached_target):
        """Set final configuration and report"""
        self.log("\n" + "="*60)
        self.log("OPTIMIZATION COMPLETE")
        self.log("="*60)
        self.log(f"Iterations: {self.iterations}")
        self.log(f"Best Similarity: {self.current_best:.2f}%")
        self.log(f"Best Y_OFFSET: {self.best_params['y_offset']:.2f}")
        
        if reached_target:
            self.log(f"\n✅ SUCCESS! Target of {self.target}% achieved!")
        else:
            gap = self.target - self.current_best
            self.log(f"\n📊 Maximum achieved: {self.current_best:.2f}%")
            self.log(f"   Gap remaining: {gap:.2f}%")
            
            if self.current_best >= 80.0:
                self.log("   Status: Very Close - Additional manual tuning recommended")
            elif self.current_best >= 78.0:
                self.log("   Status: Close - Further optimization possible")
            else:
                self.log("   Status: May need different optimization strategy")
        
        # Ensure best configuration is set
        self.set_y_offset(self.best_params['y_offset'])
        self.generate_pdf()
        
        self.log(f"\n📁 Final CV: outputs/Nicolas_Fredes_CV.pdf")
        self.log(f"📁 Log file: {self.log_file}")
        self.log("="*60)

if __name__ == "__main__":
    optimizer = AdvancedOptimizer()
    
    # Clear log file
    optimizer.log_file.write_text("")
    
    # Run optimization
    reached_target = optimizer.grid_search()
    
    # Finalize
    optimizer.finalize(reached_target)
