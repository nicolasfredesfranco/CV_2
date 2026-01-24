import json
import statistics

def audit_layout():
    coords_file = "objetivo_coords.json"
    shapes_file = "objetivo_shapes.json"
    
    with open(coords_file, 'r') as f:
        elements = json.load(f)
        
    with open(shapes_file, 'r') as f:
        shapes = json.load(f)
        
    # Group text by section
    from cv_utils import classify_element # Ensure this is available or mock it
    
    # Mocking classify if not importable from here, but it should be processing from scripts/
    # Let's just reimplement simple logic or use Y ranges 
    LEFT_COL_RANGES = {
        'HEADER': (0, 130),
        'EDUCATION': (130, 315),
        'PAPERS': (315, 409),
        'SKILLS': (409, 710),
        'LANGUAGE': (710, 1000)
    }
    
    def get_section(y):
        for sec, (ymin, ymax) in LEFT_COL_RANGES.items():
            if ymin <= y < ymax:
                return sec
        return None

    section_text_bounds = {}
    
    for e in elements:
        if e['x'] > 200: continue # Skip right col
        
        sec = get_section(e['y'])
        if not sec: continue
        
        if sec not in section_text_bounds:
            section_text_bounds[sec] = {'min_y': 9999, 'max_y': -1}
            
        # Text Y is usually baseline or top depending on extraction?
        # In this JSON, 'y' seems to be Top-Left based on PdfToText? 
        # Check cv_utils.py comments: "Objective_No_editar.pdf ... Estructura ... Left Col < 200"
        # Let's assume 'y' is the anchor.
        
        # We care mostly about the Header Text (e.g. "EDUCATION") to center the box around IT.
        # Or does the box cover the whole section?
        # Visual check: The blue box is ONLY for the Title (e.g. "EDUCATION").
        # The content is white background.
        # So we identify the TITLE element of the section.
        
        if e.get('font', '').endswith('Bold') and e.get('size', 0) > 11:
             # Likely a header
             # "EDUCATION" size?
             if e['text'].strip() in ['EDUCATION', 'PAPERS & WORKSHOPS', 'SKILLS', 'LANGUAGES']:
                 print(f"Found Header: {e['text']} at Y={e['y']}")
                 section_text_bounds[sec] = {'header_y': e['y'], 'header_text': e['text']}

    print("\n--- Shape Analysis ---")
    BLUE_COLOR = (0.176, 0.451, 0.702)
    
    for s in shapes:
        if s['type'] != 'rect': continue
        color = s.get('color', [])
        if not color or len(color) != 3: continue
        
        if not (abs(color[0] - BLUE_COLOR[0]) < 0.1): continue
        
        x0, y0, x1, y1 = s['rect']
        if x0 > 200: continue
        
        # Center
        cy = (y0 + y1) / 2
        sec = get_section(cy)
        
        print(f"Blue Rect for {sec}: y0={y0:.1f}, y1={y1:.1f}, h={y1-y0:.1f}")
        
        if sec in section_text_bounds:
            info = section_text_bounds[sec]
            if 'header_y' in info:
                hy = info['header_y']
                print(f"  -> Target Header '{info['header_text']}' at Y={hy:.1f}")
                print(f"  -> Top Padding (Text Y - Rect Top): {hy - y0:.1f}")
                print(f"  -> Bottom Padding (Rect Bottom - Text Y): {y1 - hy:.1f}")
                
                # Ideal: Centered?
                # Usually Baseline is Y. Ascent is roughly size.
                # If Y=138 is top of text (approx)?
                # We want padding to be equal ideally.

if __name__ == "__main__":
    audit_layout()
