#!/usr/bin/env python3
"""
CV Generator - Professional PDF Generation Engine
=================================================

A high-precision CV/Resume generation system using absolute coordinate mapping
to achieve 100% visual and functional identity with an objective PDF design.

Features:
    - Modular architecture with separation of concerns
    - Comprehensive data validation
    - Intelligent hyperlink detection and spatial disambiguation
    - Micro-precision visual corrections
    - Performance optimization with LRU caching
    - CLI with flexible configuration options

Author: Nicolás Ignacio Fredes Franco
License: MIT
Version: 3.0.0

Usage:
    python main.py                          # Generate with default settings
    python main.py --output custom.pdf      # Custom output path
    python main.py --validate-only          # Validate data without generating
    python main.py --debug                  # Enable verbose logging
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config import CONFIG
from src.fonts import FontManager
from src.renderer import CVRenderer


# ========== LOGGING CONFIGURATION ==========

def setup_logging(debug: bool = False) -> None:
    """
    Configure logging system.
    
    Args:
        debug: If True, set log level to DEBUG for detailed output
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )


# ========== CLI ARGUMENT PARSING ==========

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Namespace with parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="CV Generator - Professional PDF generation with pixel-perfect precision",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Generate CV with default settings
  %(prog)s --output resume.pdf          # Generate with custom output name
  %(prog)s --validate-only              # Validate JSON data without generating
  %(prog)s --debug                      # Enable detailed debug logging
  
For more information, visit: https://github.com/nicolasfredesfranco/CV_2
        """
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        metavar='PATH',
        help='Custom output PDF file path (default: outputs/Nicolas_Fredes_CV.pdf)'
    )
    
    parser.add_argument(
        '--data-dir', '-d',
        type=str,
        metavar='DIR',
        help='Custom data directory path (default: ./data)'
    )
    
    parser.add_argument(
        '--validate-only', '-v',
        action='store_true',
        help='Validate JSON data without generating PDF'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging for detailed output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 3.0.0'
    )
    
    return parser.parse_args()


# ========== MAIN EXECUTION ==========

def main() -> None:
    """
    Main execution function.
    
    Orchestrates the CV generation process:
        1. Parse CLI arguments
        2. Configure logging
        3. Register fonts
        4. Initialize renderer (loads and validates data)
        5. Render shapes and text
        6. Save PDF
    """
    # Parse arguments and setup
    args = parse_arguments()
    setup_logging(debug=args.debug)
    logger = logging.getLogger(__name__)
    
    # Banner
    print("=" * 60)
    print("🚀 CV Generator Engine v3.0")
    print("   Nicolás Ignacio Fredes Franco")
    print("=" * 60)
    print(f"📂 Data directory: {CONFIG.DATA_DIR}")
    print(f"📄 Output file: {CONFIG.FILE_OUTPUT}")
    print("=" * 60)
    
    # Register fonts
    FontManager.register_fonts()
    
    # Validate-only mode
    if args.validate_only:
        logger.info("🔍 Validation-only mode enabled")
        renderer = CVRenderer()  # This loads and validates data
        logger.info("✅ All data validated successfully")
        logger.info("Skipping PDF generation (--validate-only flag)")
        return
    
    # Full generation
    try:
        # Initialize renderer (loads and validates data)
        renderer = CVRenderer()
        
        # Render layers
        renderer.render_background_shapes()
        renderer.render_text_elements()
        
        # Save PDF
        renderer.save()
        
        # Success
        print("=" * 60)
        print("✅ PDF generated successfully")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Generation failed: {e}", exc_info=args.debug)
        sys.exit(1)


# ========== ENTRY POINT ==========

if __name__ == "__main__":
    main()
