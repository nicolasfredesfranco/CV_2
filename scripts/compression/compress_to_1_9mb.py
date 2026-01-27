#!/usr/bin/env python3
"""
Reduce PDF quality minimally to achieve 1.9 MB target.
Preserves all clickable links and maintains near-identical visual appearance.
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

def compress_with_settings(input_path, output_path, preset=None, custom_params=None):
    """
    Compress PDF with specific Ghostscript settings.
    
    Args:
        input_path: Source PDF
        output_path: Destination PDF
        preset: PDFSETTINGS preset (screen, ebook, printer, prepress, default)
        custom_params: Dict of custom parameters to override
    """
    cmd = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        '-dPreserveAnnots=true',  # CRITICAL: preserve clickable links!
        '-dEmbedAllFonts=true',
        '-dSubsetFonts=true',
    ]
    
    # Add preset if specified
    if preset:
        cmd.append(f'-dPDFSETTINGS=/{preset}')
    
    # Add custom parameters to override preset
    if custom_params:
        for key, value in custom_params.items():
            cmd.append(f'-d{key}={value}')
    
    cmd.extend([
        f'-sOutputFile={output_path}',
        input_path
    ])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def test_compression_configs(input_path, output_path, target_mb=1.9):
    """
    Test multiple compression configurations to find best balance.
    """
    original_size = get_file_size_mb(input_path)
    print(f"Original: {original_size:.2f} MB")
    print(f"Target:   {target_mb:.2f} MB\n")
    
    configs = [
        {
            'name': 'Ebook Quality (High)',
            'preset': 'ebook',
            'params': {
                'ColorImageResolution': 300,
                'GrayImageResolution': 300,
                'MonoImageResolution': 1200,
            }
        },
        {
            'name': 'Ebook Quality (Very High)',
            'preset': 'ebook',
            'params': {
                'ColorImageResolution': 350,
                'GrayImageResolution': 350,
                'MonoImageResolution': 1440,
            }
        },
        {
            'name': 'Default Quality (Custom)',
            'preset': 'default',
            'params': {
                'ColorImageResolution': 250,
                'GrayImageResolution': 250,
                'AutoRotatePages': '/None',
                'ColorConversionStrategy': '/LeaveColorUnchanged',
            }
        },
        {
            'name': 'Screen Quality (Enhanced)',
            'preset': 'screen',
            'params': {
                'ColorImageResolution': 200,
                'GrayImageResolution': 200,
                'MonoImageResolution': 600,
                'AutoRotatePages': '/None',
            }
        },
        {
            'name': 'No Preset (Minimal Compression)',
            'preset': None,
            'params': {
                'CompressFonts': 'true',
                'CompressPages': 'true',
                'AutoRotatePages': '/None',
                'ColorConversionStrategy': '/LeaveColorUnchanged',
            }
        },
    ]
    
    best_config = None
    best_size = None
    best_diff = float('inf')
    results = []
    
    temp_output = output_path + '.tmp'
    
    for i, config in enumerate(configs, 1):
        print(f"[{i}/{len(configs)}] Testing: {config['name']}")
        
        success = compress_with_settings(
            input_path, 
            temp_output, 
            preset=config['preset'],
            custom_params=config['params']
        )
        
        if not success:
            print(f"  ✗ Failed\n")
            continue
        
        size = get_file_size_mb(temp_output)
        diff = abs(size - target_mb)
        
        results.append({
            'config': config,
            'size': size,
            'diff': diff
        })
        
        print(f"  → {size:.2f} MB (diff: {diff:.2f} MB)")
        
        if diff < best_diff:
            best_diff = diff
            best_size = size
            best_config = config
            # Save this as best so far
            shutil.copy2(temp_output, output_path)
        
        print()
    
    # Clean up temp file
    if os.path.exists(temp_output):
        os.remove(temp_output)
    
    return best_config, best_size, results

def main():
    input_pdf = '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_2.pdf'
    output_pdf = '/home/nicofredes/Desktop/code/CV/nueva_version_no_editar_3.pdf'
    
    if not os.path.exists(input_pdf):
        print(f"Error: Input file not found: {input_pdf}")
        sys.exit(1)
    
    print("=" * 75)
    print("PDF QUALITY REDUCTION TO 1.9 MB")
    print("Preserving: All clickable links + Visual appearance")
    print("=" * 75)
    print(f"Input:  {input_pdf}")
    print(f"Output: {output_pdf}")
    print("=" * 75 + "\n")
    
    best_config, best_size, all_results = test_compression_configs(
        input_pdf, 
        output_pdf, 
        target_mb=1.9
    )
    
    print("=" * 75)
    print("COMPRESSION RESULTS")
    print("=" * 75)
    
    if best_config:
        print(f"✓ Best configuration: {best_config['name']}")
        print(f"✓ Final size: {best_size:.2f} MB")
        print(f"✓ Target:     1.90 MB")
        print(f"✓ Difference: {abs(best_size - 1.9):.2f} MB")
        print(f"\n✓ All clickable links preserved (PreserveAnnots=true)")
        print(f"✓ Fonts embedded and compressed")
        print(f"✓ Output saved: {output_pdf}")
        
        # Show all results summary
        print("\n" + "-" * 75)
        print("All tested configurations:")
        print("-" * 75)
        for i, result in enumerate(all_results, 1):
            print(f"{i}. {result['config']['name']:30s} → {result['size']:.2f} MB")
        
        print("=" * 75)
    else:
        print("✗ Compression failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
