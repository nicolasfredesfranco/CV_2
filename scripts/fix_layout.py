import json
import math

def fix_layout():
    coords_file = "objetivo_coords.json"
    shapes_file = "objetivo_shapes.json"
    
    print(f"Loading {coords_file}...")
    with open(coords_file, 'r') as f:
        elements = json.load(f)
        
    print(f"Loading {shapes_file}...")
    with open(shapes_file, 'r') as f:
        shapes = json.load(f)
        
    # 1. Identify Headers in Left Column
    headers = {}
    
    # Headers we care about
    TARGET_HEADERS = ['EDUCATION', 'PAPERS & WORKSHOPS', 'SKILLS', 'LANGUAGES']
    
    for e in elements:
        if e['x'] > 200: continue # Skip right col
        
        text = e['text'].strip()
        if text in TARGET_HEADERS:
            # Found a header
            # We need its geometric center. 
            # JSON has 'y' (top-left usually or baseline? pdfplumber is top)
            # and 'size'.
            # Visual center roughly y + size/2
            
            # Note: In PyMuPDF/pdfplumber, 'y' often depends on the extraction method.
            # Assuming 'y' is Top coordinate here based on previous audit logging (Header Y=133, Rect Y=113..135)
            # If Rect Y=113 and Text Y=133, then Text Y is actually the BOTTOM/Baseline?
            # Wait, audit said: "Blue Rect ... y0=113, y1=135" (Height 22). 
            # "Target Header ... at Y=133.4".
            # So Text Y (133) is near the BOTTOM of the Rect (135).
            # This implies 'y' in JSON is close to the Baseline.
            
            # Standard Font: roughly Ascent is ~70-80% of size.
            # If Y=133 is Baseline, then Top is roughly 133 - 11 = 122.
            # Center is roughly 122 + 11/2 = 127.5.
            
            # Let's align the Rect Center to (TextY - Size/2).
            # If TextY=133, Size=11 -> Center=127.5.
            # if RectHeight=18 -> Top = 127.5 - 9 = 118.5.
            # Bot = 127.5 + 9 = 136.5.
            
            headers[text] = {
                'y': e['y'],
                'size': e.get('size', 11.0), # Default to 11 if missing
                'text': text
            }
            print(f"Target: {text} | Y={e['y']} | Size={e.get('size')}")

    # 2. Find Blue Rectangles and Fix them
    BLUE_COLOR_REF = (0.176, 0.451, 0.702) # Approx
    
    modified_count = 0
    
    for s in shapes:
        if s['type'] != 'rect': continue
        color = s.get('color', [])
        if not color or len(color) != 3: continue
        
        # Check if Blue-ish
        if abs(color[2] - 0.7) < 0.2 and color[2] > color[0]:
            # This is likely a blue header background
            x0, y0, x1, y1 = s['rect']
            h = y1 - y0
            cy = (y0 + y1) / 2
            
            # Find which header this belongs to
            closest_header = None
            min_dist = 999
            
            for name, info in headers.items():
                # Compare Center Y (approx)
                # Text Y is baseline approx.
                dist = abs(info['y'] - 10 - cy) # Rough check
                if dist < 50: # proximity
                     if dist < min_dist:
                         min_dist = dist
                         closest_header = info
            
            if closest_header:
                print(f"Adjusting Rect at y={y0:.1f} for Header '{closest_header['text']}'")
                
                # Desired Dimensions
                TARGET_HEIGHT = 18.0
                
                # Desired internal alignment: Center
                # Text Baseline = info['y']
                # Text Top ~= info['y'] - info['size']
                # Text Center ~= info['y'] - (info['size'] * 0.4) # Heuristic for visual center of caps
                # Actually, strictly utilizing Cap Height center.
                # Caps are usually ~0.7 * Size.
                # Visual Center = Baseline - (0.35 * Size).
                
                # Rect Center should be Text Center
                # Assuming text_y is Top-Left and font_size ~ height
                text_y = closest_header['y']
                font_size = closest_header['size']
                center_y = text_y - (font_size * 0.35)
                
                # New Rect Coords
                new_y0 = center_y - (TARGET_HEIGHT / 2)
                new_y1 = center_y + (TARGET_HEIGHT / 2)
                
                # Preserve X/Width logic?
                # Usually X matches margins or text width + padding.
                # Current X seems fine? Let's keep X but fix Y/H.
                
                s['rect'] = [x0, new_y0, x1, new_y1]
                modified_count += 1
                print(f" -> New Y0={new_y0:.1f}, Y1={new_y1:.1f}, H={new_y1-new_y0:.1f}")

    if modified_count > 0:
        print(f"Saving {modified_count} fixed shapes to {shapes_file}...")
        with open(shapes_file, 'w') as f:
            json.dump(shapes, f, indent=2)
    else:
        print("No shapes matched for fixing.")

if __name__ == "__main__":
    fix_layout()
