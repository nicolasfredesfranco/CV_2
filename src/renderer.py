"""
CV Renderer Module
==================

High-precision PDF rendering engine using absolute coordinate mapping.
Orchestrates data loading, validation, transformation, and vector drawing.
"""

import json
import logging
import sys
from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Any, Optional

from reportlab.pdfgen import canvas

from .config import CONFIG
from .validators import DataValidator
from .transformations import CoordinateTransformer
from .hyperlinks import HyperlinkResolver
from .corrections import PrecisionCorrector

logger = logging.getLogger(__name__)


class CVRenderer:
    """
    Professional CV rendering engine with pixel-perfect output.
    
    Features:
        - Absolute coordinate mapping from JSON data
        - Y-axis transformation with global offset correction
        - Hyperlink injection with spatial disambiguation
        - Micro-precision visual corrections
        - LRU caching for performance optimization
    """
    
    def __init__(self):
        """Initialize renderer, load and validate data."""
        self._ensure_output_dir()
        self.canvas = canvas.Canvas(
            str(CONFIG.FILE_OUTPUT),
            pagesize=(CONFIG.PAGE_WIDTH, CONFIG.PAGE_HEIGHT)
        )
        
        # Load data from JSON files
        self.coordinates_data = self._load_json(CONFIG.FILE_COORDS)
        self.shapes_data = self._load_json(CONFIG.FILE_SHAPES)
        
        # Validate loaded data
        if not DataValidator.validate_coordinates(self.coordinates_data):
            logger.error("❌ Coordinates validation failed. Cannot continue.")
            sys.exit(1)
        
        if not DataValidator.validate_shapes(self.shapes_data):
            logger.error("❌ Shapes validation failed. Cannot continue.")
            sys.exit(1)
    
    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist."""
        CONFIG.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def _load_json(path: Path) -> List[Any]:
        """
        Safely load JSON file with error handling.
        
        Args:
            path: Path to JSON file
            
        Returns:
            List of loaded data, empty list if file not found
        """
        if not path.exists():
            logger.error(f"Critical file not found: {path}")
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted JSON in {path}: {e}")
            sys.exit(1)
    
    @lru_cache(maxsize=1000)
    def _get_text_width(self, text: str, font_name: str, size: float) -> float:
        """
        Calculate text width with LRU caching for performance.
        
        Args:
            text: Text content
            font_name: Font family name
            size: Font size in points
            
        Returns:
            Text width in PDF points
        """
        try:
            return self.canvas.stringWidth(text, font_name, size)
        except:
            # Fallback to Helvetica if font unavailable
            return self.canvas.stringWidth(text, "Helvetica", size)
    
    def render_background_shapes(self) -> None:
        """
        Render background geometric shapes (rectangles, decorations).
        
        Shapes come from PDF extraction with correct coordinates.
        NO transformation needed - draw directly.
        """
        logger.info("Rendering background shapes...")
        
        for shape in self.shapes_data:
            if shape['type'] == 'rect':
                # Shapes already in correct ReportLab coordinates from PDF
                x = shape['x']
                y = shape['y']
                width = shape['width']
                height = shape['height']
                r, g, b = shape['fill_color']
                
                # Color filter: Only draw blue headers
                is_blue_header = all(
                    abs(c - base) < 0.25
                    for c, base in zip([r, g, b], CONFIG.COLOR_PRIMARY_BLUE)
                )
                
                if not is_blue_header:
                    continue  # Skip non-blue shapes
                
                # Draw directly - shapes already have correct coordinates
                # No transformation needed!
                self.canvas.setFillColorRGB(*CONFIG.COLOR_PRIMARY_BLUE)
                self.canvas.rect(x, y, width, height, fill=1, stroke=0)
        
        # DEBUG: Draw green horizontal line above main name
        # Name is at X=233.63, Y=95.94 (PDF space), size=24.01
        # Calculate name top edge in ReportLab space
        # name_y_pdf = 95.94
        # name_y_reportlab = CONFIG.PAGE_HEIGHT - name_y_pdf + CONFIG.Y_GLOBAL_OFFSET
        # name_height = 24.01
        # line_y = name_y_reportlab + name_height - 6  # Top edge of text, lowered 6 pts
        
        # Draw dark green line from left edge to right edge of page
        # self.canvas.setStrokeColorRGB(0, 0.5, 0)  # Dark green
        # self.canvas.setLineWidth(1.0)  # Medium thickness
        # self.canvas.line(0, line_y, CONFIG.PAGE_WIDTH, line_y)  # Full width
    
    def render_text_elements(self) -> None:
        """
        Render all text elements with hyperlinks and precision corrections.
        
        Processes each coordinate entry, applies transformations, corrections,
        and renders text with appropriate fonts, colors, and hyperlinks.
        """
        logger.info("Rendering text elements and metadata...")
        
        for elem in self.coordinates_data:
            # 1. Extract properties
            text = elem['text']
            raw_x = elem['x']
            raw_y = elem['y']
            size = elem['size']
            
            # Font properties
            font_family = elem.get('font', 'TrebuchetMS')
            is_bold = elem.get('bold', False)
            is_italic = elem.get('italic', False)
            
            # Determine font name (handle cases where font already has suffix)
            if '-Bold' in font_family or '-Italic' in font_family:
                # Font name already includes style suffix
                font_name = font_family
            elif is_bold and is_italic:
                font_name = f"{font_family}-Bold"  # Approximation (no BoldItalic variant)
            elif is_bold:
                font_name = f"{font_family}-Bold"
            elif is_italic:
                font_name = f"{font_family}-Italic"
            else:
                font_name = font_family
            
            # Color
            color_int = elem.get('color', 0)
            rgb_color = CoordinateTransformer.rgb_from_int(color_int)
            
            # 2. Coordinate transformation
            y_reportlab = CoordinateTransformer.transform_y(raw_y)
            
            # 3. Apply precision corrections
            corrected_text, corrected_x = PrecisionCorrector.apply_corrections(
                text, raw_x, y_reportlab, elem
            )
            
            # 4. Set font and color
            self.canvas.setFont(font_name, size)
            self.canvas.setFillColorRGB(*rgb_color)
            
            # 5. Inject hyperlinks
            url = HyperlinkResolver.resolve(corrected_text, raw_y)
            if url:
                text_width = self._get_text_width(corrected_text, font_name, size)
                
                # Define clickable area: [x_left, y_bottom, x_right, y_top]
                link_rect = (
                    corrected_x,
                    y_reportlab - CONFIG.LINK_HITBOX_PADDING,
                    corrected_x + text_width,
                    y_reportlab + size
                )
                self.canvas.linkURL(url, link_rect, relative=0, thickness=0)
            
            # 6. Draw text
            try:
                self.canvas.drawString(corrected_x, y_reportlab, corrected_text)
            except Exception as e:
                logger.error(f"Failed to draw text '{corrected_text}': {e}")
        
        # Restore line configuration
        self.canvas.setLineWidth(1)
    
    def save(self) -> None:
        """
        Finalize and save PDF document.
        
        Completes the PDF page and writes to disk.
        """
        self.canvas.showPage()
        self.canvas.save()
        logger.info(f"✅ Generation completed: {CONFIG.FILE_OUTPUT}")
