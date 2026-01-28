#!/usr/bin/env python3
"""
Advanced Similarity Test: 0-100% measurement
Measures pixel-perfect similarity between generated and objective PDFs
100% = identical file copy
"""
import fitz  # PyMuPDF
import numpy as np
from PIL import Image
import sys
import os

def calculate_advanced_similarity(gen_pdf, obj_pdf, zoom=3.0):
    """
    Calculate comprehensive similarity score
    
    Args:
        gen_pdf: Path to generated PDF
        obj_pdf: Path to objective PDF
        zoom: Resolution multiplier for rendering (higher = more accurate)
    
    Returns:
        dict with detailed similarity metrics
    """
    print(f"📊 Analizando similitud con zoom={zoom}x...")
    
    gen_doc = fitz.open(gen_pdf)
    obj_doc = fitz.open(obj_pdf)
    
    # Render at high resolution
    mat = fitz.Matrix(zoom, zoom)
    
    gen_pix = gen_doc[0].get_pixmap(matrix=mat)
    obj_pix = obj_doc[0].get_pixmap(matrix=mat)
    
    # Convert to PIL Images
    gen_img = Image.frombytes('RGB', [gen_pix.width, gen_pix.height], gen_pix.samples)
    obj_img = Image.frombytes('RGB', [obj_pix.width, obj_pix.height], obj_pix.samples)
    
    # Ensure same dimensions
    if gen_img.size != obj_img.size:
        print(f"⚠️  Tamaños diferentes: gen={gen_img.size}, obj={obj_img.size}")
        print(f"   Redimensionando generado a {obj_img.size}")
        gen_img = gen_img.resize(obj_img.size, Image.Resampling.LANCZOS)
    
    # Convert to numpy arrays
    gen_arr = np.array(gen_img, dtype=np.float32)
    obj_arr = np.array(obj_img, dtype=np.float32)
    
    # Metrics
    metrics = {}
    
    # 1. Pixel-level absolute difference
    diff = np.abs(gen_arr - obj_arr)
    max_diff = 255.0
    
    # Average difference per pixel per channel
    avg_diff = np.mean(diff)
    metrics['avg_pixel_diff'] = avg_diff
    
    # 2. Similarity score (0-100%)
    # 100% = identical, 0% = completely different
    pixel_similarity = 100.0 * (1.0 - (avg_diff / max_diff))
    metrics['pixel_similarity'] = pixel_similarity
    
    # 3. Percentage of identical pixels
    # Count pixels where all RGB channels match exactly
    identical_pixels = np.all(diff == 0, axis=2)
    pct_identical = 100.0 * np.sum(identical_pixels) / identical_pixels.size
    metrics['pct_identical_pixels'] = pct_identical
    
    # 4. Maximum difference (worst pixel)
    max_pixel_diff = np.max(diff)
    metrics['max_pixel_diff'] = max_pixel_diff
    
    # 5. Structural Similarity (SSIM-like metric)
    # Standard deviation comparison
    gen_std = np.std(gen_arr)
    obj_std = np.std(obj_arr)
    std_similarity = 100.0 * (1.0 - abs(gen_std - obj_std) / max(gen_std, obj_std))
    metrics['std_similarity'] = std_similarity
    
    # 6. Create difference heatmap
    diff_img = np.mean(diff, axis=2)  # Average across RGB
    diff_img_normalized = (diff_img / max_diff * 255).astype(np.uint8)
    metrics['diff_map'] = Image.fromarray(diff_img_normalized, mode='L')
    
    # 7. Histogram comparison
    gen_hist = np.histogram(gen_arr.flatten(), bins=256, range=(0, 255))[0]
    obj_hist = np.histogram(obj_arr.flatten(), bins=256, range=(0, 255))[0]
    hist_similarity = 100.0 * (1.0 - np.sum(np.abs(gen_hist - obj_hist)) / (2 * np.sum(obj_hist)))
    metrics['histogram_similarity'] = hist_similarity
    
    # 8. COMBINED SCORE (weighted average)
    # Weight pixel similarity most heavily
    combined_score = (
        0.60 * pixel_similarity +
        0.20 * pct_identical +
        0.10 * std_similarity +
        0.10 * hist_similarity
    )
    metrics['combined_score'] = combined_score
    
    gen_doc.close()
    obj_doc.close()
    
    return metrics

