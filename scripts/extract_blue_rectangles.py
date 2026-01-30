#!/usr/bin/env python3
"""Blue Rectangle Extractor - Extracts exact coordinates of blue section header rectangles"""

import json
import fitz  # PyMuPDF
from pathlib import Path

OBJECTIVE_PDF = Path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf")
OUTPUT_JSON = Path("data/blue_rectangles_objective.json")
BLUE_TARGET = (0.118, 0.098, 0.455)
COLOR_TOLERANCE = 0.05

doc = fitz.open(OBJECTIVE_PDF)
page = doc[0]
print(f"📖 Reading: {OBJECTIVE_PDF}")
print(f"   Page size: {page.rect.width:.2f} x {page.rect.height:.2f}")

drawings = page.get_drawings()
print(f"   Total drawings found: {len(drawings)}")

blue_rectangles = []

for drawing in drawings:
    if drawing.get('type') != 'f':
        continue
    fill_color = drawing.get('fill')
    if not fill_color:
        continue
    r, g, b = fill_color[:3] if len(fill_color) >= 3 else (0, 0, 0)
    if not all(abs(c - target) < COLOR_TOLERANCE for c, target in zip([r, g, b], BLUE_TARGET)):
        continue
    rect = drawing['rect']
    rect_info = {
        'index': len(blue_rectangles),
        'x': round(float(rect.x0), 4),
        'y': round(float(rect.y0), 4),
        'width': round(float(rect.width), 4),
        'height': round(float(rect.height), 4),
        'centroid_x': round(float(rect.x0 + rect.width / 2), 4),
        'centroid_y': round(float(rect.y0 + rect.height / 2), 4),
        'fill_color': {'r': round(r, 4), 'g': round(g, 4), 'b': round(b, 4)}
    }
    blue_rectangles.append(rect_info)

blue_rectangles.sort(key=lambda r: r['y'])

# Associate with section headers
dict_file = Path("data/objective_dictionary.json")
if dict_file.exists():
    with open(dict_file, 'r') as f:
        obj_data = json.load(f)
        dictionary = obj_data.get('dictionary', [])
        targets = ['EXPERIENCE', 'EDUCATION', 'SKILLS', 'PAPERS', 'LANGUAGES']
        for rect in blue_rectangles:
            for target in targets:
                for item in dictionary:
                    if target in item.get('text', ''):
                        if abs(item['location']['centroid_y'] - rect['centroid_y']) < 20:
                            rect['section'] = target
                            rect['section_centroid'] = {
                                'x': item['location']['centroid_x'],
                                'y': item['location']['centroid_y']
                            }
                        break

output_data = {
    'metadata': {
        'source_file': str(OBJECTIVE_PDF),
        'page_dimensions': {'width': round(float(page.rect.width), 2), 'height': round(float(page.rect.height), 2)},
        'total_rectangles': len(blue_rectangles),
        'color_target': {'r': BLUE_TARGET[0], 'g': BLUE_TARGET[1], 'b': BLUE_TARGET[2], 'hex': '#1E1974'}
    },
    'rectangles': blue_rectangles
}

OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_JSON, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"\n✅ Blue rectangles saved: {OUTPUT_JSON}")
print(f"   Total rectangles: {len(blue_rectangles)}\n")
for rect in blue_rectangles:
    section = rect.get('section', 'Unknown')
    print(f"   • {section:12} @ ({rect['x']:6.2f}, {rect['y']:6.2f}) [{rect['width']:5.2f} x {rect['height']:4.2f}]")

doc.close()
