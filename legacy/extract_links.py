
import fitz  # PyMuPDF
import json
import sys

def extract_links(pdf_path):
    doc = fitz.open(pdf_path)
    links = []
    
    print(f"Analyzing {pdf_path} for links...")
    
    for page_num, page in enumerate(doc):
        # get_links returns a list of dictionaries
        page_links = page.get_links()
        
        for link in page_links:
            # link structure: {'kind': 2, 'uri': '...', 'from': Rect(...)}
            if link['kind'] == fitz.LINK_URI:
                rect = link['from']
                # Extract text under this matching rect
                # We add a small buffer to ensure we catch the text
                text_instances = page.get_text("dict", clip=rect)["blocks"]
                
                link_text = ""
                for block in text_instances:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                link_text += span["text"] + " "
                
                link_text = link_text.strip()
                
                links.append({
                    "page": page_num,
                    "uri": link['uri'],
                    "text_hint": link_text,
                    "rect": [rect.x0, rect.y0, rect.x1, rect.y1]
                })
                print(f"Found link: {link['uri']} on text '{link_text}'")

    with open("extracted_links_report.json", "w") as f:
        json.dump(links, f, indent=2)
    
    print(f"Saved {len(links)} links to extracted_links_report.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 extract_links.py <pdf_file>")
        sys.exit(1)
        
    extract_links(sys.argv[1])
