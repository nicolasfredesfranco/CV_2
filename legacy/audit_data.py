import json
import statistics

def audit_data():
    with open('objetivo_coords.json', 'r') as f:
        data = json.load(f)
        
    print(f"Total elements: {len(data)}")
    
    # Check X distribution
    xs = [e['x'] for e in data]
    print(f"X range: {min(xs):.1f} to {max(xs):.1f}")
    
    # Filter Right Column candidates
    right_col = [e for e in data if e['x'] > 200]
    print(f"Elements with X > 200: {len(right_col)}")
    if right_col:
        print("Sample X > 200:")
        for e in right_col[:5]:
            print(f"  {e['text']} (x={e['x']:.1f})")
            
    # Check Duplicates (Ghosting)
    # Same text, similar position (dist < 2px)
    print("\nChecking for Spatial Duplicates...")
    
    # naive n^2 check
    dupes = []
    seen = set()
    
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            a = data[i]
            b = data[j]
            
            if a['text'] == b['text']:
                dist = abs(a['x'] - b['x']) + abs(a['y'] - b['y'])
                if dist < 5.0 and dist > 0.1:
                   print(f"Potential Ghost: '{a['text']}' at ({a['x']:.1f}, {a['y']:.1f}) vs ({b['x']:.1f}, {b['y']:.1f}) | Dist: {dist:.1f}")
                   dupes.append((i, j))
                elif dist <= 0.1:
                    print(f"Exact Duplicate: '{a['text']}'")
                    dupes.append((i,j))

    # Check "Floating Letters"
    # Single chars with X < 200 that might be Right Column artifacts
    print("\nChecking Floating Single Chars in Left Col:")
    for e in data:
        if e['x'] < 200 and len(e['text'].strip()) == 1 and e['text'].strip().isalpha():
            print(f"  '{e['text']}' at ({e['x']:.1f}, {e['y']:.1f})")

if __name__ == "__main__":
    audit_data()
