#!/usr/bin/env python3
"""
PDF Exhaustive Verification Script
===================================

Compares generated PDF against objective PDF using:
1. Vector-level comparison (exact coordinates, text content)
2. Pixel-level comparison (visual rendering at maximum resolution)

Generates detailed similarity report with precise measurements.

Author: Nicolás Ignacio Fredes Franco
"""

import sys
from pathlib import Path
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image, ImageChops, ImageDraw, ImageFont
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class PDFVectorComparator:
    """Compares PDF vector data (text positions, fonts, sizes)."""
    
    def __init__(self, pdf1_path: Path, pdf2_path: Path):
        self.pdf1_path = pdf1_path
        self.pdf2_path = pdf2_path
    
    def extract_text_elements(self, pdf_path: Path) -> list:
        """Extract all text elements with positions from PDF."""
        elements = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                chars = page.chars
                for char in chars:
                    elements.append({
                        'text': char['text'],
                        'x0': round(char['x0'], 2),
                        'y0': round(char['y0'], 2),
                        'x1': round(char['x1'], 2),
                        'y1': round(char['y1'], 2),
                        'fontname': char.get('fontname', 'unknown'),
                        'size': round(char.get('size', 0), 2)
                    })
        return elements
    
    def compare_vectors(self) -> dict:
        """Compare vector data between two PDFs."""
        logger.info("🔍 Extracting vector data from objective PDF...")
        objective_elements = self.extract_text_elements(self.pdf1_path)
        
        logger.info("🔍 Extracting vector data from generated PDF...")
        generated_elements = self.extract_text_elements(self.pdf2_path)
        
        logger.info(f"Objective: {len(objective_elements)} characters")
        logger.info(f"Generated: {len(generated_elements)} characters")
        
        # Compare counts
        count_match = len(objective_elements) == len(generated_elements)
        
        # Compare positions (with tolerance for PDF engine differences)
        position_tolerance = 1.0  # 1 point tolerance
        position_matches = 0
        position_differences = []
        
        min_len = min(len(objective_elements), len(generated_elements))
        
        for i in range(min_len):
            obj = objective_elements[i]
            gen = generated_elements[i]
            
            # Check text match
            text_match = obj['text'] == gen['text']
            
            # Check position match (with tolerance)
            x_diff = abs(obj['x0'] - gen['x0'])
            y_diff = abs(obj['y0'] - gen['y0'])
            
            if x_diff <= position_tolerance and y_diff <= position_tolerance and text_match:
                position_matches += 1
            else:
                if len(position_differences) < 10:  # Store first 10 differences
                    position_differences.append({
                        'index': i,
                        'text': obj['text'],
                        'obj_pos': (obj['x0'], obj['y0']),
                        'gen_pos': (gen['x0'], gen['y0']),
                        'diff': (x_diff, y_diff)
                    })
        
        position_similarity = (position_matches / min_len * 100) if min_len > 0 else 0
        
        return {
            'count_match': count_match,
            'objective_count': len(objective_elements),
            'generated_count': len(generated_elements),
            'position_matches': position_matches,
            'position_similarity': position_similarity,
            'position_differences': position_differences[:5]  # Return top 5
        }


class PDFPixelComparator:
    """Compares PDF visual output at pixel level."""
    
    def __init__(self, pdf1_path: Path, pdf2_path: Path):
        self.pdf1_path = pdf1_path
        self.pdf2_path = pdf2_path
    
    def compare_pixels(self, dpi: int = 300) -> dict:
        """
        Compare PDFs at pixel level.
        
        Args:
            dpi: Resolution for rendering (higher = more precise)
        """
        logger.info(f"🖼️  Rendering objective PDF at {dpi} DPI...")
        objective_images = convert_from_path(self.pdf1_path, dpi=dpi)
        
        logger.info(f"🖼️  Rendering generated PDF at {dpi} DPI...")
        generated_images = convert_from_path(self.pdf2_path, dpi=dpi)
        
        if len(objective_images) != len(generated_images):
            logger.error("❌ Page count mismatch!")
            return {'error': 'Page count mismatch'}
        
        # Compare first page (assuming single-page CV)
        obj_img = objective_images[0]
        gen_img = generated_images[0]
        
        # Ensure same size
        if obj_img.size != gen_img.size:
            logger.warning(f"Size mismatch: {obj_img.size} vs {gen_img.size}")
            return {'error': 'Image size mismatch'}
        
        # Calculate pixel differences
        diff = ImageChops.difference(obj_img, gen_img)
        
        # Get histogram of differences
        histogram = diff.histogram()
        
        # Count total pixels
        total_pixels = obj_img.width * obj_img.height * 3  # RGB
        
        # Count different pixels (non-zero values in diff)
        different_pixels = sum(histogram) - histogram[0]
        
        # Calculate similarity
        similarity = ((total_pixels - different_pixels) / total_pixels * 100)
        
        # Find bounding box of differences
        bbox = diff.getbbox()
        
        # Save difference visualization
        diff_path = Path("outputs/pixel_difference_visualization.png")
        diff.save(diff_path)
        logger.info(f"💾 Difference visualization saved: {diff_path}")
        
        # Create side-by-side comparison
        comparison = Image.new('RGB', (obj_img.width * 2, obj_img.height))
        comparison.paste(obj_img, (0, 0))
        comparison.paste(gen_img, (obj_img.width, 0))
        
        comparison_path = Path("outputs/side_by_side_comparison.png")
        comparison.save(comparison_path)
        logger.info(f"💾 Side-by-side comparison saved: {comparison_path}")
        
        return {
            'total_pixels': total_pixels,
            'different_pixels': different_pixels,
            'similarity_percent': similarity,
            'resolution': f"{obj_img.width}x{obj_img.height}",
            'dpi': dpi,
            'difference_bbox': bbox,
            'diff_image_path': str(diff_path),
            'comparison_path': str(comparison_path)
        }


