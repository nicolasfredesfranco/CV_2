#!/usr/bin/env python3
"""
Objetivo PDF Color & Structure Analyzer
========================================

Analyzes the rasterized objetivo PDF to extract:
- Dominant colors (orange sidebar, beige, text colors)
- Layout structure (column positions, sections)
- Text regions and approximate sizes

Since the PDF is image-based, we use pixel analysis.
"""

from pdf2image import convert_from_path
from PIL import Image
import numpy as np
from collections import Counter
from pathlib import Path
import json

PDF_PATH = "pdfs/objective/Objetivo_No_editar.pdf"
DPI = 300  # High resolution for accurate color detection

print("=" * 70)
print("OBJETIVO PDF ANALYZER - Color & Structure Extraction")
print("=" * 70)

# Convert PDF to image
print(f"\n📄 Converting PDF at {DPI} DPI...")
images = convert_from_path(PDF_PATH, dpi=DPI)
img = images[0]

print(f"✅ Image size: {img.width} x {img.height}")

# Convert to numpy for analysis
img_array = np.array(img)

# Analyze dominant colors
print(f"\n🎨 Analyzing color palette...")
pixels = img_array.reshape(-1, 3)
unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)

# Sort by frequency
color_freq = sorted(zip(unique_colors, counts), key=lambda x: x[1], reverse=True)

print(f"Found {len(unique_colors)} unique colors")
print("\nTop 20 colors by pixel count:")
print(f"{'Rank':<6} {'RGB':<20} {'Normalized':<25} {'Count':<12} {'Percent':<8}")
print("-" * 80)

total_pixels = img.width * img.height
top_colors = []

for idx, (color, count) in enumerate(color_freq[:20]):
    r, g, b = color
    norm_r, norm_g, norm_b = r/255.0, g/255.0, b/255.0
    percent = (count / total_pixels) * 100
    
    print(f"{idx+1:<6} ({r:3},{g:3},{b:3})" + " " * 8 + 
          f"({norm_r:.3f}, {norm_g:.3f}, {norm_b:.3f})" + " " * 3 +
          f"{count:<12,} {percent:>6.2f}%")
    
    top_colors.append({
        'rank': idx + 1,
        'rgb': [int(r), int(g), int(b)],
        'normalized': [round(norm_r, 3), round(norm_g, 3), round(norm_b, 3)],
        'pixel_count': int(count),
        'percentage': round(percent, 2)
    })

# Detect layout regions by analyzing left edge
print(f"\n📐 Analyzing layout structure...")

# Sample left 30% of image to detect sidebar
sidebar_width_samples = []
for y in range(0, img.height, 50):
    row = img_array[y, :int(img.width * 0.3)]
    
    # Find where color changes from sidebar to main content
    # Look for transition from orange/beige to white/light
    for x in range(len(row) - 1):
        r1, g1, b1 = row[x]
        r2, g2, b2 = row[x + 1]
        
        # Detect significant color change
        if abs(int(r1) - int(r2)) > 50 or abs(int(g1) - int(g2)) > 50:
            sidebar_width_samples.append(x)
            break

if sidebar_width_samples:
    avg_sidebar_width = int(np.median(sidebar_width_samples))
    sidebar_width_pts = (avg_sidebar_width / img.width) * 623.0  # Original PDF width
    
    print(f"Detected sidebar width: {avg_sidebar_width} px ({sidebar_width_pts:.1f} pts)")
else:
    print("⚠️  Could not detect sidebar boundary")

# Save analysis results
output = {
    'pdf_dimensions': {
        'width_pts': 623.0,
        'height_pts': 806.0
    },
    'image_dimensions': {
        'width_px': img.width,
        'height_px': img.height,
        'dpi': DPI
    },
    'color_palette': top_colors,
    'layout': {
        'sidebar_width_pts': sidebar_width_pts if sidebar_width_samples else None
    }
}

output_path = Path("data/objetivo_analysis.json")
output_path.parent.mkdir(exist_ok=True)

with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\n💾 Saved analysis: {output_path}")

# Save a visual analysis image
print(f"\n🖼️  Creating visual analysis...")

# Draw vertical line at sidebar boundary
if sidebar_width_samples:
    from PIL import ImageDraw
    analysis_img = img.copy()
    draw = ImageDraw.Draw(analysis_img)
    
    # Draw sidebar boundary line
    x = avg_sidebar_width
    draw.line([(x, 0), (x, img.height)], fill=(255, 0, 0), width=3)
    
    analysis_img.save("outputs/objetivo_structure_analysis.png")
    print(f"✅ Saved: outputs/objetivo_structure_analysis.png")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
print(f"\nKey findings:")
print(f"  - Dominant colors identified: {len(top_colors)}")
print(f"  - Sidebar boundary detected: {sidebar_width_pts if sidebar_width_samples else 'N/A':.1f} pts")
print(f"  - Analysis saved to: data/objetivo_analysis.json")
print("=" * 70)
