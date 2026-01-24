import fitz
import json

def deep_inspect_skills(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Region approx
    rect = fitz.Rect(0, 400, 220, 710)
    
    print("--- Text Blocks ---")
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b['type'] == 0: # text
            bbox = fitz.Rect(b['bbox'])
            if bbox.intersects(rect):
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"]
                        print(f"Text: '{text}' Font: {s['font']} Size: {s['size']} Color: {s['color']} Origin: {s['origin']}")

    print("\n--- Images ---")
    images = page.get_images(full=True)
    for img in images:
        xref = img[0]
        # Get image rect
        try:
            img_rect = page.get_image_bbox(img)
            if img_rect.intersects(rect):
               print(f"Image found at {img_rect}")
        except:
             pass

    print("\n--- Raw Text (First 50 chars in region) ---")
    raw = page.get_text("rawdict")
    count = 0
    for b in raw["blocks"]:
        if b["type"] == 0:
            for l in b["lines"]:
                for s in l["spans"]:
                    for c in s["chars"]:
                        c_bbox = fitz.Rect(c["bbox"])
                        if c_bbox.intersects(rect):
                            print(f"Char: '{c['c']}'bbox: {c['bbox']}")
                            count += 1
                            if count > 50: break
                if count > 50: break
        if count > 50: break
