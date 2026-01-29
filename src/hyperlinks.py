"""
Hyperlink Detection Module
==========================

Detects and resolves hyperlinks from text content and position.
Handles disambiguation for social media links (GitHub vs LinkedIn).
"""

import logging
from typing import Optional
from .config import CONFIG

logger = logging.getLogger(__name__)


class HyperlinkResolver:
    """
    Intelligent hyperlink detection and resolution system.
    
    Analyzes text content and spatial position to infer the correct
    URL destination. Handles edge cases like identical social media handles
    appearing in different document locations.
    """
    
    @staticmethod
    def resolve(text: str, y_original: float) -> Optional[str]:
        """
        Determine hyperlink URL from text content and position.
        
        Args:
            text: Text content to analyze
            y_original: Original Y coordinate (PDF space) for spatial disambiguation
            
        Returns:
            URL string if link detected, None otherwise
            
        Resolution Logic:
            - Email addresses → mailto: links
            - DOI references → https://doi.org/ links
            - Twitter handle → Twitter profile
            - GitHub/LinkedIn → Spatially disambiguated based on Y position
        """
        try:
            if not text:
                return None
            
            clean_text = text.strip()
            
            # Email link
            if "nico.fredes.franco@gmail.com" in clean_text:
                return "mailto:nico.fredes.franco@gmail.com"
            
            # DOI link
            elif "DOI: 10.1109" in clean_text:
                return "https://doi.org/10.1109/ACCESS.2021.3094723"
            
            # Twitter handle (unique substring, check before GitHub/LinkedIn)
            elif "nicofredesfranc" in clean_text and "nicolasfredesfranco" not in clean_text:
                return "https://twitter.com/NicoFredesFranc"
            
            # GitHub vs LinkedIn disambiguation
            elif "nicolasfredesfranco" in clean_text:
                # Spatial Disambiguation Logic:
                # GitHub appears higher (smaller Y in original coords) than LinkedIn
                if y_original < CONFIG.THRESHOLD_LINK_DISAMBIGUATION_Y:
                    return "https://github.com/nicolasfredesfranco"
                else:
                    return "http://www.linkedin.com/in/nicolasfredesfranco"
                    
            return None
            
        except Exception as e:
            text_preview = str(text)[:30] if text else "None"
            logger.warning(f"Error detecting hyperlink in text '{text_preview}...': {e}")
            return None
