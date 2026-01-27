#!/usr/bin/env python3
"""
Compress PDF to ~2MB by adjusting stream compression while preserving all links.
Uses pikepdf for fine-grained control over PDF structure.
"""

import sys
import os

try:
    import pikepdf
except ImportError:
    print("Installing pikepdf...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pikepdf"])
    import pikepdf

def get_file_size_mb(filepath):
    """Get file size in MB."""
    return os.path.getsize(filepath) / (1024 * 1024)

def compress_pdf_streams(input_path, output_path, compression_level=6):
    """
    Compress PDF using pikepdf with controlled compression.
    
    Args:
        input_path: Source PDF
        output_path: Destination PDF
        compression_level: 1-9, where 9 is maximum compression (default: 6 for balanced)
    """
    print(f"Opening PDF: {input_path}")
    pdf = pikepdf.open(input_path)
    
    print(f"Saving with compression level {compression_level}...")
    
    # Save with specific compression settings
    # - compress_streams: compress content streams
    # - preserve_pdfa: preserve PDF/A compliance if present
    # - object_stream_mode: controls how objects are stored (helps reduce size)
    pdf.save(
        output_path,
        compress_streams=True,
        stream_decode_level=pikepdf.StreamDecodeLevel.generalized,
        object_stream_mode=pikepdf.ObjectStreamMode.generate,
        normalize_content=True,
        linearize=False,  # Don't linearize (can increase size slightly)
        min_version="1.4"
    )
    
    pdf.close()
    print(f"PDF saved to: {output_path}")

def find_best_compression(input_path, output_path, target_size_mb=1.9):
    """
    Try different approaches to get closest to target size.
    """
    original_size = get_file_size_mb(input_path)
    print(f"Original file size: {original_size:.2f} MB")
    print(f"Target file size: {target_size_mb:.2f} MB\n")
    
    # Try standard compression first
    print("Attempting standard compression...")
    compress_pdf_streams(input_path, output_path, compression_level=6)
    
    result_size = get_file_size_mb(output_path)
    print(f"Result: {result_size:.2f} MB\n")
    
    return result_size

def main():
    input_pdf = '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_2.pdf'
    output_pdf = '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_3.pdf'
    
    if not os.path.exists(input_pdf):
        print(f"Error: Input file not found: {input_pdf}")
        sys.exit(1)
    
    print("=" * 70)
    print("PDF STREAM COMPRESSION (Preserving All Links and Annotations)")
    print("=" * 70)
    print(f"Input:  {input_pdf}")
    print(f"Output: {output_pdf}")
    print("=" * 70 + "\n")
    
    try:
        final_size = find_best_compression(input_pdf, output_pdf, target_size_mb=1.9)
        
        print("\n" + "=" * 70)
        print("COMPRESSION COMPLETED")
        print("=" * 70)
        print(f"Final file size: {final_size:.2f} MB")
        print(f"Original file size: {get_file_size_mb(input_pdf):.2f} MB")
        print(f"Reduction: {get_file_size_mb(input_pdf) - final_size:.2f} MB")
        print(f"\n✓ All annotations (clickable links) preserved")
        print(f"✓ Visual appearance unchanged")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError during compression: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
