import fitz
import json

INPUT_PDF = "/home/nicofredes/Desktop/code/CV/nueva_version_no_editar.pdf"
TARGET_COLOR_INT = 1070028
# Convert to normalize RGB for fitz
R = ((TARGET_COLOR_INT >> 16) & 0xFF) / 255.0
G = ((TARGET_COLOR_INT >> 8) & 0xFF) / 255.0
B = (TARGET_COLOR_INT & 0xFF) / 255.0

print(f"Target RGB: ({R:.3f}, {G:.3f}, {B:.3f})")

def find_colored_paths():
    doc = fitz.open(INPUT_PDF)
    page = doc[0] # Assume page 1
    
    paths = page.get_drawings()
    found_paths = []
    
    for p in paths:
        # Check fill color
        fill = p['fill']
        if fill and len(fill) == 3:
            # Check proximity (tolerance 0.05)
            if (abs(fill[0] - R) < 0.05 and 
                abs(fill[1] - G) < 0.05 and 
                abs(fill[2] - B) < 0.05):
                
                # Found a blue path!
                found_paths.append(p['rect'])
    
    print(f"Found {len(found_paths)} matching paths.")
    
    # Cluster paths (simple bounding box union)
    # Ideally we cluster by Y proximity
    
    clusters = []
    # Sort by Y-coordinate of the center to group reliably
    # rect is (x0, y0, x1, y1)
    sorted_rects = sorted(found_paths, key=lambda r: (r[1] + r[3])/2)
    
    if not sorted_rects:
        print("No paths found.")
        return

    clusters = []
    current_cluster = [sorted_rects[0]]
    
    for r in sorted_rects[1:]:
        last = current_cluster[-1]
        
        # Check Y-center proximity
        y_center_r = (r[1] + r[3]) / 2
        y_center_last = (last[1] + last[3]) / 2
        
        # If centers are close (within 3 units), it's the same line
        if abs(y_center_r - y_center_last) < 4.0:
            current_cluster.append(r)
        else:
            clusters.append(current_cluster)
            current_cluster = [r]
            
    clusters.append(current_cluster)
    
    final_regions = []
    for cluster in clusters:
        # Compute union bbox
        x0 = min(r[0] for r in cluster)
        y0 = min(r[1] for r in cluster)
        x1 = max(r[2] for r in cluster)
        y1 = max(r[3] for r in cluster)
        final_regions.append([x0, y0, x1, y1])
        
    print(json.dumps(final_regions, indent=2))

if __name__ == "__main__":
    find_colored_paths()
