#!/usr/bin/env python3
"""
Automatic fixer for rectangle positions and job title colors
Iterates through Y offsets and shows results in browser
"""

import json
import subprocess
import time
import webbrowser
import os
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def fix_job_colors():
    """Fix all job title colors to pure black"""
    with open('data/coordinates.json', 'r') as f:
        coords = json.load(f)
    
    job_keywords = ['Lead', 'Senior', 'Engineer', 'Scientist', 'Specialist', 'Intelligence', 'Machine', 'Learning', 'Data', 'Computer', 'Vision']
    
    fixed = 0
    for coord in coords:
        text = coord['text']
        # If contains job keywords, set to pure black
        if any(kw in text for kw in job_keywords):
            if 'Engineer' in text or 'Scientist' in text or 'Specialist' in text:
                coord['color'] = 0x000000
                fixed += 1
    
    with open('data/coordinates.json', 'w') as f:
        json.dump(coords, f, indent=2)
    
    return fixed

def load_base_shapes():
    """Load baseline shapes from objective"""
    import pdfplumber
    
    with pdfplumber.open("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf") as pdf:
        page = pdf.pages[0]
        rects = [r for r in page.rects if 100 < r['width'] < 400 and 10 < r['height'] < 30][:5]
        
        shapes = []
        for r in rects:
            shapes.append({
                'type': 'rect',
                'x': float(r['x0']),
                'y': float(r['top']),
                'width': float(r['width']),
                'height': float(r['height']),
                'fill_color': [0.168627, 0.45098, 0.701961],
                'stroke': False,
                'opacity': 1.0
            })
        
        return shapes

def apply_y_offset(shapes, offset):
    """Apply Y offset to all shapes"""
    modified = []
    for s in shapes:
        s_copy = s.copy()
        s_copy['y'] = s['y'] + offset
        modified.append(s_copy)
    return modified

def generate_and_compare(iteration, offset):
    """Generate PDF and create comparison"""
    # Generate PDF
    result = subprocess.run(['python3', 'main.py'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Generation failed: {result.stderr[:200]}")
        return None
    
    # Create comparison
    obj = convert_from_path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf", dpi=200)[0]
    gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=200)[0]
    gen = gen.resize(obj.size)
    
    comp = Image.new('RGB', (obj.width*2+80, obj.height+200), 'white')
    comp.paste(obj, (30, 120))
    comp.paste(gen, (obj.width+50, 120))
    
    draw = ImageDraw.Draw(comp)
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 48)
    except:
        font = ImageFont.load_default()
    
    ts = time.strftime("%H:%M:%S")
    title = f"ITER {iteration}: Y{offset:+d} @ {ts}"
    draw.text((comp.width//2-350, 30), title, fill='#ffff00', font=font)
    
    # Calculate similarity
    obj_arr = np.array(obj.convert('RGB'))
    gen_arr = np.array(gen.convert('RGB'))
    diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
    sim = 100 * (1 - np.sum(np.any(diff > 10, axis=2)) / (obj_arr.shape[0] * obj_arr.shape[1]))
    
    draw.text((comp.width//2-120, obj.height+140), f"{sim:.2f}%", fill='#00ff00', font=font)
    
    comp.save("outputs/COMPARACION_ACTUAL.png")
    
    html = f"""<!DOCTYPE html><html><head><title>Iter {iteration}</title></head>
<body style="background:#000;padding:20px;">
<h1 style="color:#ff0;text-align:center;font-size:5em;">ITER {iteration}: Y{offset:+d}</h1>
<h2 style="color:#0f0;text-align:center;font-size:2.5em;">{sim:.2f}%</h2>
<img src="COMPARACION_ACTUAL.png?t={time.time()}" style="width:100%;border:6px solid #ff0;">
</body></html>"""
    
    with open("outputs/COMPARACION_ACTUAL.html", 'w') as f:
        f.write(html)
    
    return sim

def main():
    print("="*70)
    print("AUTOMATIC RECTANGLE POSITION & COLOR FIXER")
    print("="*70)
    
    # Fix job colors first
    print("\n1. Fixing job title colors to pure black...")
    fixed = fix_job_colors()
    print(f"   ✅ Fixed {fixed} job titles")
    
    # Load baseline shapes
    print("\n2. Loading baseline shapes from objective...")
    base_shapes = load_base_shapes()
    print(f"   ✅ Loaded {len(base_shapes)} rectangles")
    
    # Try different Y offsets
    offsets = [0, -50, -100, -150, -200, 50, 100, 150]
    best_sim = 0
    best_offset = 0
    
    print("\n3. Iterating through Y offsets...")
    
    for i, offset in enumerate(offsets):
        print(f"\n   Iteration {i+1}/{len(offsets)}: Y{offset:+d}")
        
        # Apply offset
        shapes = apply_y_offset(base_shapes, offset)
        
        with open('data/shapes.json', 'w') as f:
            json.dump(shapes, f, indent=2)
        
        # Generate and compare
        sim = generate_and_compare(i+1, offset)
        
        if sim is None:
            continue
        
        print(f"   Similitud: {sim:.2f}%")
        
        if sim > best_sim:
            best_sim = sim
            best_offset = offset
        
        # Open browser on first iteration
        if i == 0:
            webbrowser.open('file://' + os.path.abspath("outputs/COMPARACION_ACTUAL.html"))
        
        time.sleep(0.5)
    
    print("\n" + "="*70)
    print(f"✅ MEJOR RESULTADO: Y{best_offset:+d} con {best_sim:.2f}% similitud")
    print("="*70)
    
    # Apply best offset
    shapes = apply_y_offset(base_shapes, best_offset)
    with open('data/shapes.json', 'w') as f:
        json.dump(shapes, f, indent=2)
    
    # Final generation
    print("\nGenerando versión final...")
    generate_and_compare(99, best_offset)
    
    print("\n✅ COMPLETADO - Revisa el browser")

if __name__ == "__main__":
    main()
