#!/usr/bin/env python3
"""
High Resolution PDF Comparison - Find Exact Differences
=======================================================

Generates high-res side-by-side comparison and diff map to identify
exact areas where generated PDF differs from objective.
"""

from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont, ImageChops
from pathlib import Path
import numpy as np

# High DPI for maximum precision
DPI = 600

print("=" * 70)
print("🔬 HIGH-RESOLUTION PDF COMPARISON")
print("=" * 70)

# Convert PDFs to images
print(f"\n📄 Converting objetivo PDF at {DPI} DPI...")
obj_imgs = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=DPI)
obj_img = obj_imgs[0]

print(f"📄 Converting generated PDF at {DPI} DPI...")
gen_imgs = convert_from_path("outputs/Nicolas_Fredes_CV.pdf", dpi=DPI)
gen_img = gen_imgs[0]

print(f"\n📐 Sizes:")
print(f"  Objetivo: {obj_img.size}")
print(f"  Generado: {gen_img.size}")

# Resize if needed
if obj_img.size != gen_img.size:
    print(f"\n⚠️  Sizes differ! Resizing to match...")
    # Resize generated to match objective
    gen_img = gen_img.resize(obj_img.size, Image.Resampling.LANCZOS)

# Create difference map
print(f"\n🔍 Creating difference map...")
diff = ImageChops.difference(obj_img, gen_img)

# Convert to numpy for analysis
diff_arr = np.array(diff)
obj_arr = np.array(obj_img)
gen_arr = np.array(gen_img)

# Calculate metrics
total_pixels = diff_arr.shape[0] * diff_arr.shape[1]
different_pixels = np.count_nonzero(diff_arr)
different_percent = (different_pixels / total_pixels) * 100
similarity = 100 - different_percent

print(f"\n📊 Pixel Analysis:")
print(f"  Total pixels: {total_pixels:,}")
print(f"  Different pixels: {different_pixels:,}")
print(f"  Similarity: {similarity:.4f}%")

# Find bounding box of differences
bbox = diff.getbbox()
if bbox:
    print(f"\n📍 Difference bounding box:")
    print(f"  Top-left: ({bbox[0]}, {bbox[1]})")
    print(f"  Bottom-right: ({bbox[2]}, {bbox[3]})")
    print(f"  Size: {bbox[2]-bbox[0]} x {bbox[3]-bbox[1]} pixels")
else:
    print(f"\n✅ NO DIFFERENCES FOUND - 100% IDENTICAL!")

# Save visualizations
print(f"\n💾 Saving visualizations...")

# 1. Side by side
comparison = Image.new('RGB', (obj_img.width * 2 + 10, obj_img.height), 'white')
comparison.paste(obj_img, (0, 0))
comparison.paste(gen_img, (obj_img.width + 10, 0))

# Add labels
draw = ImageDraw.Draw(comparison)
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
except:
    font = None

draw.text((50, 50), "OBJETIVO", fill='red', font=font)
draw.text((obj_img.width + 60, 50), "GENERADO", fill='blue', font=font)

comparison.save("outputs/comparison_600dpi.png")
print(f"  ✅ outputs/comparison_600dpi.png")

# 2. Difference map (enhanced)
diff_enhanced = diff.point(lambda p: p * 10 if p > 0 else 0)  # Amplify differences
diff_enhanced.save("outputs/diff_600dpi.png")
print(f"  ✅ outputs/diff_600dpi.png")

# 3. Highlighted differences overlay
if bbox:
    overlay = obj_img.copy().convert('RGBA')
    diff_rgba = diff.convert('RGBA')
    
    # Make differences red
    pixels = diff_rgba.load()
    for y in range(diff_rgba.height):
        for x in range(diff_rgba.width):
            if diff_rgba.getpixel((x, y))[0] > 0:  # If different
                pixels[x, y] = (255, 0, 0, 128)  # Semi-transparent red
    
    overlay.paste(diff_rgba, (0, 0), diff_rgba)
    overlay = overlay.convert('RGB')
    overlay.save("outputs/overlay_600dpi.png")
    print(f"  ✅ outputs/overlay_600dpi.png")

print("=" * 70)
print(f"🏆 SIMILARITY: {similarity:.4f}%")
print("=" * 70)
