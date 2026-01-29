#!/usr/bin/env python3
"""
Interactive Histogram-Based CV Optimizer

Shows a visual histogram of word position discrepancies between
objective and generated CVs, applies corrections incrementally,
and regenerates for visual inspection after each iteration.

Usage:
    python3 scripts/histogram_optimizer.py
"""

import json
import fitz
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict

# Configuration
OBJECTIVE_PDF = Path("outputs/Nicolas_Fredes_CV.pdf")  # Current perfect CV as baseline
GENERATED_PDF = Path("outputs/Nicolas_Fredes_CV.pdf")
COORDS_JSON = Path("data/coordinates.json")

class CVOptimizer:
    def __init__(self):
        self.iteration = 0
        self.objective_words = []
        self.generated_words = []
        self.matches = []
        
    def extract_words(self, pdf_path: Path) -> List[Dict]:
        """Extract all words with positions from PDF."""
        doc = fitz.open(pdf_path)
        page = doc[0]
        words_raw = page.get_text("words")
        doc.close()
        
        words = []
        for w in words_raw:
            x0, y0, x1, y1, text, block_no, line_no, word_no = w
            cx = x0 + (x1 - x0) / 2
            cy = y0 + (y1 - y0) / 2
            
            words.append({
                'text': text,
                'cx': round(float(cx), 2),
                'cy': round(float(cy), 2),
                'x0': round(float(x0), 2),
                'y0': round(float(y0), 2),
                'block': block_no,
                'line': line_no
            })
        
        return words
    
    def match_words(self, obj_words: List[Dict], gen_words: List[Dict]) -> List[Tuple]:
        """Match each generated word to closest objective counterpart."""
        matches = []
        
        for gen_word in gen_words:
            text = gen_word['text']
            candidates = [w for w in obj_words if w['text'] == text]
            
            if not candidates:
                continue
            
            # Find closest by Euclidean distance
            best_match = min(candidates, key=lambda c: 
                ((c['cx'] - gen_word['cx'])**2 + (c['cy'] - gen_word['cy'])**2)**0.5
            )
            
            dx = gen_word['cx'] - best_match['cx']
            dy = gen_word['cy'] - best_match['cy']
            distance = (dx**2 + dy**2)**0.5
            
            matches.append({
                'text': text,
                'obj': best_match,
                'gen': gen_word,
                'distance': round(distance, 2),
                'dx': round(dx, 2),
                'dy': round(dy, 2)
            })
        
        return matches
    
    def show_histogram(self, matches: List[Dict]):
        """Display visual histogram of word distances."""
        if not matches:
            print("⚠️  No hay coincidencias para mostrar")
            return
        
        # Sort by distance (descending)
        sorted_matches = sorted(matches, key=lambda m: m['distance'], reverse=True)
        
        # Calculate average
        avg_dist = sum(m['distance'] for m in matches) / len(matches)
        max_dist = max(m['distance'] for m in matches)
        
        print(f"\n{'='*70}")
        print(f"ITERACIÓN #{self.iteration} - HISTOGRAMA DE DISTANCIAS")
        print(f"{'='*70}")
        print(f"📊 Total palabras: {len(matches)}")
        print(f"📏 Distancia promedio: {avg_dist:.4f} px")
        print(f"🔴 Distancia máxima: {max_dist:.2f} px")
        print(f"{'='*70}\n")
        
        # Show top 20 worst offenders
        print("🔴 Top 20 Palabras con MAYOR distancia:\n")
        for i, m in enumerate(sorted_matches[:20], 1):
            # Visual bar
            bar_len = int((m['distance'] / max(max_dist, 1)) * 40)
            bar = "█" * bar_len
            
            print(f"{i:2d}. {m['distance']:6.2f}px {bar} '{m['text']}'")
            if i <= 5:  # Show details for top 5
                print(f"    Δx:{m['dx']:6.2f}px  Δy:{m['dy']:6.2f}px")
                print(f"    Obj:({m['obj']['cx']:6.1f}, {m['obj']['cy']:6.1f})  Gen:({m['gen']['cx']:6.1f}, {m['gen']['cy']:6.1f})")
        
        # Distribution
        print(f"\n📊 DISTRIBUCIÓN:")
        bins = [
            (0, 0.5, "Perfecto"),
            (0.5, 1, "Excelente"),  
            (1, 2, "Muy bueno"),
            (2, 5, "Bueno"),
            (5, 10, "Mejorable"),
            (10, 50, "Crítico"),
            (50, 1000, "Grave")
        ]
        
        for min_d, max_d, label in bins:
            count = sum(1 for m in matches if min_d <= m['distance'] < max_d)
            if count > 0:
                pct = (count / len(matches)) * 100
                bar = "█" * int(pct / 2)
                print(f"{label:12} ({min_d:4.1f}-{max_d:4.1f}px): {count:4d} ({pct:5.1f}%) {bar}")
        
        print(f"{'='*70}\n")
        
        return avg_dist, sorted_matches
    
    def apply_corrections(self, sorted_matches: List[Dict], num_corrections: int = 5):
        """Apply corrections for top N worst offenders."""
        
        # Load coordinates
        with open(COORDS_JSON, 'r') as f:
            coords = json.load(f)
        
        corrections_applied = 0
        
        print(f"🔧 APLICANDO {num_corrections} CORRECCIONES:\n")
        
        for i, match in enumerate(sorted_matches[:num_corrections], 1):
            text = match['text']
            obj_word = match['obj']
            gen_word = match['gen']
            
            # Find in coordinates.json (match by proximity)
            for item in coords:
                if text not in item.get('text', ''):
                    continue
                
                current_x = item.get('x', 0)
                current_y = item.get('y', 0)
                
                # Check if this is the right occurrence
                if abs(current_x - gen_word['x0']) < 50 and abs(current_y - gen_word['y0']) < 50:
                    # Apply correction
                    new_x = obj_word['x0']
                    new_y = obj_word['y0']
                    
                    print(f"{i}. '{text}' ({match['distance']:.2f}px)")
                    print(f"   ({current_x:.1f}, {current_y:.1f}) → ({new_x:.1f}, {new_y:.1f})")
                    
                    item['x'] = new_x
                    item['y'] = new_y
                    
                    corrections_applied += 1
                    break
        
        if corrections_applied > 0:
            with open(COORDS_JSON, 'w') as f:
                json.dump(coords, f, indent=2)
            print(f"\n✅ {corrections_applied} correcciones guardadas en coordinates.json")
        
        return corrections_applied
    
    def regenerate(self):
        """Regenerate CV."""
        print(f"\n🔄 Regenerando CV...\n")
        result = subprocess.run(['python3', 'main.py'], capture_output=True, text=True, cwd='.')
        return result.returncode == 0
    
    def run_iteration(self, num_corrections: int = 5):
        """Run one optimization iteration."""
        self.iteration += 1
        
        print(f"\n{'#'*70}")
        print(f"# ITERACIÓN {self.iteration}")
        print(f"{'#'*70}\n")
        
        # Extract
        print("📖 Extrayendo palabras...")
        self.objective_words = self.extract_words(OBJECTIVE_PDF)
        self.generated_words = self.extract_words(GENERATED_PDF)
        print(f"   Objetivo: {len(self.objective_words)} palabras")
        print(f"   Generado: {len(self.generated_words)} palabras")
        
        # Match
        print(f"\n🧠 Matcheando...")
        self.matches = self.match_words(self.objective_words, self.generated_words)
        
        # Show histogram
        avg_dist, sorted_matches = self.show_histogram(self.matches)
        
        # Check if done
        if avg_dist < 0.1:
            print(f"✅ PERFECCIÓN ALCANZADA (distancia < 0.1px)")
            return False  # Stop iterating
        
        # Apply corrections
        if num_corrections > 0:
            self.apply_corrections(sorted_matches, num_corrections)
            
            # Regenerate
            if self.regenerate():
                print(f"✅ CV regenerado exitosamente")
                return True  # Continue
            else:
                print(f"❌ Error al regenerar")
                return False
        
        return False

def main():
    optimizer = CVOptimizer()
    
    print(f"\n{'='*70}")
    print(f"OPTIMIZADOR INTERACTIVO CON HISTOGRAMA")
    print(f"{'='*70}")
    
    # First iteration - baseline
    optimizer.run_iteration(num_corrections=0)
    
    print(f"\n{'='*70}")
    print(f"Opciones:")
    print(f"  1. Aplicar 5 correcciones y regenerar")
    print(f"  2. Aplicar 10 correcciones y regenerar")
    print(f"  3. Aplicar 20 correcciones y regenerar")
    print(f"  4. Solo mostrar histograma actual")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
