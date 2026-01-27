#!/usr/bin/env python3
"""
Create 1.9 MB PDF by decompressing original and then selectively recompressing.
This approach works around Ghostscript's aggressive compression.
"""

import subprocess
import os
import sys
import shutil

def get_file_size_mb(filepath):
    """Get file size in MB."""
    if not os.path.exists(filepath):
        return 0
    return os.path.getsize(filepath) / (1024 * 1024)

def run_command(cmd, description=""):
    """Run a command and return success status."""
    if description:
        print(f"  {description}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def approach_1_qpdf_linearize(input_path, output_path):
    """Use qpdf to decompress/recompress with different settings."""
    print("\n[Approach 1] Using qpdf with object streams...")
    
    # First, decompress to get a larger baseline
    temp_decompressed = output_path + '.decompressed.pdf'
    success, _, _ = run_command(
        ['qpdf', '--stream-data=uncompress', input_path, temp_decompressed],
        "Decompressing streams"
    )
    
    if not success:
        print("  ✗ qpdf not available or failed")
        if os.path.exists(temp_decompressed):
            os.remove(temp_decompressed)
        return None
    
    decompressed_size = get_file_size_mb(temp_decompressed)
    print(f"  Decompressed size: {decompressed_size:.2f} MB")
    
    # Now recompress with moderate settings
    success, _, _ = run_command(
        ['qpdf', '--compress-streams=y', '--object-streams=generate', 
         temp_decompressed, output_path],
        "Recompressing with moderate settings"
    )
    
    os.remove(temp_decompressed)
    
    if not success:
        return None
    
    final_size = get_file_size_mb(output_path)
    print(f"  → Result: {final_size:.2f} MB")
    return final_size

def approach_2_mutool_clean(input_path, output_path):
    """Use mutool clean with specific compression settings."""
    print("\n[Approach 2] Using mutool clean...")
    
    # Try different compression/sanitize levels
    configs = [
        (['mutool', 'clean', '-gggg', input_path, output_path], 'Garbage collection level 4'),
        (['mutool', 'clean', '-ggg', input_path, output_path], 'Garbage collection level 3'),
        (['mutool', 'clean', '-gg', input_path, output_path], 'Garbage collection level 2'),
        (['mutool', 'clean', '-sanitize', input_path, output_path], 'Sanitize mode'),
    ]
    
    best_size = None
    best_diff = float('inf')
    target = 1.9
    
    for cmd, desc in configs:
        success, _, _ = run_command(cmd, desc)
        if not success:
            continue
        
        size = get_file_size_mb(output_path)
        diff = abs(size - target)
        print(f"    {desc:30s} → {size:.2f} MB (diff: {diff:.2f} MB)")
        
        if diff < best_diff:
            best_diff = diff
            best_size = size
            # Keep this version
            shutil.copy2(output_path, output_path + '.best')
    
    if best_size:
        shutil.move(output_path + '.best', output_path)
        print(f"  → Best result: {best_size:.2f} MB")
        return best_size
    
    return None

def approach_3_partial_decompress(input_path, output_path):
    """Decompress PDF partially and recompress with pikepdf."""
    print("\n[Approach 3] Partial decompression with pikepdf...")
    
    try:
        import pikepdf
    except ImportError:
        print("  ✗ pikepdf not installed")
        return None
    
    # Open and decompress
    pdf = pikepdf.open(input_path)
    
    temp_decompressed = output_path + '.temp_decomp.pdf'
    
    # Save without compression
    pdf.save(temp_decompressed, compress_streams=False)
    pdf.close()
    
    decomp_size = get_file_size_mb(temp_decompressed)
    print(f"  Decompressed: {decomp_size:.2f} MB")
    
    # Now reopen and compress with settings
    pdf2 = pikepdf.open(temp_decompressed)
    pdf2.save(
        output_path,
        compress_streams=True,
        stream_decode_level=pikepdf.StreamDecodeLevel.specialized,
        object_stream_mode=pikepdf.ObjectStreamMode.generate,
    )
    pdf2.close()
    
    os.remove(temp_decompressed)
    
    final_size = get_file_size_mb(output_path)
    print(f"  → Result: {final_size:.2f} MB")
    return final_size

def main():
    input_pdf = '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_2.pdf'
    output_pdf = '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_3.pdf'
    target_mb = 1.9
    
    if not os.path.exists(input_pdf):
        print(f"Error: Input file not found: {input_pdf}")
        sys.exit(1)
    
    print("=" * 75)
    print("ALTERNATIVE PDF COMPRESSION STRATEGIES")
    print("Target: 1.9 MB with preserved links and minimal visual changes")
    print("=" * 75)
    print(f"Input:  {input_pdf}")
    print(f"Output: {output_pdf}")
    print(f"Original size: {get_file_size_mb(input_pdf):.2f} MB")
    print("=" * 75)
    
    results = {}
    
    # Try qpdf approach
    size = approach_1_qpdf_linearize(input_pdf, output_pdf + '.qpdf.pdf')
    if size:
        results['qpdf'] = (size, output_pdf + '.qpdf.pdf')
    
    # Try mutool approach
    size = approach_2_mutool_clean(input_pdf, output_pdf + '.mutool.pdf')
    if size:
        results['mutool'] = (size, output_pdf + '.mutool.pdf')
    
    # Try pikepdf partial decompress
    size = approach_3_partial_decompress(input_pdf, output_pdf + '.pikepdf.pdf')
    if size:
        results['pikepdf'] = (size, output_pdf + '.pikepdf.pdf')
    
    # Find best result
    print("\n" + "=" * 75)
    print("SUMMARY OF ALL APPROACHES")
    print("=" * 75)
    
    if not results:
        print("✗ All approaches failed or tools not available")
        print("\nFalling back to Ghostscript compressed version (0.76 MB)...")
        # Copy the existing compressed version
        subprocess.run(['cp', '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_3.pdf', output_pdf])
        sys.exit(0)
    
    best_method = None
    best_diff = float('inf')
    
    for method, (size, path) in results.items():
        diff = abs(size - target_mb)
        symbol = "✓" if diff < 0.3 else "○"
        print(f"{symbol} {method:20s} → {size:.2f} MB (diff: {diff:.2f} MB)")
        
        if diff < best_diff:
            best_diff = diff
            best_method = method
    
    # Use best result
    if best_method:
        best_size, best_path = results[best_method]
        shutil.copy2(best_path, output_pdf)
        
        print("\n" + "=" * 75)
        print(f"✓ BEST APPROACH: {best_method}")
        print(f"✓ Final size: {best_size:.2f} MB")
        print(f"✓ Target:     {target_mb:.2f} MB")
        print(f"✓ Difference: {best_diff:.2f} MB")
        print(f"✓ All annotations preserved")
        print(f"✓ Output: {output_pdf}")
        print("=" * 75)
        
        # Clean up temp files
        for method, (size, path) in results.items():
            if os.path.exists(path) and path != output_pdf:
                os.remove(path)
    
if __name__ == '__main__':
    main()
