#!/usr/bin/env python3
"""
Automatic Rectangle Position Iterator
Adjusts Y positions and shows visual feedback in browser
"""

import json
import subprocess
import time
import webbrowser
import os
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def load_shapes():
    with open('data/shapes.json', 'r') as f:
        return json.load(f)

def save_shapes(shapes):
    with open('data/shapes.json', 'w') as f:
        json.dump(shapes, f, indent=2)

def generate_pdf():
    result = subprocess.run(['python3', 'main.py'], capture_output=True, text=True)
    return result.returncode == 0

def create_comparison(iteration, adjustment):
    obj = convert_from_path("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf", dpi=200)[0]
    gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=200)[0]
    gen = gen.resize(obj.size)
    
    comp = Image.new('RGB', (obj.width*2+80, obj.height+200), 'white')
    comp.paste(obj, (30, 120))
    comp.paste(gen, (obj.width+50, 120))
    
    draw = ImageDraw.Draw(comp)
    try:
        font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 56)
        font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 32)
    except:
        font_big = font_med = ImageFont.load_default()
    
    # Header
    ts = time.strftime("%H:%M:%S")
    title = f"ITER {iteration}: Y{adjustment:+d} @ {ts}"
    draw.text((comp.width//2-350, 25), title, fill='#00ffff', font=font_big)
    
    # Similarity
    obj_arr = np.array(obj.convert('RGB'))
    gen_arr = np.array(gen.convert('RGB'))
    diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
    sim = 100 * (1 - np.sum(np.any(diff > 10, axis=2)) / (obj_arr.shape[0] * obj_arr.shape[1]))
    
    draw.text((comp.width//2-120, obj.height+140), f"{sim:.2f}%", fill='#00ff00', font=font_med)
    
    comp.save("outputs/COMPARACION_ACTUAL.png")
    
    html = f"""<!DOCTYPE html><html><head><title>Iter {iteration}</title></head>
<body style="background:#000;padding:20px;margin:0;">
<h1 style="color:#0ff;font-size:5em;text-align:center;">ITERATION {iteration}: Y{adjustment:+d}</h1>
<h2 style="color:#0f0;font-size:2em;text-align:center;">Similitud: {sim:.2f}%</h2>
<img src="COMPARACION_ACTUAL.png?t={time.time()}" style="width:100%;border:6px solid #0ff;">
</body></html>"""
    
    with open("outputs/COMPARACION_ACTUAL.html", 'w') as f:
        f.write(html)
    
    return sim

def main():
    print("="*60)
    print("ITERADOR AUTOMÁTICO DE RECTÁNGULOS")
    print("="*60)
    
    # Start with baseline
    shapes = load_shapes()
    base_y = shapes[0]['y']
    
    # Try different offsets
    offsets = [0, +50, +100, +150, +200, +250]
    
    for i, offset in enumerate(offsets):
        print(f"\n--- Iteration {i+1}: Y+{offset} ---")
        
        # Adjust ALL rectangles
        for shape in shapes:
            shape['y'] = base_y + offset
        
        save_shapes(shapes)
        
        # Generate and compare
        if not generate_pdf():
            print("❌ PDF generation failed")
            continue
        
        sim = create_comparison(i+1, offset)
        print(f"✅ Similitud: {sim:.2f}%")
        
        # Open in browser (first iteration only)
        if i == 0:
            webbrowser.open('file://' + os.path.abspath("outputs/COMPARACION_ACTUAL.html"))
        
        time.sleep(1)  # Give browser time to update
    
    print("\n" + "="*60)
    print(f"✅ Completadas {len(offsets)} iteraciones")
    print("Revisa el browser para ver todas las versiones")
    print("="*60)

if __name__ == "__main__":
    main()
