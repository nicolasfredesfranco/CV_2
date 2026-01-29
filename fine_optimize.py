#!/usr/bin/env python3
"""
Fine Optimization Script - Reach 80%+

Systematic fine-tuning to close the 2.63% gap.

Author: Nicolás Ignacio Fredes Franco
"""

import subprocess
import re
from pdf2image import convert_from_path
import numpy as np

def measure_similarity():
    """Measure visual similarity"""
    obj = convert_from_path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf", dpi=200)[0]
    gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=200)[0]
    
    obj_arr = np.array(obj.convert('RGB'))
    gen_arr = np.array(gen.convert('RGB').resize(obj.size))
    
    diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
    diff[diff < 10] = 0
    
    return 100 * (1 - np.sum(np.any(diff > 0, axis=2)) / (obj_arr.shape[0] * obj_arr.shape[1]))

def set_y_offset(value):
    """Set Y_GLOBAL_OFFSET in config"""
    with open('src/config.py', 'r') as f:
        config = f.read()
    
    config = re.sub(
        r'(Y_GLOBAL_OFFSET:\s*float\s*=\s*)[\d.]+',
        f'\\g<1>{value}',
        config
    )
    
    with open('src/config.py', 'w') as f:
        f.write(config)

def generate():
    """Generate CV"""
    result = subprocess.run(['python', 'main.py'], capture_output=True)
    return result.returncode == 0

def optimize():
    """Run fine optimization"""
    print("="*70)
    print("FINE OPTIMIZATION - TARGETING 80%+")
    print("="*70)
    
    # Read baseline
    try:
        with open('outputs/baseline.txt', 'r') as f:
            baseline = float(f.read().strip())
    except:
        baseline = 77.37
    
    print(f"\nBaseline: {baseline:.2f}%")
    print(f"Target:   80.00%")
    print(f"Gap:      {80 - baseline:.2f}%\n")
    
    best_sim = baseline
    best_y = 39.30  # Current value
    
    # Phase 1: Explore Y offset range
    print("Phase 1: Y_GLOBAL_OFFSET fine-tuning")
    print("-" * 70)
    
    test_values = [
        39.00, 39.10, 39.15, 39.20, 39.25, 39.28,
        39.30, 39.32, 39.35, 39.40, 39.45, 39.50,
        39.60, 39.70, 39.80
    ]
    
    for y_val in test_values:
        set_y_offset(y_val)
        if not generate():
            print(f"  {y_val:.2f} - FAILED")
            continue
        
        sim = measure_similarity()
        status = "✨ NEW BEST" if sim > best_sim else ""
        print(f"  Y={y_val:.2f} → {sim:.2f}%  {status}")
        
        if sim > best_sim:
            best_sim = sim
            best_y = y_val
        
        # Early exit if we hit 80%
        if sim >= 80.0:
            print(f"\n{'='*70}")
            print(f"🎉 TARGET REACHED! {sim:.2f}%")
            print(f"{'='*70}")
            break
    
    # Set to best
    set_y_offset(best_y)
    generate()
    
    # Phase 2: If still not at 80%, try micro-adjustments around best
    if best_sim < 80.0:
        print(f"\nPhase 2: Micro-adjustments around {best_y:.2f}")
        print("-" * 70)
        
        micro_values = [
            best_y - 0.10, best_y - 0.05, best_y - 0.02,
            best_y,
            best_y + 0.02, best_y + 0.05, best_y + 0.10
        ]
        
        for y_val in micro_values:
            set_y_offset(y_val)
            if not generate():
                continue
            
            sim = measure_similarity()
            status = "✨ NEW BEST" if sim > best_sim else ""
            print(f"  Y={y_val:.2f} → {sim:.2f}%  {status}")
            
            if sim > best_sim:
                best_sim = sim
                best_y = y_val
            
            if sim >= 80.0:
                print(f"\n{'='*70}")
                print(f"🎉 TARGET REACHED! {sim:.2f}%")
                print(f"{'='*70}")
                break
    
    # Final result
    set_y_offset(best_y)
    generate()
    final_sim = measure_similarity()
    
    print(f"\n{'='*70}")
    print(f"OPTIMIZATION COMPLETE")
    print(f"{'='*70}")
    print(f"Initial:  {baseline:.2f}%")
    print(f"Final:    {final_sim:.2f}%")
    print(f"Gain:     +{final_sim - baseline:.2f}%")
    print(f"Best Y:   {best_y:.2f}")
    print(f"{'='*70}")
    
    if final_sim >= 80.0:
        print(f"\n✅ SUCCESS - Target 80%+ achieved!")
    else:
        print(f"\n⚠️  Close - {80 - final_sim:.2f}% short of 80%")
    
    # Save result
    with open('outputs/final_result.txt', 'w') as f:
        f.write(f"Similarity: {final_sim:.2f}%\n")
        f.write(f"Y_GLOBAL_OFFSET: {best_y:.2f}\n")
    
    return final_sim, best_y

if __name__ == "__main__":
    final_sim, best_y = optimize()
