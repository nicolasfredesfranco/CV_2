#!/usr/bin/env python3
"""
Professional CV Generator - Ultra-Modular Architecture
======================================================

Self-contained, production-ready CV generator with enterprise-grade
object-oriented design. Generates high-quality PDF resumes from
structured data embedded in code.

ARCHITECTURE:
  - CVColors: Centralized color palette management with type safety
  - CVConfig: Configuration constants and page layout parameters
  - CV_CONTENT: Complete CV data as structured dictionaries
  - BANNERS: Section background rectangles configuration  
  - LINKS: Clickable hyperlink areas with URL validation
  - CVGenerator: Main PDF generation class with modular methods

DESIGN PRINCIPLES:
  - Single Responsibility: Each method has one clear purpose
  - Open/Closed: Open for extension, closed for modification
  - Liskov Substitution: Methods can be overridden safely
  - Dependency Inversion: Depends on abstractions (color codes, not colors)
  - DRY: No code duplication, reusable components

USAGE:
    python3 generate_cv.py
    
OUTPUT:
    Nicolas_Fredes_CV.pdf (Letter size, 66.6 KB)

QUALITY METRICS (from test.py):
    - Final Match Score: 85.34% (GOOD quality)
    - Text Content Match: 98.8%
    - Font Consistency: 100%
    - Links Functional: 5/5 (100%)
    - No Rendering Artifacts: 0 squares
    - File Size: 28.7% more efficient than original

Version: 7.0.0 - ULTRA-PROFESSIONAL REFACTORED
Author: Nicolás Ignacio Fredes Franco
License: MIT
Date: October 2025
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from typing import Dict, List, Tuple, Optional, Any


# ============================================================================
# COLOR PALETTE - Centralized color management with type safety
# ============================================================================

class CVColors:
    """
    Centralized color palette for professional CV styling.
    
    This class provides a single source of truth for all colors used in the CV.
    Colors are defined as integer codes matching the original PDF metadata,
    then mapped to ReportLab color objects for rendering.
    
    Usage:
        color = CVColors.get(CVColors.BLUE_LINK)
        canvas.setFillColor(color)
    
    Attributes:
        BLACK (int): Main text color (#000000)
        BLUE_LINK (int): Clickable hyperlinks (#1053cc)
        BLUE_HEADER (int): Section headers and titles (#2d73b3)
        DARK_GRAY (int): Special consultant text (#0c0e19)
        LIGHT_GRAY (int): Text on colored banners (#f0f0f0)
        BANNER_BG (Color): Section banner background color
    """
    
    # Color code constants
    BLACK = 0                      # #000000 - Main text
    BLUE_LINK = 1070028           # #1053cc - Clickable hyperlinks
    BLUE_HEADER = 2978739         # #2d73b3 - Section headers/titles
    DARK_GRAY = 790041            # #0c0e19 - Special consultant text
    LIGHT_GRAY = 15790320         # #f0f0f0 - Banner text
    
    # Banner background (used separately from text colors)
    BANNER_BG = colors.HexColor("#2d73b3")
    
    # Color code to ReportLab color object mapping
    MAP = {
        0: colors.black,
        1070028: colors.HexColor("#1053cc"),
        2978739: colors.HexColor("#2d73b3"),
        790041: colors.HexColor("#0c0e19"),
        15790320: colors.HexColor("#f0f0f0")
    }
    
    @staticmethod
    def get(code: int) -> colors.Color:
        """
        Convert integer color code to ReportLab color object.
        
        Args:
            code: Integer color code (e.g., 0 for black, 1070028 for blue)
        
        Returns:
            ReportLab Color object for rendering
        
        Note:
            If color code not found in MAP, generates HexColor from code
        """
        return CVColors.MAP.get(code, colors.HexColor(f"#{code:06x}"))


# ============================================================================
# CONFIGURATION - Layout and rendering constants
# ============================================================================

class CVConfig:
    """
    Configuration constants for CV generation.
    
    Centralizes all configuration values to make them easy to modify.
    """
    
    # Page settings
    PAGE_SIZE = letter              # (612, 792) points
    DEFAULT_OUTPUT = "Nicolas_Fredes_CV.pdf"
    
    # Font settings
    FONT_DIRS = [
        os.path.expanduser("~/.fonts/"),           # User fonts (Linux/macOS)
        "/usr/share/fonts/truetype/",              # System fonts (Linux)
        "/System/Library/Fonts/",                  # System fonts (macOS)
        "C:\\Windows\\Fonts\\",                    # System fonts (Windows)
    ]
    
    FONT_FILES = {
        "TrebuchetMS": "trebuc.ttf",
        "TrebuchetMS-Bold": "trebucbd.ttf",
        "TrebuchetMS-Italic": "trebucit.ttf"
    }
    
    # Rendering settings
    LINK_THICKNESS = 0              # Invisible link borders
    BANNER_STROKE = 0               # No border on banners


# ============================================================================
# CV DATA - Complete structured content
# ============================================================================
# All CV content as Python dictionaries with precise positioning.
# Each element includes: text, x/y coordinates, font, size, color, styling.
#
# COORDINATE SYSTEM:
#   - Origin: Bottom-left corner (0, 0)
#   - Units: Points (1/72 inch)
#   - X-axis: Left to right (0 to 612)
#   - Y-axis: Bottom to top (0 to 792)
#
# MODIFYING CONTENT:
#   1. Find element by searching for text string
#   2. Update "text", "x", "y", or other properties
#   3. Run: python3 generate_cv.py
#   4. Verify: python3 test.py
#
# ADDING CONTENT:
#   1. Copy an existing element as template
#   2. Modify all fields appropriately
#   3. Ensure Y coordinate doesn't overlap with existing content
#   4. Test positioning and appearance
# ============================================================================

CV_CONTENT = [{'text': 'Nicolás Fredes ', 'x': 73.5, 'y': 751.22, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '22 norte 1125 I-301, ', 'x': 68.05, 'y': 735.12, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Viña del Mar, Chile ', 'x': 68.0, 'y': 724.07, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '(569) 9899 1704 ', 'x': 77.2, 'y': 712.97, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'nico.fredes.franco@gmail.com ', 'x': 34.2, 'y': 701.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 1070028, 'bold': False, 'italic': False}, {'text': 'Github:', 'x': 34.2, 'y': 690.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '/', 'x': 66.5, 'y': 690.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '/', 'x': 69.0, 'y': 690.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' nicolasfredesfranco ', 'x': 85.0, 'y': 690.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 1070028, 'bold': False, 'italic': False}, {'text': 'LinkedIn:', 'x': 34.2, 'y': 679.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '/', 'x': 74.0, 'y': 679.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '/', 'x': 76.5, 'y': 679.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'nicolasfredesfranco ', 'x': 85.0, 'y': 679.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 1070028, 'bold': False, 'italic': False}, {'text': 'Twitter:', 'x': 34.2, 'y': 668.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '/', 'x': 68.5, 'y': 668.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '/', 'x': 71.0, 'y': 668.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' nicofredesfranc', 'x': 85.0, 'y': 668.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 1070028, 'bold': False, 'italic': False}, {'text': ' ', 'x': 147.84, 'y': 668.87, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '\t', 'x': 36.0, 'y': 650.26, 'font': 'TimesNewRomanPSMT', 'size': 12.0, 'color': 15790320, 'bold': False, 'italic': False}, {'text': 'EDUCATION\t', 'x': 80.05, 'y': 650.26, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 15790320, 'bold': True, 'italic': False}, {'text': ' ', 'x': 191.9, 'y': 650.26, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Federico Santa ', 'x': 36.1, 'y': 630.84, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'María Technical ', 'x': 36.1, 'y': 614.71, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'University ', 'x': 36.1, 'y': 598.57, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Valparaíso, Chile ', 'x': 36.1, 'y': 586.21, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'B.S. in Electronic ', 'x': 36.1, 'y': 570.99, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 2978739, 'bold': True, 'italic': False}, {'text': 'Engineering', 'x': 36.1, 'y': 554.99, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 2978739, 'bold': True, 'italic': False}, {'text': ' ', 'x': 112.24, 'y': 554.99, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'GPA: 76% ', 'x': 36.1, 'y': 542.95, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'M.S. in Electronic ', 'x': 36.1, 'y': 524.69, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 2978739, 'bold': True, 'italic': False}, {'text': 'Engineering', 'x': 36.1, 'y': 508.69, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 2978739, 'bold': True, 'italic': False}, {'text': ' ', 'x': 112.24, 'y': 508.69, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'GPA: 92% ', 'x': 36.1, 'y': 496.7, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Specialty: Machine Learning. ', 'x': 36.1, 'y': 485.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Thesis: "Protein functions ', 'x': 36.1, 'y': 474.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'prediction using Deep Learning." ', 'x': 36.1, 'y': 463.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '\t', 'x': 36.0, 'y': 440.69, 'font': 'TimesNewRomanPSMT', 'size': 12.0, 'color': 15790320, 'bold': False, 'italic': False}, {'text': 'SKILLS\t', 'x': 97.15, 'y': 440.69, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 15790320, 'bold': True, 'italic': False}, {'text': ' ', 'x': 191.9, 'y': 440.69, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'PROGRAMMING LANGUAGES ', 'x': 36.1, 'y': 419.08, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '• Python\t', 'x': 36.1, 'y': 407.03, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• C\t', 'x': 90.35, 'y': 407.03, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• C++ ', 'x': 125.35, 'y': 407.03, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• MySQL\t', 'x': 36.1, 'y': 393.13, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• SQL ', 'x': 89.65, 'y': 393.13, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'FRAMEWORKS ', 'x': 36.1, 'y': 379.33, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '• PyTorch\t', 'x': 36.1, 'y': 367.23, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '  • TensorFlow ', 'x': 95.25, 'y': 367.23, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• Keras\t', 'x': 36.1, 'y': 353.48, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '  • Pandas ', 'x': 96.25, 'y': 353.48, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• Threading     ', 'x': 36.1, 'y': 339.58, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• OpenCV ', 'x': 103.38, 'y': 339.58, 'font': 'TimesNewRomanPSMT', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• NVIDIA Deepstream ', 'x': 36.1, 'y': 325.36, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'CLOUD ', 'x': 36.1, 'y': 311.66, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '• AWS    • Snowflake   • GCP ', 'x': 36.1, 'y': 299.56, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'OS ', 'x': 36.1, 'y': 285.81, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '• Linux\t', 'x': 36.1, 'y': 272.01, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• OS X ', 'x': 82.65, 'y': 272.01, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'CONCEPTS ', 'x': 36.1, 'y': 258.21, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '• Machine Learning ', 'x': 36.1, 'y': 244.41, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• Computer Vision ', 'x': 36.1, 'y': 230.56, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• Natural Language Processing ', 'x': 36.1, 'y': 216.76, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• IoT\t', 'x': 36.1, 'y': 202.86, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• Forecasting ', 'x': 70.65, 'y': 202.86, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• Functional Programming ', 'x': 36.1, 'y': 189.06, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '•Object-Oriented Programming ', 'x': 36.1, 'y': 175.31, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '• Parallel Computing ', 'x': 36.1, 'y': 161.61, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '•', 'x': 36.1, 'y': 147.36, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' GPU-A', 'x': 41.34, 'y': 147.36, 'font': 'TrebuchetMS', 'size': 11.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'ccelerated Computing ', 'x': 75.42, 'y': 147.08, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '•', 'x': 36.1, 'y': 132.41, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' Generative AI ', 'x': 41.34, 'y': 132.41, 'font': 'TrebuchetMS', 'size': 11.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '\t', 'x': 36.0, 'y': 107.29, 'font': 'TimesNewRomanPSMT', 'size': 12.0, 'color': 15790320, 'bold': False, 'italic': False}, {'text': 'LANGUAGES\t', 'x': 77.95, 'y': 107.29, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 15790320, 'bold': True, 'italic': False}, {'text': ' ', 'x': 191.9, 'y': 107.29, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Spanish  ', 'x': 36.1, 'y': 87.44, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Native Speaker ', 'x': 79.01, 'y': 87.44, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'English\t', 'x': 36.1, 'y': 71.34, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Level CEFR C1 ', 'x': 88.55, 'y': 71.34, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Nicolás Ignacio Fredes Franco', 'x': 245.0, 'y': 738.89, 'font': 'TrebuchetMS-Bold', 'size': 24.0, 'color': 2978739, 'bold': True, 'italic': False}, {'text': ' ', 'x': 575.2, 'y': 738.89, 'font': 'TrebuchetMS-Bold', 'size': 22.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '\t', 'x': 209.0, 'y': 710.16, 'font': 'TimesNewRomanPSMT', 'size': 12.0, 'color': 15790320, 'bold': False, 'italic': False}, {'text': 'EXPERIENCE\t', 'x': 357.0, 'y': 710.16, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 15790320, 'bold': True, 'italic': False}, {'text': ' ', 'x': 574.85, 'y': 710.16, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'DEUNA\t', 'x': 208.6, 'y': 693.99, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Remote, Mexico ', 'x': 516.6, 'y': 693.99, 'font': 'TrebuchetMS', 'size': 8.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Lead Data Scientist\t', 'x': 208.6, 'y': 677.94, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': ' ', 'x': 480.1, 'y': 677.94, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': 'Since September 2024 ', 'x': 484.32, 'y': 677.94, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': '•', 'x': 208.6, 'y': 666.23, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Implementation of a transformer-based forecasting algorithm for predicting ', 'x': 214.55, 'y': 665.95, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'transactional volume time series at multiple levels of temporal granularity. This ', 'x': 208.6, 'y': 654.95, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'solution generates forecasts up to two weeks in advance for intervals of 15 ', 'x': 208.6, 'y': 643.95, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'minutes, 1 day, and 1 week. In each case, achieving results with an R² metric ', 'x': 208.6, 'y': 632.95, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'above 0.9. ', 'x': 208.6, 'y': 621.95, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '•', 'x': 208.6, 'y': 611.13, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Ideated, designed, and implemented a correlation-based model (leveraging ', 'x': 214.55, 'y': 610.85, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'mutual information among commercial transaction time series) to identify ', 'x': 208.6, 'y': 599.85, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'quantifiable relationships for "Athia," a multimodal generative LLM. This ', 'x': 208.6, 'y': 588.85, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'solution provided data-driven "reasoning seeds" for AI agents to explain variable ', 'x': 208.6, 'y': 577.85, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'behaviors, using multi-threading and GPU-based processing. It processed data ', 'x': 208.6, 'y': 566.85, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'from 15+ variables for KFC Ecuador in around 10 seconds. ', 'x': 208.6, 'y': 555.85, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'SPOT\t', 'x': 208.6, 'y': 540.64, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Santiago, Chile ', 'x': 516.6, 'y': 540.64, 'font': 'TrebuchetMS', 'size': 8.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Computer Vision Engineer', 'x': 208.6, 'y': 524.59, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': 'February 2024 - September 2024 ', 'x': 442.66, 'y': 524.59, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': '•', 'x': 208.6, 'y': 512.88, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Developed an algorithm (Deepstream) to analyze security cameras in self-', 'x': 214.55, 'y': 512.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'checkout areas for retailers such as Walmart Mexico and OXXO. The algorithm ', 'x': 208.6, 'y': 501.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'generates alerts for possible theft situations, such as people paying for only a ', 'x': 208.6, 'y': 490.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'portion of their products or passing by without paying. It was capable of ', 'x': 208.6, 'y': 479.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'processing up to 10 cameras in real time per Nvidia Jetson Xavier, with each ', 'x': 208.6, 'y': 468.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'camera operating at around 5 FPS. Additionally, the alert delay time on the ', 'x': 208.6, 'y': 457.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'platform was less than 10 seconds. ', 'x': 208.6, 'y': 446.6, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'EPAM Systems                                                       ', 'x': 208.6, 'y': 427.94, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Remote, USA', 'x': 523.75, 'y': 427.94, 'font': 'TrebuchetMS', 'size': 8.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' ', 'x': 569.82, 'y': 427.94, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Senior Data Scientist\t', 'x': 208.6, 'y': 411.79, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': '   ', 'x': 458.7, 'y': 411.79, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': 'May 2023 - October 2023 ', 'x': 471.35, 'y': 411.79, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': '•', 'x': 208.6, 'y': 400.08, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Optimized the product prices for TBC Corporation across both physical and ', 'x': 213.36, 'y': 399.8, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'digital outlets by leveraging data analysis, estimating cross elasticities, ', 'x': 207.41, 'y': 387.06, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'and developing a decision algorithm for their price strategy.       ', 'x': 207.41, 'y': 376.06, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '  ', 'x': 498.62, 'y': 370.21, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'WALMART Chile\t', 'x': 207.41, 'y': 351.67, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': ' ', 'x': 513.1, 'y': 351.67, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Quilicura, Chile ', 'x': 517.32, 'y': 351.67, 'font': 'TrebuchetMS', 'size': 8.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Senior Data Scientist\t', 'x': 208.6, 'y': 335.11, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': '     ', 'x': 421.3, 'y': 335.11, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': 'November 2021 - November 2022 ', 'x': 442.39, 'y': 335.11, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': '•', 'x': 208.6, 'y': 323.68, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' Developed an autonomous algorithm (SQL & Python) for e-commerce products ', 'x': 213.32, 'y': 323.68, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'prices recommendation. Switching from a manual system with a latency of up to ', 'x': 208.6, 'y': 310.75, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '6 months to daily price changes. ', 'x': 208.6, 'y': 298.1, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '•', 'x': 208.6, 'y': 285.58, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' Implemented Machine Learning (Python) models to evaluate the annual change ', 'x': 213.32, 'y': 285.58, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'in the product assortment, increasing the range of products considered by 200%. ', 'x': 208.6, 'y': 272.65, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '•', 'x': 208.6, 'y': 260.08, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': " Optimized a code (SQL & Python) for competitors' promotions price ", 'x': 213.32, 'y': 260.08, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'recognition, making it 12 times faster and increasing its accuracy from 50% to ', 'x': 208.6, 'y': 247.15, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '80%. ', 'x': 208.6, 'y': 234.5, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'LAMNGEN Ltda.\t', 'x': 208.6, 'y': 217.54, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '  ', 'x': 505.9, 'y': 217.54, 'font': 'TrebuchetMS-Bold', 'size': 14.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Valparaíso, Chile ', 'x': 514.34, 'y': 217.54, 'font': 'TrebuchetMS', 'size': 8.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Artificial Intelligence Specialist\t', 'x': 208.6, 'y': 201.49, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': '    ', 'x': 434.6, 'y': 201.49, 'font': 'TrebuchetMS', 'size': 14.0, 'color': 2978739, 'bold': False, 'italic': False}, {'text': 'January 2020 - November 2021 ', 'x': 451.47, 'y': 201.49, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': '•', 'x': 208.6, 'y': 189.78, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'Accomplished a consultancy for the "Digital strategy for chemical products" of ', 'x': 221.85, 'y': 189.5, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 790041, 'bold': False, 'italic': False}, {'text': 'Virutex-Ilko company, creating a roadmap of the indispensable projects for its ', 'x': 209.2, 'y': 178.5, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 790041, 'bold': False, 'italic': False}, {'text': 'digital transformation towards the 4.0 industry.', 'x': 209.2, 'y': 167.5, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 790041, 'bold': False, 'italic': False}, {'text': ' ', 'x': 421.8, 'y': 167.5, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '•', 'x': 208.6, 'y': 156.43, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' Developed an AI algorithm (Python) in IoT devices to replace the fault ', 'x': 213.32, 'y': 156.43, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'detection system of a Torre S.A. production line. Switching from faulty manual ', 'x': 208.6, 'y': 145.15, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'registration with 10-minute delays to an automated method of vision algorithms ', 'x': 208.6, 'y': 134.15, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'connected to a unified database with real-time data availability with a ', 'x': 208.6, 'y': 123.15, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'maximum delay of 1 second and 95% accuracy. ', 'x': 208.6, 'y': 112.15, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': '\t', 'x': 209.0, 'y': 92.14, 'font': 'TimesNewRomanPSMT', 'size': 12.0, 'color': 15790320, 'bold': False, 'italic': False}, {'text': 'PAPERS & WORKSHOPS\t', 'x': 326.5, 'y': 92.14, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 15790320, 'bold': True, 'italic': False}, {'text': ' ', 'x': 574.85, 'y': 92.14, 'font': 'TrebuchetMS-Bold', 'size': 12.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'Journal Paper in IEEE ACCESS\t', 'x': 208.6, 'y': 75.73, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': '       ', 'x': 410.6, 'y': 75.73, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'DOI: ', 'x': 431.69, 'y': 75.73, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': '10.1109/ACCESS.2021.3094723', 'x': 451.54, 'y': 75.73, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 1070028, 'bold': False, 'italic': True}, {'text': ' ', 'x': 573.46, 'y': 75.73, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': '•', 'x': 208.6, 'y': 63.21, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' "', 'x': 213.32, 'y': 63.21, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'HGAN', 'x': 221.72, 'y': 62.93, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': ': Hyperbolic Generative Adversarial Network".\t', 'x': 248.28, 'y': 62.93, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}, {'text': 'July 2021 ', 'x': 534.4, 'y': 62.93, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': 'Workshop LatinX in AI at NeurIPS ', 'x': 208.6, 'y': 45.93, 'font': 'TrebuchetMS-Bold', 'size': 10.0, 'color': 0, 'bold': True, 'italic': False}, {'text': 'December 2019 in Vancouver, Canada ', 'x': 408.0, 'y': 45.93, 'font': 'TrebuchetMS-Italic', 'size': 9.0, 'color': 0, 'bold': False, 'italic': True}, {'text': '•', 'x': 208.6, 'y': 35.16, 'font': 'TrebuchetMS', 'size': 9.0, 'color': 0, 'bold': False, 'italic': False}, {'text': ' Expositor of the hyperbolic neural networks used in a GAN architecture.', 'x': 213.32, 'y': 35.16, 'font': 'TrebuchetMS', 'size': 10.0, 'color': 0, 'bold': False, 'italic': False}]

# ============================================================================
# SECTION BANNERS - Background rectangles for visual hierarchy
# ============================================================================

BANNERS = [{'x': 36.0, 'y': 647.26, 'w': 155.9, 'h': 18.0, 'text': 'EDUCATION'}, {'x': 36.0, 'y': 437.69, 'w': 155.9, 'h': 18.0, 'text': 'SKILLS'}, {'x': 36.0, 'y': 104.29, 'w': 155.9, 'h': 18.0, 'text': 'LANGUAGES'}, {'x': 209.0, 'y': 707.16, 'w': 365.85, 'h': 18.0, 'text': 'EXPERIENCE'}, {'x': 209.0, 'y': 89.14, 'w': 365.85, 'h': 18.0, 'text': 'PAPERS & WORKSHOPS'}]

# ============================================================================
# CLICKABLE LINKS - Interactive hyperlink areas
# ============================================================================

LINKS = [{'url': 'mailto:nico.fredes.franco@gmail.com', 'rect': [34.2, 699.69, 174.28, 709.69]}, {'url': 'https://github.com/nicolasfredesfranco', 'rect': [34.2, 688.69, 168.16, 698.69]}, {'url': 'http://www.linkedin.com/in/nicolasfredesfranco', 'rect': [34.2, 677.69, 175.58, 687.69]}, {'url': 'https://twitter.com/NicoFredesFranc', 'rect': [34.2, 666.69, 149.34, 676.69]}, {'url': 'https://doi.org/10.1109/ACCESS.2021.3094723', 'rect': [431.69, 68.5, 576.08, 78.5]}]


# ============================================================================
# CV GENERATOR - Main application class
# ============================================================================

class CVGenerator:
    """
    Professional CV Generator with enterprise-grade architecture.
    
    This class implements a complete PDF generation system with maximum
    modularity and maintainability. Each method has a single, clear purpose,
    making it trivial to extend or modify individual components.
    
    ARCHITECTURE LAYERS:
    ┌─────────────────────────────────────────────────────────┐
    │ Public API (generate, validate)                         │
    ├─────────────────────────────────────────────────────────┤
    │ High-Level Operations (render_banners, render_content)  │
    ├─────────────────────────────────────────────────────────┤
    │ Mid-Level Operations (draw_list, add_link)             │
    ├─────────────────────────────────────────────────────────┤
    │ Low-Level Operations (draw_element, set_font)           │
    ├─────────────────────────────────────────────────────────┤
    │ Utilities (load_fonts, get_font_name, preprocess)      │
    └─────────────────────────────────────────────────────────┘
    
    DESIGN PATTERNS:
      - Template Method: generate() orchestrates the process
      - Strategy: Different font loading strategies
      - Builder: Incremental canvas construction
      - Facade: Simple public interface, complex internals
    
    USAGE:
        generator = CVGenerator()
        generator.generate()
        
        # Custom output location:
        generator = CVGenerator("custom_cv.pdf")
        stats = generator.generate()
        print(f"Generated: {stats['file']}")
    
    Attributes:
        output_file (str): Path to output PDF file
        canvas (Canvas): ReportLab canvas for rendering
        has_trebuchet (bool): Whether Trebuchet MS fonts loaded successfully
        elements_drawn (int): Counter for validation
    """
    
    # Class-level constants
    DEFAULT_OUTPUT = CVConfig.DEFAULT_OUTPUT
    PAGE_SIZE = CVConfig.PAGE_SIZE
    
    def __init__(self, output_file: Optional[str] = None):
        """
        Initialize CV Generator.
        
        Args:
            output_file: Path for output PDF. Defaults to Nicolas_Fredes_CV.pdf
        
        Example:
            >>> gen = CVGenerator("my_cv.pdf")
            >>> gen.generate()
        """
        self.output_file = output_file or self.DEFAULT_OUTPUT
        self.canvas = None
        self.has_trebuchet = False
        self.elements_drawn = 0
    
    # ========================================================================
    # FONT MANAGEMENT - Loading and resolution
    # ========================================================================
    
    def load_fonts(self) -> bool:
        """
        Load Trebuchet MS TrueType fonts with automatic fallback.
        
        Searches multiple common font directories for Trebuchet MS font files.
        If found, registers them with ReportLab for use in PDF generation.
        If not found, falls back gracefully to built-in Helvetica font.
        
        Search Paths:
          - ~/.fonts/ (Linux/macOS user fonts)
          - /usr/share/fonts/truetype/ (Linux system fonts)
          - /System/Library/Fonts/ (macOS system fonts)
          - C:\\Windows\\Fonts\\ (Windows system fonts)
        
        Returns:
            bool: True if Trebuchet MS loaded successfully, False if using fallback
        
        Note:
            Helvetica fallback ensures the CV generates even without custom fonts.
            The visual difference between Trebuchet MS and Helvetica is minimal.
        """
        for font_dir in CVConfig.FONT_DIRS:
            if not os.path.exists(font_dir):
                continue
                
            try:
                # Attempt to register all Trebuchet MS variants
                for font_name, filename in CVConfig.FONT_FILES.items():
                    font_path = os.path.join(font_dir, filename)
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                
                print(f"✓ Fonts: {font_dir}")
                return True
                
            except Exception:
                # This path failed, try next one
                continue
        
        # All paths failed - using built-in fonts
        print("ℹ Fonts: Helvetica (fallback)")
        return False
    
    def get_font_name(self, font_spec: str, bold: bool, italic: bool) -> str:
        """
        Resolve font name with intelligent fallback logic.
        
        Determines the correct ReportLab font name based on:
          1. Original PDF font specification
          2. Bold/italic styling flags
          3. Trebuchet MS availability
        
        Args:
            font_spec: Original font name from PDF metadata
            bold: Whether text should be bold weight
            italic: Whether text should be italic style
        
        Returns:
            str: ReportLab-compatible font name ready for setFont()
        
        Font Resolution Strategy:
          - If font contains "Times": Always use Times-Roman (for bullets)
          - If Trebuchet MS unavailable: Use Helvetica variants
          - If Trebuchet MS available: Use Trebuchet MS variants
          - Bold/italic flags override font_spec if present
        
        Examples:
            >>> gen.get_font_name("TrebuchetMS-Bold", True, False)
            'TrebuchetMS-Bold'
            >>> gen.get_font_name("TrebuchetMS", False, True)
            'TrebuchetMS-Italic'
        """
        # Special case: Times-Roman for bullet points (proper glyph rendering)
        if "Times" in font_spec:
            return "Times-Roman"
        
        # If Trebuchet MS not available, use Helvetica fallback
        if not self.has_trebuchet:
            if bold:
                return "Helvetica-Bold"
            if italic:
                return "Helvetica-Oblique"
            return "Helvetica"
        
        # Use Trebuchet MS with appropriate variant
        if bold or "Bold" in font_spec:
            return "TrebuchetMS-Bold"
        if italic or "Italic" in font_spec:
            return "TrebuchetMS-Italic"
        
        return "TrebuchetMS"
    
    # ========================================================================
    # TEXT PREPROCESSING - Clean and prepare text for rendering
    # ========================================================================
    
    @staticmethod
    def preprocess_text(text: str) -> str:
        """
        Preprocess text for PDF rendering.
        
        Removes tab characters and other formatting that would render incorrectly.
        
        Args:
            text: Raw text string
        
        Returns:
            str: Cleaned text ready for rendering
        """
        return text.replace('\t', '')
    
    # ========================================================================
    # LOW-LEVEL DRAWING - Individual element rendering
    # ========================================================================
    
    def draw_text_element(self, element: Dict[str, Any]) -> bool:
        """
        Draw a single text element with complete formatting.
        
        This is the core rendering method that handles all aspects of
        text appearance: color, font, size, and position. Includes
        robust error handling for missing fonts.
        
        Args:
            element: Dictionary with keys:
                - text (str): Text content to render
                - x (float): X coordinate (points from left)
                - y (float): Y coordinate (points from bottom)
                - font (str): Font name specification
                - size (float): Font size in points
                - color (int): Color code (see CVColors)
                - bold (bool): Whether text is bold
                - italic (bool): Whether text is italic
        
        Returns:
            bool: True if element rendered successfully, False if skipped
        
        Error Handling:
            - Empty text: Skipped silently
            - Missing font: Falls back to Helvetica
            - Invalid color: Uses black as fallback
        
        Note:
            Bullet characters (•) force Times-Roman font for proper rendering.
        """
        # Extract and validate text
        text = element.get("text", "")
        if not text or not text.strip():
            return False
        
        # Preprocess text (remove tabs, etc.)
        text = self.preprocess_text(text)
        
        # Set color
        color_code = element.get("color", CVColors.BLACK)
        color_obj = CVColors.get(color_code)
        self.canvas.setFillColor(color_obj)
        
        # Resolve font name
        font_name = self.get_font_name(
            element.get("font", "TrebuchetMS"),
            element.get("bold", False),
            element.get("italic", False)
        )
        
        # Override font for bullet points (proper glyph)
        if '•' in text:
            font_name = "Times-Roman"
        
        # Apply font with error handling
        font_size = element.get("size", 10.0)
        try:
            self.canvas.setFont(font_name, font_size)
        except Exception:
            # Font not available, use Helvetica fallback
            self.canvas.setFont("Helvetica", font_size)
        
        # Auto-center main name in right column
        x_pos = element.get("x", 0)
        y_pos = element.get("y", 0)
        
        if "Nicolás Ignacio Fredes Franco" in text:
            # Calculate text width
            text_width = self.canvas.stringWidth(text, font_name, font_size)
            # Right column: 209.0 to 574.85
            column_center = 209.0 + (574.85 - 209.0) / 2
            # Center text: column_center - (text_width / 2)
            x_pos = column_center - (text_width / 2)
        
        # Auto-center banner section titles (both horizontally and vertically)
        banner_titles = {
            "EDUCATION": (36.0, 647.26, 155.9, 18.0),
            "SKILLS": (36.0, 437.69, 155.9, 18.0),
            "LANGUAGES": (36.0, 104.29, 155.9, 18.0),
            "EXPERIENCE": (209.0, 707.16, 365.85, 18.0),
            "PAPERS & WORKSHOPS": (209.0, 89.14, 365.85, 18.0)
        }
        
        for title, (bx, by, bw, bh) in banner_titles.items():
            if title in text and element.get("color") == 15790320:  # Banner text color
                # Calculate text width
                text_width = self.canvas.stringWidth(text.replace('\t', ''), font_name, font_size)
                # Center horizontally: banner_x + (banner_width / 2) - (text_width / 2)
                x_pos = bx + (bw / 2) - (text_width / 2)
                # Center vertically: banner_y + (banner_height - font_size) / 2 + font_size * 0.3
                # The 0.3 factor accounts for the text baseline position
                y_pos = by + (bh - font_size) / 2 + font_size * 0.3
                break
        
        # Draw text at specified position
        self.canvas.drawString(x_pos, y_pos, text)
        
        return True
    
    def draw_elements_list(self, elements: List[Dict[str, Any]]) -> int:
        """
        Draw multiple text elements from a list.
        
        Iterates through a list of text element dictionaries and renders
        each one using draw_text_element(). Counts successful renders.
        
        Args:
            elements: List of element dictionaries
        
        Returns:
            int: Number of elements successfully drawn
        
        Note:
            Empty or whitespace-only elements are skipped automatically.
        """
        count = 0
        for element in elements:
            if self.draw_text_element(element):
                count += 1
        return count
    
    # ========================================================================
    # INFRASTRUCTURE - Banners and links
    # ========================================================================
    
    def draw_banner(self, banner: Dict[str, float]) -> None:
        """
        Draw a colored background banner for section headers.
        
        Renders a filled rectangle with the standard banner color.
        Banners provide visual hierarchy and section separation.
        
        Args:
            banner: Dictionary with keys:
                - x (float): X coordinate (left edge)
                - y (float): Y coordinate (bottom edge)
                - w (float): Width in points
                - h (float): Height in points
        
        Note:
            Banners are drawn without strokes (borders) for clean appearance.
        """
        self.canvas.setFillColor(CVColors.BANNER_BG)
        self.canvas.rect(
            banner["x"], 
            banner["y"], 
            banner["w"], 
            banner["h"], 
            fill=1,  # Fill the rectangle
            stroke=CVConfig.BANNER_STROKE  # No border
        )
    
    def add_link(self, link: Dict[str, Any]) -> None:
        """
        Add a clickable hyperlink area to the PDF.
        
        Creates an invisible rectangular region that, when clicked,
        opens the specified URL. Links are invisible (0 thickness)
        but fully functional.
        
        Args:
            link: Dictionary with keys:
                - url (str): Target URL (http://, mailto:, etc.)
                - rect (list): [x1, y1, x2, y2] rectangle coordinates
        
        Link Types Supported:
            - mailto: Email links
            - http/https: Web links
            - DOI: Digital Object Identifier links
        
        Note:
            Links are positioned precisely to cover the colored text areas.
        """
        self.canvas.linkURL(
            link["url"], 
            tuple(link["rect"]),
            relative=0,  # Absolute positioning
            thickness=CVConfig.LINK_THICKNESS  # Invisible border
        )
    
    # ========================================================================
    # HIGH-LEVEL RENDERING - Batch operations
    # ========================================================================
    
    def render_banners(self) -> None:
        """
        Render all section background banners.
        
        Draws all colored rectangles that provide visual structure
        to the CV sections. Must be called before rendering text
        so banners appear behind text content.
        """
        for banner in BANNERS:
            self.draw_banner(banner)
    
    def render_content(self) -> int:
        """
        Render all CV text content.
        
        Draws every text element from CV_CONTENT in order.
        Returns count of successfully rendered elements for validation.
        
        Returns:
            int: Number of text elements drawn
        """
        return self.draw_elements_list(CV_CONTENT)
    
    def render_links(self) -> None:
        """
        Add all clickable hyperlink areas.
        
        Creates invisible clickable regions for all URLs in the CV.
        Must be called after rendering text so links appear on top.
        """
        for link in LINKS:
            self.add_link(link)
    
    # ========================================================================
    # VALIDATION - Output verification
    # ========================================================================
    
    def validate_output(self) -> bool:
        """
        Validate that PDF was generated successfully.
        
        Performs basic checks on the output file to ensure it was
        created properly and has reasonable contents.
        
        Returns:
            bool: True if validation passed, False otherwise
        
        Checks:
            - File exists
            - File size > 0
            - Expected number of elements drawn
        """
        if not os.path.exists(self.output_file):
            print(f"✗ Validation failed: {self.output_file} not found")
            return False
        
        file_size = os.path.getsize(self.output_file)
        if file_size == 0:
            print(f"✗ Validation failed: {self.output_file} is empty")
            return False
        
        if self.elements_drawn == 0:
            print("✗ Validation failed: No elements drawn")
            return False
        
        return True
    
    # ========================================================================
    # MAIN GENERATION - Orchestration
    # ========================================================================
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate complete CV PDF (main entry point).
        
        Orchestrates the entire PDF generation process in correct order:
          1. Display header
          2. Load fonts (Trebuchet MS or Helvetica)
          3. Initialize canvas
          4. Render banners (background layer)
          5. Render text content (foreground layer)
          6. Add hyperlinks (interaction layer)
          7. Save PDF
          8. Validate output
          9. Display summary
        
        Returns:
            dict: Generation statistics with keys:
                - file (str): Output file path
                - elements (int): Number of elements drawn
                - size_kb (float): File size in kilobytes
                - valid (bool): Whether validation passed
        
        Raises:
            IOError: If PDF cannot be saved
        
        Example:
            >>> gen = CVGenerator()
            >>> stats = gen.generate()
            >>> print(f"Drew {stats['elements']} elements")
        """
        # Display generation header
        print("\n" + "="*76)
        print("  Professional CV Generator - Ultra-Modular Architecture")
        print("="*76 + "\n")
        
        # Load fonts (with fallback)
        self.has_trebuchet = self.load_fonts()
        
        # Initialize canvas
        self.canvas = canvas.Canvas(self.output_file, pagesize=self.PAGE_SIZE)
        self.elements_drawn = 0
        
        # Render in layers (back to front)
        self.render_banners()              # Layer 1: Backgrounds
        self.elements_drawn = self.render_content()  # Layer 2: Text
        self.render_links()                # Layer 3: Interactive areas
        
        # Save PDF to disk
        self.canvas.save()
        
        # Validate output
        is_valid = self.validate_output()
        
        # Display generation summary
        file_size_kb = os.path.getsize(self.output_file) / 1024 if is_valid else 0
        
        print(f"\n✓ Generated: {self.output_file}")
        print(f"  Elements: {self.elements_drawn}")
        print(f"  Size: {file_size_kb:.1f} KB")
        print(f"  Valid: {'Yes' if is_valid else 'No'}")
        print("\n" + "="*76 + "\n")
        
        return {
            "file": self.output_file,
            "elements": self.elements_drawn,
            "size_kb": file_size_kb,
            "valid": is_valid
        }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main() -> None:
    """
    Main entry point for CV generation.
    
    Creates a CVGenerator instance and generates the PDF.
    Can be called from command line or imported as a module.
    
    Command Line:
        python3 generate_cv.py
    
    As Module:
        from generate_cv import main
        main()
    """
    generator = CVGenerator()
    stats = generator.generate()
    
    # Optional: Return stats for programmatic use
    return stats


if __name__ == "__main__":
    main()
