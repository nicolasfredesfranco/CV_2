#!/usr/bin/env python3
"""
CV Color Comparison Tool
========================

Compares job title colors between the generated PDF and the objective reference PDF.
Identifies mismatches and suggests corrections.

Usage:
    python3 compare_colors.py

Author: Nicolás Ignacio Fredes Franco
License: MIT
"""

import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


JOB_TITLES = [
    'Lead Artificial Intelligence Engineer',
    'Senior Machine Learning Engineer',
    'Lead Data Scientist',
    'Computer Vision Engineer'
]


def extract_colors(pdf_path: str, titles: list) -> dict:
    """
    Extract colors for specific job titles from PDF.
    
    Args:
        pdf_path: Path to PDF file
        titles: List of job titles to search for
        
    Returns:
        Dictionary mapping titles to their colors
    """
    pdf = fitz.open(pdf_path)
    page = pdf[0]
    colors = {}
    
    blocks = page.get_text('dict')['blocks']
    for block in blocks:
        if block['type'] == 0:  # text block
            for line in block['lines']:
                line_text = ''.join([span['text'] for span in line['spans']]).strip()
                for title in titles:
                    if title in line_text and title not in colors:
                        for span in line['spans']:
                            if title in span['text']:
                                colors[title] = span['color']
                                break
    
    pdf.close()
    return colors


def color_to_hex(color: int) -> str:
    """Convert decimal color to hex string."""
    r = (color >> 16) & 0xFF
    g = (color >> 8) & 0xFF
    b = color & 0xFF
    return f"#{r:02X}{g:02X}{b:02X}"


def main():
    """Main entry point."""
    print("=" * 80)
    print(" " * 25 + "CV COLOR VERIFICATION")
    print("=" * 80)
    print()
    
    # Paths
    data_dir = Path(__file__).parent.parent / 'data'
    generated_pdf = Path(__file__).parent.parent / 'outputs' / 'Nicolas_Fredes_CV.pdf'
    objective_pdf = data_dir / 'objective_reference.pdf'
    
    # Verify files exist
    if not generated_pdf.exists():
        print(f"❌ Generated PDF not found: {generated_pdf}")
        sys.exit(1)
    
    if not objective_pdf.exists():
        print(f"❌ Objective PDF not found: {objective_pdf}")
        sys.exit(1)
    
    # Extract colors
    print("📄 Extracting colors from PDFs...\n")
    generated_colors = extract_colors(str(generated_pdf), JOB_TITLES)
    objective_colors = extract_colors(str(objective_pdf), JOB_TITLES)
    
    # Compare
    all_match = True
    
    for title in JOB_TITLES:
        gen_color = generated_colors.get(title)
        obj_color = objective_colors.get(title)
        
        print(f"▸ {title}")
        
        if gen_color is None:
            print(f"  ❌ Not found in generated PDF")
            all_match = False
        elif obj_color is None:
            print(f"  ⚠️  Not found in objective PDF")
            all_match = False
        else:
            gen_hex = color_to_hex(gen_color)
            obj_hex = color_to_hex(obj_color)
            
            if gen_color == obj_color:
                print(f"  ✅ MATCH: {obj_hex} (decimal: {obj_color})")
            else:
                print(f"  ❌ MISMATCH:")
                print(f"     Generated:  {gen_hex} (decimal: {gen_color})")
                print(f"     Objective:  {obj_hex} (decimal: {obj_color})")
                print(f"     → Update coordinates.json: {gen_color} → {obj_color}")
                all_match = False
        print()
    
    print("=" * 80)
    if all_match:
        print("✅ ALL COLORS MATCH OBJECTIVE PDF")
    else:
        print("⚠️  SOME COLORS NEED CORRECTION")
    print("=" * 80)
    
    sys.exit(0 if all_match else 1)


if __name__ == "__main__":
    main()
