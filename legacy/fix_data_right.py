import json

def fix_data_right():
    coords_file = "objetivo_coords.json"
    with open(coords_file, 'r') as f:
        data = json.load(f)
        
    updated = 0
    # Dark Blue for Job Titles
    # 0x0f3b60 = 998240
    DARK_BLUE = 998240 
    
    for e in data:
        txt = e['text']
        
        # Job Titles containing "Lead" or "Engineer" in right col
        if e['x'] > 200 and ("Lead" in txt or "Engineer" in txt):
            # Check if likely a title
            if e['size'] > 11:
                print(f"Darkening Title: {txt} ({e['color']} -> {DARK_BLUE})")
                e['color'] = DARK_BLUE
                updated += 1
                
        # Force Company Name Bold/Black check
        if "JOBSITY" in txt:
             # Just verify it's black
             if e['color'] != 0:
                 e['color'] = 0
                 updated += 1
                 
    if updated > 0:
        with open(coords_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated {updated} elements.")

if __name__ == "__main__":
    fix_data_right()
