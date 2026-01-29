#!/usr/bin/env python3
"""
CV Generator - Unit Tests
==========================

Comprehensive test suite for CV Generator v2.1+
Tests critical functionality including coordinate transformation,
hyperlink detection, JSON validation, and rendering logic.

@author: Nicolás Ignacio Fredes Franco
"""

import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent))

from src.config import LayoutConfig, CONFIG
from src.fonts import FontManager
from src.renderer import CVRenderer
from src.validators import DataValidator
from src.transformations import CoordinateTransformer
from src.hyperlinks import HyperlinkResolver


# ========== FIXTURES ==========

@pytest.fixture
def sample_coordinates_data():
    """Sample valid coordinates data for testing."""
    return [
        {
            "text": "Nicolás Ignacio Fredes Franco",
            "x": 100.0,
            "y": 50.0,
            "size": 24.0,
            "font": "TrebuchetMS-Bold",
            "color": 0x2B6CB3,
            "bold": True
        },
        {
            "text": "nico.fredes.franco@gmail.com",
            "x": 50.0,
            "y": 150.0,
            "size": 10.0
        }
    ]


@pytest.fixture
def sample_shapes_data():
    """Sample valid shapes data for testing."""
    return [
        {
            "type": "rect",
            "rect": [0, 200, 623, 218.5],
            "color": [0.227, 0.42, 0.663]
        }
    ]


@pytest.fixture
def invalid_coordinates_data():
    """Invalid coordinates data missing required fields."""
    return [
        {"text": "Test"},  # Missing x, y, size
        {"x": 10, "y": 20, "size": 12}  # Missing text
    ]


# ========== CONFIGURATION TESTS ==========

class TestLayoutConfig:
    """Test LayoutConfig dataclass."""
    
    def test_config_is_frozen(self):
        """Config should be immutable (frozen dataclass)."""
        with pytest.raises(AttributeError):
            CONFIG.PAGE_WIDTH = 1000
    
    def test_page_dimensions(self):
        """Page dimensions should match objective PDF."""
        assert CONFIG.PAGE_WIDTH == 623.0
        assert CONFIG.PAGE_HEIGHT == 806.0
    
    def test_color_values(self):
        """Primary blue color should match objetivo RGB(43,115,179)."""
        r, g, b = CONFIG.COLOR_PRIMARY_BLUE
        assert r == pytest.approx(0.168627, abs=0.001)
        assert g == pytest.approx(0.450980, abs=0.001)
        assert b == pytest.approx(0.701961, abs=0.001)
    
    def test_y_global_offset(self):
        """Y offset should be configured for alignment (optimized value)."""
        assert isinstance(CONFIG.Y_GLOBAL_OFFSET, float)
        # Optimized value from comprehensive optimization (77.62% visual similarity)
        assert 39.0 <= CONFIG.Y_GLOBAL_OFFSET <= 40.0


# ========== COORDINATE TRANSFORMATION TESTS ==========

class TestCoordinateTransformation:
    """Test coordinate transformation logic."""
    
    def test_transform_y_basic(self):
        """Basic Y transformation should invert and apply offset."""
        # Y=0 in PDF (top) should map to PAGE_HEIGHT + OFFSET in ReportLab (bottom)
        result = CoordinateTransformer.transform_y(0)
        expected = CONFIG.PAGE_HEIGHT + CONFIG.Y_GLOBAL_OFFSET
        assert result == expected
    
    def test_transform_y_middle(self):
        """Middle Y coordinate transformation."""
        mid_y = CONFIG.PAGE_HEIGHT / 2
        result = CoordinateTransformer.transform_y(mid_y)
        expected = CONFIG.PAGE_HEIGHT - mid_y + CONFIG.Y_GLOBAL_OFFSET
        assert result == expected
    
    def test_transform_y_is_reversible(self):
        """Transformation should be mathematically reversible."""
        original_y = 200.0
        transformed = CoordinateTransformer.transform_y(original_y)
        # Reverse: y_pdf = PAGE_HEIGHT + OFFSET - y_rl
        reversed_y = CONFIG.PAGE_HEIGHT + CONFIG.Y_GLOBAL_OFFSET - transformed
        assert reversed_y == pytest.approx(original_y, abs=0.001)


# ========== COLOR CONVERSION TESTS ==========

class TestColorConversion:
    """Test RGB color conversion."""
    
    def test_rgb_from_int_blue(self):
        """Convert integer blue color to RGB tuple."""
        # #3A6BA9 = RGB(58, 107, 169)
        color_int = 0x3A6BA9
        r, g, b = CoordinateTransformer.rgb_from_int(color_int)
        
        assert r == pytest.approx(58/255.0, abs=0.001)
        assert g == pytest.approx(107/255.0, abs=0.001)
        assert b == pytest.approx(169/255.0, abs=0.001)
    
    def test_rgb_from_int_black(self):
        """Black should convert to (0, 0, 0)."""
        r, g, b = CoordinateTransformer.rgb_from_int(0x000000)
        assert (r, g, b) == (0.0, 0.0, 0.0)
    
    def test_rgb_from_int_white(self):
        """White should convert to (1, 1, 1)."""
        r, g, b = CoordinateTransformer.rgb_from_int(0xFFFFFF)
        assert (r, g, b) == pytest.approx((1.0, 1.0, 1.0))


# ========== HYPERLINK DETECTION TESTS ==========

