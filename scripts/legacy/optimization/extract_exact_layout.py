#!/usr/bin/env python3
"""
ESTRATEGIA FINAL PARA 95%: Extracción directa del PDF objetivo
Usa pdfplumber para extraer coordenadas EXACTAS del objetivo y replicarlas.

Author: Nicolás Ignacio Fredes Franco
"""

import pdfplumber
from pathlib import Path
import json

def extract_exact_layout_from_objective():
    """Extract exact coordinates, fonts, sizes from objective PDF"""
    
    print("="*100)
    print("EXTRACCIÓN EXACTA DE LAYOUT DEL PDF OBJETIVO")
    print("="*100)
    
    pdf_path = "pdfs/objective/Objetivo_No_editar.pdf"
    
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        
        print(f"\nDimensiones de página: {page.width} x {page.height} pts")
        
        # Extract all text with exact positions
        words = page.extract_words(
            x_tolerance=3,
            y_tolerance=3,
            keep_blank_chars=False,
            use_text_flow=True,
            extra_attrs=['fontname', 'size']
        )
        
        print(f"\nPalabras extraídas: {len(words)}")
        
        # Extract rectangles (colored boxes)
        rects = page.rects
        print(f"Rectángulos extraídos: {len(rects)}")
        
        # Extract lines
        lines = page.lines
        print(f"Líneas extraídas: {len(lines)}")
        
        # Organize data
        extracted_data = {
            'page_dimensions': {
                'width': float(page.width),
                'height': float(page.height)
            },
            'text_elements': [],
            'rectangles': [],
            'lines': []
        }
        
        # Process text
        for i, word in enumerate(words[:100]):  # Show first 100
            extracted_data['text_elements'].append({
                'text': word['text'],
                'x0': float(word['x0']),
                'y0': float(word['top']),
                'x1': float(word['x1']),
                'y1': float(word['bottom']),
                'fontname': word.get('fontname', 'unknown'),
                'fontsize': float(word.get('size', 10))
            })
            
            if i < 20:
                print(f"\n  Palabra {i+1}: '{word['text']}'")
                print(f"    Posición: ({word['x0']:.1f}, {word['top']:.1f})")
                print(f"    Fuente: {word.get('fontname', 'unknown')} {word.get('size', 0):.1f}pt")
        
        # Process rectangles
        for i, rect in enumerate(rects[:50]):
            extracted_data['rectangles'].append({
                'x0': float(rect['x0']),
                'y0': float(rect['y0']),
                'x1': float(rect['x1']),
                'y1': float(rect['y1']),
                'width': float(rect['width']),
                'height': float(rect['height']),
                'linewidth': float(rect.get('linewidth', 1))
            })
            
            if i < 10:
                print(f"\n  Rectángulo {i+1}:")
                print(f"    Posición: ({rect['x0']:.1f}, {rect['y0']:.1f})")
                print(f"    Tamaño: {rect['width']:.1f} x {rect['height']:.1f}")
        
        # Save to file
        output_file = Path("outputs/objetivo_exact_layout.json")
        with open(output_file, 'w') as f:
            json.dump(extracted_data, f, indent=2)
        
        print(f"\n{'='*100}")
        print(f"EXTRACCIÓN COMPLETA")
        print(f"{'='*100}")
        print(f"Datos guardados: {output_file}")
        print(f"  - {len(extracted_data['text_elements'])} elementos de texto")
        print(f"  - {len(extracted_data['rectangles'])} rectángulos")
        print(f"  - {len(extracted_data['lines'])} líneas")
        
        return extracted_data

if __name__ == "__main__":
    data = extract_exact_layout_from_objective()
    
    print("\n🎯 SIGUIENTE PASO:")
    print("   Usar estos datos exactos para regenerar el PDF con las coordenadas precisas del objetivo")
