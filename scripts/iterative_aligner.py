#!/usr/bin/env python3
"""
Iterative OCR Alignment Optimizer

Compares objective PDF with generated CV using OCR word extraction,
identifies discrepancies, and applies corrections iteratively.

Usage:
    python3 scripts/iterative_aligner.py [--max-iterations 10]
"""

import json
import fitz
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Paths
OBJECTIVE_PDF = Path("pdfs/objective/Objetivo_No_editar.pdf")
GENERATED_PDF = Path("outputs/Nicolas_Fredes_CV.pdf")
COORDS_JSON = Path("data/coordinates.json")
OBJ_DICT_JSON = Path("data/objective_dictionary.json")
GEN_DICT_JSON = Path("data/generated_dictionary.json")

def extract_ocr_dictionary(pdf_path: Path) -> Dict:
    """Extract OCR dictionary from PDF."""
    print(f"📖 Extrayendo OCR de: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    page = doc[0]
    words = page.get_text("words")
    
    # Get page dimensions before closing
    page_width = float(page.rect.width)
    page_height = float(page.rect.height)
    
    entries = []
    for w in words:
        x0, y0, x1, y1, text, block_no, line_no, word_no = w
        
        cx = x0 + (x1 - x0) / 2
        cy = y0 + (y1 - y0) / 2
        
        entries.append({
            'text': text,
            'location': {
                'x0': round(float(x0), 4),
                'top': round(float(y0), 4),
                'x1': round(float(x1), 4),
                'bottom': round(float(y1), 4),
                'centroid_x': round(float(cx), 4),
                'centroid_y': round(float(cy), 4)
            }
        })
    
    doc.close()
    
    result = {
        'metadata': {
            'source_file': str(pdf_path),
            'total_elements': len(entries),
            'page_dimensions': {
                'width': round(page_width, 2),
                'height': round(page_height, 2)
            }
        },
        'dictionary': entries
    }
    
    print(f"   ✅ Extraídas {len(entries)} palabras\n")
    return result

def compare_dictionaries(obj_dict: Dict, gen_dict: Dict) -> List[Dict]:
    """Compare two OCR dictionaries and find discrepancies."""
    print("🔍 Comparando diccionarios...")
    
    discrepancies = []
    
    for obj_entry in obj_dict['dictionary']:
        text = obj_entry['text']
        
        # Find matching word in generated
        gen_matches = [e for e in gen_dict['dictionary'] if e['text'] == text]
        
        if not gen_matches:
            # Word missing in generated
            discrepancies.append({
                'text': text,
                'type': 'missing',
                'obj_pos': obj_entry['location'],
                'gen_pos': None,
                'distance': 999
            })
        else:
            # Compare positions
            gen_entry = gen_matches[0]
            
            dx = obj_entry['location']['centroid_x'] - gen_entry['location']['centroid_x']
            dy = obj_entry['location']['centroid_y'] - gen_entry['location']['centroid_y']
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 0.5:  # Threshold for considering it different
                discrepancies.append({
                    'text': text,
                    'type': 'misaligned',
                    'obj_pos': obj_entry['location'],
                    'gen_pos': gen_entry['location'],
                    'distance': round(distance, 2),
                    'dx': round(dx, 2),
                    'dy': round(dy, 2)
                })
    
    # Sort by distance (largest first)
    discrepancies.sort(key=lambda x: x['distance'], reverse=True)
    
    print(f"   Total discrepancias: {len(discrepancies)}\n")
    return discrepancies

def show_top_discrepancies(discrepancies: List[Dict], top_n: int = 10):
    """Display top N discrepancies."""
    print(f"🎯 Top {top_n} Discrepancias:\n")
    
    for i, disc in enumerate(discrepancies[:top_n], 1):
        print(f"{i}. '{disc['text']}' - {disc['type']}")
        if disc['type'] == 'misaligned':
            print(f"   Distancia: {disc['distance']:.2f}px")
            print(f"   ΔX: {disc['dx']:.2f}px, ΔY: {disc['dy']:.2f}px")
            print(f"   Objetivo: ({disc['obj_pos']['centroid_x']:.1f}, {disc['obj_pos']['centroid_y']:.1f})")
            print(f"   Generado: ({disc['gen_pos']['centroid_x']:.1f}, {disc['gen_pos']['centroid_y']:.1f})")
        print()

def apply_corrections(discrepancies: List[Dict], threshold: float):
    """Apply corrections to coordinates.json for discrepancies above threshold."""
    print(f"🔧 Aplicando correcciones (umbral: >{threshold}px)...\n")
    
    # Load current coordinates
    with open(COORDS_JSON, 'r') as f:
        coords = json.load(f)
    
    corrections_applied = 0
    
    for disc in discrepancies:
        if disc['type'] != 'misaligned' or disc['distance'] <= threshold:
            continue
        
        # Find matching entry in coordinates.json
        for item in coords:
            if disc['text'] in item.get('text', ''):
                # Apply correction
                old_x = item.get('x', 0)
                old_y = item.get('y', 0)
                
                # Move towards objective position
                item['x'] = disc['obj_pos']['x0']
                item['y'] = disc['obj_pos']['top']
                
                print(f"   ✅ Corrigiendo '{disc['text']}':")
                print(f"      Antes: ({old_x:.1f}, {old_y:.1f})")
                print(f"      Después: ({item['x']:.1f}, {item['y']:.1f})")
                
                corrections_applied += 1
                break
    
    # Save
    if corrections_applied > 0:
        with open(COORDS_JSON, 'w') as f:
            json.dump(coords, f, indent=2)
        
        print(f"\n✅ Aplicadas {corrections_applied} correcciones")
    else:
        print(f"\n⚠️  No se aplicaron correcciones")
    
    return corrections_applied

def main():
    print("=" * 60)
    print("OPTIMIZADOR ITERATIVO OCR")
    print("=" * 60)
    print()
    
    # Step 1: Extract objective dictionary
    if not OBJ_DICT_JSON.exists():
        obj_dict = extract_ocr_dictionary(OBJECTIVE_PDF)
        with open(OBJ_DICT_JSON, 'w') as f:
            json.dump(obj_dict, f, indent=2)
    else:
        with open(OBJ_DICT_JSON, 'r') as f:
            obj_dict = json.load(f)
        print(f"✅ Diccionario objetivo cargado: {obj_dict['metadata']['total_elements']} palabras\n")
    
    # Step 2: Extract generated dictionary
    gen_dict = extract_ocr_dictionary(GENERATED_PDF)
    with open(GEN_DICT_JSON, 'w') as f:
        json.dump(gen_dict, f, indent=2)
    
    # Step 3: Compare
    discrepancies = compare_dictionaries(obj_dict, gen_dict)
    
    # Step 4: Show top issues
    show_top_discrepancies(discrepancies, 15)
    
    # Step 5: Ask for action
    print("=" * 60)
    print("SIGUIENTE ACCIÓN:")
    print("1. Corregir diferencias >10px")
    print("2. Corregir diferencias >5px")
    print("3. Corregir diferencias >2px")
    print("4. Mostrar todas las diferencias")
    print("=" * 60)
    
    return discrepancies

if __name__ == "__main__":
    discrepancies = main()
