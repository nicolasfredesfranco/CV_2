"""
Calculate New X Positions for Right Edge Alignment at X=590
=============================================================
"""

import json
from pathlib import Path

# Font width estimation (approximate, in points per character at size 1.0)
FONT_WIDTHS = {
    "TrebuchetMS": 0.50,
    "TrebuchetMS-Italic": 0.50,
    "TrebuchetMS-Bold": 0.55,
}

TARGET_RIGHT_EDGE = 590.0

def estimate_text_width(text, font, size):
    """Estimate the width of text in points."""
    base_width = FONT_WIDTHS.get(font, 0.50)
    return len(text) * base_width * size

def calculate_new_positions():
    """Calculate new X positions for all locations and dates."""
    
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
    print(f"NEW X POSITIONS FOR RIGHT EDGE ALIGNMENT AT X = {TARGET_RIGHT_EDGE}")
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
            
            text_width = estimate_text_width(text, font, size)
            new_x = TARGET_RIGHT_EDGE - text_width
            shift = new_x - old_x
            
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
            
            text_width = estimate_text_width(text, font, size)
            new_x = TARGET_RIGHT_EDGE - text_width
            shift = new_x - old_x
            
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
    
    # Summary
    print("=" * 90)
    print("SUMMARY")
    print("=" * 90)
    print(f"Target right edge: X = {TARGET_RIGHT_EDGE}")
    print(f"Locations to modify: {len(location_changes)}")
    print(f"Dates to modify: {len(date_changes)}")
    print(f"Total modifications: {len(location_changes) + len(date_changes)}")
    print()
    
    return location_changes, date_changes

if __name__ == "__main__":
    calculate_new_positions()