def generate_report(vector_results: dict, pixel_results: dict) -> None:
    """Generate comprehensive verification report."""
    print("\n" + "=" * 80)
    print("📊 EXHAUSTIVE PDF VERIFICATION REPORT")
    print("=" * 80)
    
    # Vector Comparison
    print("\n📐 VECTOR COMPARISON (Coordinate-level)")
    print("-" * 80)
    print(f"Objective character count: {vector_results['objective_count']}")
    print(f"Generated character count: {vector_results['generated_count']}")
    print(f"Count match: {'✅ YES' if vector_results['count_match'] else '❌ NO'}")
    print(f"\nPosition matches: {vector_results['position_matches']}/{min(vector_results['objective_count'], vector_results['generated_count'])}")
    print(f"Position similarity: {vector_results['position_similarity']:.2f}%")
    
    if vector_results['position_differences']:
        print("\nTop position differences:")
        for diff in vector_results['position_differences']:
            print(f"  Char '{diff['text']}' at index {diff['index']}")
            print(f"    Objective: {diff['obj_pos']}")
            print(f"    Generated: {diff['gen_pos']}")
            print(f"    Δ: {diff['diff']}")
    
    # Pixel Comparison
    print("\n\n🖼️  PIXEL COMPARISON (Visual-level)")
    print("-" * 80)
    if 'error' not in pixel_results:
        print(f"Resolution: {pixel_results['resolution']} @ {pixel_results['dpi']} DPI")
        print(f"Total pixels: {pixel_results['total_pixels']:,}")
        print(f"Different pixels: {pixel_results['different_pixels']:,}")
        print(f"Pixel similarity: {pixel_results['similarity_percent']:.4f}%")
        
        if pixel_results['difference_bbox']:
            print(f"Difference bounding box: {pixel_results['difference_bbox']}")
        else:
            print("Difference bounding box: None (identical)")
        
        print(f"\n📁 Visualizations:")
        print(f"  - Diff map: {pixel_results['diff_image_path']}")
        print(f"  - Side-by-side: {pixel_results['comparison_path']}")
    else:
        print(f"❌ Error: {pixel_results['error']}")
    
    # Overall verdict
    print("\n\n🏆 FINAL VERDICT")
    print("=" * 80)
    vector_pass = vector_results['position_similarity'] >= 99.0
    pixel_pass = pixel_results.get('similarity_percent', 0) >= 99.0
    
    if vector_pass and pixel_pass:
        print("✅ EXCELLENT - PDFs are virtually identical!")
    elif vector_pass or pixel_pass:
        print("⚠️  GOOD - Minor differences detected")
    else:
        print("❌ NEEDS REVIEW - Significant differences found")
    
    print("=" * 80 + "\n")


def main():
    """Main execution."""
    # Using previous generated version as reference (objective design)
    objective_pdf = Path("pdfs/objective/Objetivo_No_editar.pdf")
    generated_pdf = Path("outputs/Nicolas_Fredes_CV.pdf")
    
    if not objective_pdf.exists():
        logger.error(f"❌ Objective PDF not found: {objective_pdf}")
        sys.exit(1)
    
    if not generated_pdf.exists():
        logger.error(f"❌ Generated PDF not found: {generated_pdf}")
        sys.exit(1)
    
    # Vector comparison
    logger.info("Starting vector comparison...")
    vector_comparator = PDFVectorComparator(objective_pdf, generated_pdf)
    vector_results = vector_comparator.compare_vectors()
    
    # Pixel comparison at high resolution
    logger.info("Starting pixel comparison...")
    pixel_comparator = PDFPixelComparator(objective_pdf, generated_pdf)
    pixel_results = pixel_comparator.compare_pixels(dpi=300)
    
    # Generate report
    generate_report(vector_results, pixel_results)
    
    # Save JSON report
    report = {
        'vector_comparison': vector_results,
        'pixel_comparison': pixel_results
    }
    
    report_path = Path("outputs/verification_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"💾 Full report saved: {report_path}")


if __name__ == "__main__":
    main()
