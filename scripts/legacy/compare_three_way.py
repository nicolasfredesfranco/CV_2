#!/usr/bin/env python3
"""
Three-way comparison: Objetivo vs v2.2 vs v3.0
"""

from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import numpy as np

DPI = 300

print("=" * 70)
print("THREE-WAY COMPARISON: Objetivo vs v2.2 vs v3.0")
print("=" * 70)

# Convert all three PDFs
print("\n📄 Converting PDFs...")
obj = convert_from_path("pdfs/objective/Objetivo_No_editar.pdf", dpi=DPI)[0]
v22 = convert_from_path("outputs/v22_backup_generated.pdf", dpi=DPI)[0]
v30 = convert_from_path("outputs/v30_modular_generated.pdf", dpi=DPI)[0]

print(f"Objetivo: {obj.size}")
print(f"v2.2:     {v22.size}")
print(f"v3.0:     {v30.size}")

# Resize to match
target_size = obj.size
if v22.size != target_size:
    v22 = v22.resize(target_size, Image.Resampling.LANCZOS)
if v30.size != target_size:
    v30 = v30.resize(target_size, Image.Resampling.LANCZOS)

# Create side-by-side-by-side
total_width = target_size[0] * 3 + 20
comparison = Image.new('RGB', (total_width, target_size[1]), 'white')
comparison.paste(obj, (0, 0))
comparison.paste(v22, (target_size[0] + 10, 0))
comparison.paste(v30, (target_size[0] * 2 + 20, 0))

# Add labels
draw = ImageDraw.Draw(comparison)
draw.text((50, 30), "OBJETIVO", fill='red')
draw.text((target_size[0] + 60, 30), "v2.2 BACKUP", fill='green')
draw.text((target_size[0] * 2 + 70, 30), "v3.0 MODULAR", fill='blue')

comparison.save("outputs/three_way_comparison.png")
print("\n✅ Saved: outputs/three_way_comparison.png")

# Compare v2.2 vs v3.0
print("\n🔍 Comparing v2.2 vs v3.0...")
v22_arr = np.array(v22)
v30_arr = np.array(v30)

diff_v2_v3 = np.sum(np.abs(v22_arr.astype(int) - v30_arr.astype(int)))
total_diff = v22_arr.shape[0] * v22_arr.shape[1] * 3 * 255

similarity_v2_v3 = 100 * (1 - diff_v2_v3 / total_diff)

print(f"v2.2 vs v3.0 similarity: {similarity_v2_v3:.4f}%")

if similarity_v2_v3 > 99.9:
    print("✅ v2.2 and v3.0 are PRACTICALLY IDENTICAL")
elif similarity_v2_v3 > 99:
    print("⚠️  v2.2 and v3.0 have minor differences")
else:
    print("❌ v2.2 and v3.0 are SIGNIFICANTLY DIFFERENT")

print("=" * 70)
