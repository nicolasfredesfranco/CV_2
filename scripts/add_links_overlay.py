import json
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfWriter, PdfReader

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
COORDS_FILE = os.path.join(DATA_DIR, 'coordinates.json')
INPUT_PDF = os.path.join(BASE_DIR, 'nueva_version_no_editar.pdf')
OUTPUT_PDF = os.path.join(BASE_DIR, 'nueva_version_no_editar_2.pdf')
OVERLAY_PDF = os.path.join(BASE_DIR, 'temp_overlay.pdf')

def create_overlay():
    """Generates a transparent PDF with only link annotations."""
    print("Generating link overlay...")
    
    # Load Coordinates
    with open(COORDS_FILE, 'r') as f:
        elements = json.load(f)

    c = canvas.Canvas(OVERLAY_PDF, pagesize=A4)
    _, page_height = A4 # 595.27 x 841.89 pts

    count = 0
    for elem in elements:
        text = elem['text']
        x = elem['x']
        y_orig = elem['y']
        
        # Coordinate Transformation (Top-Down -> Bottom-Up)
        y = page_height - y_orig
        
        url_target = None
        clean_t = text.strip()
        
        # Logic from main.py
        if "nico.fredes.franco@gmail.com" in clean_t:
            url_target = "mailto:nico.fredes.franco@gmail.com"
        elif "DOI: 10.1109/ACCESS.2021.3094723" in clean_t:
            url_target = "https://doi.org/10.1109/ACCESS.2021.3094723"
        elif "nicofredesfranc" in clean_t:
            url_target = "https://twitter.com/NicoFredesFranc"
        elif "nicolasfredesfranco" in clean_t:
            # GitHub vs LinkedIn Logic
            if y_orig < 102:
                 url_target = "https://github.com/nicolasfredesfranco"
            else:
                 url_target = "http://www.linkedin.com/in/nicolasfredesfranco"
        
        if url_target:
            # Estimate width/height (approximate since we don't have font metrics loaded perfectly here, 
            # but usually the bounding box in coords could be used if available. 
            # main.py used stringWidth. We'll approximate or use a generic width based on char count for safety 
            # OR better: use main.py logic if we loaded fonts.
            # To be safe and simple: text length * approx width per char (e.g. 5) 
            # But main.py uses exact fonts. Let's try to grab font size from elem.
            
            size = elem['size']
            # Approximation: width ~ len * size * 0.5
            width = len(text) * size * 0.5 
            
            # Corrections for specific links if needed, but this approx is usually fine for a hitbox
            
            # Define Hitbox: [x, y_bottom, x_right, y_top]
            # y is the baseline. 
            link_rect = (x, y - 2, x + width, y + size)
            
            c.linkURL(url_target, link_rect, relative=0, thickness=0)
            count += 1
            print(f"Added link: {url_target} at ({x}, {y})")

    # Force page creation
    c.showPage()
    c.save()
    print(f"Overlay created with {count} links.")
    return count

def merge_pdfs():
    """Merges the overlay onto the original PDF."""
    print("Merging PDFs...")
    
    if not os.path.exists(OVERLAY_PDF) or os.path.getsize(OVERLAY_PDF) == 0:
        print("❌ Error: Overlay PDF is empty or missing.")
        return

    reader_base = PdfReader(INPUT_PDF)
    if len(reader_base.pages) == 0:
         print("❌ Error: Base PDF is empty.")
         return
    page_base = reader_base.pages[0]
    
    reader_overlay = PdfReader(OVERLAY_PDF)
    if len(reader_overlay.pages) == 0:
         print("❌ Error: Overlay PDF has no pages.")
         return
    page_overlay = reader_overlay.pages[0]
    
    page_base.merge_page(page_overlay)
    
    writer = PdfWriter()
    writer.add_page(page_base)
    
    with open(OUTPUT_PDF, 'wb') as f:
        writer.write(f)
        
    print(f"✅ Created {OUTPUT_PDF}")
    
    # Cleanup
    if os.path.exists(OVERLAY_PDF):
        os.remove(OVERLAY_PDF)

if __name__ == "__main__":
    create_overlay()
    merge_pdfs()
