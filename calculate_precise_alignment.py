"""
Calculate Precise X Positions Using ReportLab
==============================================
Uses the actual ReportLab font metrics for accurate width calculations.
"""

import json
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

TARGET_RIGHT_EDGE = 590.0

def register_fonts():
    """Register custom fonts."""
    fonts_dir = Path(__file__).parent / "data" / "assets"
    
    pdfmetrics.registerFont(TTFont("TrebuchetMS", str(fonts_dir / "trebuc.ttf")))
    pdfmetrics.registerFont(TTFont("TrebuchetMS-Bold", str(fonts_dir / "trebucbd.ttf")))
    pdfmetrics.registerFont(TTFont("TrebuchetMS-Italic", str(fonts_dir / "trebucit.ttf")))

def get_text_width(text, font_name, font_size):
    """Get the actual width of text using ReportLab metrics."""
    return pdfmetrics.stringWidth(text, font_name, font_size)

def calculate_precise_positions():
    """Calculate precise X positions using actual font metrics."""
    
    # Register fonts
    register_fonts()
    
    # Load coordinates
    data_path = Path(__file__).parent / "data" / "coordinates.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        coords = json.load(f)
    
    # Define elements to modify
    locations = [
        "Remote, USA",
        "Las Condes, Chile ",
        "Remote, Mexico ",
        "Santiago, Chile ",
        "Remote, USA",  # EPAM (second occurrence)
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
    
    print("=" * 90)
    print(f"PRECISE X POSITIONS FOR RIGHT EDGE ALIGNMENT AT X = {TARGET_RIGHT_EDGE}")
    print("=" * 90)
    print()
    
    # Calculate new positions for locations
    print("LOCATIONS:")
    print("-" * 90)
    print(f"{'#':<4} {'Company':<20} {'Old X':<10} {'Width':<10} {'New X':<10} {'Shift':<10}")
    print("-" * 90)
    
    location_changes = []
    location_index = 0
    
    for i, coord in enumerate(coords):
        if location_index < len(locations) and coord.get("text") == locations[location_index]:
            old_x = coord["x"]
            text = coord["text"]
            font = coord["font"]
            size = coord["size"]
            
            # Get ACTUAL width using ReportLab
            text_width = get_text_width(text, font, size)
            new_x = round(TARGET_RIGHT_EDGE - text_width, 2)
            shift = round(new_x - old_x, 2)
            
            location_changes.append({
                "index": i,
                "company": companies[location_index],
                "text": text,
                "old_x": old_x,
                "new_x": new_x,
                "width": text_width,
                "shift": shift
            })
            
            print(f"{location_index + 1:<4} {companies[location_index]:<20} {old_x:<10.2f} {text_width:<10.2f} {new_x:<10.2f} {shift:+10.2f}")
            location_index += 1
    
    print("-" * 90)
    print()
    
    # Calculate new positions for dates
    print("DATES:")
    print("-" * 90)
    print(f"{'#':<4} {'Company':<20} {'Old X':<10} {'Width':<10} {'New X':<10} {'Shift':<10}")
    print("-" * 90)
    
    date_changes = []
    date_index = 0
    
    for i, coord in enumerate(coords):
        if date_index < len(dates) and coord.get("text") == dates[date_index]:
            old_x = coord["x"]
            text = coord["text"]
            font = coord["font"]
            size = coord["size"]
            
            # Get ACTUAL width using ReportLab
            text_width = get_text_width(text, font, size)
            new_x = round(TARGET_RIGHT_EDGE - text_width, 2)
            shift = round(new_x - old_x, 2)
            
            date_changes.append({
                "index": i,
                "company": companies[date_index],
                "text": text,
                "old_x": old_x,
                "new_x": new_x,
                "width": text_width,
                "shift": shift
            })
            
            print(f"{date_index + 1:<4} {companies[date_index]:<20} {old_x:<10.2f} {text_width:<10.2f} {new_x:<10.2f} {shift:+10.2f}")
            date_index += 1
    
    print("-" * 90)
    print()
    
    # Output for copy-paste
    print("=" * 90)
    print("NEW X VALUES FOR COORDINATES.JSON")
    print("=" * 90)
    print()
    print("LOCATIONS:")
    for change in location_changes:
        print(f"{change['company']:<20} X: {change['new_x']}")
    print()
    print("DATES:")
    for change in date_changes:
        print(f"{change['company']:<20} X: {change['new_x']}")
    print()
    
    return location_changes, date_changes

if __name__ == "__main__":
    calculate_precise_positions()
