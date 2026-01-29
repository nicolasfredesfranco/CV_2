#!/usr/bin/env python3
"""
OCR Dictionary Extractor

Extracts every word, number, and symbol from the objective PDF
and saves it as a comprehensive dictionary for future alignment reference.

This script uses pdfplumber to extract:
- Text content
- Exact coordinates (x0, top, x1, bottom, centroids)
- Font information (family, size)
- Bounding boxes

Usage:
    python3 scripts/extract_dictionary.py
"""

import json
import pdfplumber
from pathlib import Path

# Configuration
OBJECTIVE_PDF = Path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf")
OUTPUT_JSON = Path("data/objective_dictionary.json")

def extract_dictionary():
    """Extract all text elements and metadata from the objective PDF."""
    
    print(f"📖 Reading: {OBJECTIVE_PDF}")
    
    if not OBJECTIVE_PDF.exists():
        print(f"❌ Error: File not found: {OBJECTIVE_PDF}")
        return False
    
    entries = []
    
    with pdfplumber.open(OBJECTIVE_PDF) as pdf:
        page = pdf.pages[0]  # First page only
        
        # Extract words with detailed attributes
        words = page.extract_words(
            x_tolerance=2,
            y_tolerance=2,
            keep_blank_chars=False,
            extra_attrs=['fontname', 'size']
        )
        
        print(f"   Found {len(words)} text elements")
        
        for w in words:
            # Calculate centroid
            cx = w['x0'] + (w['width'] / 2)
            cy = w['top'] + (w['height'] / 2)
            
            entry = {
                'text': w['text'],
                'location': {
                    'x0': round(float(w['x0']), 4),
                    'top': round(float(w['top']), 4),
                    'x1': round(float(w['x1']), 4),
                    'bottom': round(float(w['bottom']), 4),
                    'width': round(float(w['width']), 4),
                    'height': round(float(w['height']), 4),
                    'centroid_x': round(float(cx), 4),
                    'centroid_y': round(float(cy), 4)
                },
                'style': {
                    'font_name': str(w.get('fontname', 'Unknown')),
                    'font_size': round(float(w.get('size', 0)), 2)
                }
            }
            entries.append(entry)
        
        # Build complete data structure
        full_data = {
            'metadata': {
                'source_file': str(OBJECTIVE_PDF),
                'page_dimensions': {
                    'width': round(float(page.width), 2),
                    'height': round(float(page.height), 2)
                },
                'total_elements': len(entries),
                'extraction_method': 'pdfplumber'
            },
            'dictionary': entries
        }
        
        # Save to JSON
        OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_JSON, 'w') as f:
            json.dump(full_data, f, indent=2)
        
        print(f"✅ Dictionary saved: {OUTPUT_JSON}")
        print(f"   Total elements: {len(entries)}")
        
        # Show samples
        print("\n📝 Sample entries:")
        for i in range(min(5, len(entries))):
            e = entries[i]
            print(f"   [{i+1}] '{e['text']}' @ ({e['location']['centroid_x']:.1f}, {e['location']['centroid_y']:.1f})")
            print(f"       {e['style']['font_name']} {e['style']['font_size']}pt")
        
        # Verify key sections
        print("\n🎯 Verifying key sections:")
        targets = ["EXPERIENCE", "EDUCATION", "SKILLS", "PAPERS", "LANGUAGES"]
        for target in targets:
            found = next((e for e in entries if target in e['text']), None)
            if found:
                print(f"   ✅ {target}")
            else:
                print(f"   ⚠️  {target} - not found as exact match")
        
        return True

if __name__ == "__main__":
    success = extract_dictionary()
    exit(0 if success else 1)
