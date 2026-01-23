
import fitz
import json
import math
from collections import defaultdict
from cv_utils import classify_element

def extract_all_elements(pdf_path):
    """Extrae todos los elementos de texto con sus posiciones exactas"""
    doc = fitz.open(pdf_path)
    page = doc[0]
    words = page.get_text("words")
    doc.close()
    
    elements = []
    for w in words:
        elements.append({
            'text': w[4],
            'x': w[0],
            'y': w[1],
            'x_end': w[2],
            'y_end': w[3],
            'width': w[2] - w[0],
            'height': w[3] - w[1]
        })
    return elements

def generate_gap_report(gen_path, obj_path, output_md):
    gen_elements = extract_all_elements(gen_path)
    obj_elements = extract_all_elements(obj_path)
    
    # Match elements by text content (approximate) to find position errors
    issues = []
    
    # Create a map of objective elements for faster lookup
    # Using a simple heuristic: first word match + proximity
    # This is a simplification, but sufficient for gap analysis
    
    used_obj_indices = set()
    
    for i, gen in enumerate(gen_elements):
        best_match = None
        min_dist = float('inf')
        best_idx = -1
        
        for j, obj in enumerate(obj_elements):
            if j in used_obj_indices:
                continue
                
            if gen['text'] == obj['text']:
                # Calculate Euclidean distance
                dist = math.sqrt((gen['x'] - obj['x'])**2 + (gen['y'] - obj['y'])**2)
                if dist < min_dist and dist < 20: # Search radius
                    min_dist = dist
                    best_match = obj
                    best_idx = j
        
        if best_match:
            used_obj_indices.add(best_idx)
            dx = gen['x'] - best_match['x']
            dy = gen['y'] - best_match['y']
            
            # Threshold for "gap": 0.1 pt
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                section = classify_element(gen)
                issues.append({
                    'type': 'POSITION',
                    'text': gen['text'],
                    'section': section,
                    'dx': dx,
                    'dy': dy,
                    'magnitude': math.sqrt(dx*dx + dy*dy)
                })
        else:
            issues.append({
                'type': 'MISSING/MISMATCH',
                'text': gen['text'],
                'section': classify_element(gen),
                'dx': 0, 'dy': 0,
                'magnitude': 100 # High priority
            })

    # Find elements in objective not matched
    for j, obj in enumerate(obj_elements):
        if j not in used_obj_indices:
            issues.append({
                'type': 'EXTRA_IN_TARGET',
                'text': obj['text'],
                'section': classify_element(obj),
                'dx': 0, 'dy': 0,
                'magnitude': 100
            })
            
    # Sort by magnitude (biggest errors first)
    issues.sort(key=lambda x: x['magnitude'], reverse=True)
    
    # Generate Markdown
    with open(output_md, 'w') as f:
        f.write("# 100 Gap Analysis Report\n\n")
        f.write(f"Total discrepancies found: {len(issues)}\n\n")
        f.write("| Rank | Section | Type | Text | ΔX | ΔY | Magnitude |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        
        for i, issue in enumerate(issues[:100]):
            f.write(f"| {i+1} | {issue['section']} | {issue['type']} | `{issue['text']}` | {issue['dx']:.2f} | {issue['dy']:.2f} | {issue['magnitude']:.2f} |\n")

    print(f"Report generated: {output_md}")
    return issues

if __name__ == "__main__":
    generate_gap_report('outputs/Nicolas_Fredes_CV.pdf', 'Objetivo_No_editar.pdf', 'gap_analysis_100.md')
