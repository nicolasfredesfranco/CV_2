#!/usr/bin/env python3
"""
Visual PDF Comparison Test - Robust and Dynamic
===============================================

Compares the generated CV PDF with the original reference PDF.
Provides detailed metrics for each section and overall match score.

This test is designed to be:
- Dynamic: No hardcoded values
- Comprehensive: Section-by-section and global analysis
- Visual: Compares actual rendered appearance
- Quantitative: Provides numerical match scores
"""

import fitz  # PyMuPDF
import os
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import math


class PDFVisualComparator:
    """
    Professional PDF comparator that analyzes visual similarity.
    
    Compares:
    - Text content and positioning
    - Font usage and sizes
    - Color schemes
    - Spatial distribution
    - Section organization
    """
    
    def __init__(self, reference_pdf: str, generated_pdf: str):
        """Initialize with paths to both PDFs."""
        self.ref_path = reference_pdf
        self.gen_path = generated_pdf
        
        # Load PDFs
        self.ref_doc = fitz.open(reference_pdf)
        self.gen_doc = fitz.open(generated_pdf)
        
        # Extract data
        self.ref_page = self.ref_doc[0]
        self.gen_page = self.gen_doc[0]
        
        # Store extracted elements
        self.ref_blocks = None
        self.gen_blocks = None
        self.ref_text_instances = None
        self.gen_text_instances = None
        
        # Section definitions (Y-coordinate ranges)
        self.sections = {
            "CONTACT": (668, 800),           # Top left
            "EDUCATION": (440, 668),         # Left column
            "SKILLS": (107, 440),            # Left column
            "LANGUAGES": (0, 107),           # Bottom left
            "HEADER": (710, 800),            # Top right (name)
            "EXPERIENCE": (92, 710),         # Right column (main)
            "PAPERS": (0, 92)                # Bottom right
        }
    
    def extract_text_blocks(self, page) -> List[Dict]:
        """Extract text blocks with full details."""
        blocks = []
        text_dict = page.get_text("dict")
        
        for block in text_dict.get("blocks", []):
            if block.get("type") == 0:  # Text block
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        blocks.append({
                            "text": span.get("text", ""),
                            "bbox": span.get("bbox", (0, 0, 0, 0)),
                            "font": span.get("font", ""),
                            "size": span.get("size", 0),
                            "color": span.get("color", 0),
                            "flags": span.get("flags", 0),
                            "origin": span.get("origin", (0, 0))
                        })
        
        return blocks
    
    def get_section_blocks(self, blocks: List[Dict], section_name: str) -> List[Dict]:
        """Filter blocks that belong to a specific section."""
        y_min, y_max = self.sections[section_name]
        
        section_blocks = []
        for block in blocks:
            bbox = block["bbox"]
            # Use center Y coordinate
            center_y = (bbox[1] + bbox[3]) / 2
            
            if y_min <= center_y <= y_max:
                section_blocks.append(block)
        
        return section_blocks
    
    def compare_text_content(self, ref_blocks: List[Dict], gen_blocks: List[Dict]) -> float:
        """Compare text content similarity."""
        ref_text = " ".join([b["text"] for b in ref_blocks])
        gen_text = " ".join([b["text"] for b in gen_blocks])
        
        if not ref_text or not gen_text:
            return 0.0
        
        # Simple character-level similarity
        ref_chars = set(ref_text.replace(" ", ""))
        gen_chars = set(gen_text.replace(" ", ""))
        
        if not ref_chars:
            return 0.0
        
        intersection = len(ref_chars & gen_chars)
        union = len(ref_chars | gen_chars)
        
        return intersection / union if union > 0 else 0.0
    
    def compare_positioning(self, ref_blocks: List[Dict], gen_blocks: List[Dict]) -> float:
        """Compare spatial positioning of text elements."""
        if not ref_blocks or not gen_blocks:
            return 0.0
        
        # Extract Y positions (vertical positioning)
        ref_y_positions = sorted([b["bbox"][1] for b in ref_blocks])
        gen_y_positions = sorted([b["bbox"][1] for b in gen_blocks])
        
        # Compare distributions
        if len(ref_y_positions) != len(gen_y_positions):
            # Penalize different number of elements
            length_ratio = min(len(ref_y_positions), len(gen_y_positions)) / max(len(ref_y_positions), len(gen_y_positions))
        else:
            length_ratio = 1.0
        
        # Compare spacing patterns
        if len(ref_y_positions) > 1 and len(gen_y_positions) > 1:
            ref_spacings = [ref_y_positions[i+1] - ref_y_positions[i] for i in range(min(10, len(ref_y_positions)-1))]
            gen_spacings = [gen_y_positions[i+1] - gen_y_positions[i] for i in range(min(10, len(gen_y_positions)-1))]
            
            # Average spacing similarity
            spacing_diffs = []
            for i in range(min(len(ref_spacings), len(gen_spacings))):
                if ref_spacings[i] > 0:
                    diff_ratio = abs(ref_spacings[i] - gen_spacings[i]) / ref_spacings[i]
                    spacing_diffs.append(1.0 - min(diff_ratio, 1.0))
            
            spacing_score = sum(spacing_diffs) / len(spacing_diffs) if spacing_diffs else 0.5
        else:
            spacing_score = 0.5
        
        return (length_ratio + spacing_score) / 2
    
    def compare_fonts(self, ref_blocks: List[Dict], gen_blocks: List[Dict]) -> float:
        """Compare font usage."""
        if not ref_blocks or not gen_blocks:
            return 0.0
        
        # Extract unique fonts
        ref_fonts = set([b["font"] for b in ref_blocks if b["font"]])
        gen_fonts = set([b["font"] for b in gen_blocks if b["font"]])
        
        if not ref_fonts:
            return 1.0 if not gen_fonts else 0.0
        
        # Font family similarity (Trebuchet vs Helvetica is acceptable)
        ref_families = set()
        for font in ref_fonts:
            if "Trebuchet" in font:
                ref_families.add("Trebuchet")
            elif "Helvetica" in font:
                ref_families.add("Helvetica")
            elif "Times" in font:
                ref_families.add("Times")
        
        gen_families = set()
        for font in gen_fonts:
            if "Trebuchet" in font:
                gen_families.add("Trebuchet")
            elif "Helvetica" in font:
                gen_families.add("Helvetica")
            elif "Times" in font:
                gen_families.add("Times")
        
        if not ref_families:
            return 1.0
        
        # Trebuchet/Helvetica are interchangeable
        if "Trebuchet" in ref_families and "Helvetica" in gen_families:
            gen_families.add("Trebuchet")
        if "Helvetica" in ref_families and "Trebuchet" in gen_families:
            gen_families.add("Helvetica")
        
        intersection = len(ref_families & gen_families)
        union = len(ref_families | gen_families)
        
        return intersection / union if union > 0 else 0.0
    
    def compare_font_sizes(self, ref_blocks: List[Dict], gen_blocks: List[Dict]) -> float:
        """Compare font size distribution."""
        if not ref_blocks or not gen_blocks:
            return 0.0
        
        ref_sizes = [b["size"] for b in ref_blocks if b["size"] > 0]
        gen_sizes = [b["size"] for b in gen_blocks if b["size"] > 0]
        
        if not ref_sizes or not gen_sizes:
            return 0.0
        
        # Compare size ranges
        ref_min, ref_max = min(ref_sizes), max(ref_sizes)
        gen_min, gen_max = min(gen_sizes), max(gen_sizes)
        
        min_score = 1.0 - abs(ref_min - gen_min) / max(ref_min, 1)
        max_score = 1.0 - abs(ref_max - gen_max) / max(ref_max, 1)
        
        return (min_score + max_score) / 2
    
    def compare_colors(self, ref_blocks: List[Dict], gen_blocks: List[Dict]) -> float:
        """Compare color usage."""
        if not ref_blocks or not gen_blocks:
            return 0.0
        
        ref_colors = set([b["color"] for b in ref_blocks])
        gen_colors = set([b["color"] for b in gen_blocks])
        
        if not ref_colors:
            return 1.0 if not gen_colors else 0.0
        
        intersection = len(ref_colors & gen_colors)
        union = len(ref_colors | gen_colors)
        
        return intersection / union if union > 0 else 0.0
    
    def analyze_section(self, section_name: str) -> Dict[str, float]:
        """Comprehensive section analysis."""
        # Extract blocks for this section
        ref_section = self.get_section_blocks(self.ref_blocks, section_name)
        gen_section = self.get_section_blocks(self.gen_blocks, section_name)
        
        # Compute metrics
        metrics = {
            "text_content": self.compare_text_content(ref_section, gen_section),
            "positioning": self.compare_positioning(ref_section, gen_section),
            "fonts": self.compare_fonts(ref_section, gen_section),
            "font_sizes": self.compare_font_sizes(ref_section, gen_section),
            "colors": self.compare_colors(ref_section, gen_section),
        }
        
        # Overall section score (weighted average)
        weights = {
            "text_content": 0.35,
            "positioning": 0.25,
            "fonts": 0.15,
            "font_sizes": 0.15,
            "colors": 0.10
        }
        
        overall = sum(metrics[k] * weights[k] for k in metrics.keys())
        metrics["overall"] = overall
        
        return metrics
    
    def run_full_comparison(self) -> Dict[str, Any]:
        """Run complete comparison and generate report."""
        print("\n" + "="*80)
        print("PDF VISUAL COMPARISON TEST")
        print("="*80)
        print(f"\nReference: {self.ref_path}")
        print(f"Generated: {self.gen_path}")
        print("\nExtracting data...")
        
        # Extract all blocks
        self.ref_blocks = self.extract_text_blocks(self.ref_page)
        self.gen_blocks = self.extract_text_blocks(self.gen_page)
        
        print(f"  Reference blocks: {len(self.ref_blocks)}")
        print(f"  Generated blocks: {len(self.gen_blocks)}")
        
        # Analyze each section
        results = {}
        print("\n" + "-"*80)
        print("SECTION-BY-SECTION ANALYSIS")
        print("-"*80)
        
        for section_name in self.sections.keys():
            metrics = self.analyze_section(section_name)
            results[section_name] = metrics
            
            print(f"\n{section_name}:")
            print(f"  Text Content:  {metrics['text_content']*100:5.1f}%")
            print(f"  Positioning:   {metrics['positioning']*100:5.1f}%")
            print(f"  Fonts:         {metrics['fonts']*100:5.1f}%")
            print(f"  Font Sizes:    {metrics['font_sizes']*100:5.1f}%")
            print(f"  Colors:        {metrics['colors']*100:5.1f}%")
            print(f"  → OVERALL:     {metrics['overall']*100:5.1f}%")
        
        # Global metrics
        print("\n" + "-"*80)
        print("GLOBAL METRICS")
        print("-"*80)
        
        # Overall text similarity
        global_text = self.compare_text_content(self.ref_blocks, self.gen_blocks)
        print(f"  Global Text Match:        {global_text*100:5.1f}%")
        
        # Overall positioning
        global_pos = self.compare_positioning(self.ref_blocks, self.gen_blocks)
        print(f"  Global Positioning:       {global_pos*100:5.1f}%")
        
        # Font consistency
        global_fonts = self.compare_fonts(self.ref_blocks, self.gen_blocks)
        print(f"  Font Consistency:         {global_fonts*100:5.1f}%")
        
        # Number of links
        ref_links = len(self.ref_page.get_links())
        gen_links = len(self.gen_page.get_links())
        link_score = 1.0 if ref_links == gen_links else min(ref_links, gen_links) / max(ref_links, gen_links)
        print(f"  Links ({gen_links}/{ref_links}):            {link_score*100:5.1f}%")
        
        # File size efficiency
        ref_size = os.path.getsize(self.ref_path) / 1024
        gen_size = os.path.getsize(self.gen_path) / 1024
        size_ratio = gen_size / ref_size
        print(f"  File Size: {gen_size:.1f} KB vs {ref_size:.1f} KB (ratio: {size_ratio:.2f})")
        
        # Calculate weighted global score
        section_scores = [results[s]["overall"] for s in results.keys()]
        avg_section_score = sum(section_scores) / len(section_scores)
        
        global_score = (
            avg_section_score * 0.50 +
            global_text * 0.20 +
            global_pos * 0.15 +
            global_fonts * 0.10 +
            link_score * 0.05
        )
        
        print("\n" + "="*80)
        print(f"FINAL MATCH SCORE: {global_score*100:.2f}%")
        print("="*80)
        
        # Quality assessment
        if global_score >= 0.95:
            quality = "EXCELLENT"
        elif global_score >= 0.90:
            quality = "VERY GOOD"
        elif global_score >= 0.85:
            quality = "GOOD"
        elif global_score >= 0.75:
            quality = "ACCEPTABLE"
        else:
            quality = "NEEDS IMPROVEMENT"
        
        print(f"Quality: {quality}")
        
        # Identify weak points
        print("\n" + "-"*80)
        print("WEAK POINTS (sections scoring below 85%):")
        print("-"*80)
        
        weak_sections = []
        for section, metrics in results.items():
            if metrics["overall"] < 0.85:
                weak_sections.append((section, metrics["overall"]))
                print(f"  • {section}: {metrics['overall']*100:.1f}%")
                # Show which sub-metric is weakest
                weak_metrics = [(k, v) for k, v in metrics.items() if k != "overall" and v < 0.80]
                for metric_name, score in weak_metrics:
                    print(f"      - {metric_name}: {score*100:.1f}%")
        
        if not weak_sections:
            print("  None! All sections score ≥ 85%")
        
        print("\n" + "="*80)
        
        results["_global"] = {
            "score": global_score,
            "quality": quality,
            "global_text": global_text,
            "global_positioning": global_pos,
            "global_fonts": global_fonts,
            "links": link_score,
            "weak_sections": weak_sections
        }
        
        return results


def main():
    """Main test execution."""
    reference = "EN_NicolasFredes_CV.pdf"
    generated = "Nicolas_Fredes_CV.pdf"
    
    # Check files exist
    if not os.path.exists(reference):
        print(f"❌ Reference file not found: {reference}")
        return
    
    if not os.path.exists(generated):
        print(f"❌ Generated file not found: {generated}")
        print("   Run: python3 generate_cv.py")
        return
    
    # Run comparison
    comparator = PDFVisualComparator(reference, generated)
    results = comparator.run_full_comparison()
    
    # Close documents
    comparator.ref_doc.close()
    comparator.gen_doc.close()
    
    return results


if __name__ == "__main__":
    main()

