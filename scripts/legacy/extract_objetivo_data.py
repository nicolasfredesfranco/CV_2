#!/usr/bin/env python3
"""
PDF Data Extractor for Objetivo CV
===================================

Extracts shapes, colors, and text coordinates from the objetivo PDF
to create new data files for exact replication.
"""

import fitz  # PyMuPDF
from pathlib import Path
import json
from collections import defaultdict

PDF_PATH = "pdfs/objective/Objetivo_No_editar.pdf"
OUTPUT_SHAPES = "data/shapes_extracted.json"
OUTPUT_COORDS = "data/coordinates_extracted.json"

print("=" * 70)
print("PDF DATA EXTRACTOR - Objetivo CV Analysis")
print("=" * 70)

# Open PDF
doc = fitz.open(PDF_PATH)
page = doc[0]  # First page

print(f"\n📄 Page size: {page.rect.width} x {page.rect.height}")

# Extract shapes (rectangles/paths)
print(f"\n🔍 Extracting shapes...")
shapes = []
paths = page.get_drawings()

print(f"Found {len(paths)} drawing paths")

for idx, path in enumerate(paths):
    if path['type'] == 'f':  # Filled shape
        # Get bounding box
        bbox = path['rect']
        color = path.get('color', None)
        
        # Skip if no color
        if color is None:
            continue
        
        shape = {
            'type': 'rect',
            'rect': [bbox.x0, bbox.y0, bbox.x1, bbox.y1],
            'color': list(color),
            'fill_opacity': path.get('fill_opacity', 1.0)
        }
        shapes.append(shape)
        
        if idx < 10:  # Show first 10
            print(f"  Shape {idx}: {shape['rect']}, color: {color}")

print(f"\n✅ Extracted {len(shapes)} shapes")

# Extract text with positions
print(f"\n🔍 Extracting text blocks...")
blocks = page.get_text("dict")["blocks"]

text_elements = []
for block in blocks:
    if block['type'] == 0:  # Text block
        for line in block['lines']:
            for span in line['spans']:
                elem = {
                    'text': span['text'],
                    'x': span['origin'][0],
                    'y': span['origin'][1],
                    'size': span['size'],
                    'font': span['font'],
                    'color': span['color'],
                    'flags': span['flags']
                }
                text_elements.append(elem)

print(f"✅ Extracted {len(text_elements)} text elements")

# Analyze colors
print(f"\n🎨 Color analysis...")
colors = defaultdict(int)
for shape in shapes:
    color_key = tuple(shape['color'])
    colors[color_key] += 1

print("Top colors found:")
for color, count in sorted(colors.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  RGB{color}: {count} occurrences")

# Save extracted data
print(f"\n💾 Saving extracted data...")

Path("data").mkdir(exist_ok=True)

with open(OUTPUT_SHAPES, 'w') as f:
    json.dump(shapes, f, indent=2)
print(f"  ✅ {OUTPUT_SHAPES}")

with open(OUTPUT_COORDS, 'w') as f:
    json.dump(text_elements, f, indent=2)
print(f"  ✅ {OUTPUT_COORDS}")

print("\n" + "=" * 70)
print(f"📊 SUMMARY")
print("=" * 70)
print(f"Shapes extracted:  {len(shapes)}")
print(f"Text elements:     {len(text_elements)}")
print(f"Unique colors:     {len(colors)}")
print("=" * 70)

doc.close()
