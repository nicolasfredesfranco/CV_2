#!/usr/bin/env python3
"""
CV Alignment Verification Tool
================================

Verifies pixel-perfect alignment of the 5 blue section header rectangles
with their corresponding text elements.

This tool uses PyMuPDF to extract exact coordinates from the generated PDF
and validates that all rectangles are properly centered (tolerance: <1.0px).

Usage:
    python3 verify_alignment.py [--json] [--pdf PATH]

Options:
    --json          Output results in JSON format
    --pdf PATH      Custom PDF path (default: outputs/Nicolas_Fredes_CV.pdf)

Author: Nicolás Ignacio Fredes Franco
License: MIT
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


# Section names and their expected text
SECTIONS = [
    'EXPERIENCE',
    'EDUCATION', 
    'PAPERS & WORKSHOPS',
    'SKILLS',
    'LANGUAGES'
]


def verify_alignment(pdf_path: str, output_json: bool = False) -> dict:
    """
    Verify alignment of all 5 rectangles.
    
    Args:
        pdf_path: Path to PDF file
        output_json: If True, return results as JSON
        
    Returns:
        Dictionary with verification results
    """
    # Load PDF and data
    pdf = fitz.open(pdf_path)
    page = pdf[0]
    page_height = page.rect.height
    
    data_dir = Path(__file__).parent.parent / 'data'
    with open(data_dir / 'shapes.json', 'r') as f:
        shapes = json.load(f)
    
    results = {
        'pdf': pdf_path,
        'sections': [],
        'all_perfect': True
    }
    
    # Verify each section
    for i, name in enumerate(SECTIONS):
        rect = shapes[i]
        target = name
        
        # Calculate rectangle center
        rect_y_fitz = page_height - rect['y']
        rect_y2_fitz = rect_y_fitz - rect['height']
        rect_center = rect['y'] + rect['height'] / 2
        
        # Search for text
        search_area = fitz.Rect(
            rect['x'] - 5,
            rect_y2_fitz - 5,
            rect['x'] + rect['width'] + 5,
            rect_y_fitz + 5
        )
        
        found_text = None
        text_center = None
        
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block['type'] == 0:
                block_bbox = fitz.Rect(block['bbox'])
                if block_bbox.intersects(search_area):
                    for line in block['lines']:
                        line_text = ''.join([span['text'] for span in line['spans']]).strip()
                        if target in line_text:
                            line_bbox = fitz.Rect(line['bbox'])
                            line_y_shapes = page_height - line_bbox.y1
                            line_y2_shapes = page_height - line_bbox.y0
                            text_center = (line_y_shapes + line_y2_shapes) / 2
                            found_text = line_text
                            break
        
        # Analyze results
        section_result = {
            'name': name,
            'rect_y': rect['y'],
            'rect_height': rect['height'],
            'rect_center': rect_center,
            'text_found': found_text,
            'text_center': text_center,
            'status': 'PERFECT',
            'delta': 0.0
        }
        
        if found_text and text_center:
            diff = abs(rect_center - text_center)
            section_result['delta'] = round(diff, 2)
            
            if diff >= 1.0:
                section_result['status'] = f'MISALIGNED (Δ{diff:.2f}px)'
                results['all_perfect'] = False
        else:
            section_result['status'] = 'TEXT_NOT_FOUND'
            results['all_perfect'] = False
        
        results['sections'].append(section_result)
    
    pdf.close()
    
    # Output
    if output_json:
        print(json.dumps(results, indent=2))
    else:
        print_results(results)
    
    return results


def print_results(results: dict) -> None:
    """Print formatted results to console."""
    print("=" * 100)
    print(" " * 35 + "CV ALIGNMENT VERIFICATION")
    print("=" * 100)
    print(f"\nPDF: {results['pdf']}\n")
    
    for section in results['sections']:
        print(f"[{section['name']}]")
        print(f"    Rectangle: y={section['rect_y']:.2f}, "
              f"height={section['rect_height']:.2f}, "
              f"center={section['rect_center']:.2f}")
        
        if section['text_found']:
            print(f"    Text: '{section['text_found']}', center={section['text_center']:.2f}")
            
        status = section['status']
        if status == 'PERFECT':
            print(f"    ✅ {status}")
        else:
            print(f"    ⚠️  {status}")
        print()
    
    print("=" * 100)
    if results['all_perfect']:
        print("✅ ALL SECTIONS PERFECTLY ALIGNED")
    else:
        print("⚠️  SOME SECTIONS REQUIRE ADJUSTMENT")
    print("=" * 100)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Verify CV rectangle alignment',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    parser.add_argument(
        '--pdf',
        type=str,
        default='outputs/Nicolas_Fredes_CV.pdf',
        help='Path to PDF file (default: outputs/Nicolas_Fredes_CV.pdf)'
    )
    
    args = parser.parse_args()
    
    # Verify PDF exists
    if not Path(args.pdf).exists():
        print(f"❌ Error: PDF not found at {args.pdf}")
        sys.exit(1)
    
    # Run verification
    results = verify_alignment(args.pdf, args.json)
    
    # Exit code
    sys.exit(0 if results['all_perfect'] else 1)


if __name__ == "__main__":
    main()
