import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfWriter, PdfReader
import fitz

# Configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PDF = os.path.join(BASE_DIR, 'nueva_version_no_editar.pdf')
OUTPUT_PDF = os.path.join(BASE_DIR, 'nueva_version_no_editar_2.pdf')
OVERLAY_PDF = os.path.join(BASE_DIR, 'temp_overlay.pdf')

# Get ACTUAL page size from the INPUT PDF
doc = fitz.open(INPUT_PDF)
page_rect = doc[0].rect
ACTUAL_PAGE_WIDTH = page_rect.width
ACTUAL_PAGE_HEIGHT = page_rect.height
doc.close()

print(f"Using actual page dimensions: {ACTUAL_PAGE_WIDTH} x {ACTUAL_PAGE_HEIGHT} pts")

# Extracted Coordinates from fitz (Top-Down: x0, y0, x1, y1)
# These are in PDF coordinate system (top-left origin)
LINK_MAP = [
    {
        "url": "mailto:nico.fredes.franco@gmail.com",
        "rect": [45.38, 87.27, 181.09, 96.69]
    },
    {
        "url": "https://github.com/nicolasfredesfranco",
        "rect": [99.72, 98.27, 186.31, 105.74]
    },
    {
        "url": "http://www.linkedin.com/in/nicolasfredesfranco",
        "rect": [99.72, 109.28, 186.31, 116.75]
    },
    {
        "url": "https://twitter.com/NicoFredesFranc",
        "rect": [99.72, 120.29, 168.71, 127.75]
    },
    {
        "url": "https://doi.org/10.1109/ACCESS.2021.3094723",
        "rect": [44.72, 372.83, 188.80, 379.48]
    }
]

def create_overlay():
    print("Generating link overlay with corrected page height...")
    
    # Create canvas with ACTUAL page size (not A4!)
    c = canvas.Canvas(OVERLAY_PDF, pagesize=(ACTUAL_PAGE_WIDTH, ACTUAL_PAGE_HEIGHT))

    for link in LINK_MAP:
        url = link['url']
        # Input rect is [x0, y0, x1, y1] (Top-Left Origin from fitz)
        rx0, ry0, rx1, ry1 = link['rect']
        
        # Convert to ReportLab (Bottom-Left Origin)
        # RL_y_bottom = PageHeight - PDF_y1 (since y1 is the bottom edge in top-down)
        # RL_y_top = PageHeight - PDF_y0 (since y0 is the top edge in top-down)
        
        x = rx0
        y = ACTUAL_PAGE_HEIGHT - ry1  # Bottom edge of rect
        w = rx1 - rx0
        h = ry1 - ry0
        
        link_rect = (x, y, x + w, y + h)
        
        c.linkURL(url, link_rect, relative=0, thickness=0)
        print(f"Added link: {url}")
        print(f"  PDF coords (top-down):   [{rx0:.2f}, {ry0:.2f}, {rx1:.2f}, {ry1:.2f}]")
        print(f"  ReportLab rect (bottom-up): ({x:.2f}, {y:.2f}, {x+w:.2f}, {y+h:.2f})")

    # Force page creation
    c.showPage()
    c.save()
    print(f"\nOverlay created with {len(LINK_MAP)} links using page dimensions {ACTUAL_PAGE_WIDTH}x{ACTUAL_PAGE_HEIGHT}.")

def merge_pdfs():
    print("\nMerging PDFs...")
    
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
    
    # Merge the overlay
    page_base.merge_page(reader_overlay.pages[0])
    
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