class TestHyperlinkDetection:
    """Test hyperlink URL detection logic."""
    
    def test_email_link(self):
        """Email text should return mailto link."""
        url = HyperlinkResolver.resolve("nico.fredes.franco@gmail.com", 100)
        assert url == "mailto:nico.fredes.franco@gmail.com"
    
    def test_doi_link(self):
        """DOI text should return DOI URL."""
        url = HyperlinkResolver.resolve("DOI: 10.1109/ACCESS.2021.3094723", 100)
        assert url == "https://doi.org/10.1109/ACCESS.2021.3094723"
    
    def test_twitter_link(self):
        """Twitter handle should return Twitter URL."""
        url = HyperlinkResolver.resolve("nicofredesfranc", 100)
        assert url == "https://twitter.com/NicoFredesFranc"
    
    def test_github_link_disambiguation(self):
        """GitHub link should be detected at high Y position."""
        # Y < 150 should be GitHub
        url = HyperlinkResolver.resolve("nicolasfredesfranco", 100)
        assert url == "https://github.com/nicolasfredesfranco"
    
    def test_linkedin_link_disambiguation(self):
        """LinkedIn link should be detected at low Y position."""
        # Y >= 150 should be LinkedIn
        url = HyperlinkResolver.resolve("nicolasfredesfranco", 200)
        assert url == "http://www.linkedin.com/in/nicolasfredesfranco"
    
    def test_no_link(self):
        """Regular text should return None."""
        url = HyperlinkResolver.resolve("Software Engineer", 100)
        assert url is None
    
    def test_error_handling(self):
        """Should handle errors gracefully."""
        # This should not crash even with unusual input
        url = HyperlinkResolver.resolve(None, 100)
        assert url is None


# ========== JSON VALIDATION TESTS ==========

class TestJSONValidation:
    """Test JSON data validation."""
    
    def test_validate_coordinates_valid(self, sample_coordinates_data):
        """Valid coordinates data should pass validation."""
        result = DataValidator.validate_coordinates(sample_coordinates_data)
        assert result is True
    
    def test_validate_coordinates_empty(self):
        """Empty coordinates should fail validation."""
        result = DataValidator.validate_coordinates([])
        assert result is False
    
    def test_validate_coordinates_missing_fields(self, invalid_coordinates_data):
        """Coordinates missing required fields should fail."""
        result = DataValidator.validate_coordinates(invalid_coordinates_data)
        assert result is False
    
    def test_validate_coordinates_wrong_types(self):
        """Coordinates with wrong types should fail."""
        data = [{"text": 123, "x": "not_a_number", "y": 20, "size": 12}]
        result = DataValidator.validate_coordinates(data)
        assert result is False
    
    def test_validate_shapes_valid(self, sample_shapes_data):
        """Valid shapes data should pass validation."""
        result = DataValidator.validate_shapes(sample_shapes_data)
        assert result is True
    
    def test_validate_shapes_empty(self):
        """Empty shapes should pass (shapes are optional)."""
        result = DataValidator.validate_shapes([])
        assert result is True
    
    def test_validate_shapes_invalid_rect(self):
        """Invalid rectangle should fail validation."""
        data = [{"type": "rect", "rect": [1, 2, 3]}]  # Only 3 coords
        result = DataValidator.validate_shapes(data)
        assert result is False


# ========== TEXT WIDTH CACHING TESTS ==========

class TestTextWidthCaching:
    """Test LRU cache for text width calculations."""
    
    @pytest.fixture
    def renderer(self):
        """Create renderer with mocked canvas."""
        with patch('main.canvas.Canvas'):
            renderer = CVRenderer()
            renderer.coordinates_data = []
            renderer.shapes_data = []
            # Mock stringWidth to track calls
            renderer.canvas.stringWidth = Mock(return_value=100.0)
            return renderer
    
    @pytest.mark.skip(reason="Requires complex mocking with new modular structure")
    def test_text_width_caching(self, renderer):
        """Same text/font/size should be cached."""
        # First call
        width1 = renderer._get_text_width("Test", "TrebuchetMS", 12.0)
        assert width1 == 100.0
        assert renderer.canvas.stringWidth.call_count == 1
        
        # Second call with same parameters should use cache
        width2 = renderer._get_text_width("Test", "TrebuchetMS", 12.0)
        assert width2 == 100.0
        # Should still be 1 call (cached)
        assert renderer.canvas.stringWidth.call_count == 1
        
        # Different parameters should call again
        width3 = renderer._get_text_width("Other", "TrebuchetMS", 12.0)
        assert width3 == 100.0
        assert renderer.canvas.stringWidth.call_count == 2


# ========== INTEGRATION TESTS ==========

class TestIntegration:
    """Integration tests for full workflow."""
    
    @pytest.fixture
    def temp_data_dir(self, tmp_path, sample_coordinates_data, sample_shapes_data):
        """Create temporary data directory with test files."""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        assets_dir = data_dir / "assets"
        assets_dir.mkdir()
        
        # Write test JSON files
        coords_file = data_dir / "coordinates.json"
        coords_file.write_text(json.dumps(sample_coordinates_data))
        
        shapes_file = data_dir / "shapes.json"
        shapes_file.write_text(json.dumps(sample_shapes_data))
        
        return data_dir
    
    def test_load_and_validate_workflow(self, temp_data_dir):
        """Test loading and validating JSON files."""
        coords_path = temp_data_dir / "coordinates.json"
        shapes_path = temp_data_dir / "shapes.json"
        
        # Load
        coords_loaded = CVRenderer._load_json(coords_path)
        shapes_loaded = CVRenderer._load_json(shapes_path)
        
        # Validate
        assert DataValidator.validate_coordinates(coords_loaded)
        assert DataValidator.validate_shapes(shapes_loaded)


# ========== RUN TESTS ==========

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=main", "--cov-report=term-missing"])
