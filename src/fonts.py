"""
Font Management Module
======================

Handles font registration and loading for the CV generation system.
Provides graceful fallbacks if custom fonts are not available.
"""

import logging
from pathlib import Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .config import CONFIG

logger = logging.getLogger(__name__)


class FontManager:
    """
    Font registration and management system.
    
    Registers the TrebuchetMS font family (Regular, Bold, Italic) with ReportLab.
    Provides fallback to Helvetica if custom fonts are unavailable.
    """
    
    @staticmethod
    def register_fonts() -> None:
        """
        Register TrebuchetMS font family in the ReportLab system.
        
        Attempts to load all three font variants from the assets directory.
        Logs warnings for missing fonts and provides detailed status information.
        """
        font_map = {
            'TrebuchetMS': 'trebuc.ttf',
            'TrebuchetMS-Bold': 'trebucbd.ttf',
            'TrebuchetMS-Italic': 'trebucit.ttf'
        }
        
        loaded_count = 0
        for font_name, filename in font_map.items():
            font_path = CONFIG.ASSETS_DIR / filename
            if font_path.exists():
                try:
                    pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
                    loaded_count += 1
                    logger.debug(f"Font loaded: {font_name}")
                except Exception as e:
                    logger.warning(f"Error loading font {font_name}: {e}")
            else:
                logger.warning(f"Font file not found: {font_path}")
        
        if loaded_count == 0:
            logger.error("No custom fonts loaded. Will use Helvetica as fallback.")
        else:
            logger.info(f"✅ {loaded_count} fonts loaded successfully")
