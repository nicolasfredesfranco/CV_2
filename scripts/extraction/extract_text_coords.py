from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextLine
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PDF = os.path.join(BASE_DIR, 'nueva_version_no_editar.pdf')

target_texts = [
    "nico.fredes.franco@gmail.com",
    "nicolasfredesfranco", 
    "nicofredesfranc",
    "DOI: 10.1109/ACCESS.2021.3094723"
]

found_coords = []

def extract_coords():
    print("Extracting with pdfminer...")
    for page_layout in extract_pages(INPUT_PDF):
        # We assume single page or we only care about first page for now
        # Page height is needed to flip coordinates if pdfminer uses bottom-up (it does)
        # pdfminer coordinates are usually bottom-up. pypdf/reportlab are also bottom-up.
        
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    if isinstance(text_line, LTTextLine):
                        line_text = text_line.get_text().strip()
                        # specific hit checks
                        for target in target_texts:
                            # We check if target is in line
                            if target in line_text or line_text in target:
                                # We found a line.
                                # Get bbox of the matching part?
                                # For simplicity, let's take the meaningful bbox of matched line.
                                # If the line IS exactly the target or close enough
                                
                                # Refinement: "nicolasfredesfranco" appears twice.
                                # We need top and bottom.
                                
                                # Log it
                                found_coords.append({
                                    "text": line_text,
                                    "target_key": target,
                                    "bbox": text_line.bbox, # (x0, y0, x1, y1)
                                    "page": page_layout.pageid
                                })
    
    print(json.dumps(found_coords, indent=2))

if __name__ == "__main__":
    extract_coords()
