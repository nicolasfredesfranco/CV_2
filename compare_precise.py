#!/usr/bin/env python3
"""
Pixel-Perfect Comparison & Parameter Suggester
===============================================

Compares current output with objetivo and suggests parameter adjustments.
"""

from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json

DPI = 600  # High resolution for precision

print("=" * 70)
print("PIXEL-PERFECT COMPARISON - v3.0 vs Objetivo")
print("=" * 70)

# Convert both PDFs
print(f"\n📄 Converting PDFs at {DPI} DPI...")
obj_img = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=DPI)[0]
cur_img = convert_from_path("outputs/current_v3_output.pdf", dpi=DPI)[0]

print(f"Objetivo: {obj_img.size}")
print(f"Current:  {cur_img.size}")

# Resize if needed
if obj_img.size != cur_img.size:
    print(f"\n⚠️  Resizing current to match objetivo...")
    cur_img = cur_img.resize(obj_img.size, Image.Resampling.LANCZOS)

# Convert to numpy
obj_arr = np.array(obj_img)
cur_arr = np.array(cur_img)

# Calculate pixel differences
print(f"\n🔍 Analyzing differences...")
diff = np.abs(obj_arr.astype(int) - cur_arr.astype(int))

# Per-channel differences
total_diff_r = np.sum(diff[:, :, 0])
total_diff_g = np.sum(diff[:, :, 1])
total_diff_b = np.sum(diff[:, :, 2])
total_diff = total_diff_r + total_diff_g + total_diff_b

# Calculate similarity
max_possible_diff = obj_img.width * obj_img.height * 3 * 255
similarity = 100 * (1 - total_diff / max_possible_diff)

print(f"\n📊 SIMILARITY: {similarity:.4f}%")

# Identify problem regions
print(f"\n🎯 Identifying problem regions...")

# Convert difference to grayscale for analysis
diff_gray = np.sum(diff, axis=2)

# Find rows/columns with most differences
row_diffs = np.sum(diff_gray, axis=1)
col_diffs = np.sum(diff_gray, axis=0)

# Top 10 problem rows
top_rows = np.argsort(row_diffs)[-10:][::-1]
print(f"\nTop 10 problematic rows (by pixel difference):")
for idx, row in enumerate(top_rows):
    row_pts = (row / obj_img.height) * 806.0  # PDF points
    print(f"  {idx+1}. Row {row} ({row_pts:.1f} pts): {row_diffs[row]:,.0f} diff")

# Top 10 problem columns  
top_cols = np.argsort(col_diffs)[-10:][::-1]
print(f"\nTop 10 problematic columns (by pixel difference):")
for idx, col in enumerate(top_cols):
    col_pts = (col / obj_img.width) * 623.0  # PDF points
    print(f"  {idx+1}. Col {col} ({col_pts:.1f} pts): {col_diffs[col]:,.0f} diff")

# Create difference heatmap
print(f"\n🖼️  Creating difference visualization...")

# Normalize difference for visualization
diff_visual = (diff_gray / diff_gray.max() * 255).astype(np.uint8) if diff_gray.max() > 0 else diff_gray.astype(np.uint8)
diff_heatmap = Image.fromarray(diff_visual, mode='L')

# Colorize (red = high difference)
diff_colored = Image.new('RGB', diff_heatmap.size)
pixels = diff_heatmap.load()
colored_pixels = diff_colored.load()

for y in range(diff_heatmap.height):
    for x in range(diff_heatmap.width):
        intensity = pixels[x, y]
        if intensity > 10:  # Threshold for visibility
            colored_pixels[x, y] = (intensity, 0, 0)  # Red
        else:
            colored_pixels[x, y] = (intensity, intensity, intensity)  # Gray

diff_colored.save("outputs/difference_heatmap_600dpi.png")
print(f"✅ Saved: outputs/difference_heatmap_600dpi.png"

)

# Side-by-side with overlay
comparison = Image.new('RGB', (obj_img.width * 2 + 10, obj_img.height), 'white')
comparison.paste(obj_img, (0, 0))
comparison.paste(cur_img, (obj_img.width + 10, 0))

draw = ImageDraw.Draw(comparison)
draw.text((50, 30), "OBJETIVO", fill='red')
draw.text((obj_img.width + 60, 30), "CURRENT v3.0", fill='blue')

comparison.save("outputs/sideby side_600dpi.png")
print(f"✅ Saved: outputs/sidebyside_600dpi.png")

# Parameter suggestions
print(f"\n💡 PARAMETER SUGGESTIONS")
print("=" * 70)

if similarity < 99.5:
    print(f"⚠️  Similarity {similarity:.2f}% is below target (99.5%)")
    print(f"\nRecommended adjustments:")
    
    # Analyze if there's a systematic offset
    # Check top/bottom differences
    top_third = np.sum(diff_gray[:obj_img.height//3, :])
    middle_third = np.sum(diff_gray[obj_img.height//3:2*obj_img.height//3, :])
    bottom_third = np.sum(diff_gray[2*obj_img.height//3:, :])
    
    print(f"\nVertical distribution of differences:")
    print(f"  Top third:    {top_third:,.0f}")
    print(f"  Middle third: {middle_third:,.0f}")
    print(f"  Bottom third: {bottom_third:,.0f}")
    
    if top_third > bottom_third * 1.5:
        print(f"\n→ Consider DECREASING Y_GLOBAL_OFFSET by ~5-10 pts")
    elif bottom_third > top_third * 1.5:
        print(f"\n→ Consider INCREASING Y_GLOBAL_OFFSET by ~5-10 pts")
    else:
        print(f"\n→ Y_GLOBAL_OFFSET appears balanced")
else:
    print(f"✅ Similarity {similarity:.2f}% EXCEEDS target!")
    print(f"   Current configuration is EXCELLENT")

print("=" * 70)

# Save report
report = {
    'similarity_percent': round(similarity, 4),
    'total_difference': int(total_diff),
    'max_possible_difference': int(max_possible_diff),
    'meets_target': similarity >= 99.5,
    'top_problem_rows': [{'row': int(r), 'diff': int(row_diffs[r])} for r in top_rows],
    'top_problem_cols': [{'col': int(c), 'diff': int(col_diffs[c])} for c in top_cols]
}

with open("outputs/comparison_report.json", 'w') as f:
    json.dump(report, f, indent=2)

print(f"\n💾 Report saved: outputs/comparison_report.json")
print("=" * 70)
