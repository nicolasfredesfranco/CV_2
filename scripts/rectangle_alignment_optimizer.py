#!/usr/bin/env python3
"""
Blue Rectangle Alignment Optimizer

Iteratively optimizes rectangle positions to match the objective PDF.
Uses coordinate transformation, reflection, and convergence detection.
"""

import json
import fitz
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
import sys
from datetime import datetime

# Configuration
GENERATED_PDF = Path("outputs/Nicolas_Fredes_CV.pdf")
OBJECTIVE_PDF = Path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf")
SHAPES_JSON = Path("data/shapes.json")
OBJECTIVE_RECTS_JSON = Path("data/blue_rectangles_objective.json")
LOG_FILE = Path("data/optimizer_log.txt")

PAGE_HEIGHT = 806.0  # From config.py
BLUE_COLORS = [(0.169, 0.451, 0.701), (0.059, 0.318, 0.793)]
COLOR_TOLERANCE = 0.02
MIN_WIDTH = 30
MIN_HEIGHT = 8

MAX_ITERATIONS = 100
TARGET_SCORE = 99.9
CONVERGENCE_THRESHOLD = 0.01  # Stop if improvement < 0.01%


def log_message(msg: str):
    """Log message to both console and file."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_line = f"[{timestamp}] {msg}"
    print(log_line)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + "\n")


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
            'height': round(height, 4)
        })
    
    rectangles.sort(key=lambda r: r['y'])
    doc.close()
    return rectangles


def calculate_score(generated: List[Dict], objective: List[Dict]) -> Tuple[float, List[Dict]]:
    """Calculate alignment score and errors."""
    if len(generated) != len(objective):
        return 0.0, []
    
    errors = []
    total_error = 0.0
    
    for i, (gen, obj) in enumerate(zip(generated, objective)):
        dx = abs(gen['x'] - obj['x'])
        dy = abs(gen['y'] - obj['y'])
        dw = abs(gen['width'] - obj['width'])
        dh = abs(gen['height'] - obj['height'])
        
        pos_error = (dx**2 + dy**2)**0.5
        size_error = (dw**2 + dh**2)**0.5
        rect_error = pos_error + size_error
        total_error += rect_error
        
        errors.append({
            'index': i,
            'dx': dx, 'dy': dy, 'dw': dw, 'dh': dh,
            'total_error': rect_error
        })
    
    max_acceptable_error = 10.0
    score = max(0.0, 100.0 - (total_error / len(generated) / max_acceptable_error * 100.0))
    return score, errors


def transform_y_pdf_to_reportlab(y_pdf: float, height: float) -> float:
    """Transform Y coordinate from PDF (top-left) to ReportLab (bottom-left)."""
    # PDF: Y increases downward from top
    # ReportLab: Y increases upward from bottom
    # y_reportlab = PAGE_HEIGHT - y_pdf - height
    return PAGE_HEIGHT - y_pdf - height


def generate_cv() -> bool:
    """Generate CV by running main.py."""
    try:
        result = subprocess.run(
            ["python3", "main.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        log_message(f"❌ CV generation failed: {e}")
        return False


def optimize_rectangles():
    """Main optimization loop."""
    log_message("=" * 70)
    log_message("🚀 Blue Rectangle Alignment Optimizer v1.0")
    log_message("=" * 70)
    
    # Load objective rectangles
    with open(OBJECTIVE_RECTS_JSON, 'r') as f:
        obj_data = json.load(f)
    objective_rects = obj_data['rectangles']
    
    log_message(f"\n🎯 Target: {len(objective_rects)} blue rectangles from objective PDF")
    log_message(f"📊 Goal: ≥{TARGET_SCORE}% alignment score")
    log_message(f"🔄 Max iterations: {MAX_ITERATIONS}\n")
    
    # Initialize shapes.json with transformed coordinates
    log_message("🔧 Initializing shapes.json with coordinate transformation...")
    shapes = []
    for rect in objective_rects:
        # Transform Y coordinate from PDF to ReportLab
        y_reportlab = transform_y_pdf_to_reportlab(rect['y'], rect['height'])
        
        shape = {
            "type": "rect",
            "x": rect['x'],
            "y": y_reportlab,
            "width": rect['width'],
            "height": rect['height'],
            "fill_color": [
                rect['fill_color']['r'],
                rect['fill_color']['g'],
                rect['fill_color']['b']
            ]
        }
        shapes.append(shape)
    
    with open(SHAPES_JSON, 'w') as f:
        json.dump(shapes, f, indent=2)
    
    log_message(f"   ✅ Wrote {len(shapes)} shapes with Y-axis transformation")
    
    # Iteration loop
    prev_score = 0.0
    best_score = 0.0
    
    for iteration in range(MAX_ITERATIONS):
        log_message(f"\n{'='*70}")
        log_message(f"🔄 ITERATION {iteration + 1}/{MAX_ITERATIONS}")
        log_message(f"{'='*70}")
        
        # Generate CV
        log_message("   Generating CV...")
        if not generate_cv():
            log_message("   ❌ Generation failed, stopping")
            return False
        
        # Extract rectangles
        log_message("   Extracting rectangles...")
        generated_rects = extract_rectangles(GENERATED_PDF)
        
        if len(generated_rects) != len(objective_rects):
            log_message(f"   ❌ Count mismatch: {len(generated_rects)} vs {len(objective_rects)}")
            return False
        
        # Calculate score
        score, errors = calculate_score(generated_rects, objective_rects)
        improvement = score - prev_score
        
        log_message(f"\n   📊 Score: {score:.3f}%  (Δ {improvement:+.3f}%)")
        
        if score > best_score:
            best_score = score
            log_message(f"   🎉 New best score: {best_score:.3f}%")
        
        # Check convergence
        if score >= TARGET_SCORE:
            log_message(f"\n{'='*70}")
            log_message(f"✅ TARGET ACHIEVED! Score: {score:.3f}% ≥ {TARGET_SCORE}%")
            log_message(f"{'='*70}")
            return True
        
        if iteration > 0 and abs(improvement) < CONVERGENCE_THRESHOLD:
            log_message(f"\n   ⚠️  Convergence detected (improvement < {CONVERGENCE_THRESHOLD}%)")
            log_message(f"   Best score achieved: {best_score:.3f}%")
            break
        
        # Analyze errors and apply corrections
        log_message("\n   🔍 Error analysis:")
        total_adjustments = 0
        
        for i, (err, gen, obj, shape) in enumerate(zip(errors, generated_rects, objective_rects, shapes)):
            if err['total_error'] > 0.5:
                log_message(f"      Rect #{i+1}: Error={err['total_error']:.2f}pts "
                          f"(ΔX={err['dx']:.2f}, ΔY={err['dy']:.2f})")
                
                # Apply corrections with damping to prevent oscillation
                damping = 0.8
                if err['dx'] > 0.1:
                    correction_x = (obj['x'] - gen['x']) * damping
                    shape['x'] += correction_x
                    total_adjustments += 1
                
                if err['dy'] > 0.1:
                    correction_y = (obj['y'] - gen['y']) * damping
                    shape['y'] += correction_y
                    total_adjustments += 1
        
        if total_adjustments > 0:
            log_message(f"   🔧 Applied {total_adjustments} corrections to shapes.json")
            with open(SHAPES_JSON, 'w') as f:
                json.dump(shapes, f, indent=2)
        else:
            log_message(f"   ✓  No corrections needed")
        
        prev_score = score
    
    # Final summary
    log_message(f"\n{'='*70}")
    log_message(f"🏁 OPTIMIZATION COMPLETE")
    log_message(f"{'='*70}")
    log_message(f"   Iterations: {iteration + 1}")
    log_message(f"   Best score: {best_score:.3f}%")
    log_message(f"   Target: {TARGET_SCORE}%")
    
    if best_score >= TARGET_SCORE:
        log_message(f"\n   ✅ SUCCESS! Target achieved.")
        return True
    else:
        log_message(f"\n   ⚠️  Target not reached. Manual adjustment may be needed.")
        return False


if __name__ == "__main__":
    # Clear log file
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'w') as f:
        f.write(f"Optimization Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    success = optimize_rectangles()
    
    log_message(f"\n📝 Full log saved to: {LOG_FILE}")
    
    sys.exit(0 if success else 1)
