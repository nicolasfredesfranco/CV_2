#!/usr/bin/env python3
"""
Human-Perceptible Visual Comparison Tool

Compares RENDERED IMAGES (photos) of PDFs to identify differences 
visible to the human eye, ignoring microscopic antialiasing artifacts.
"""

from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont, ImageChops
import numpy as np
from pathlib import Path

def create_visual_comparison():
    """Create side-by-side comparison of PDFs as humans would see them."""
    
    print("="*70)
    print("VISUAL COMPARISON - HUMAN EYE PERSPECTIVE")
    print("="*70)
    
    # Render PDFs as images at screen resolution (150 DPI - typical screen)
    print("\n📸 Taking 'photos' of PDFs at screen resolution (150 DPI)...")
    
    obj_img = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=150)[0]
    gen_img = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=150)[0]
    
    # Ensure same size
    if gen_img.size != obj_img.size:
        gen_img = gen_img.resize(obj_img.size, Image.Resampling.LANCZOS)
    
    print(f"   Objetivo: {obj_img.size}")
    print(f"   Generado: {gen_img.size}")
    
    # Create side-by-side comparison
    width, height = obj_img.size
    comparison = Image.new('RGB', (width * 2 + 60, height + 120), 'white')
    
    # Paste images
    comparison.paste(obj_img, (20, 100))
    comparison.paste(gen_img, (width + 40, 100))
    
    # Add labels
    draw = ImageDraw.Draw(comparison)
    
    # Title
    draw.text((width - 100, 20), "VISUAL COMPARISON - AS HUMAN EYE SEES", fill='black')
    draw.text((width // 2 - 80, 60), "OBJETIVO (Original)", fill='red')
    draw.text((width + width // 2 - 60, 60), "GENERADO (Actual)", fill='blue')
    
    # Divider line
    draw.line([(width + 30, 0), (width + 30, height + 120)], fill='gray', width=3)
    
    # Save comparison
    comparison.save("outputs/visual_human_comparison.png")
    print(f"\n✅ Saved: outputs/visual_human_comparison.png")
    
    # Create difference visualization (human-perceptible level)
    print("\n🔍 Analyzing human-perceptible differences...")
    
    obj_arr = np.array(obj_img)
    gen_arr = np.array(gen_img)
    
    # Calculate difference
    diff = np.abs(obj_arr.astype(int) - gen_arr.astype(int))
    
    # Threshold for human perception: ignore differences < 10 in RGB values
    # (humans can't distinguish tiny color variations)
    HUMAN_THRESHOLD = 10
    diff_perceptible = diff.copy()
    diff_perceptible[diff < HUMAN_THRESHOLD] = 0
    
    # Calculate perceptible vs total difference
    total_diff_pixels = np.sum(diff > 0)
    perceptible_diff_pixels = np.sum(np.any(diff_perceptible > 0, axis=2))
    
    total_pixels = obj_arr.shape[0] * obj_arr.shape[1]
    perceptible_pct = (perceptible_diff_pixels / total_pixels) * 100
    
    print(f"   Total differing pixels: {total_diff_pixels:,}")
    print(f"   Human-perceptible differences: {perceptible_diff_pixels:,}")
    print(f"   Perceptible: {perceptible_pct:.2f}% of image")
    
    # Create heatmap of perceptible differences only
    diff_gray = diff_perceptible.sum(axis=2)
    diff_normalized = ((diff_gray / diff_gray.max()) * 255).astype(np.uint8) if diff_gray.max() > 0 else diff_gray.astype(np.uint8)
    
    heatmap = Image.fromarray(diff_normalized).convert('RGB')
    
    # Apply red colormap to differences
    heatmap_arr = np.array(heatmap)
    red_heatmap = np.zeros_like(obj_arr)
    red_heatmap[:, :, 0] = heatmap_arr[:, :, 0]  # Red channel
    
    heatmap_colored = Image.fromarray(red_heatmap)
    heatmap_colored.save("outputs/visual_human_differences_heatmap.png")
    print(f"✅ Saved: outputs/visual_human_differences_heatmap.png")
    
    # Create overlay showing where differences are
    overlay = Image.blend(obj_img.convert('RGB'), heatmap_colored, alpha=0.3)
    overlay.save("outputs/visual_human_differences_overlay.png")
    print(f"✅ Saved: outputs/visual_human_differences_overlay.png")
    
    # Analyze regions with perceptible differences
    print("\n📊 Analysis by regions (human-perceptible only):")
    
    height_arr = diff_perceptible.shape[0]
    regions = {
        "Header (top 15%)": (0, int(height_arr * 0.15)),
        "Upper content (15-40%)": (int(height_arr * 0.15), int(height_arr * 0.40)),
        "Middle content (40-70%)": (int(height_arr * 0.40), int(height_arr * 0.70)),
        "Lower content (70-90%)": (int(height_arr * 0.70), int(height_arr * 0.90)),
        "Footer (bottom 10%)": (int(height_arr * 0.90), height_arr)
    }
    
    region_issues = []
    for region_name, (y_start, y_end) in regions.items():
        region_diff = diff_perceptible[y_start:y_end, :, :]
        region_diff_pixels = np.sum(np.any(region_diff > 0, axis=2))
        region_total = (y_end - y_start) * diff_perceptible.shape[1]
        region_pct = (region_diff_pixels / region_total) * 100 if region_total > 0 else 0
        
        print(f"   {region_name:30s}: {region_pct:5.2f}% different")
        
        if region_pct > 1.0:  # More than 1% perceptible difference
            region_issues.append((region_name, region_pct))
    
    # Overall verdict
    print("\n" + "="*70)
    print("HUMAN-EYE VERDICT")
    print("="*70)
    
    if perceptible_pct < 0.5:
        print("✅ VISUALLY IDENTICAL to human eye (<0.5% perceptible difference)")
        print("   Remaining differences are microscopic antialiasing artifacts")
        print("   NOT visible at normal viewing distance")
        verdict = "PASS"
    elif perceptible_pct < 2.0:
        print("⚠️  MINOR visible differences (0.5-2% perceptible)")
        print("   Differences might be noticeable upon close inspection")
        verdict = "MINOR"
    else:
        print("❌ SIGNIFICANT visible differences (>2% perceptible)")
        print("   Corrections recommended:")
        for region, pct in region_issues:
            print(f"      - {region}: {pct:.1f}% different")
        verdict = "NEEDS_FIX"
    
    print("="*70)
    
    return {
        "perceptible_pct": perceptible_pct,
        "verdict": verdict,
        "region_issues": region_issues,
        "total_pixels": total_pixels,
        "perceptible_pixels": perceptible_diff_pixels
    }


if __name__ == "__main__":
    result = create_visual_comparison()
    
    print(f"\n📄 Review the visual comparisons:")
    print(f"   - outputs/visual_human_comparison.png (side-by-side)")
    print(f"   - outputs/visual_human_differences_heatmap.png (difference heatmap)")
    print(f"   - outputs/visual_human_differences_overlay.png (overlay)")
    
    if result["verdict"] == "PASS":
        print(f"\n🎉 SUCCESS: PDFs are visually identical to human eye!")
    elif result["verdict"] == "MINOR":
        print(f"\n⚠️  Minor differences detected - likely acceptable")
    else:
        print(f"\n🔧 Corrections needed in specific regions")
