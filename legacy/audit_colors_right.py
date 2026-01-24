import json

def audit_right_details():
    with open('objetivo_coords.json', 'r') as f:
        coords = json.load(f)
        
    targets = ['EXPERIENCE', 'Lead Artificial Intelligence Engineer', 'JOBSITY']
    
    for e in coords:
        txt = e['text'].strip()
        found = False
        for t in targets:
            if t in txt:
                found = True
                break
        
        if found:
            print(f"Text: '{txt[:30]}...'")
            print(f"  Pos: ({e['x']:.1f}, {e['y']:.1f})")
            print(f"  Font: {e.get('font')} | Size: {e.get('size'):.2f}")
            print(f"  Color Int: {e.get('color')}")
            # Decode Color
            c = e.get('color', 0)
            if c:
                r = (c >> 16) & 0xFF
                g = (c >> 8) & 0xFF
                b = c & 0xFF
                print(f"  RGB: ({r}, {g}, {b}) -> Hex: #{r:02x}{g:02x}{b:02x}")
            print("-" * 40)

if __name__ == "__main__":
    audit_right_details()
