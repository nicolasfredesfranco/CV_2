#!/usr/bin/env python3
"""
Precise Section Comparison Tool
Compares PAPERS & WORKSHOPS and SKILLS sections in detail
"""
import fitz
import json
from pathlib import Path

def extract_section_elements(pdf_path, section_name, y_min, y_max):
    """Extract all text elements in a specific section"""
    pdf = fitz.open(pdf_path)
    page = pdf[0]
    page_height = page.rect.height
    
    elements = []
    blocks = page.get_text("dict")["blocks"]
    
    for block in blocks:
        if block['type'] == 0:  # text
            for line in block['lines']:
                for span in line['spans']:
                    # Convert to shapes.json coordinates (bottom-left origin)
                    y_shapes = page_height - span['bbox'][3]
                    
                    if y_min <= y_shapes <= y_max:
                        elements.append({
                            'text': span['text'].strip(),
                            'x': round(span['bbox'][0], 2),
                            'y': round(y_shapes, 2),
                            'font': span['font'],
                            'size': round(span['size'], 2),
                            'bold': 'Bold' in span['font'],
                            'color': span['color']
                        })
    
    pdf.close()
    # Sort by y (descending), then x
    elements.sort(key=lambda e: (-e['y'], e['x']))
    return elements

# Paths
obj_pdf = 'data/objective_reference.pdf'
gen_pdf = 'outputs/Nicolas_Fredes_CV.pdf'

print("="*100)
print("DETAILED SECTION COMPARISON - OBJECTIVE vs GENERATED")
print("="*100)

# Check if objective PDF exists and has text
try:
    pdf = fitz.open(obj_pdf)
    page = pdf[0]
    blocks = page.get_text("dict")["blocks"]
    text_blocks = [b for b in blocks if b['type'] == 0]
    pdf.close()
    
    if len(text_blocks) == 0:
        print(f"\n⚠️  WARNING: {obj_pdf} has no extractable text!")
        print("This PDF may be image-based or corrupted.")
        print("\nTrying alternative objective PDF...")
        obj_pdf = 'pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf'
except Exception as e:
    print(f"\n❌ Error reading objective PDF: {e}")

# PAPERS & WORKSHOPS Section (y: 360-441 in shapes coords)
print("\n" + "="*100)
print("PAPERS & WORKSHOPS SECTION")
print("="*100)

obj_papers = extract_section_elements(obj_pdf, "PAPERS", 360, 441)
gen_papers = extract_section_elements(gen_pdf, "PAPERS", 360, 441)

print(f"\nObjective: {len(obj_papers)} elements")
print(f"Generated: {len(gen_papers)} elements")

if len(obj_papers) > 0:
    print("\n--- OBJECTIVE PDF ---")
    for i, e in enumerate(obj_papers[:20]):
        bold = "[B]" if e['bold'] else "   "
        print(f"{i:2d}. {bold} y={e['y']:6.2f} x={e['x']:6.2f} sz={e['size']:4.1f} {e['font'][:20]:20s} \"{e['text'][:50]}\"")
    
    print("\n--- GENERATED PDF ---")
    for i, e in enumerate(gen_papers[:20]):
        bold = "[B]" if e['bold'] else "   "
        # Try to find matching element in objective
        match = None
        for obj_e in obj_papers:
            if obj_e['text'] == e['text']:
                match = obj_e
                break
        
        delta_y = f"Δy={e['y']-match['y']:+5.2f}" if match else ""
        delta_x = f"Δx={e['x']-match['x']:+5.2f}" if match else ""
        
        print(f"{i:2d}. {bold} y={e['y']:6.2f} x={e['x']:6.2f} sz={e['size']:4.1f} {e['font'][:20]:20s} \"{e['text'][:50]}\" {delta_y} {delta_x}")
else:
    print("\n⚠️  No text extracted from objective PDF in PAPERS section")
    print("\n--- GENERATED PDF (for reference) ---")
    for i, e in enumerate(gen_papers[:20]):
        bold = "[B]" if e['bold'] else "   "
        print(f"{i:2d}. {bold} y={e['y']:6.2f} x={e['x']:6.2f} sz={e['size']:4.1f} {e['font'][:20]:20s} \"{e['text'][:50]}\"")

# SKILLS Section (y: 280-520 in shapes coords)
print("\n" + "="*100)
print("SKILLS SECTION")
print("="*100)

obj_skills = extract_section_elements(obj_pdf, "SKILLS", 280, 520)
gen_skills = extract_section_elements(gen_pdf, "SKILLS", 280, 520)

print(f"\nObjective: {len(obj_skills)} elements")
print(f"Generated: {len(gen_skills)} elements")

if len(obj_skills) > 0:
    print("\n--- OBJECTIVE PDF ---")
    for i, e in enumerate(obj_skills[:25]):
        bold = "[B]" if e['bold'] else "   "
        print(f"{i:2d}. {bold} y={e['y']:6.2f} x={e['x']:6.2f} sz={e['size']:4.1f} {e['font'][:20]:20s} \"{e['text'][:50]}\"")
    
    print("\n--- GENERATED PDF ---")
    for i, e in enumerate(gen_skills[:25]):
        bold = "[B]" if e['bold'] else "   "
        match = None
        for obj_e in obj_skills:
            if obj_e['text'] == e['text']:
                match = obj_e
                break
        
        delta_y = f"Δy={e['y']-match['y']:+5.2f}" if match else ""
        delta_x = f"Δx={e['x']-match['x']:+5.2f}" if match else ""
        
        print(f"{i:2d}. {bold} y={e['y']:6.2f} x={e['x']:6.2f} sz={e['size']:4.1f} {e['font'][:20]:20s} \"{e['text'][:50]}\" {delta_y} {delta_x}")
else:
    print("\n⚠️  No text extracted from objective PDF in SKILLS section")
    print("\n--- GENERATED PDF (for reference) ---")
    for i, e in enumerate(gen_skills[:25]):
        bold = "[B]" if e['bold'] else "   "
        print(f"{i:2d}. {bold} y={e['y']:6.2f} x={e['x']:6.2f} sz={e['size']:4.1f} {e['font'][:20]:20s} \"{e['text'][:50]}\"")

print("\n" + "="*100)
print("ANALYSIS COMPLETE")
print("="*100)
