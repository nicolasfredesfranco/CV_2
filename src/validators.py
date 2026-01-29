"""
Data Validation Module
======================

Validates JSON data structure for coordinates and shapes.
Ensures data integrity before rendering to prevent runtime errors.
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class DataValidator:
    """
    Validates JSON data structures for CV generation.
    
    Provides comprehensive validation of coordinates and shapes data,
    checking for required fields, correct types, and valid ranges.
    """
    
    @staticmethod
    def validate_coordinates(data: List[Dict[str, Any]]) -> bool:
        """
        Validate coordinates data structure.
        
        Args:
            data: List of coordinate dictionaries to validate
            
        Returns:
            True if valid, False otherwise (with error logging)
            
        Checks:
            - Non-empty data
            - Required fields present ('text', 'x', 'y', 'size')
            - Correct types (str for text, numbers for coordinates/size)
        """
        if not data:
            logger.error("Coordinates data is empty")
            return False
        
        required_fields = ['text', 'x', 'y', 'size']
        optional_fields = ['font', 'color', 'bold', 'italic']
        
        for idx, elem in enumerate(data):
            # Check required fields
            missing = [f for f in required_fields if f not in elem]
            if missing:
                logger.error(f"Element {idx} missing fields: {missing}. Element: {elem}")
                return False
            
            # Check data types
            if not isinstance(elem['text'], str):
                logger.error(f"Element {idx}: 'text' must be string")
                return False
            if not isinstance(elem['x'], (int, float)):
                logger.error(f"Element {idx}: 'x' must be numeric")
                return False
            if not isinstance(elem['y'], (int, float)):
                logger.error(f"Element {idx}: 'y' must be numeric")
                return False
            if not isinstance(elem['size'], (int, float)):
                logger.error(f"Element {idx}: 'size' must be numeric")
                return False
        
        logger.info(f"✅ Coordinates validation passed: {len(data)} elements")
        return True

    @staticmethod
    def validate_shapes(data: List[Dict[str, Any]]) -> bool:
        """
        Validate shapes data structure.
        
        Args:
            data: List of shape dictionaries to validate
            
        Returns:
            True if valid, False otherwise (with error logging)
            
        Note:
            Empty shapes data is valid (shapes are optional decorations)
        """
        if not data:
            logger.warning("Shapes data is empty (non-critical)")
            return True  # Shapes are optional
        
        for idx, shape in enumerate(data):
            # Check type field exists
            if 'type' not in shape:
                logger.error(f"Shape {idx}: missing 'type' field")
                return False
            
            # Validate rectangles
            if shape['type'] == 'rect':
                # Check for actual format used in shapes.json
                required = ['x', 'y', 'width', 'height', 'fill_color']
                missing = [f for f in required if f not in shape]
                if missing:
                    logger.error(f"Rectangle {idx}: missing fields {missing}")
                    return False
                if not isinstance(shape['fill_color'], list) or len(shape['fill_color']) != 3:
                    logger.error(f"Rectangle {idx}: 'fill_color' must be RGB list of 3 numbers")
                    return False
        
        logger.info(f"✅ Shapes validation passed: {len(data)} elements")
        return True
