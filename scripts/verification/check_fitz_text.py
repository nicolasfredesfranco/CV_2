import fitz
import sys

def check_text():
    doc = fitz.open("/home/nicofredes/Desktop/code/CV/nueva_version_no_editar.pdf")
    page = doc[0]
    text = page.get_text("dict")
    
    blocks = text.get("blocks", [])
    print(f"Found {len(blocks)} blocks.")
    
    found_any = False
    for b in blocks:
        if "lines" in b:
            for l in b["lines"]:
                for s in l["spans"]:
                    t = s["text"].strip()
                    if t:
                        found_any = True
                        print(f"Found text: '{t}' at {s['bbox']}")
                        # Just print a few
                        if len(t) > 5:
                            break
            if found_any: break
            
    if not found_any:
        print("NO TEXT FOUND. Purely graphical.")
    else:
        print("Text extraction SUCCESS.")

if __name__ == "__main__":
    check_text()
