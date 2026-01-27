from pypdf import PdfReader
import os

OUTPUT_PDF = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'nueva_version_no_editar_2.pdf')

def verify_links():
    reader = PdfReader(OUTPUT_PDF)
    page = reader.pages[0]
    
    if '/Annots' not in page:
        print("❌ No annotations found on the page.")
        return

    annots = page['/Annots']
    print(f"Found {len(annots)} annotations.")
    
    found_links = []
    
    for annot in annots:
        obj = annot.get_object()
        if '/A' in obj and '/URI' in obj['/A']:
            uri = obj['/A']['/URI']
            found_links.append(uri)
            print(f"✅ Found Link: {uri}")
            
    expected_links = [
        "mailto:nico.fredes.franco@gmail.com",
        "https://github.com/nicolasfredesfranco",
        "http://www.linkedin.com/in/nicolasfredesfranco",
        "https://twitter.com/NicoFredesFranc",
        "https://doi.org/10.1109/ACCESS.2021.3094723"
    ]
    
    # Check if all expected links are present
    missing = [link for link in expected_links if link not in found_links]
    
    if not missing:
        print("\n🚀 SUCCESS: All expected links are present.")
    else:
        print(f"\n⚠️ WARNING: Missing expected links: {missing}")

if __name__ == "__main__":
    verify_links()
