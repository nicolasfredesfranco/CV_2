#!/usr/bin/env python3
"""
Detailed PDF Comparison Script
Extracts all text elements from both PDFs for precise diff analysis
"""
import fitz
import json

def extract_all_text_with_positions(pdf_path):
    """Extract every text element with exact positioning"""
    pdf = fitz.open(pdf_path)
    page = pdf[0]
    page_height = page.rect.height
    
    elements = []
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if block['type'] == 0:  # text
            for line in block['lines']:
                for span in line['spans']:
                    # Convert to shapes.json coordinate system (origin at bottom-left)
                    y_shapes = page_height - span['bbox'][3]
                    
                    elements.append({
                        'text': span['text'],
                        'x': round(span['bbox'][0], 2),
                        'y': round(y_shapes, 2),
                        'font': span['font'],
                        'size': round(span['size'], 2),
                        'bold': 'Bold' in span['font'],
                        'italic': 'Italic' in span['font']
                    })
    
    pdf.close()
    return elements

# Extract from both PDFs
print("Extracting from objective PDF...")
obj_elements = extract_all_text_with_positions('pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf')

print("Extracting from generated PDF...")
gen_elements = extract_all_text_with_positions('outputs/Nicolas_Fredes_CV.pdf')

# Focus on PAPERS & WORKSHOPS section (y: 360-441)
obj_papers = [e for e in obj_elements if 360 < e['y'] < 441 and e['text'].strip()]
gen_papers = [e for e in gen_elements if 360 < e['y'] < 441 and e['text'].strip()]

# Focus on SKILLS section (y: 450-520)
obj_skills = [e for e in obj_elements if 450 < e['y'] < 520 and e['text'].strip()]
gen_skills = [e for e in gen_elements if 450 < e['y'] < 520 and e['text'].strip()]

print("\n" + "="*100)
print("PAPERS & WORKSHOPS SECTION - OBJECTIVE vs GENERATED")
print("="*100)
print(f"\nObjective: {len(obj_papers)} elements | Generated: {len(gen_papers)} elements\n")

# Show first 15 elements of each
print("OBJECTIVE (first 15):")
for i, e in enumerate(obj_papers[:15]):
    bold_marker = " [B]" if e['bold'] else ""
    print(f"{i:2d}. y={e['y']:6.2f} x={e['x']:6.2f} size={e['size']:4.1f} {e['font']:25s}{bold_marker} \"{e['text'][:50]}\"")

print("\nGENERATED (first 15):")
for i, e in enumerate(gen_papers[:15]):
    bold_marker = " [B]" if e['bold'] else ""
    print(f"{i:2d}. y={e['y']:6.2f} x={e['x']:6.2f} size={e['size']:4.1f} {e['font']:25s}{bold_marker} \"{e['text'][:50]}\"")

print("\n" + "="*100)
print("SKILLS SECTION - OBJECTIVE vs GENERATED")
print("="*100)
print(f"\nObjective: {len(obj_skills)} elements | Generated: {len(gen_skills)} elements\n")

print("OBJECTIVE (first 15):")
for i, e in enumerate(obj_skills[:15]):
    bold_marker = " [B]" if e['bold'] else ""
    print(f"{i:2d}. y={e['y']:6.2f} x={e['x']:6.2f} size={e['size']:4.1f} {e['font']:25s}{bold_marker} \"{e['text'][:50]}\"")

print("\nGENERATED (first 15):")
for i, e in enumerate(gen_skills[:15]):
    bold_marker = " [B]" if e['bold'] else ""
    print(f"{i:2d}. y={e['y']:6.2f} x={e['x']:6.2f} size={e['size']:4.1f} {e['font']:25s}{bold_marker} \"{e['text'][:50]}\"")

# Find HGAN bolding issue
print("\n" + "="*100)
print("HGAN BOLDING ANALYSIS")
print("="*100)
obj_hgan = [e for e in obj_elements if 'HGAN' in e['text'] or 'Hyperbolic' in e['text']]
gen_hgan = [e for e in gen_elements if 'HGAN' in e['text'] or 'Hyperbolic' in e['text']]

print("\nOBJECTIVE:")
for e in obj_hgan:
    bold_marker = " [BOLD]" if e['bold'] else " [normal]"
    print(f"  \"{e['text']}\"{bold_marker}")

print("\nGENERATED:")
for e in gen_hgan:
    bold_marker = " [BOLD]" if e['bold'] else " [normal]"
    print(f"  \"{e['text']}\"{bold_marker}")
