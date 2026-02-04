"""
Calculate positions for X=589 alignment
"""
import json
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

TARGET_RIGHT_EDGE = 589.0  # Changed from 590 to 589
OFFSET_DATE_CORRECTION = 1.5

def register_fonts():
    fonts_dir = Path(__file__).parent / "data" / "assets"
    pdfmetrics.registerFont(TTFont("TrebuchetMS", str(fonts_dir / "trebuc.ttf")))
    pdfmetrics.registerFont(TTFont("TrebuchetMS-Bold", str(fonts_dir / "trebucbd.ttf")))
    pdfmetrics.registerFont(TTFont("TrebuchetMS-Italic", str(fonts_dir / "trebucit.ttf")))

def get_text_width(text, font_name, font_size):
    return pdfmetrics.stringWidth(text, font_name, font_size)

def calculate():
    register_fonts()
    data_path = Path(__file__).parent / "data" / "coordinates.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        coords = json.load(f)
    
    locations = ["Remote, USA", "Las Condes, Chile ", "Remote, Mexico ", "Santiago, Chile ", 
                 "Remote, USA", "Quilicura, Chile ", "Valparaíso, Chile "]
    dates = ["Since January 2026 ", "November 2025 - January 2026", "September 2024 - October 2025",
             "February 2024 - September 2024 ", "May 2023 - October 2023 ", "November 2021 - November 2022 ",
             "January 2020 - November 2021 "]
    companies = ["JOBSITY", "ZENTA GROUP", "DEUNA", "SPOT", "EPAM Systems", "WALMART Chile", "LAMNGEN Ltda."]
    
    print(f"Target: X={TARGET_RIGHT_EDGE}")
    print("\nLOCATIONS (new X):")
    loc_idx = 0
    for coord in coords:
        if loc_idx < len(locations) and coord.get("text") == locations[loc_idx]:
            width = get_text_width(coord["text"], coord["font"], coord["size"])
            new_x = round(TARGET_RIGHT_EDGE - width, 2)
            print(f"{companies[loc_idx]:<20} {coord['x']:.2f} → {new_x:.2f} (shift: {new_x - coord['x']:+.2f})")
            loc_idx += 1
    
    print("\nDATES (new X, +1.5 for PrecisionCorrector):")
    date_idx = 0
    for coord in coords:
        if date_idx < len(dates) and coord.get("text") == dates[date_idx]:
            width = get_text_width(coord["text"], coord["font"], coord["size"])
            new_x = round(TARGET_RIGHT_EDGE - width + OFFSET_DATE_CORRECTION, 2)
            print(f"{companies[date_idx]:<20} {coord['x']:.2f} → {new_x:.2f} (shift: {new_x - coord['x']:+.2f})")
            date_idx += 1

if __name__ == "__main__":
    calculate()
