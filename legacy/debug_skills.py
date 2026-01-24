import fitz
import json
import sys

def debug_skills_text(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    # Define SKILLS region (Left column, approx Y=400 to 710)
    # Based on previous JSON analysis: 
    # SKILLS title is at y=409. 
    # LANGUAGE starts at y=710.
    # X range approx 0 to 220.
    
    rect = fitz.Rect(0, 400, 220, 710)
    
    words = page.get_text("words")
    
    skills_words = []
    for w in words:
        # w is (x0, y0, x1, y1, "text", block_no, line_no, word_no)
        x0, y0, x1, y1, text = w[:5]
        
        # Check intersection with SKILLS rect
        if x0 >= rect.x0 and y0 >= rect.y0 and x1 <= rect.x1 and y1 <= rect.y1:
            skills_words.append({
                'text': text,
                'x': x0,
                'y': y0, # Up-left
                'x1': x1,
                'y1': y1
            })
            
    print(f"Found {len(skills_words)} words in SKILLS region.")
    for sw in skills_words:
        print(f"  {sw['text']} (x={sw['x']:.2f}, y={sw['y']:.2f})")

if __name__ == "__main__":
    debug_skills_text("Objetivo_No_editar.pdf")
