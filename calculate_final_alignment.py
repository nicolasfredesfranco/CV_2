"""
Calculate Final X Positions Accounting for PrecisionCorrector
==============================================================
This script accounts for ALL transformations including PrecisionCorrector
"""

import json
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

TARGET_RIGHT_EDGE = 590.0

# From config.py
THRESHOLD_DATE_ALIGN_X = 380.0
THRESHOLD_DATE_ALIGN_Y_LIMIT = 750.0
OFFSET_DATE_CORRECTION = 1.5
PAGE_HEIGHT = 806.0

def register_fonts():
    """Register custom fonts."""
    fonts_dir = Path(__file__).parent / "data" / "assets"
    
    pdfmetrics.registerFont(TTFont("TrebuchetMS", str(fonts_dir / "trebuc.ttf")))
    pdfmetrics.registerFont(TTFont("TrebuchetMS-Bold", str(fonts_dir / "trebucbd.ttf")))
    pdfmetrics.registerFont(TTFont("TrebuchetMS-Italic", str(fonts_dir / "trebucit.ttf")))

def get_text_width(text, font_name, font_size):
    """Get the actual width of text using ReportLab metrics."""
    return pdfmetrics.stringWidth(text, font_name, font_size)

def calculate_final_positions():
    """Calculate final X positions accounting for PrecisionCorrector."""
    
    # Register fonts
    register_fonts()
    
    # Load coordinates
    data_path = Path(__file__).parent / "data" / "coordinates.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        coords = json.load(f)
    
    # Define elements
    locations = [
        "Remote, USA",
        "Las Condes, Chile ",
        "Remote, Mexico ",
        "Santiago, Chile ",
        "Remote, USA",  # EPAM
        "Quilicura, Chile ",
        "Valparaíso, Chile ",
    ]
    
    dates = [
        "Since January 2026 ",
        "November 2025 - January 2026",
        "September 2024 - October 2025",
        "February 2024 - September 2024 ",
        "May 2023 - October 2023 ",
        "November 2021 - November 2022 ",
        "January 2020 - November 2021 ",
    ]
    
    companies = ["JOBSITY", "ZENTA GROUP", "DEUNA", "SPOT", "EPAM Systems", "WALMART Chile", "LAMNGEN Ltda."]
    
    print("=" * 100)
    print(f"FINAL X POSITIONS ACCOUNTING FOR PRECISIONCORRECTOR (Target: X = {TARGET_RIGHT_EDGE})")
    print("=" * 100)
    print()
    
    # Calculate locations
    print("LOCATIONS (No PrecisionCorrector offset):")
    print("-" * 100)
    print(f"{'#':<4} {'Company':<20} {'Width':<10} {'Target X':<10} {'Current X':<10} {'Adjustment':<12}")
    print("-" * 100)
    
    location_changes = []
    location_index = 0
    
    for i, coord in enumerate(coords):
        if location_index < len(locations) and coord.get("text") == locations[location_index]:
            current_x = coord["x"]
            text = coord["text"]
            font = coord["font"]
            size = coord["size"]
            
            # Calculate width
            text_width = get_text_width(text, font, size)
            
            # Locations do NOT get PrecisionCorrector offset (they're location text, not in date column)
            # Target: START_X = 590 - text_width
            target_x = round(TARGET_RIGHT_EDGE - text_width, 2)
            adjustment = round(target_x - current_x, 2)
            
            location_changes.append({
                "company": companies[location_index],
                "current_x": current_x,
                "target_x": target_x,
                "adjustment": adjustment
            })
            
            print(f"{location_index + 1:<4} {companies[location_index]:<20} {text_width:<10.2f} {target_x:<10.2f} {current_x:<10.2f} {adjustment:+12.2f}")
            location_index += 1
    
    print("-" * 100)
    print()
    
    # Calculate dates  
    print("DATES (WITH PrecisionCorrector offset of -1.5):")
    print("-" * 100)
    print(f"{'#':<4} {'Company':<20} {'Width':<10} {'Target X':<12} {'Current X':<10} {'Adjustment':<12}")
    print("-" * 100)
    
    date_changes = []
    date_index = 0
    
    for i, coord in enumerate(coords):
        if date_index < len(dates) and coord.get("text") == dates[date_index]:
            current_x = coord["x"]
            text = coord["text"]
            font = coord["font"]
            size = coord["size"]
            raw_y = coord["y"]
            
            # Calculate width
            text_width = get_text_width(text, font, size)
            
            # Dates GET PrecisionCorrector offset: final_x = start_x - 1.5
            # So: start_x - 1.5 + text_width = 590
            # Therefore: start_x = 590 - text_width + 1.5
            target_x = round(TARGET_RIGHT_EDGE - text_width + OFFSET_DATE_CORRECTION, 2)
            adjustment = round(target_x - current_x, 2)
            
            date_changes.append({
                "company": companies[date_index],
                "current_x": current_x,
                "target_x": target_x,
                "adjustment": adjustment
            })
            
            print(f"{date_index + 1:<4} {companies[date_index]:<20} {text_width:<10.2f} {target_x:<12.2f} {current_x:<10.2f} {adjustment:+12.2f}")
            date_index += 1
    
    print("-" * 100)
    print()
    
    # Output changes
    print("=" * 100)
    print("REQUIRED CHANGES:")
    print("=" * 100)
    print()
    print("LOCATIONS:")
    for change in location_changes:
        print(f"{change['company']:<20} {change['current_x']:.2f} → {change['target_x']:.2f} ({change['adjustment']:+.2f})")
    print()
    print("DATES:")
    for change in date_changes:
        print(f"{change['company']:<20} {change['current_x']:.2f} → {change['target_x']:.2f} ({change['adjustment']:+.2f})")
    print()
    
    return location_changes, date_changes

if __name__ == "__main__":
    calculate_final_positions()
