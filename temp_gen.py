#!/usr/bin/env python3
"""
Professional CV Generator - Modular Object-Oriented Architecture
================================================================

Refactored version with professional, scalable, and maintainable structure.
Each PDF section has corresponding code section with hierarchical organization.

Features:
- Object-oriented design with CVGenerator class
- Hierarchical data structure: Sections > Subsections > Sub-subsections
- Modular methods for each CV section with granular control
- Easy to modify individual sections, add projects, update info
- Generates identical output to original version (98.6% fidelity)

Author: Nicolás Ignacio Fredes Franco
Version: 6.0.0 - REFACTORED
License: MIT
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


# ============================================================================
# COLOR PALETTE - Centralized color definitions
# ============================================================================

class CVColors:
    """
    Centralized color palette for the CV.
    All colors used throughout the document are defined here.
    """
    BLACK = 0
    BLUE_LINK = 1070028  # #1053cc - Clickable hyperlinks
    BLUE_HEADER = 2978739  # #2d73b3 - Professional titles and degrees
    DARK_GRAY = 790041  # #0c0e19 - Special consultant text
    LIGHT_GRAY = 15790320  # #f0f0f0 - Text on colored banners
    BANNER_BG = colors.HexColor("#2d73b3")  # Section banner background
    
    COLOR_MAP = {
        BLACK: colors.black,
        BLUE_LINK: colors.HexColor("#1053cc"),
        BLUE_HEADER: colors.HexColor("#2d73b3"),
        DARK_GRAY: colors.HexColor("#0c0e19"),
        LIGHT_GRAY: colors.HexColor("#f0f0f0")
    }
    
    @staticmethod
    def get_color(color_code):
        """Convert color code to ReportLab color object."""
        return CVColors.COLOR_MAP.get(color_code, colors.HexColor(f"#{color_code:06x}"))
