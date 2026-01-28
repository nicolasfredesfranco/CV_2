#!/usr/bin/env python3
"""
Professional CV Generator
=========================

High-precision PDF generation system for creating pixel-perfect curriculum vitae
documents using coordinate-based positioning and vector graphics rendering.

Author: Nicolás Ignacio Fredes Franco
License: MIT
Version: 1.3.5

Features:
    - Coordinate-based element positioning from data/coordinates.json
    - Vector shape rendering from data/shapes.json  
    - Custom font support (TrebuchetMS family)
    - Clickable hyperlink injection
    - Exact color reproduction
    - Custom page dimensions (623x806pt)

Usage:
    python main.py

Output:
    outputs/Nicolas_Fredes_CV.pdf

Dependencies:
    - reportlab>=4.0.0
"""

import sys
import os
import json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Configuration
CUSTOM_PAGE_SIZE = (623.622, 806.299)  # Exact page size from objective PDF (floating-point precision)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ASSETS_DIR = os.path.join(DATA_DIR, 'assets')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

COORDS_FILE = os.path.join(DATA_DIR, 'coordinates.json')
SHAPES_FILE = os.path.join(DATA_DIR, 'shapes.json')
OUTPUT_PDF = os.path.join(OUTPUT_DIR, 'Nicolas_Fredes_CV.pdf')

# Font Configuration
FONT_PATHS = {
    'TrebuchetMS': os.path.join(ASSETS_DIR, 'trebuc.ttf'),
    'TrebuchetMS-Bold': os.path.join(ASSETS_DIR, 'trebucbd.ttf'),
    'TrebuchetMS-Italic': os.path.join(ASSETS_DIR, 'trebucit.ttf'),
    'AbyssinicaSIL-Regular': '/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-Regular.ttf'
}

# Precision Constants
# Exact colors from objective PDF vector analysis
BLUE_COLOR = (0.1687, 0.4509, 0.7012)  # Light blue for headers RGB(43, 115, 179)
DARK_BLUE = (0.0588, 0.3176, 0.7930)   # Dark blue for name RGB(15, 81, 202)

def load_fonts():
    """Registers TTF fonts with ReportLab."""
    loaded = []
    for name, path in FONT_PATHS.items():
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont(name, path))
                loaded.append(name)
            except Exception as e:
                print(f"⚠️ Warning: Could not load font {name}: {e}")
    return loaded

def rgb_from_int(color_int):
    """Converts integer color value to normalized RGB tuple (0.0-1.0)."""
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return (r/255.0, g/255.0, b/255.0)

