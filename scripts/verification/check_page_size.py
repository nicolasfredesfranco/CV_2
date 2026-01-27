import fitz
import json

INPUT_PDF = "/home/nicofredes/Desktop/code/CV/nueva_version_no_editar.pdf"

def get_page_dimensions():
    """Get the actual page dimensions from the PDF"""
    doc = fitz.open(INPUT_PDF)
    page = doc[0]
    rect = page.rect  # Returns fitz.Rect with x0, y0, x1, y1
    
    print(f"Page dimensions:")
    print(f"  Width: {rect.width}")
    print(f"  Height: {rect.height}")
    print(f"  Rect: {rect}")
    
    return rect.width, rect.height

if __name__ == "__main__":
    get_page_dimensions()
