#!/usr/bin/env python3
"""
Output Verification Script
Ensures CV generation produces IDENTICAL output after any refactoring

Author: Nicolás Ignacio Fredes Franco
"""

import subprocess
import hashlib
from pathlib import Path

def get_file_hash(filepath):
    """Calculate MD5 hash of file"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def verify_output_unchanged():
    """Verify that generated CV matches reference"""
    
    print("="*80)
    print("CV OUTPUT VERIFICATION")
    print("="*80)
    
    # Read reference hash
    reference_file = Path("outputs/REFERENCE_HASH.txt")
    if not reference_file.exists():
        print("❌ ERROR: Reference hash not found!")
        print("   Run: md5sum outputs/Nicolas_Fredes_CV.pdf > outputs/REFERENCE_HASH.txt")
        return False
    
    with open(reference_file, 'r') as f:
        reference_hash = f.read().strip().split()[0]
    
    print(f"\nReference Hash: {reference_hash}")
    
    # Generate fresh CV
    print("\nGenerating fresh CV...")
    result = subprocess.run(['python', 'main.py'], capture_output=True)
    
    if result.returncode != 0:
        print(f"❌ ERROR: CV generation failed!")
        print(result.stderr.decode())
        return False
    
    # Calculate current hash
    current_hash = get_file_hash("outputs/Nicolas_Fredes_CV.pdf")
    print(f"Current Hash:   {current_hash}")
    
    # Compare
    print("\n" + "="*80)
    if current_hash == reference_hash:
        print("✅ OUTPUT UNCHANGED - CV is IDENTICAL to reference")
        print("="*80)
        return True
    else:
        print("❌ OUTPUT CHANGED - CV differs from reference!")
        print("="*80)
        print("\n⚠️  CRITICAL: Refactoring has altered the generated PDF")
        print("   This violates the requirement to preserve output")
        print("   Please revert changes that modified the output")
        return False

if __name__ == "__main__":
    success = verify_output_unchanged()
    exit(0 if success else 1)
