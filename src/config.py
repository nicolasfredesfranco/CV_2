"""
Configuration Module
===================

Centralized configuration for CV generation including page dimensions,
color palette, thresholds, and file paths.

All "magic numbers" are defined here as named constants for easy modification.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class LayoutConfig:
    """
    Centralized configuration for document layout and rendering rules.
    
    Defines the 'physics' of the document to ensure consistency across
    all rendering operations. Immutable (frozen) to prevent accidental modifications.
    
    Attributes:
        PAGE_WIDTH: Page width in PDF points (verified from objective)
        PAGE_HEIGHT: Page height in PDF points (verified from objective)
        COLOR_PRIMARY_BLUE: Primary blue color in normalized RGB (0-1)
        Y_GLOBAL_OFFSET: Y-axis offset to correct PDF engine differences
        THRESHOLD_*: Various positional thresholds for business logic
        OFFSET_*: Micro-precision adjustments for visual corrections
    """
    
    # Page Dimensions (PDF Points - corrected based on pdfinfo)
    # Objective verified: 623 x 806 pts (NO floating point)
    PAGE_WIDTH: float = 623.0
    PAGE_HEIGHT: float = 806.0

    # Color Palette (Normalized RGB 0-1)
    # Corporate blue extracted from shapes.json: #3A6BA9 = RGB(58,107,169)
    COLOR_PRIMARY_BLUE: Tuple[float, float, float] = (0.227, 0.42, 0.663)
    
    # Global Y-Axis Offset (PDF Points)
    # Corrects differences between Ghostscript (objective) and ReportLab (generated)
    # Positive value moves content UP, negative moves DOWN
    # RESTORED from v2.2 - DO NOT CHANGE (empirically calibrated for objective PDF)
    Y_GLOBAL_OFFSET: float = 32.0  # Empirically adjusted for perfect alignment
    
    # Layout Logic Thresholds (Reverse Engineered)
    # X/Y coordinates that trigger specific behaviors
    THRESHOLD_RIGHT_COLUMN_X: float = 215.0
    THRESHOLD_LOCATION_TEXT_X: float = 250.0
    THRESHOLD_DATE_ALIGN_X: float = 380.0
    THRESHOLD_DATE_ALIGN_Y_LIMIT: float = 750.0  # Apply correction only in body
    
    # Vertical threshold to disambiguate links (Github vs LinkedIn)
    THRESHOLD_LINK_DISAMBIGUATION_Y: float = 150.0

    # Micro-Precision Offsets (PDF Points)
    OFFSET_DATE_CORRECTION: float = 1.5
    OFFSET_BULLET_INDENT: float = 8.5
    LINK_HITBOX_PADDING: float = 2.0

    # File System Paths (using pathlib for cross-platform compatibility)
    BASE_DIR: Path = Path(__file__).parent.parent.resolve()
    DATA_DIR: Path = BASE_DIR / 'data'
    ASSETS_DIR: Path = DATA_DIR / 'assets'
    OUTPUT_DIR: Path = BASE_DIR / 'outputs'
    
    FILE_COORDS: Path = DATA_DIR / 'coordinates.json'
    FILE_SHAPES: Path = DATA_DIR / 'shapes.json'
    FILE_OUTPUT: Path = OUTPUT_DIR / 'Nicolas_Fredes_CV.pdf'


# Global configuration instance
CONFIG = LayoutConfig()
