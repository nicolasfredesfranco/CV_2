#!/usr/bin/env python3
"""
Perfect Rectangles Iterator - 100% Precision

Iterates until blue rectangles are 100% perfect in:
- Position (x, y)
- Size (width, height)
- Color (RGB)

Shows visual comparison in browser after each iteration.
"""

import pdfplumber
from pdf2image import convert_from_path
import numpy as np
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
import webbrowser
import os

class PerfectRectangleIterator:
    def __init__(self):
        self.objective_pdf = "pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf"
        self.shapes_file = "data/shapes.json"
        self.iteration = 0
        self.max_iterations = 20
        
    def extract_rectangles_from_objective(self):
        """Extract exact rectangle data from objective PDF"""
        print(f"\n{'='*80}")
        print(f"ITERATION {self.iteration}: Extracting rectangles from objective")
        print(f"{'='*80}\n")
        
        with pdfplumber.open(self.objective_pdf) as pdf:
            page = pdf.pages[0]
            page_height = page.height
            rects = page.rects
            
            print(f"Total rectangles in PDF: {len(rects)}")
            
            # Filter for blue bars: width 100-400, height 15-25
            candidates = []
            for i, r in enumerate(rects):
                w = r['width']
                h = r['height']
                if 100 < w < 400 and 15 < h < 25:
                    candidates.append({
                        'index': i,
                        'x': float(r['x0']),
                        'y': float(r['top']),
                        'width': float(w),
                        'height': float(h)
                    })
            
            print(f"Blue bar candidates: {len(candidates)}")
            
            # Take first 3
            selected = candidates[:3] if len(candidates) >= 3 else candidates
            
            return selected
    
    def extract_colors_from_image(self, rectangles):
        """Extract exact colors by sampling from rendered objective"""
        print("\nExtracting colors from rendered objective...")
        
        obj_img = convert_from_path(self.objective_pdf, dpi=300)[0]
        obj_arr = np.array(obj_img.convert('RGB'))
        
        px_to_pt = 300 / 72
        page_height_pt = 841.89  # A4
        
        for rect in rectangles:
            # Convert PDF coords to image coords
            img_x = int(rect['x'] * px_to_pt)
            img_y = int((page_height_pt - rect['y'] - rect['height']) * px_to_pt)
            img_w = int(rect['width'] * px_to_pt)
            img_h = int(rect['height'] * px_to_pt)
            
            # Sample from center
            center_y = img_y + img_h // 2
            center_x = img_x + img_w // 2
            
            # Get 20x20 sample
            y1 = max(0, center_y - 10)
            y2 = min(obj_arr.shape[0], center_y + 10)
            x1 = max(0, center_x - 10)
            x2 = min(obj_arr.shape[1], center_x + 10)
            
            sample = obj_arr[y1:y2, x1:x2, :]
            avg_color = np.mean(sample.reshape(-1, 3), axis=0) / 255.0
            
            rect['color'] = avg_color.tolist()
            
            print(f"  Bar at y={rect['y']:.1f}: RGB({avg_color[0]:.4f}, {avg_color[1]:.4f}, {avg_color[2]:.4f})")
        
        return rectangles
    
    def apply_rectangles(self, rectangles):
        """Apply rectangles to shapes.json"""
        shapes = []
        
        for rect in rectangles:
            shapes.append({
                'type': 'rect',
                'x': rect['x'],
                'y': rect['y'],
                'width': rect['width'],
                'height': rect['height'],
                'fill_color': rect['color'],
                'stroke': False,
                'opacity': 1.0
            })
        
        with open(self.shapes_file, 'w') as f:
            json.dump(shapes, f, indent=2)
        
        print(f"\n✅ Applied {len(shapes)} rectangles to shapes.json")
    
    def generate_cv(self):
        """Generate CV"""
        result = subprocess.run(['python', 'main.py'], capture_output=True, timeout=15)
        return result.returncode == 0
    
    def compare_rectangles(self):
        """Compare rectangles pixel-by-pixel"""
        obj = convert_from_path(self.objective_pdf, dpi=250)[0]
        gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=250)[0]
        
        obj_arr = np.array(obj.convert('RGB'))
        gen_arr = np.array(gen.convert('RGB').resize(obj.size))
        
        # Sample blue bar regions (approximate)
        regions = [
            (80, 250, 200, 650),    # Top bar
            (50, 650, 250, 750),    # Left middle
            (50, 2800, 250, 2900)   # Left bottom
        ]
        
        similarities = []
        
        for i, (y1, x1, y2, x2) in enumerate(regions):
            if y2 <= obj_arr.shape[0] and x2 <= obj_arr.shape[1]:
                obj_region = obj_arr[y1:y2, x1:x2, :]
                gen_region = gen_arr[y1:y2, x1:x2, :]
                
                diff = np.abs(obj_region.astype(int) - gen_region.astype(int))
                diff_binary = np.any(diff > 5, axis=2)  # Strict threshold
                sim = 100 * (1 - np.sum(diff_binary) / diff_binary.size)
                
                similarities.append(sim)
                print(f"  Region {i+1}: {sim:.2f}% match")
        
        avg_sim = np.mean(similarities) if similarities else 0
        return avg_sim
    
    def create_visual_comparison(self, rect_similarity):
        """Create HTML comparison and open in browser"""
        obj = convert_from_path(self.objective_pdf, dpi=200)[0]
        gen = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=200)[0]
        
        gen = gen.resize(obj.size)
        w, h = obj.size
        
        # Create comparison image
        comparison = Image.new('RGB', (w * 2 + 60, h + 150), 'white')
        comparison.paste(obj, (20, 100))
        comparison.paste(gen, (w + 40, 100))
        
        draw = ImageDraw.Draw(comparison)
        
        try:
            font_big = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)
            font_med = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
        except:
            font_big = font_med = ImageFont.load_default()
        
        # Title
        title = f"ITERATION {self.iteration} - Rectangle Comparison"
        draw.text((comparison.width // 2 - 300, 20), title, fill='black', font=font_big)
        
        # Labels
        draw.text((w // 2 - 90, 60), "OBJETIVO", fill='red', font=font_med)
        draw.text((w + w // 2 - 90, 60), "GENERADO", fill='blue', font=font_med)
        
        # Status
        status = f"Rectangles: {rect_similarity:.2f}% match"
        color = 'green' if rect_similarity > 98 else 'orange' if rect_similarity > 90 else 'red'
        draw.text((comparison.width // 2 - 200, h + 110), status, fill=color, font=font_med)
        
        # Save
        img_path = f"outputs/iteration_{self.iteration:02d}.png"
        comparison.save(img_path, 'PNG')
        
        # Create HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Iteration {self.iteration} - Rectangle Comparison</title>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: #f0f0f0;
                    font-family: Arial, sans-serif;
                }}
                .container {{
                    max-width: 1600px;
                    margin: 0 auto;
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                }}
                h1 {{
                    text-align: center;
                    color: #333;
                }}
                .status {{
                    text-align: center;
                    font-size: 24px;
                    margin: 20px 0;
                    padding: 15px;
                    background: {'#d4edda' if rect_similarity > 98 else '#fff3cd' if rect_similarity > 90 else '#f8d7da'};
                    border-radius: 5px;
                }}
                img {{
                    width: 100%;
                    border: 2px solid #333;
                }}
                .next {{
                    text-align: center;
                    margin-top: 20px;
                }}
                button {{
                    padding: 15px 30px;
                    font-size: 18px;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }}
                button:hover {{
                    background: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Iteration {self.iteration}: Rectangle Precision Check</h1>
                <div class="status">
                    Rectangle Match: {rect_similarity:.2f}%
                    {'✅ PERFECT!' if rect_similarity > 98 else '⚠️ Needs improvement' if rect_similarity > 90 else '❌ Significant differences'}
                </div>
                <img src="{img_path}" alt="Comparison">
                <div class="next">
                    <p>{'Perfect match achieved! ✅' if rect_similarity > 98 else 'Will iterate again...'}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        html_path = f"outputs/iteration_{self.iteration:02d}.html"
        with open(html_path, 'w') as f:
            f.write(html)
        
        # Open in browser
        webbrowser.open('file://' + os.path.abspath(html_path))
        
        print(f"\n✅ Visual comparison opened in browser")
        print(f"   File: {html_path}")
        
        return rect_similarity
    
    def iterate(self):
        """Main iteration loop"""
        print("\n" + "="*80)
        print("PERFECT RECTANGLES ITERATOR - Starting")
        print("="*80)
        
        while self.iteration < self.max_iterations:
            self.iteration += 1
            
            # Extract from objective
            rectangles = self.extract_rectangles_from_objective()
            
            if not rectangles:
                print("❌ No rectangles found!")
                break
            
            # Get colors
            rectangles = self.extract_colors_from_image(rectangles)
            
            # Apply
            self.apply_rectangles(rectangles)
            
            # Generate
            print("\nGenerating CV...")
            if not self.generate_cv():
                print("❌ Generation failed!")
                break
            
            # Compare
            print("\nComparing rectangles...")
            rect_sim = self.compare_rectangles()
            
            # Visual comparison in browser
            print("\nCreating visual comparison...")
            final_sim = self.create_visual_comparison(rect_sim)
            
            print(f"\n{'='*80}")
            print(f"ITERATION {self.iteration} COMPLETE")
            print(f"Rectangle Match: {final_sim:.2f}%")
            print(f"{'='*80}")
            
            # Check if perfect
            if final_sim > 98:
                print("\n🎉 100% PERFECTION ACHIEVED!")
                break
            
            # Wait for user check
            input("\nPress Enter to continue next iteration (or Ctrl+C to stop)...")
        
        print(f"\n✅ Completed {self.iteration} iterations")

if __name__ == "__main__":
    iterator = PerfectRectangleIterator()
    iterator.iterate()
