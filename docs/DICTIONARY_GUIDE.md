# OCR Dictionary Reference Guide

## Overview

The `data/objective_dictionary.json` file is a comprehensive OCR extraction from the objective PDF (`pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf`). It serves as the **master reference** for all visual properties of text elements in the CV.

## Purpose

This dictionary is used to:
1. **Position Correction**: Align text elements to match exact coordinates from the objective
2. **Size Validation**: Ensure font sizes match the target design
3. **Style Reference**: Verify font families and weights (Bold, Italic, Regular)
4. **Layout Guide**: Provide centroids for centering elements within backgrounds

## File Structure

```json
{
  "metadata": {
    "source_file": "path/to/objective.pdf",
    "page_dimensions": {
      "width": 595.27,
      "height": 841.89
    },
    "total_elements": 450
  },
  "dictionary": [
    {
      "text": "EXPERIENCE",
      "location": {
        "x0": 312.4567,           // Left edge
        "top": 156.7890,          // Top edge (PDF coords, top-down)
        "x1": 398.1234,           // Right edge
        "bottom": 168.5432,       // Bottom edge
        "width": 85.6667,         // Width
        "height": 11.7542,        // Height
        "centroid_x": 355.2901,   // Horizontal center
        "centroid_y": 162.6661    // Vertical center
      },
      "style": {
        "font_name": "TrebuchetMS-Bold",
        "font_size": 11.0
      }
    }
  ]
}
```

## Using the Dictionary for Corrections

### 1. Position Correction

**Problem**: A company name "JOBSITY" is misaligned horizontally.

**Solution**:
```python
import json

# Load dictionary
with open('data/objective_dictionary.json', 'r') as f:
    objective = json.load(f)

# Find reference position
target = next(e for e in objective['dictionary'] if 'JOBSITY' in e['text'])
correct_x = target['location']['x0']  # Use left edge

# Update coordinates.json
with open('data/coordinates.json', 'r') as f:
    coords = json.load(f)

for item in coords:
    if 'JOBSITY' in item['text']:
        item['x'] = correct_x  # Apply correction

# Save
with open('data/coordinates.json', 'w') as f:
    json.dump(coords, f, indent=2)
```

### 2. Size Correction

**Problem**: Degree titles appear smaller than the objective.

**Solution**:
```python
# Find reference
target = next(e for e in objective['dictionary'] if 'B.S.' in e['text'])
correct_size = target['style']['font_size']

# Apply to coordinates
for item in coords:
    if 'B.S.' in item['text'] or 'M.S.' in item['text']:
        item['size'] = correct_size
```

### 3. Font Weight Correction

**Problem**: Section headers should be Bold but appear Regular.

**Solution**:
```python
target = next(e for e in objective['dictionary'] if 'EXPERIENCE' in e['text'])
font_name = target['style']['font_name']  # e.g., "TrebuchetMS-Bold"

# Update
for item in coords:
    if item['text'] in ['EXPERIENCE', 'EDUCATION', 'SKILLS']:
        item['bold'] = True if 'Bold' in font_name else False
```

### 4. Centering Elements

**Problem**: Text needs to be centered within a blue rectangle.

**Solution**:
```python
# Use centroid to find the rectangle
text_centroid_y = target['location']['centroid_y']

# Find rectangle closest to this Y position
best_rect = min(rects, key=lambda r: abs(r['top'] + r['height']/2 - text_centroid_y))

# The rectangle should be positioned such that its vertical center matches text_centroid_y
```

## Color Information

**Note**: `pdfplumber` does not extract color information directly. For color corrections:
1. Use external tools (Adobe Acrobat, `pymupdf`) to inspect the objective PDF colors
2. Record color values in `src/config.py` as constants
3. Apply via the `color` field in `coordinates.json` (integer hex format: `0x2B73B3`)

## Maintenance

### Re-generating the Dictionary

If the objective PDF changes:

```bash
cd /home/nicofredes/Desktop/code/CV
python3 << 'EOF'
import pdfplumber
import json

with pdfplumber.open("pdfs/objective/backups/Objetivo_Original_20260129_012245.pdf") as pdf:
    page = pdf.pages[0]
    words = page.extract_words(x_tolerance=2, y_tolerance=2, extra_attrs=['fontname', 'size'])
    
    entries = []
    for w in words:
        entries.append({
            'text': w['text'],
            'location': {
                'x0': round(float(w['x0']), 4),
                'top': round(float(w['top']), 4),
                'centroid_x': round(float(w['x0'] + w['width']/2), 4),
                'centroid_y': round(float(w['top'] + w['height']/2), 4),
                # ... other fields
            },
            'style': {
                'font_name': str(w.get('fontname', 'Unknown')),
                'font_size': round(float(w.get('size', 0)), 2)
            }
        })
    
    with open('data/objective_dictionary.json', 'w') as f:
        json.dump({'metadata': {...}, 'dictionary': entries}, f, indent=2)
EOF
```

## Best Practices

1. **Never modify the dictionary manually** - it should always be regenerated from the source PDF
2. **Use it as read-only reference** - apply corrections to `coordinates.json` and `shapes.json` instead
3. **Search by text content** - use `next(e for e in dict if 'TEXT' in e['text'])` for reliable lookups
4. **Consider partial matches** - "PAPERS & WORKSHOPS" might be split into multiple entries
5. **Validate after changes** - run `python3 main.py` and compare the output visually

## Troubleshooting

**Issue**: Can't find a word in the dictionary  
**Solution**: Check if it's split across multiple entries or uses special characters

**Issue**: Coordinates don't match after applying dictionary values  
**Solution**: Remember coordinate system transformation (PDF top-down vs ReportLab bottom-up)

**Issue**: Font size looks different despite matching the dictionary  
**Solution**: Verify the font file itself is correct and registered in `src/fonts.py`
