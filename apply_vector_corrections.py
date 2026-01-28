#!/usr/bin/env python3
"""
Vector-Level Precision Corrections
===================================

Applying exact corrections identified from 200% zoom analysis:
- Shift entire content UP by 5pts (not 5px - working in PDF points)
- Reduce bullet indentation by 2.5pts
- Reduce bar heights by 1pt (from 25pt to 24pt)
- Reduce section gap after name by 3pts

Author: Nicolás Fredes
"""
import json

print("="*80)
print("VECTOR-LEVEL PRECISION CORRECTIONS")
print("="*80)

with open('data/coordinates.json') as f:
    coords = json.load(f)

with open('data/shapes.json') as f:
    shapes = json.load(f)

# === 1. SHIFT CONTENT UP BY 5 POINTS ===
print("\n1. Shifting entire content UP by 5 points...")
UPSHIFT = 5

for elem in coords:
    elem['y'] += UPSHIFT

for shape in shapes:
    if 'rect' in shape:
        rect = shape['rect']
        rect[1] += UPSHIFT
        rect[3] += UPSHIFT
        shape['rect'] = rect

print(f"   ✅ Content shifted up {UPSHIFT}pt")

# === 2. REDUCE SECTION GAP AFTER NAME BY 3 POINTS ===
print("\n2. Reducing gap after name by 3 points...")

# Find name position
name_y = None
for elem in coords:
    if "Nicolás Ignacio Fredes Franco" in elem['text'] and elem['size'] > 20:
        name_y = elem['y']
        print(f"   Name found at Y={name_y:.2f}")
        break

if name_y:
    GAP_REDUCTION = 3
    # Move content below name up
    for elem in coords:
        if elem['y'] < name_y - 10:
            elem['y'] += GAP_REDUCTION
    
    for shape in shapes:
        if 'rect' in shape:
            rect = shape['rect']
            if rect[3] < name_y - 10:
                rect[1] += GAP_REDUCTION
                rect[3] += GAP_REDUCTION
                shape['rect'] = rect
    
    print(f"   ✅ Gap reduced by {GAP_REDUCTION}pt")

# === 3. REDUCE BAR HEIGHTS FROM 25PT TO 24PT ===
print("\n3. Setting all blue bars to exactly 24pt height...")

TARGET_BAR_HEIGHT = 24.0

bar_count = 0
for shape in shapes:
    if shape['type'] == 'rect':
        color = shape.get('color', [0,0,0])
        if len(color) == 3 and color[2] > 0.5:  # Blue bars
            rect = shape['rect']
            current_height = rect[3] - rect[1]
            center_y = (rect[1] + rect[3]) / 2
            
            # Recalculate from center
            rect[1] = center_y - (TARGET_BAR_HEIGHT / 2)
            rect[3] = center_y + (TARGET_BAR_HEIGHT / 2)
            shape['rect'] = rect
            
            bar_count += 1

print(f"   ✅ {bar_count} bars set to {TARGET_BAR_HEIGHT}pt")

# Save
with open('data/coordinates.json', 'w') as f:
    json.dump(coords, f, indent=2)

with open('data/shapes.json', 'w') as f:
    json.dump(shapes, f, indent=2)

print("\n" + "="*80)
print("VECTOR-LEVEL CORRECTIONS APPLIED")
print(f"  ✅ Global shift: +{UPSHIFT}pt")
print(f"  ✅ Name gap: -{GAP_REDUCTION}pt")
print(f"  ✅ Bar heights: {TARGET_BAR_HEIGHT}pt uniform")
print("="*80)
print("\nNOTE: Bullet indentation will be fixed in main.py")
