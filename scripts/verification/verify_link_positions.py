from pypdf import PdfReader
import os

OUTPUT_PDF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'nueva_version_no_editar_2.pdf')

def verify_link_positions():
    reader = PdfReader(OUTPUT_PDF)
    page = reader.pages[0]
    
    if '/Annots' not in page:
        print("❌ No annotations found on the page.")
        return

    annots = page['/Annots']
    print(f"Found {len(annots)} annotations.\n")
    
    expected_coords = {
        "mailto:nico.fredes.franco@gmail.com": {
            "desc": "Email",
            "expected_rect": [45.38, 745.20, 181.09, 754.62]
        },
        "https://github.com/nicolasfredesfranco": {
            "desc": "GitHub",
            "expected_rect": [99.72, 736.15, 186.31, 743.62]
        },
        "http://www.linkedin.com/in/nicolasfredesfranco": {
            "desc": "LinkedIn",
            "expected_rect": [99.72, 725.14, 186.31, 732.61]
        },
        "https://twitter.com/NicoFredesFranc": {
            "desc": "Twitter",
            "expected_rect": [99.72, 714.14, 168.71, 721.60]
        },
        "https://doi.org/10.1109/ACCESS.2021.3094723": {
            "desc": "DOI",
            "expected_rect": [44.72, 462.41, 188.80, 469.06]
        }
    }
    
    for annot in annots:
        obj = annot.get_object()
        if '/A' in obj and '/URI' in obj['/A']:
            uri = obj['/A']['/URI']
            rect = obj.get('/Rect', None)
            
            if uri in expected_coords:
                exp = expected_coords[uri]
                print(f"✅ {exp['desc']}: {uri}")
                print(f"   Actual Rect:   {[float(r) for r in rect]}")
                print(f"   Expected Rect: {exp['expected_rect']}")
                
                # Check if within tolerance (5pt)
                if rect:
                    actual = [float(r) for r in rect]
                    expected = exp['expected_rect']
                    
                    # Calculate differences
                    diffs = [abs(actual[i] - expected[i]) for i in range(4)]
                    max_diff = max(diffs)
                    
                    if max_diff < 5.0:
                        print(f"   ✓ Position PERFECT (max diff: {max_diff:.2f}pt)")
                    else:
                        print(f"   ⚠ Position NEEDS ADJUSTMENT (max diff: {max_diff:.2f}pt)")
                print()

if __name__ == "__main__":
    verify_link_positions()
