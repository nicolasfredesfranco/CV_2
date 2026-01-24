import fitz
import json
import sys

def extract_drawings(pdf_path, output_json):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    drawings = []
    
    # Extract paths/drawings
    paths = page.get_drawings()
    
    for p in paths:
        # We are interested in filled rectangles primarily for the blue headers
        if p['fill'] and p['type'] == 'f':
            # Get color
            color = p['fill']
            if isinstance(color, (list, tuple)) and len(color) == 3:
                 # Check if it's the blue color or similar (approx check if needed)
                 pass
            
            # Get bounding rect
            rect = p['rect']
            
            drawings.append({
                'type': 'rect',
                'rect': [rect.x0, rect.y0, rect.x1, rect.y1],
                'color': color,
                'fill_opacity': p.get('fill_opacity', 1),
                'stroke_opacity': p.get('stroke_opacity', 1)
            })
            
    print(f"Extracted {len(drawings)} drawing elements.")
    
    with open(output_json, 'w') as f:
        json.dump(drawings, f, indent=2)

if __name__ == "__main__":
    extract_drawings("Objetivo_No_editar.pdf", "objetivo_shapes.json")
