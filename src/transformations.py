"""
Coordinate Transformation Module
================================

Handles coordinate system transformations between PDF and ReportLab spaces.
Provides color conversion utilities.
"""

from typing import Tuple
from .config import CONFIG


class CoordinateTransformer:
    """
    Coordinate system transformation utilities.
    
    Converts between PDF's top-down coordinate system and ReportLab's
    bottom-up coordinate system, applying global offset correction.
    """
    
    @staticmethod
    def transform_y(y_pdf: float) -> float:
        """
        Transform Y coordinate from PDF space (Top-Down) to ReportLab space (Bottom-Up).
        
        Applies global offset to correct differences between PDF engines
        (Ghostscript vs ReportLab).
        
        Args:
            y_pdf: Y coordinate in PDF space (0 = top)
            
        Returns:
            Y coordinate in ReportLab space (0 = bottom)
            
        Formula:
            Y_reportlab = PAGE_HEIGHT - Y_pdf + Y_GLOBAL_OFFSET
        """
        return CONFIG.PAGE_HEIGHT - y_pdf + CONFIG.Y_GLOBAL_OFFSET
    
    @staticmethod
    def rgb_from_int(color_int: int) -> Tuple[float, float, float]:
        """
        Convert integer color to normalized RGB tuple.
        
        Args:
            color_int: Color as integer (e.g., 0x3A6BA9 for blue)
            
        Returns:
            Tuple of (r, g, b) normalized to 0-1 range
            
        Example:
            >>> rgb_from_int(0x3A6BA9)
            (0.227, 0.420, 0.663)
        """
        r = (color_int >> 16) & 0xFF
        g = (color_int >> 8) & 0xFF
        b = color_int & 0xFF
        return (r / 255.0, g / 255.0, b / 255.0)