def print_similarity_report(metrics, save_path=None):
    """Print detailed similarity report"""
    print("\n" + "="*100)
    print("REPORTE DE SIMILITUD AVANZADO".center(100))
    print("="*100)
    
    print(f"\n{'MÉTRICA':<40} {'VALOR':>20} {'INTERPRETACIÓN'}")
    print("-"*100)
    
    # Pixel Similarity
    ps = float(metrics['pixel_similarity'])
    ps_interp = "EXCELENTE" if ps >= 99 else "MUY BUENO" if ps >= 95 else "BUENO" if ps >= 90 else "MEJORABLE"
    print(f"{'Similitud de Píxeles':<40} {ps:>19.4f}% {ps_interp:>20}")
    
    # Identical Pixels
    ip = float(metrics['pct_identical_pixels'])
    ip_interp = "PERFECTO" if ip >= 99 else "EXCELENTE" if ip >= 95 else "BUENO" if ip >= 90 else "MEJORABLE"
    print(f"{'% Píxeles Idénticos':<40} {ip:>19.4f}% {ip_interp:>20}")
    
    # Avg Diff
    ad = float(metrics['avg_pixel_diff'])
    ad_interp = "MÍNIMA" if ad < 2 else "BAJA" if ad < 5 else "MEDIA" if ad < 10 else "ALTA"
    print(f"{'Diferencia Promedio (0-255)':<40} {ad:>19.4f} {ad_interp:>20}")
    
    # Max Diff
    md = float(metrics['max_pixel_diff'])
    md_interp = "EXCELENTE" if md < 10 else "BUENO" if md < 30 else "MEJORABLE"
    print(f"{'Diferencia Máxima (0-255)':<40} {md:>19.4f} {md_interp:>20}")
    
    # Histogram Similarity
    hs = float(metrics['histogram_similarity'])
    hs_interp = "EXCELENTE" if hs >= 99 else "MUY BUENO" if hs >= 95 else "BUENO"
    print(f"{'Similitud de Histograma':<40} {hs:>19.4f}% {hs_interp:>20}")
    
    # Structural Similarity
    ss = float(metrics['std_similarity'])
    ss_interp = "EXCELENTE" if ss >= 99 else "MUY BUENO" if ss >= 95 else "BUENO"
    print(f"{'Similitud Estructural':<40} {ss:>19.4f}% {ss_interp:>20}")
    
    print("-"*100)
    
    # COMBINED SCORE (main metric)
    cs = float(metrics['combined_score'])
    if cs >= 99.5:
        cs_interp = "🎯 OBJETIVO ALCANZADO"
        cs_color = "🟢"
    elif cs >= 99.0:
        cs_interp = "⭐ CASI PERFECTO"
        cs_color = "🟢"
    elif cs >= 95.0:
        cs_interp = "✅ MUY BUENO"
        cs_color = "🟡"
    elif cs >= 90.0:
        cs_interp = "👍 BUENO"
        cs_color = "🟡"
    else:
        cs_interp = "⚠️  NECESITA MEJORA"
        cs_color = "🔴"
    
    print(f"\n{cs_color} {'SCORE COMBINADO (OBJETIVO: >99%)':<40} {cs:>19.4f}% {cs_interp:>20}")
    print("="*100 + "\n")
    
    # Save difference map
    if save_path and 'diff_map' in metrics:
        diff_path = save_path.replace('.json', '_diff.png')
        metrics['diff_map'].save(diff_path)
        print(f"💾 Mapa de diferencias guardado: {diff_path}")
        # Remove from dict for JSON serialization
        del metrics['diff_map']
    
    # Convert all numpy types to native Python types for JSON
    for key in metrics:
        if hasattr(metrics[key], 'item'):  # numpy scalar
            metrics[key] = float(metrics[key])
    
    return cs

if __name__ == "__main__":
    import json
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))  # Go up two levels from scripts/verification/
    
    gen_pdf = os.path.join(repo_root, 'outputs', 'Nicolas_Fredes_CV.pdf')
    obj_pdf = os.path.join(repo_root, 'pdfs', 'objective', 'Objetivo_No_editar.pdf')
    
    # Allow command line override
    if len(sys.argv) > 1:
        gen_pdf = sys.argv[1]
    if len(sys.argv) > 2:
        obj_pdf = sys.argv[2]
    
    print(f"📄 Generado: {gen_pdf}")
    print(f"📄 Objetivo: {obj_pdf}")
    
    metrics = calculate_advanced_similarity(gen_pdf, obj_pdf, zoom=3.0)
    
    report_path = os.path.join(repo_root, 'similarity_report.json')
    score = print_similarity_report(metrics, save_path=report_path)
    
    # Save JSON report
    with open(report_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"📊 Reporte JSON guardado: {report_path}")
    
    # Exit code based on score
    if score >= 99.0:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Needs improvement
