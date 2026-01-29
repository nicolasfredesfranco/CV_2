#!/usr/bin/env python3
"""
Detailed Visual Difference Analyzer
Identifies 100+ specific visual differences between objective and generated PDFs.

Author: Nicolás Ignacio Fredes Franco
"""

import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import json
from pathlib import Path

def analyze_differences():
    """Analyze and list 100+ specific visual differences"""
    
    print("="*100)
    print("DETAILED VISUAL DIFFERENCE ANALYSIS - Finding 100+ Differences")
    print("="*100)
    
    # Load PDFs at high resolution for precision
    print("\nLoading PDFs at 200 DPI for precision analysis...")
    obj = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=200)[0]
    gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=200)[0]
    
    obj_arr = np.array(obj.convert('RGB'))
    gen_arr = np.array(gen.convert('RGB').resize(obj.size))
    
    h, w = obj_arr.shape[0], obj_arr.shape[1]
    
    print(f"Image dimensions: {w}x{h} pixels")
    
    # Calculate difference map
    diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
    diff_binary = np.any(diff > 10, axis=2)
    
    # Find all different pixel regions
    differences = []
    
    # Scan in 20x20 pixel blocks
    block_size = 20
    diff_id = 1
    
    print("\nScanning for differences in 20x20 pixel blocks...")
    
    for y in range(0, h - block_size, block_size):
        for x in range(0, w - block_size, block_size):
            block_diff = diff_binary[y:y+block_size, x:x+block_size]
            diff_pixels = np.sum(block_diff)
            
            if diff_pixels > 10:  # At least 10 pixels different in this block
                # Calculate average color in each
                obj_block = obj_arr[y:y+block_size, x:x+block_size]
                gen_block = gen_arr[y:y+block_size, x:x+block_size]
                
                obj_avg = np.mean(obj_block, axis=(0,1))
                gen_avg = np.mean(gen_block, axis=(0,1))
                
                color_diff = np.sqrt(np.sum((obj_avg - gen_avg)**2))
                
                differences.append({
                    'id': diff_id,
                    'x': x,
                    'y': y,
                    'width': block_size,
                    'height': block_size,
                    'diff_pixels': int(diff_pixels),
                    'diff_percentage': float(diff_pixels / (block_size * block_size) * 100),
                    'color_diff': float(color_diff),
                    'obj_color': obj_avg.tolist(),
                    'gen_color': gen_avg.tolist()
                })
                diff_id += 1
    
    # Sort by severity (most different first)
    differences.sort(key=lambda x: x['diff_percentage'] * x['color_diff'], reverse=True)
    
    print(f"\n✅ Found {len(differences)} distinct visual difference regions!")
    print("\n" + "="*100)
    print("TOP 100 MOST SIGNIFICANT VISUAL DIFFERENCES")
    print("="*100)
    
    # List top 100
    for i, diff in enumerate(differences[:100], 1):
        y_pt = diff['y'] * 72 / 200  # Convert to PDF points
        x_pt = diff['x'] * 72 / 200
        
        print(f"\n{i}. DIFFERENCE at ({diff['x']}, {diff['y']}) px / ({x_pt:.1f}, {y_pt:.1f}) pt")
        print(f"   Size: {diff['width']}x{diff['height']} px")
        print(f"   Affected pixels: {diff['diff_pixels']}/{diff['width']*diff['height']} ({diff['diff_percentage']:.1f}%)")
        print(f"   Color difference: {diff['color_diff']:.1f}")
        print(f"   Objetivo RGB: {[int(c) for c in diff['obj_color']]}")
        print(f"   Generated RGB: {[int(c) for c in diff['gen_color']]}")
        
        # Infer what element this might be
        if y_pt < 100:
            region = "HEADER"
        elif y_pt < 200:
            region = "EDUCATION/SKILLS"
        elif y_pt < 600:
            region = "EXPERIENCE"
        else:
            region = "BOTTOM SECTIONS"
        
        print(f"   Likely region: {region}")
    
    # Save detailed report
    report_file = Path("outputs/difference_analysis_100plus.json")
    with open(report_file, 'w') as f:
        json.dump({
            'total_differences': len(differences),
            'top_100': differences[:100],
            'image_dimensions': {'width': w, 'height': h},
            'dpi': 200
        }, f, indent=2)
    
    print(f"\n{'='*100}")
    print(f"SUMMARY")
    print(f"{'='*100}")
    print(f"Total difference regions found: {len(differences)}")
    print(f"Detailed report saved: {report_file}")
    
    # Create visual difference map
    print("\nCreating visual difference map...")
    diff_map = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(diff_map)
    
    for i, diff in enumerate(differences[:100]):
        # Color code by severity (red = most severe)
        severity = min(255, int(diff['diff_percentage'] * 2.55))
        color = (severity, 255 - severity, 0)
        
        draw.rectangle(
            [diff['x'], diff['y'], diff['x'] + diff['width'], diff['y'] + diff['height']],
            outline=color,
            width=2
        )
        
        # Label top 20
        if i < 20:
            draw.text((diff['x'] + 2, diff['y'] + 2), str(i+1), fill='black')
    
    diff_map.save("outputs/difference_map_top100.png")
    print("✅ Difference map saved: outputs/difference_map_top100.png")
    
    # Create side-by-side comparison with annotations
    comparison = Image.new('RGB', (w*2 + 40, h + 60), 'white')
    comparison.paste(obj, (10, 50))
    comparison.paste(gen, (w + 30, 50))
    
    draw_comp = ImageDraw.Draw(comparison)
    draw_comp.text((w//2 - 50, 10), "OBJETIVO", fill='blue')
    draw_comp.text((w + w//2 - 50, 10), "GENERATED", fill='green')
    
    # Mark top 20 differences on both
    for i, diff in enumerate(differences[:20]):
        x, y = diff['x'], diff['y']
        # On objective
        draw_comp.rectangle([x + 10, y + 50, x + diff['width'] + 10, y + diff['height'] + 50],
                          outline='red', width=2)
        # On generated
        draw_comp.rectangle([x + w + 30, y + 50, x + diff['width'] + w + 30, y + diff['height'] + 50],
                          outline='red', width=2)
    
    comparison.save("outputs/comparison_annotated_top20.png")
    print("✅ Annotated comparison saved: outputs/comparison_annotated_top20.png")
    
    print("\n" + "="*100)
    print("ANALYSIS COMPLETE")
    print("="*100)
    
    return differences

if __name__ == "__main__":
    differences = analyze_differences()
    print(f"\n🎯 Next step: Use these {len(differences)} identified differences to make surgical corrections")
    print("   Focus on top 100 most severe differences for maximum impact")
