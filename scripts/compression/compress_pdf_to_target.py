#!/usr/bin/env python3
"""
Compress PDF to target size while preserving links and visual quality.
Target: reduce from 2.5MB to ~1.9MB with minimal quality loss.
"""

import subprocess
import os
import sys

def get_file_size_mb(filepath):
    """Get file size in MB."""
    return os.path.getsize(filepath) / (1024 * 1024)

def compress_pdf_with_gs(input_path, output_path, image_resolution=300):
    """
    Compress PDF using Ghostscript with custom parameters.
    
    Args:
        input_path: Source PDF file
        output_path: Destination PDF file
        image_resolution: DPI for image compression (higher = better quality, larger file)
    """
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        '-dPreserveAnnots=true',  # CRITICAL: Preserve clickable links
        '-dEmbedAllFonts=true',
        '-dSubsetFonts=true',
        '-dCompressFonts=true',
        f'-dColorImageResolution={image_resolution}',
        f'-dGrayImageResolution={image_resolution}',
        f'-dMonoImageResolution={image_resolution}',
        '-dColorImageDownsampleType=/Bicubic',
        '-dGrayImageDownsampleType=/Bicubic',
        '-dAutoRotatePages=/None',
        '-dColorConversionStrategy=/LeaveColorUnchanged',
        '-dDetectDuplicateImages=true',
        '-dCompressPages=true',
        f'-sOutputFile={output_path}',
        input_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during compression: {result.stderr}")
        return False
    return True

def find_optimal_resolution(input_path, output_path, target_size_mb=1.9, tolerance_mb=0.1):
    """
    Binary search to find the optimal image resolution to achieve target file size.
    
    Args:
        input_path: Source PDF
        output_path: Destination PDF
        target_size_mb: Target size in MB (default 1.9 MB)
        tolerance_mb: Acceptable deviation from target
    """
    original_size = get_file_size_mb(input_path)
    print(f"Original file size: {original_size:.2f} MB")
    print(f"Target file size: {target_size_mb:.2f} MB")
    print(f"Tolerance: ±{tolerance_mb:.2f} MB\n")
    
    # Binary search parameters
    min_resolution = 150
    max_resolution = 450
    best_resolution = None
    best_size = None
    best_diff = float('inf')
    
    iteration = 0
    max_iterations = 10
    
    while iteration < max_iterations and (max_resolution - min_resolution) > 10:
        iteration += 1
        current_resolution = (min_resolution + max_resolution) // 2
        
        print(f"Iteration {iteration}: Testing resolution {current_resolution} DPI...")
        
        # Compress with current resolution
        success = compress_pdf_with_gs(input_path, output_path, current_resolution)
        if not success:
            print("Compression failed, trying next iteration...")
            max_resolution = current_resolution - 10
            continue
        
        current_size = get_file_size_mb(output_path)
        diff = abs(current_size - target_size_mb)
        
        print(f"  → Result: {current_size:.2f} MB (diff: {diff:.2f} MB)")
        
        # Track best result
        if diff < best_diff:
            best_diff = diff
            best_resolution = current_resolution
            best_size = current_size
        
        # Check if we're within tolerance
        if diff <= tolerance_mb:
            print(f"\n✓ SUCCESS! Achieved {current_size:.2f} MB at {current_resolution} DPI")
            print(f"  Difference from target: {diff:.2f} MB")
            return True
        
        # Adjust search range
        if current_size < target_size_mb:
            # File too small, increase resolution
            min_resolution = current_resolution
        else:
            # File too large, decrease resolution
            max_resolution = current_resolution
    
    # If we couldn't hit exact target, use best result
    if best_resolution:
        print(f"\nUsing best result: {best_size:.2f} MB at {best_resolution} DPI")
        print(f"Difference from target: {best_diff:.2f} MB")
        compress_pdf_with_gs(input_path, output_path, best_resolution)
        return True
    
    return False

def main():
    input_pdf = '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_2.pdf'
    output_pdf = '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_3.pdf'
    
    if not os.path.exists(input_pdf):
        print(f"Error: Input file not found: {input_pdf}")
        sys.exit(1)
    
    print("=" * 60)
    print("PDF COMPRESSION TO TARGET SIZE")
    print("=" * 60)
    print(f"Input:  {input_pdf}")
    print(f"Output: {output_pdf}")
    print("=" * 60 + "\n")
    
    # Find optimal compression
    success = find_optimal_resolution(input_pdf, output_pdf, target_size_mb=1.9, tolerance_mb=0.1)
    
    if success:
        final_size = get_file_size_mb(output_pdf)
        print("\n" + "=" * 60)
        print("COMPRESSION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Final file size: {final_size:.2f} MB")
        print(f"Reduction: {get_file_size_mb(input_pdf) - final_size:.2f} MB")
        print(f"Output saved to: {output_pdf}")
        print("\n✓ All clickable links preserved (PreserveAnnots=true)")
        print("=" * 60)
    else:
        print("\nCompression failed to achieve target size.")
        sys.exit(1)

if __name__ == '__main__':
    main()
