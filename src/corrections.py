"""
Precision Corrections Module
============================

Business logic for visual micro-adjustments and layout corrections.
Applies heuristic rules to match the exact visual appearance of the objective PDF.
"""

import logging
from typing import Tuple, Dict, Any
from .config import CONFIG

logger = logging.getLogger(__name__)


class PrecisionCorrector:
    """
    Applies micro-precision corrections for perfect visual alignment.
    
    Implements reverse-engineered layout rules to correct OCR extraction
    imperfections and ensure pixel-perfect rendering.
    """
    
    @staticmethod
    def apply_corrections(
        text: str, 
        x: float, 
        y_reportlab: float,
        elem_props: Dict[str, Any]
    ) -> Tuple[str, float]:
        """
        Apply visual precision corrections to text position and content.
        
        Args:
            text: Original text content
            x: X coordinate in ReportLab space
            y_reportlab: Y coordinate in ReportLab space
            elem_props: Element properties (font, size, bold, italic, etc.)
            
        Returns:
            Tuple of (corrected_text, corrected_x)
            
        Corrections Applied:
            - Date alignment adjustments
            - Bullet point injection for lists
        """
        corrected_text = text
        corrected_x = x
        
        # Correction A: Date Alignment
        # Dates in the right column tend to drift, apply horizontal offset
        is_date_column = (x > CONFIG.THRESHOLD_DATE_ALIGN_X)
        is_body_section = (y_reportlab > (CONFIG.PAGE_HEIGHT - CONFIG.THRESHOLD_DATE_ALIGN_Y_LIMIT))
        
        if is_date_column and is_body_section:
            corrected_x -= CONFIG.OFFSET_DATE_CORRECTION
        
        # Correction B: Bullet Point Injection
        # Infer list items based on position and formatting
        is_right_column = (x > CONFIG.THRESHOLD_RIGHT_COLUMN_X)
        is_plain_text = not (elem_props.get('bold', False) or elem_props.get('italic', False))
        
        if is_right_column and is_plain_text:
            clean = text.strip()
            # Heuristic: Starts with capital, sufficient length, not a location name
            if (clean and clean[0].isupper() and len(clean) > 3 and 
                x < CONFIG.THRESHOLD_LOCATION_TEXT_X):
                corrected_text = "• " + text
                corrected_x -= CONFIG.OFFSET_BULLET_INDENT
        
        return corrected_text, corrected_x
