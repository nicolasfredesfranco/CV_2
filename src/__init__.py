"""
CV Generator - Professional PDF Generation Engine
=================================================

A high-precision CV/Resume generation system using absolute coordinate mapping
to achieve 100% visual and functional identity with an objective PDF design.

Author: Nicolás Ignacio Fredes Franco
License: MIT
Version: 3.0.0
"""

__version__ = "3.0.0"
__author__ = "Nicolás Ignacio Fredes Franco"

from .config import LayoutConfig, CONFIG
from .fonts import FontManager
from .renderer import CVRenderer

__all__ = [
    "LayoutConfig",
    "CONFIG",
    "FontManager",
    "CVRenderer",
]
