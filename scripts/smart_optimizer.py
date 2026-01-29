#!/usr/bin/env python3
"""
Intelligent Word-by-Word Position Optimizer

Compares objective and generated CVs by matching each word occurrence
to its closest counterpart, computing average centroid distance as a
similarity metric, and iteratively reducing this distance.

Metric: Average distance between matched word centroids (lower is better)

Usage:
    python3 scripts/smart_optimizer.py
"""

import json
import fitz
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess

# Paths
OBJECTIVE_PDF = Path("pdfs/objective/Objetivo_No_editar.pdf")
GENERATED_PDF = Path("outputs/Nicolas_Fredes_CV.pdf")
COORDS_JSON = Path("data/coordinates.json")
OBJ_DICT_JSON = Path("data/objective_dictionary.json")
GEN_DICT_JSON = Path("data/generated_dictionary.json")

def extract_ocr(pdf_path: Path) -> List[Dict]:
    """Extract words from PDF."""
    doc = fitz.open(pdf_path)
    page = doc[0]
    words = page.get_text("words")
    doc.close()
    
    entries = []
    for w in words:
        x0, y0, x1, y1, text, block_no, line_no, word_no = w
        cx = x0 + (x1 - x0) / 2
        cy = y0 + (y1 - y0) / 2
        
        entries.append({
            'text': text,
            'cx': round(float(cx), 4),
            'cy': round(float(cy), 4),
            'x0': round(float(x0), 4),
            'y0': round(float(y0), 4)
        })
    
    return entries

def match_words_intelligently(obj_words: List[Dict], gen_words: List[Dict]) -> List[Tuple]:
    """
    Match each word in generated CV to its closest counterpart in objective.
    Returns: List of (obj_word, gen_word, distance) tuples
    """
    matches = []
    
    # For each word in generated CV
    for gen_word in gen_words:
        text = gen_word['text']
        
        # Find ALL occurrences of this word in objective
        candidates = [w for w in obj_words if w['text'] == text]
        
        if not candidates:
            # Word doesn't exist in objective (shouldn't happen if CVs are the same)
            continue
        
        # Find the closest occurrence by Euclidean distance
        best_match = None
        best_distance = float('inf')
        
        for candidate in candidates:
            dx = gen_word['cx'] - candidate['cx']
            dy = gen_word['cy'] - candidate['cy']
            distance = (dx**2 + dy**2)**0.5
            
            if distance < best_distance:
                best_distance = distance
                best_match = candidate
        
        matches.append((best_match, gen_word, best_distance))
    
    return matches

def calculate_average_distance(matches: List[Tuple]) -> float:
    """Calculate average centroid distance across all matched words."""
    if not matches:
        return 0.0
    
    total_distance = sum(m[2] for m in matches)
    return total_distance / len(matches)

def print_statistics(matches: List[Tuple]):
    """Print detailed statistics about the matching."""
    avg_dist = calculate_average_distance(matches)
    
    print(f"\n{'='*60}")
    print(f"MÉTRICA DE SIMILITUD")
    print(f"{'='*60}")
    print(f"Total palabras matcheadas: {len(matches)}")
    print(f"Distancia promedio: {avg_dist:.4f} px")
    print(f"{'='*60}\n")
    
    # Show worst offenders
    worst = sorted(matches, key=lambda x: x[2], reverse=True)[:10]
    
    print("🔴 Top 10 palabras con MAYOR desviación:\n")
    for i, (obj_w, gen_w, dist) in enumerate(worst, 1):
        print(f"{i:2d}. '{obj_w['text']}' - {dist:.2f}px")
        print(f"    Objetivo: ({obj_w['cx']:.1f}, {obj_w['cy']:.1f})")
        print(f"    Generado: ({gen_w['cx']:.1f}, {gen_w['cy']:.1f})")
        print()
    
    # Show distribution
    ranges = [
        (0, 1, "Perfecto"),
        (1, 5, "Excelente"),
        (5, 10, "Bueno"),
        (10, 50, "Mejorable"),
        (50, float('inf'), "Crítico")
    ]
    
    print("📊 DISTRIBUCIÓN DE DISTANCIAS:\n")
    for min_d, max_d, label in ranges:
        count = sum(1 for m in matches if min_d <= m[2] < max_d)
        pct = (count / len(matches)) * 100
        bar = "█" * int(pct / 2)
        print(f"{label:12} ({min_d:3.0f}-{max_d:3.0f}px): {count:4d} ({pct:5.1f}%) {bar}")
    
    return avg_dist