class CVGenerator:
    """
    Main engine for generating the CV using high-precision coordinates.
    """
    def __init__(self, coords_path, shapes_path, output_path):
        self.coords_path = coords_path
        self.shapes_path = shapes_path
        self.output_path = output_path
        self.elements = []
        self.shapes = []
        
        self._load_data()
        
    def _load_data(self):
        """Loads JSON data for text elements and geometric shapes."""
        try:
            with open(self.coords_path, 'r', encoding='utf-8') as f:
                self.elements = json.load(f)
            
            if os.path.exists(self.shapes_path):
                with open(self.shapes_path, 'r') as f:
                    self.shapes = json.load(f)
        except FileNotFoundError as e:
            print(f"❌ Error: Could not find data file: {e}")
            sys.exit(1)

    def generate(self):
        """Executes the PDF generation process."""
        print(f"Generating CV to {self.output_path}...")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        
        c = canvas.Canvas(self.output_path, pagesize=CUSTOM_PAGE_SIZE)
        _, page_height = CUSTOM_PAGE_SIZE  # 623 x 806 pts (matches objective)
        
        # 1. Render Background Shapes
        self._draw_shapes(c, page_height)
        
        # 2. Render Text Content
        self._draw_elements(c, page_height)
        
        c.save()
        print("✅ CV Generation Complete.")

    def _draw_shapes(self, c, page_height):
        """Draws geometric shapes (e.g., Blue Headers) with coordinate transformation."""
        for shape in self.shapes:
            if shape['type'] == 'rect':
                sc = shape.get('color', [])
                if len(sc) != 3: continue
                
                # Filter for Blue-ish rectangles only
                is_blue = (abs(sc[0] - BLUE_COLOR[0]) < 0.2 and
                           abs(sc[1] - BLUE_COLOR[1]) < 0.2 and
                           abs(sc[2] - BLUE_COLOR[2]) < 0.2)
                
                if is_blue:
                    rect = shape['rect'] # [x0, y0, x1, y1] (PDF Top-down y1 is bottom)
                    x0, y0, x1, y1 = rect
                    
                    w = x1 - x0
                    h = y1 - y0
                    
                    # Convert PDF Y (Top-Down) to ReportLab Y (Bottom-Up)
                    # Note: In PDF coords, y1 is the larger value (lower physically on page)
                    # ReportLab y = Height - y1
                    y = page_height - y1 
                    
                    c.setFillColorRGB(*sc)
                    c.rect(x0, y, w, h, stroke=0, fill=1)

    def _draw_elements(self, c, page_height):
        """
        Draws text elements and applies Hyper-Precision logic:
        - Font Weight Simulation
        - Bullet Injection
        - Alignment Correction
        - Hyperlinking
        """
        for elem in self.elements:
            text = elem['text']
            x = elem['x']
            y_orig = elem['y']
            
            # Coordinate Transformation (Top-Down -> Bottom-Up)
            y = page_height - y_orig
            
            # --- Hyper-Precision Fixes ---
            
            # 1. Date Alignment Fix
            # Right-aligned dates (X > 380) in the Right Column tend to drift right by ~1.5px.
            # We correct this to ensure perfect alignment with location text.
            if x > 380 and y > (page_height - 750):
                 x -= 1.5
            
            # 2. Bullet Point Injection (Heuristic)
            # The extracted data relies on indentation but often misses the actual bullet char.
            # Logic: If Right Column AND Not Bold/Italic AND Starts with Uppercase -> Inject Bullet.
            is_right_col = (x > 215)
            is_bold = elem.get('bold', False)
            is_italic = elem.get('italic', False)
            
            if is_right_col and not is_bold and not is_italic:
                clean_text = text.strip()
                if clean_text and clean_text[0].isupper() and len(clean_text) > 3:
                     # Filter out location text (X > 250)
                     if x < 250:
                         text = "• " + text
                         x -= 8.5 # Shift left to accommodate bullet (reduced by 2.5pt for vector precision)
            
            # 3. Font Selection
            font_family = elem.get('font', 'TrebuchetMS')
            size = elem['size']
            
            font_name = 'TrebuchetMS'
            if 'Bold' in font_family or is_bold:
                font_name = 'TrebuchetMS-Bold'
            elif 'Italic' in font_family or is_italic:
                font_name = 'TrebuchetMS-Italic'
            
            c.setFont(font_name, size)
            
            # 4. Color Application
            color_int = elem.get('color', 0)
            rgb = rgb_from_int(color_int)
            c.setFillColorRGB(*rgb)
            
            # 5. Text Rendering Mode
            # UPDATED: Removed weight simulation entirely to match objective PDF
            # The objective PDF uses clean, standard font rendering without stroke.
            # Using standard fill-only mode (mode 0) for all text.
            
            # Ensure we're in standard fill mode
            if hasattr(c, 'setTextRenderMode'):
                c.setTextRenderMode(0)
            else:
                 c._code.append('0 Tr')

                
            # 6. Hyperlink Injection
            # Detects context-aware strings and applies clickable links.
            url_target = None
            clean_t = text.strip()
            
            if "nico.fredes.franco@gmail.com" in clean_t:
                url_target = "mailto:nico.fredes.franco@gmail.com"
            elif "DOI: 10.1109/ACCESS.2021.3094723" in clean_t:
                url_target = "https://doi.org/10.1109/ACCESS.2021.3094723"
            elif "nicofredesfranc" in clean_t:
                url_target = "https://twitter.com/NicoFredesFranc"
            elif "nicolasfredesfranco" in clean_t:
                # Disambiguation: GitHub vs LinkedIn
                # Both share the username text. We use Y-coordinate to distinguish.
                # GitHub is at Y=145.27, LinkedIn at Y=156.27 (after vector shifts)
                if y_orig < 150:
                     url_target = "https://github.com/nicolasfredesfranco"
                else:
                     url_target = "http://www.linkedin.com/in/nicolasfredesfranco"
            
            if url_target:
                string_width = c.stringWidth(text, font_name, size)
                # Define Hitbox: [x, y_bottom, x_right, y_top]
                link_rect = (x, y - 2, x + string_width, y + size)
                c.linkURL(url_target, link_rect, relative=0, thickness=0)

            # Draw String
            try:
                c.drawString(x, y, text)
            except Exception as e:
                print(f"⚠️ Error drawing '{text}': {e}")
                
            # Reset Rendering Mode
            if hasattr(c, 'setTextRenderMode'):
                c.setTextRenderMode(0) 
            else:
                 c._code.append('0 Tr') 
            c.setLineWidth(1)

if __name__ == "__main__":
    print("🚀 Initializing Precision CV Engine...")
    fonts = load_fonts()
    print(f"📚 Loaded {len(fonts)} Fonts.")
    
    generator = CVGenerator(COORDS_FILE, SHAPES_FILE, OUTPUT_PDF)
    generator.generate()
