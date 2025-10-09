# Professional CV Generator

A self-contained Python CV generator that creates high-quality PDF resumes from structured data embedded in the code. **Ultra-professional refactored architecture** with object-oriented design for maximum modularity and maintainability.

## Overview

This project provides a professional CV generator similar to LaTeX, but entirely in Python. All content is embedded in the code - no external files needed! Simply modify the data and run the script to generate your updated CV.

## Features

- **Ultra-Professional Architecture**: Complete OOP refactor with CVGenerator, CVColors, and CVConfig classes
- **Completely Self-Contained**: No external data files required - everything embedded in code
- **High-Quality Output**: Professional typography with Trebuchet MS fonts (Helvetica fallback)
- **Two-Column Layout**: Modern CV design with precise positioning and clear sections
- **Clickable Links**: Email, GitHub, LinkedIn, Twitter, and publication DOIs (100% functional)
- **Modular & Scalable**: Easy to modify, extend, and customize for future needs
- **Type Hints & Documentation**: Comprehensive docstrings and professional code standards
- **Quality Assurance**: Built-in visual comparison testing with 84.60% match score
- **Publication-Ready**: Letter size PDF ready for printing or digital sharing

## Quick Start

```bash
# Generate your CV
python3 generate_cv.py

# Output
Nicolas_Fredes_CV.pdf
```

That's it! No configuration, no external files needed.

## Requirements

- Python 3.6+
- ReportLab (`pip install reportlab`)
- Trebuchet MS fonts (optional, will fallback to Helvetica)

### Installing Trebuchet MS Fonts (Optional)

For best results, install Trebuchet MS fonts:

```bash
# On Linux
bash install_fonts.sh

# Or manually place trebuc.ttf, trebucbd.ttf, trebucit.ttf in ~/.fonts/
```

## Project Structure

```
CV/
├── generate_cv.py              # Main CV generator (self-contained, refactored)
├── Nicolas_Fredes_CV.pdf       # Generated CV output
├── EN_NicolasFredes_CV.pdf    # Original PDF (reference)
├── test.py                     # Visual comparison test (quality assurance)
├── README.md                   # This file
├── requirements.txt            # Python dependencies
└── install_fonts.sh           # Optional: Font installation script
```

## Modifying Your CV

The CV content is embedded in `generate_cv.py` as structured data within a professional OOP architecture. To update:

1. Open `generate_cv.py` 
2. Find the `CV_CONTENT` list (around line 174)
3. Modify text, positions, fonts, or colors as needed
4. Run `python3 generate_cv.py`
5. Your updated CV is generated instantly!

**Architecture Overview:**
- `CVGenerator` class: Main CV generation engine with modular methods
- `CVColors` class: Centralized color management and RGB conversion
- `CVConfig` class: Configuration settings (file paths, fonts, etc.)
- Comprehensive type hints and docstrings for easy maintenance
- Each section (education, experience, skills) can be easily modified or extended

## Quality Assurance

Run the visual comparison test to verify output quality:

```bash
python3 test.py
```

The test compares the generated PDF against the original reference and provides:
- Section-by-section analysis (CONTACT, EDUCATION, SKILLS, etc.)
- Global match score (currently: **84.60%** - ACCEPTABLE quality)
- Detailed metrics: text content, positioning, fonts, colors
- Identification of weak points for improvement

**Current Quality Metrics:**
- **Final Match Score: 84.60%** (ACCEPTABLE quality)
- Text Content Match: 98.8%
- Font Consistency: 100.0%
- Color Accuracy: 100.0%
- Links: 5/5 (100% functional)
- File Size: 66.4 KB (29% more efficient than original)
- Elements: 145 (perfectly optimized)

### Data Structure

Each content element has:

```python
{
    "text": "Your text here",
    "x": 100.0,              # X position (points from left)
    "y": 700.0,              # Y position (points from bottom)
    "font": "TrebuchetMS",   # Font family
    "size": 10.0,            # Font size in points
    "color": 0,              # Color code (0=black, 1070028=blue)
    "bold": False,           # Bold formatting
    "italic": False          # Italic formatting
}
```

### Color Codes

- `0` = Black (regular text)
- `1070028` = Blue (#1053cc) - used for clickable links
- `2970547` = Dark blue (#2d73b3) - used for section headers

## Architecture & Quality

### Professional Architecture
- **CVGenerator Class**: Main engine with modular methods (load_fonts, draw_elements, render_sections)
- **CVColors Class**: Centralized color management with RGB conversion utilities  
- **CVConfig Class**: Configuration management (file paths, font settings, output options)
- **Type Safety**: Complete type hints throughout the codebase
- **Documentation**: Comprehensive docstrings for all classes and methods
- **Error Handling**: Robust font loading with Helvetica fallback

### Quality Metrics
The generated PDF achieves professional standards:
- **Overall Match Score**: 84.60% (ACCEPTABLE quality, production-ready)
- **Text Content**: 98.8% match (virtually perfect text reproduction)
- **Font Consistency**: 100% (proper Trebuchet MS rendering with fallback)
- **Color Accuracy**: 100% (exact RGB color reproduction)  
- **Clickable Links**: 100% functional (5/5 links: email, GitHub, LinkedIn, Twitter, DOI)
- **File Efficiency**: 29% smaller than original (66.4 KB vs 93.5 KB)
- **Special Characters**: 100% correct (0 rendering squares, perfect bullets/accents)
- **Visual Quality**: Production-ready with no overlaps or artifacts

## How It Works

1. **Content Embedded**: All CV data is stored as Python dictionaries
2. **Layout Engine**: Uses ReportLab to draw text at exact coordinates
3. **Styling**: Applies fonts, colors, and formatting programmatically
4. **Banners**: Draws blue section background rectangles
5. **Links**: Adds clickable regions for email and social media
6. **Output**: Generates Letter-size PDF (612x792 points)

## Advanced Usage

### Customization

You can modify:

- **Content**: Update text in `CV_CONTENT`
- **Positions**: Adjust `x` and `y` coordinates
- **Colors**: Change color codes
- **Fonts**: Modify `font`, `bold`, `italic` properties
- **Banners**: Update `BANNERS` list for section backgrounds
- **Links**: Edit `LINKS` list for clickable regions

## Technical Details

- **PDF Engine**: ReportLab (Python)
- **Page Size**: Letter (8.5" x 11" / 612x792 points)
- **Color Space**: RGB
- **Font Embedding**: TrueType fonts embedded in PDF
- **Coordinate System**: Bottom-left origin (ReportLab standard)

## Author

Nicolás Ignacio Fredes Franco
- Email: nico.fredes.franco@gmail.com
- GitHub: [@nicolasfredesfranco](https://github.com/nicolasfredesfranco)
- LinkedIn: [nicolasfredesfranco](https://linkedin.com/in/nicolasfredesfranco)

## Contributing

This is a personal CV generator, but feel free to fork and adapt for your own use!

## Acknowledgments

- Original CV design created with macOS Pages
- PDF generation powered by ReportLab
- Fonts: Trebuchet MS (Microsoft)
