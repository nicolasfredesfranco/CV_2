import json

def audit_right():
    print("--- Shapes (High X) ---")
    with open('objetivo_shapes.json', 'r') as f:
        shapes = json.load(f)
        
    blue_candidates = []
    for s in shapes:
        if s['type'] == 'rect':
            x0, y0, x1, y1 = s['rect']
            if x0 > 200:
                h = y1 - y0
                w = x1 - x0
                color = s.get('color', None)
                print(f"Rect at ({x0:.1f}, {y0:.1f}) | W={w:.1f} H={h:.1f} | Color={color}")
                if color and color[2] > 0.5: # Blue-ish?
                     blue_candidates.append(s)

    print(f"\nFound {len(blue_candidates)} potential blue headers in Right Column.")
    
    print("\n--- Text (High X) ---")
    with open('objetivo_coords.json', 'r') as f:
        coords = json.load(f)
        
    headers = ['EXPERIENCE', 'EDUCATION', 'PROJECTS'] # Education is Left, but check if separate
    
    for e in coords:
        if e['x'] > 200:
            if e['text'].strip() in headers or 'EXPERIENCE' in e['text']:
                print(f"Header Text: '{e['text']}' at ({e['x']:.1f}, {e['y']:.1f}) | Color={e.get('color')} | Font={e.get('font')}")

if __name__ == "__main__":
    audit_right()
