#!/usr/bin/env python3
"""
Rectangle Alignment Verifier

Compares blue rectangles between generated CV and objective PDF.
Provides detailed alignment metrics and visual feedback.
"""

import json
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict, Tuple
import sys

# Configuration
GENERATED_PDF = Path("outputs/Nicolas_Fredes_CV.pdf")
OBJECTIVE_PDF = Path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf")
BLUE_COLORS = [(0.169, 0.451, 0.701), (0.059, 0.318, 0.793)]
COLOR_TOLERANCE = 0.02
MIN_WIDTH = 30
MIN_HEIGHT = 8


def extract_rectangles(pdf_path: Path) -> List[Dict]:
    """Extract blue rectangles from a PDF."""
    doc = fitz.open(pdf_path)
    page = doc[0]
    drawings = page.get_drawings()
    
    rectangles = []
    for drawing in drawings:
        if drawing.get('type') != 'f':
            continue
        fill_color = drawing.get('fill')
        if not fill_color:
            continue
        r, g, b = fill_color[:3]
        
        is_blue = any(
            all(abs(c - target) < COLOR_TOLERANCE 
                for c, target in zip([r, g, b], blue_target))
            for blue_target in BLUE_COLORS
        )
        
        if not is_blue:
            continue
        
        rect = drawing['rect']
        width = rect.width
        height = rect.height
        
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            continue
        
        rectangles.append({
            'x': round(float(rect.x0), 4),
            'y': round(float(rect.y0), 4),
            'width': round(width, 4),
            'height': round(height, 4),
            'centroid_x': round(rect.x0 + width / 2, 4),
            'centroid_y': round(rect.y0 + height / 2, 4)
        })
    
    rectangles.sort(key=lambda r: r['y'])
    doc.close()
    return rectangles


def calculate_alignment_score(generated: List[Dict], objective: List[Dict]) -> Tuple[float, List[Dict]]:
    """Calculate alignment score and per-rectangle errors."""
    if len(generated) != len(objective):
        print(f"⚠️  Rectangle count mismatch: Generated={len(generated)}, Objective={len(objective)}")
        return 0.0, []
    
    errors = []
    total_error = 0.0
    
    for i, (gen, obj) in enumerate(zip(generated, objective)):
        dx = abs(gen['x'] - obj['x'])
        dy = abs(gen['y'] - obj['y'])
        dw = abs(gen['width'] - obj['width'])
        dh = abs(gen['height'] - obj['height'])
        
        # Position error (Euclidean distance)
        pos_error = (dx**2 + dy**2)**0.5
        
        # Size error
        size_error = (dw**2 + dh**2)**0.5
        
        # Total error for this rectangle
        rect_error = pos_error + size_error
        total_error += rect_error
        
        errors.append({
            'index': i,
            'position_error': round(pos_error, 4),
            'size_error': round(size_error, 4),
            'total_error': round(rect_error, 4),
            'dx': round(dx, 4),
            'dy': round(dy, 4),
            'dw': round(dw, 4),
            'dh': round(dh, 4)
        })
    
    # Calculate score (0-100%)
    # Perfect alignment = 0 error, score = 100%
    # Each point of error reduces score
    max_acceptable_error = 10.0  # 10 points total error = 0% score
    score = max(0.0, 100.0 - (total_error / len(generated) / max_acceptable_error * 100.0))
    
    return score, errors


def main():
    """Main verification routine."""
    print("=" * 60)
    print("🔍 Blue Rectangle Alignment Verifier")
    print("=" * 60)
    
    if not GENERATED_PDF.exists():
        print(f"❌ Generated PDF not found: {GENERATED_PDF}")
        return False
    
    if not OBJECTIVE_PDF.exists():
        print(f"❌ Objective PDF not found: {OBJECTIVE_PDF}")
        return False
    
    print(f"\n📄 Generated: {GENERATED_PDF.name}")
    print(f"🎯 Objective: {OBJECTIVE_PDF.name}\n")
    
    # Extract rectangles
    print("Extracting rectangles...")
    generated_rects = extract_rectangles(GENERATED_PDF)
    objective_rects = extract_rectangles(OBJECTIVE_PDF)
    
    print(f"  Generated: {len(generated_rects)} rectangles")
    print(f"  Objective: {len(objective_rects)} rectangles\n")
    
    if len(generated_rects) == 0:
        print("❌ No rectangles found in generated PDF!")
        return False
    
    # Calculate alignment
    score, errors = calculate_alignment_score(generated_rects, objective_rects)
    
    print("=" * 60)
    print(f"📊 ALIGNMENT SCORE: {score:.2f}%")
    print("=" * 60)
    
    # Detailed error breakdown
    print("\n📋 Per-Rectangle Analysis:\n")
    for err in errors:
        print(f"  Rectangle #{err['index'] + 1}:")
        print(f"    Position Error: {err['position_error']:6.2f} pts  (ΔX={err['dx']:5.2f}, ΔY={err['dy']:5.2f})")
        print(f"    Size Error:     {err['size_error']:6.2f} pts  (ΔW={err['dw']:5.2f}, ΔH={err['dh']:5.2f})")
        print(f"    Total Error:    {err['total_error']:6.2f} pts")
        
        # Visual indicator
        if err['total_error'] < 0.5:
            print(f"    Status: ✅ PERFECT")
        elif err['total_error'] < 2.0:
            print(f"    Status: ✓  Good")
        elif err['total_error'] < 5.0:
            print(f"    Status: ⚠️  Needs adjustment")
        else:
            print(f"    Status: ❌ Poor alignment")
        print()
    
    # Overall verdict
    print("=" * 60)
    if score >= 99.9:
        print("🎉 PERFECT ALIGNMENT ACHIEVED!")
        print("=" * 60)
        return True
    elif score >= 95.0:
        print("✅ Excellent alignment (minor adjustments possible)")
    elif score >= 90.0:
        print("✓  Good alignment (some refinement needed)")
    elif score >= 80.0:
        print("⚠️  Fair alignment (significant adjustments required)")
    else:
        print("❌ Poor alignment (major corrections needed)")
    print("=" * 60)
    
    return score >= 99.9


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
