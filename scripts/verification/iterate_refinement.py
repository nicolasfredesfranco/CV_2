#!/usr/bin/env python3
"""
Iterative CV Refinement Script
Automatically iterates code modifications to improve similarity score
"""
import subprocess
import json
import os
import sys

def run_test():
    """Run similarity test and get score"""
    result = subprocess.run(
        ['python3', 'scripts/verification/test_similarity.py'],
        capture_output=True,
        text=True,
        cwd='/home/nicofredes/Desktop/code/CV'
    )
    
    # Parse JSON report
    with open('/home/nicofredes/Desktop/code/CV/similarity_report.json') as f:
        metrics = json.load(f)
    
    return metrics

def generate_cv():
    """Generate CV"""
    result = subprocess.run(
        ['python3', 'main.py'],
        capture_output=True,
        text=True,
        cwd='/home/nicofredes/Desktop/code/CV'
    )
    return result.returncode == 0

def analyze_and_suggest(metrics, iteration):
    """Analyze metrics and suggest improvements"""
    print(f"\n{'='*80}")
    print(f"ITERATION {iteration} ANALYSIS")
    print(f"{'='*80}")
    
    score = metrics['combined_score']
    pixel_sim = metrics['pixel_similarity']
    identical = metrics['pct_identical_pixels']
    avg_diff = metrics['avg_pixel_diff']
    
    print(f"📊 Combined Score: {score:.2f}%")
    print(f"   Pixel Similarity: {pixel_sim:.2f}%")
    print(f"   Identical Pixels: {identical:.2f}%")
    print(f"   Avg Difference: {avg_diff:.2f}/255")
    
    suggestions = []
    
    # Analyze what needs improvement
    if avg_diff > 20:
        suggestions.append("HIGH AVG DIFF: Text rendering or colors significantly different")
        suggestions.append("  → Check font weights, colors, or use different rendering mode")
    elif avg_diff > 10:
        suggestions.append("MEDIUM AVG DIFF: Minor color/rendering differences")
        suggestions.append("  → Fine-tune colors or font rendering")
    elif avg_diff > 5:
        suggestions.append("LOW AVG DIFF: Subtle differences remain")
        suggestions.append("  → Adjust spacing, kerning, or precise coordinates")
    
    if identical < 80:
        suggestions.append("LOW IDENTICAL PIXELS: Major structural differences")
        suggestions.append("  → Check page size, margins, or layout structure")
    elif identical < 90:
        suggestions.append("MEDIUM IDENTICAL: Some pixels differ")
        suggestions.append("  → Likely font anti-aliasing or color precision")
    
    if score < 90:
        suggestions.append("⚠️  PRIORITY: Focus on major issues first")
    elif score < 95:
        suggestions.append("✅ GOOD PROGRESS: Refinebased details")
    elif score < 99:
        suggestions.append("⭐ ALMOST THERE: Focus on micro-optimizations")
    else:
        suggestions.append("🎯 TARGET ACHIEVED!")
    
    print("\n💡 SUGGESTIONS:")
    for s in suggestions:
        print(f"   {s}")
    
    return suggestions

if __name__ == "__main__":
    print("🚀 Starting Iterative CV Refinement")
    print("="*80)
    
    # Initial state
    print("\n📋 Step 1: Generate initial CV")
    if not generate_cv():
        print("❌ CV generation failed!")
        sys.exit(1)
    
    print("\n📊 Step 2: Run similarity test")
    metrics = run_test()
    
    analyze_and_suggest(metrics, iteration=1)
    
    print("\n" + "="*80)
    print("Initial analysis complete. Ready for manual code modifications.")
    print("="*80)
