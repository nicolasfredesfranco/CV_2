#!/usr/bin/env python3
"""
🔒 CV Column Integrity Validator
Ensures that modifications respect the LEFT/RIGHT column boundary.

CRITICAL RULE:
- LEFT column (X < 200): Modifications allowed
- RIGHT column (X ≥ 200): FROZEN - NO modifications allowed
"""

import json
import sys
from typing import List, Dict, Tuple

# Column boundaries (from analysis)
LEFT_COLUMN_MAX_X = 158.04
RIGHT_COLUMN_MIN_X = 213.08
BOUNDARY_THRESHOLD = 200.0  # Simplified threshold

class ColumnViolation(Exception):
    """Raised when a modification violates the frozen right column rule."""
    pass


def load_coordinates(filepath: str) -> List[Dict]:
    """Load coordinates from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_column_distribution(coords: List[Dict]) -> Dict:
    """Analyze the distribution of elements across columns."""
    left_elements = [e for e in coords if e['x'] < BOUNDARY_THRESHOLD]
    right_elements = [e for e in coords if e['x'] >= BOUNDARY_THRESHOLD]
    
    return {
        'left_column': {
            'count': len(left_elements),
            'x_range': (
                min(e['x'] for e in left_elements),
                max(e['x'] for e in left_elements)
            ),
            'elements': left_elements
        },
        'right_column': {
            'count': len(right_elements),
            'x_range': (
                min(e['x'] for e in right_elements),
                max(e['x'] for e in right_elements)
            ),
            'elements': right_elements
        }
    }


def compare_columns(
    original: List[Dict], 
    modified: List[Dict]
) -> Tuple[List[str], List[str]]:
    """
    Compare original and modified coordinates.
    Returns (left_changes, right_changes) lists of change descriptions.
    """
    left_changes = []
    right_changes = []
    
    # Create lookup dictionaries
    orig_dict = {i: elem for i, elem in enumerate(original)}
    mod_dict = {i: elem for i, elem in enumerate(modified)}
    
    # Check for changes in existing elements
    for i in range(min(len(original), len(modified))):
        orig = orig_dict[i]
        mod = mod_dict[i]
        
        # Skip if identical
        if orig == mod:
            continue
        
        # Determine which column
        is_right_column = orig['x'] >= BOUNDARY_THRESHOLD
        change_desc = f"Element {i}: '{orig['text'][:30]}' at X={orig['x']:.2f}"
        
        # Check what changed
        changes = []
        if orig['x'] != mod['x']:
            changes.append(f"X: {orig['x']:.2f} → {mod['x']:.2f}")
        if orig['y'] != mod['y']:
            changes.append(f"Y: {orig['y']:.2f} → {mod['y']:.2f}")
        if orig.get('size') != mod.get('size'):
            changes.append(f"Size: {orig.get('size')} → {mod.get('size')}")
        if orig.get('text') != mod.get('text'):
            changes.append(f"Text modified")
        
        if changes:
            change_desc += f" - Changes: {', '.join(changes)}"
            
            if is_right_column:
                right_changes.append(change_desc)
            else:
                left_changes.append(change_desc)
    
    # Check for added/removed elements
    if len(modified) > len(original):
        for i in range(len(original), len(modified)):
            elem = modified[i]
            is_right = elem['x'] >= BOUNDARY_THRESHOLD
            desc = f"NEW Element {i}: '{elem['text'][:30]}' at X={elem['x']:.2f}"
            if is_right:
                right_changes.append(desc)
            else:
                left_changes.append(desc)
    
    if len(original) > len(modified):
        for i in range(len(modified), len(original)):
            elem = original[i]
            is_right = elem['x'] >= BOUNDARY_THRESHOLD
            desc = f"DELETED Element {i}: '{elem['text'][:30]}' at X={elem['x']:.2f}"
            if is_right:
                right_changes.append(desc)
            else:
                left_changes.append(desc)
    
    return left_changes, right_changes


def validate_modifications(
    original_path: str,
    modified_path: str,
    strict: bool = True
) -> bool:
    """
    Validate that modifications only affect the left column.
    
    Args:
        original_path: Path to original coordinates.json
        modified_path: Path to modified coordinates.json
        strict: If True, raise exception on right column changes
    
    Returns:
        True if validation passes, False otherwise
    """
    original = load_coordinates(original_path)
    modified = load_coordinates(modified_path)
    
    left_changes, right_changes = compare_columns(original, modified)
    
    print("=" * 70)
    print("🔍 CV COLUMN INTEGRITY VALIDATION")
    print("=" * 70)
    
    # Report left column changes (allowed)
    if left_changes:
        print(f"\n✅ LEFT COLUMN Changes (ALLOWED): {len(left_changes)}")
        for change in left_changes[:10]:  # Show first 10
            print(f"  • {change}")
        if len(left_changes) > 10:
            print(f"  ... and {len(left_changes) - 10} more")
    else:
        print("\n✅ LEFT COLUMN: No changes detected")
    
    # Report right column changes (FORBIDDEN)
    if right_changes:
        print(f"\n❌ RIGHT COLUMN Changes (FORBIDDEN): {len(right_changes)}")
        for change in right_changes:
            print(f"  ⚠️  {change}")
        
        print("\n" + "=" * 70)
        print("🚨 VALIDATION FAILED: Right column modifications detected!")
        print("=" * 70)
        print("RULE VIOLATION: The right column (X ≥ 200) must remain FROZEN.")
        print("Only the left column (X < 200) can be modified.")
        print("=" * 70)
        
        if strict:
            raise ColumnViolation(
                f"{len(right_changes)} forbidden modifications detected in right column"
            )
        return False
    else:
        print("\n✅ RIGHT COLUMN: No changes detected (FROZEN - CORRECT)")
    
    print("\n" + "=" * 70)
    print("✅ VALIDATION PASSED: All modifications respect column boundaries")
    print("=" * 70)
    
    return True


def main():
    """CLI interface for validation."""
    if len(sys.argv) < 2:
        print("Usage: python validate_column_integrity.py <modified_coordinates.json>")
        print("   Or: python validate_column_integrity.py <original.json> <modified.json>")
        sys.exit(1)
    
    if len(sys.argv) == 2:
        # Compare against baseline
        original_path = "data/coordinates.json"
        modified_path = sys.argv[1]
    else:
        original_path = sys.argv[1]
        modified_path = sys.argv[2]
    
    try:
        validate_modifications(original_path, modified_path, strict=True)
        sys.exit(0)
    except ColumnViolation as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
