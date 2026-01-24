import json
import shutil

def tune_shapes():
    shapes_path = "objetivo_shapes.json"
    
    # Backup
    shutil.copy(shapes_path, shapes_path + ".bak")
    
    with open(shapes_path, 'r') as f:
        shapes = json.load(f)
        
    # Stats
    modified = 0
    BLUE_COLOR = (0.176, 0.451, 0.702) # normalized
    
    new_shapes = []
    
    for s in shapes:
        if s['type'] != 'rect':
            new_shapes.append(s)
            continue
            
        color = s.get('color', [])
        if not color or len(color) != 3:
            new_shapes.append(s)
            continue
            
        # Check Blue
        is_blue = (abs(color[0] - BLUE_COLOR[0]) < 0.1 and
                   abs(color[1] - BLUE_COLOR[1]) < 0.1 and
                   abs(color[2] - BLUE_COLOR[2]) < 0.1)
                   
        # Check Left Column
        rect = s['rect'] # [x0, y0, x1, y1]
        x0, y0, x1, y1 = rect
        is_left_col = x0 < 200
        
        # Check Height (Section headers are ~18px, so we set range 15-50)
        h = y1 - y0
        is_header_bar = 15 < h < 50
        
        if is_blue and is_left_col and is_header_bar:
            print(f"Adjusting shape at y={y0:.1f} (Height: {h:.1f})")
            
            # Action: Shift UP (-18px on Y) and Increase Height (+6px)
            # Y0 decreases (moves up).
            # Y1 moves up but less, or height increases.
            # New Height = Old Height + 6
            # New Top (y0) = Old Top - 18
            # New Bottom (y1) = New Top + New Height = (y0 - 18) + (h + 6) = y0 + h - 12
            # Wait, y1 is bottom. y0 is top.
            # Shift UP means DECREASING y (in PDF usually). 
            # WAIT. PyMuPDF coords: (0,0) Top Left. 
            # So "UP" means DECREASING Y. Correct.
            
            shift_up = 12.0
            height_inc = 4.0
            
            new_y0 = y0 - shift_up
            new_h = h + height_inc
            new_y1 = new_y0 + new_h
            
            s['rect'] = [x0, new_y0, x1, new_y1]
            modified += 1
            
        new_shapes.append(s)
        
    with open(shapes_path, 'w') as f:
        json.dump(new_shapes, f, indent=2)
        
    print(f"Modified {modified} header shapes.")

if __name__ == "__main__":
    tune_shapes()
