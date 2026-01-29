#!/usr/bin/env python3
"""
Intelligent optimizer for Phase 1 & 2 improvements
Uses grid search with multiple parameters
"""

import subprocess
import re
import json
from pdf2image import convert_from_path
import numpy as np
from pathlib import Path

def measure_similarity():
    """Measure current similarity"""
    obj = convert_from_path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf", dpi=150)[0]
    gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
    
    obj_arr = np.array(obj.convert('RGB'))
    gen_arr = np.array(gen.convert('RGB').resize(obj.size))
    
    diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
    diff[diff < 10] = 0
    
    return 100 * (1 - np.sum(np.any(diff > 0, axis=2)) / (obj_arr.shape[0] * obj_arr.shape[1]))

def set_y_offset(value):
    """Set Y_GLOBAL_OFFSET"""
    with open('src/config.py', 'r') as f:
        config = f.read()
    
    config = re.sub(
        r'(Y_GLOBAL_OFFSET:\s*float\s*=\s*)[\d.]+',
        f'\\g<1>{value}',
        config
    )
    
    with open('src/config.py', 'w') as f:
        f.write(config)

def set_bullet_indent(value):
    """Set OFFSET_BULLET_INDENT"""
    with open('src/config.py', 'r') as f:
        config = f.read()
    
    config = re.sub(
        r'(OFFSET_BULLET_INDENT:\s*float\s*=\s*)[\d.]+',
        f'\\g<1>{value}',
        config
    )
    
    with open('src/config.py', 'w') as f:
        f.write(config)

def generate_cv():
    """Generate CV"""
    subprocess.run(['python', 'main.py'], capture_output=True)

def optimize_phase1():
    """Phase 1: Quick parameter optimization"""
    print("="*80)
    print("PHASE 1: PARAMETER OPTIMIZATION")
    print("="*80)
    
    best_sim = 0
    best_y = 39.30
    best_bullet = 8.5
    
    # Grid search Y offset
    print("\n1. Optimizing Y_GLOBAL_OFFSET...")
    for y_offset in [38.8, 39.0, 39.1, 39.2, 39.3, 39.4, 39.5, 39.6, 39.8, 40.0]:
        set_y_offset(y_offset)
        generate_cv()
        sim = measure_similarity()
        
        print(f"   Y={y_offset:.1f} → {sim:.2f}%", end="")
        
        if sim > best_sim:
            best_sim = sim
            best_y = y_offset
            print(" ✨ NEW BEST")
        else:
            print()
    
    # Set best Y
    set_y_offset(best_y)
    
    # Grid search bullet indent
    print(f"\n2. Optimizing OFFSET_BULLET_INDENT (Y fixed at {best_y})...")
    for bullet in [8.3, 8.4, 8.45, 8.5, 8.55, 8.6, 8.7]:
        set_bullet_indent(bullet)
        generate_cv()
        sim = measure_similarity()
        
        print(f"   Bullet={bullet:.2f} → {sim:.2f}%", end="")
        
        if sim > best_sim:
            best_sim = sim
            best_bullet = bullet
            print(" ✨ NEW BEST")
        else:
            print()
    
    print(f"\n{'='*80}")
    print(f"PHASE 1 COMPLETE")
    print(f"Best Y_GLOBAL_OFFSET: {best_y}")
    print(f"Best OFFSET_BULLET_INDENT: {best_bullet}")
    print(f"Best Similarity: {best_sim:.2f}%")
    print(f"{'='*80}")
    
    return best_y, best_bullet, best_sim

if __name__ == "__main__":
    best_y, best_bullet, best_sim = optimize_phase1()
    
    # Save results
    results = {
        "phase": 1,
        "best_y_offset": best_y,
        "best_bullet_indent": best_bullet,
        "best_similarity": best_sim
    }
    
    with open('outputs/phase1_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to outputs/phase1_results.json")
