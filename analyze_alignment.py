"""
Analysis Script: Location and Date Right Edge Positions
========================================================

This script analyzes the coordinates.json file to determine which location 
and date elements extend furthest to the right (X axis).

Purpose: Identify alignment targets for making all locations and dates 
end at the same right edge position.
"""

import json
from pathlib import Path

# Font width estimation (approximate, in points per character at size 1.0)
FONT_WIDTHS = {
    "TrebuchetMS": 0.50,  # Regular
    "TrebuchetMS-Italic": 0.50,  # Italic
    "TrebuchetMS-Bold": 0.55,  # Bold
}

def estimate_text_width(text, font, size):
    """
    Estimate the width of text in points.
    
    Args:
        text: The text string
        font: Font name
        size: Font size in points
        
    Returns:
        Estimated width in points
    """
    base_width = FONT_WIDTHS.get(font, 0.50)
    return len(text) * base_width * size

def analyze_positions():
    """Analyze and report location and date right edge positions."""
    
    # Load coordinates
    data_path = Path(__file__).parent / "data" / "coordinates.json"
    with open(data_path, 'r', encoding='utf-8') as f:
        coords = json.load(f)
    
    # Define the 7 locations and their expected texts
    locations = [
        "Remote, USA",
        "Las Condes, Chile ",
        "Remote, Mexico ",
        "Santiago, Chile ",
        "Remote, USA",  # EPAM (second occurrence)
        "Quilicura, Chile ",
        "Valparaíso, Chile ",
    ]
    
    # Define the 7 dates
    dates = [
        "Since January 2026 ",
        "November 2025 - January 2026",
        "September 2024 - October 2025",
        "February 2024 - September 2024 ",
        "May 2023 - October 2023 ",
        "November 2021 - November 2022 ",
        "January 2020 - November 2021 ",
    ]
    
    print("=" * 80)
    print("LOCATION AND DATE RIGHT EDGE ANALYSIS")
    print("=" * 80)
    print()
    
    # Analyze locations
    print("LOCATIONS:")
    print("-" * 80)
    print(f"{'#':<4} {'Company':<20} {'X Start':<10} {'Text Width':<12} {'X End':<10}")
    print("-" * 80)
    
    location_data = []
    location_index = 0
    companies = ["JOBSITY", "ZENTA GROUP", "DEUNA", "SPOT", "EPAM Systems", "WALMART Chile", "LAMNGEN Ltda."]
    
    for i, coord in enumerate(coords):
        if location_index < len(locations) and coord.get("text") == locations[location_index]:
            x_start = coord["x"]
            text = coord["text"]
            font = coord["font"]
            size = coord["size"]
            
            # Estimate width
            text_width = estimate_text_width(text, font, size)
            x_end = x_start + text_width
            
            location_data.append({
                "company": companies[location_index],
                "x_start": x_start,
                "text": text,
                "width": text_width,
                "x_end": x_end
            })
            
            print(f"{location_index + 1:<4} {companies[location_index]:<20} {x_start:<10.2f} {text_width:<12.2f} {x_end:<10.2f}")
            location_index += 1
    
    print("-" * 80)
    
    # Find furthest right location
    max_loc = max(location_data, key=lambda x: x["x_end"])
    print(f"\n🎯 FURTHEST RIGHT LOCATION: {max_loc['company']} ends at X = {max_loc['x_end']:.2f}")
    print()
    
    # Analyze dates
    print("DATES:")
    print("-" * 80)
    print(f"{'#':<4} {'Company':<20} {'X Start':<10} {'Text Width':<12} {'X End':<10}")
    print("-" * 80)
    
    date_data = []
    date_index = 0
    
    for i, coord in enumerate(coords):
        if date_index < len(dates) and coord.get("text") == dates[date_index]:
            x_start = coord["x"]
            text = coord["text"]
            font = coord["font"]
            size = coord["size"]
            
            # Estimate width
            text_width = estimate_text_width(text, font, size)
            x_end = x_start + text_width
            
            date_data.append({
                "company": companies[date_index],
                "x_start": x_start,
                "text": text,
                "width": text_width,
                "x_end": x_end
            })
            
            print(f"{date_index + 1:<4} {companies[date_index]:<20} {x_start:<10.2f} {text_width:<12.2f} {x_end:<10.2f}")
            date_index += 1
    
    print("-" * 80)
    
    # Find furthest right date
    max_date = max(date_data, key=lambda x: x["x_end"])
    print(f"\n🎯 FURTHEST RIGHT DATE: {max_date['company']} ends at X = {max_date['x_end']:.2f}")
    print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Furthest right LOCATION: {max_loc['company']}")
    print(f"  - Text: \"{max_loc['text']}\"")
    print(f"  - Starts at: X = {max_loc['x_start']:.2f}")
    print(f"  - Ends at: X = {max_loc['x_end']:.2f}")
    print()
    print(f"Furthest right DATE: {max_date['company']}")
    print(f"  - Text: \"{max_date['text']}\"")
    print(f"  - Starts at: X = {max_date['x_start']:.2f}")
    print(f"  - Ends at: X = {max_date['x_end']:.2f}")
    print()
    
    # Overall furthest
    overall_max = max(max_loc["x_end"], max_date["x_end"])
    if max_loc["x_end"] > max_date["x_end"]:
        print(f"🏆 OVERALL FURTHEST RIGHT: LOCATION ({max_loc['company']}) at X = {max_loc['x_end']:.2f}")
    else:
        print(f"🏆 OVERALL FURTHEST RIGHT: DATE ({max_date['company']}) at X = {max_date['x_end']:.2f}")
    
    print()
    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print()
    print(f"To align all locations and dates to the same right edge:")
    print(f"  - Target right edge position: X = {overall_max:.2f}")
    print(f"  - All other elements should be shifted so their right edge aligns to this position")
    print()
    
    return location_data, date_data

if __name__ == "__main__":
    analyze_positions()