def apply_top_corrections(matches: List[Tuple], threshold: float, max_corrections: int = 20):
    """Apply corrections for the worst offenders above threshold."""
    
    # Load current coordinates
    with open(COORDS_JSON, 'r') as f:
        coords = json.load(f)
    
    # Get worst offenders above threshold
    to_fix = [m for m in matches if m[2] > threshold]
    to_fix.sort(key=lambda x: x[2], reverse=True)
    to_fix = to_fix[:max_corrections]
    
    if not to_fix:
        print(f"\n✅ No hay palabras con distancia >{threshold}px")
        return 0
    
    print(f"\n{'='*60}")
    print(f"APLICANDO CORRECCIONES (umbral: >{threshold}px)")
    print(f"{'='*60}\n")
    
    corrections_applied = 0
    
    for obj_word, gen_word, distance in to_fix:
        text = obj_word['text']
        
        # Find this word in coordinates.json
        for item in coords:
            if text in item.get('text', ''):
                # Check if this is approximately the right occurrence
                # (within 100px of current generated position)
                current_x = item.get('x', 0)
                current_y = item.get('y', 0)
                
                if abs(current_x - gen_word['x0']) < 100 and abs(current_y - gen_word['y0']) < 100:
                    # Apply correction
                    new_x = obj_word['x0']
                    new_y = obj_word['y0']
                    
                    print(f"✏️  Corrigiendo '{text}':")
                    print(f"   Distancia: {distance:.2f}px")
                    print(f"   Antes: ({current_x:.1f}, {current_y:.1f})")
                    print(f"   Después: ({new_x:.1f}, {new_y:.1f})")
                    
                    item['x'] = new_x
                    item['y'] = new_y
                    
                    corrections_applied += 1
                    break
    
    # Save
    if corrections_applied > 0:
        with open(COORDS_JSON, 'w') as f:
            json.dump(coords, f, indent=2)
        
        print(f"\n✅ Aplicadas {corrections_applied} correcciones a coordinates.json")
    
    return corrections_applied

def regenerate_cv():
    """Regenerate the CV using main.py."""
    print(f"\n🔄 Regenerando CV...")
    result = subprocess.run(['python3', 'main.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ CV regenerado\n")
        return True
    else:
        print(f"❌ Error regenerando CV")
        print(result.stderr)
        return False

def main():
    print("\n" + "="*60)
    print("OPTIMIZADOR INTELIGENTE PALABRA-POR-PALABRA")
    print("="*60)
    
    # Step 1: Extract from both PDFs
    print(f"\n📖 Extrayendo OCR del objetivo...")
    obj_words = extract_ocr(OBJECTIVE_PDF)
    print(f"   ✅ {len(obj_words)} palabras")
    
    print(f"\n📖 Extrayendo OCR del generado...")
    gen_words = extract_ocr(GENERATED_PDF)
    print(f"   ✅ {len(gen_words)} palabras")
    
    # Step 2: Match intelligently
    print(f"\n🧠 Matcheando palabras (búsqueda inteligente)...")
    matches = match_words_intelligently(obj_words, gen_words)
    
    # Step 3: Calculate and show statistics
    avg_distance = print_statistics(matches)
    
    # Step 4: Decide on action
    print(f"\n{'='*60}")
    print(f"SIGUIENTE ACCIÓN:")
    print(f"{'='*60}")
    
    if avg_distance < 1.0:
        print(f"✅ Distancia promedio < 1px - Alineación PERFECTA")
        print(f"   No se requieren correcciones")
    elif avg_distance < 5.0:
        print(f"✅ Distancia promedio < 5px - Alineación EXCELENTE")
        print(f"   Pequeños ajustes disponibles")
    else:
        print(f"⚠️  Distancia promedio = {avg_distance:.2f}px")
        print(f"   Se recomienda optimización iterativa")
    
    print(f"{'='*60}\n")
    
    return matches, avg_distance

if __name__ == "__main__":
    matches, avg_dist = main()
