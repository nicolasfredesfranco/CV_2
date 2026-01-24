import json
import shutil

def fix_university():
    json_path = "objetivo_coords.json"
    
    # Backup
    shutil.copy(json_path, json_path + ".bak")
    
    with open(json_path, 'r') as f:
        elements = json.load(f)
    
    # Remove existing university entries (fuzzy match)
    # Search for "Federico" or "Santa" near Y=150
    # Region: X < 200, 140 < Y < 170
    
    new_elements = []
    removed = 0
    
    for e in elements:
        y = e['y']
        x = e['x']
        text = e.get('text', '')
        
        is_uni = False
        if x < 200 and 140 < y < 180:
            if "Federico" in text or "Santa" in text or "Technical" in text or "University" in text:
                 is_uni = True
        
        if not is_uni:
            new_elements.append(e)
        else:
            removed += 1
            
    print(f"Removed {removed} potential university text elements.")
    
    # Inject correct entries
    # Based on "Federico Santa " at y=150.92 from previous grep
    # Desired Lines:
    # 1. Federico Santa María
    # 2. Technical University
    
    # Line 1
    # Note: "Tech" was appearing here, "Technical" appearing in line 2.
    # We force split.
    
    base_x = 42.13
    base_y = 150.92
    
    uni_entries = [
        {
            "text": "Federico Santa María",
            "x": base_x,
            "y": base_y,
            "font": "TrebuchetMS-Bold",
            "size": 14.0,
            "color": 0,
            "bold": True,
            "italic": False
        },
        {
            "text": "Technical University",
            "x": base_x,
            "y": base_y + 16.0, # Guessing line height
            "font": "TrebuchetMS-Bold",
            "size": 14.0,
            "color": 0,
            "bold": True,
            "italic": False
        }
    ]
    
    new_elements.extend(uni_entries)
    
    # Sort
    new_elements.sort(key=lambda k: (k['y'], k['x']))
    
    with open(json_path, 'w') as f:
        json.dump(new_elements, f, indent=2)
        
    print(f"Injected correct University Name. Total elements: {len(new_elements)}")

if __name__ == "__main__":
    fix_university()
