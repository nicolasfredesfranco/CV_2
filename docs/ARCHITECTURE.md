# Technical Architecture

## Overview

The Professional CV Generator employs a coordinate-based rendering strategy to achieve pixel-perfect PDF generation. This document details the system architecture, design decisions, and implementation patterns.

## System Architecture

### Component Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                      CVGenerator                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Canvas Initialization (ReportLab)               │   │
│  │  - Custom page size: 623.62 x 806.30 pt         │   │
│  │  - Font registration: TrebuchetMS family        │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Shape Renderer                                  │   │
│  │  - Geometric transformations                     │   │
│  │  - Blue bar rendering (24pt height)             │   │
│  │  - RGB color accuracy                           │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Text Renderer                                   │   │
│  │  - Coordinate transformation                     │   │
│  │  - Hyperlink injection                          │   │
│  │  - Font/size/color application                  │   │
│  │  - Bullet point insertion                       │   │
│  └─────────────────────────────────────────────────┘   │
│                          ↓                              │
│  ┌─────────────────────────────────────────────────┐   │
│  │  PDF Output                                      │   │
│  │  outputs/Nicolas_Fredes_CV.pdf                  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## Core Design Patterns

### 1. Coordinate Transformation Pattern

**Problem**: PDF and ReportLab use opposite Y-axis orientations.

**Solution**: Mathematical transformation for all Y-coordinates:

```python
# PDF: Y=0 at top, increases downward
# ReportLab: Y=0 at bottom, increases upward

def transform_coordinate(y_pdf, page_height):
    """
    Converts PDF top-down Y to ReportLab bottom-up Y.
    
    Args:
        y_pdf: Y-coordinate in PDF space (0 = top)
        page_height: Total page height in points
    
    Returns:
        Y-coordinate in ReportLab space (0 = bottom)
    """
    return page_height - y_pdf
```

**Application**:
- Text elements: Direct transformation
- Rectangles: Transform y1 (PDF bottom) to get y (ReportLab bottom)

### 2. Context-Aware Hyperlink Injection

**Problem**: Multiple elements share similar text but require different link targets.

**Solution**: Multi-layer contextual detection:

```python
def detect_hyperlink(text, y_coord):
    """
    Determines hyperlink target based on text content and position.
    
    Strategy:
    1. Exact text matching (email, DOI, Twitter handle)
    2. Y-coordinate disambiguation (GitHub vs LinkedIn)
    
    Args:
        text: Element text content
        y_coord: Element Y-coordinate for positional disambiguation
    
    Returns:
        URL string or None
    """
    if "@gmail.com" in text:
        return "mailto:" + extract_email(text)
    elif "nicolasfredesfranco" in text:
        # Spatial disambiguation
        return "https://github.com/..." if y_coord < 150 else "https://linkedin.com/..."
    # ... additional patterns
```

**Key Insight**: GitHub (Y=145.27) and LinkedIn (Y=156.27) share identical usernames but occupy different vertical positions. The threshold Y=150 provides perfect disambiguation.

### 3. Heuristic Bullet Injection

**Problem**: Extracted coordinate data lacks bullet characters.

**Solution**: Pattern-based bullet insertion:

```python
def should_inject_bullet(element):
    """
    Determines if a text element requires bullet injection.
    
    Heuristics:
    - Located in right column (x > 215, x < 250)
    - Not bold/italic (indicates header/title)
    - Starts with uppercase letter
    - Length > 3 characters
    
    Returns:
        bool: True if bullet should be injected
    """
    is_right_col = 215 < element['x'] < 250
    is_plain_text = not (element.get('bold') or element.get('italic'))
    starts_upper = element['text'][0].isupper() if element['text'] else False
    sufficient_length = len(element['text'].strip()) > 3
    
    return all([is_right_col, is_plain_text, starts_upper, sufficient_length])
```

**Correction**: Bullets shift text left by 8.5pt to maintain alignment with non-bulleted content.

## Data Structures

### Coordinates JSON Schema

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "text": { "type": "string" },
      "x": { "type": "number", "description": "Horizontal position in pt" },
      "y": { "type": "number", "description": "Vertical position (top-down)" },
      "size": { "type": "number", "description": "Font size in pt" },
      "font": { "type": "string", "enum": ["TrebuchetMS", "TrebuchetMS-Bold", "TrebuchetMS-Italic"] },
      "color": { "type": "integer", "description": "RGB packed as int" },
      "bold": { "type": "boolean", "optional": true },
      "italic": { "type": "boolean", "optional": true }
    },
    "required": ["text", "x", "y", "size"]
  }
}
```

### Shapes JSON Schema

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "type": { "type": "string", "enum": ["rect"] },
      "rect": { 
        "type": "array", 
        "items": { "type": "number" },
        "minItems": 4,
        "maxItems": 4,
        "description": "[x0, y0, x1, y1] - top-down coordinates"
      },
      "color": {
        "type": "array",
        "items": { "type": "number", "minimum": 0, "maximum": 1 },
        "minItems": 3,
        "maxItems": 3,
        "description": "[R, G, B] normalized to 0-1"
      }
    },
    "required": ["type", "rect", "color"]
  }
}
```

## Rendering Pipeline

### Stage 1: Initialization

```python
# 1. Load JSON data
coordinates = load_json('data/coordinates.json')
shapes = load_json('data/shapes.json')

# 2. Create canvas with custom geometry
canvas = canvas.Canvas(output_path, pagesize=(623.62, 806.30))

# 3. Register fonts
canvas.registerFont('fonts/trebuc.ttf', 'TrebuchetMS')
canvas.registerFont('fonts/trebucbd.ttf', 'TrebuchetMS-Bold')
canvas.registerFont('fonts/trebucit.ttf', 'TrebuchetMS-Italic')
```

### Stage 2: Shape Rendering

```python
for shape in shapes:
    if shape['type'] == 'rect' and is_blue(shape['color']):
        # 1. Extract rect coordinates
        x0, y0_top, x1, y1_bottom = shape['rect']
        
        # 2. Calculate dimensions
        width = x1 - x0
        height = y1_bottom - y0_top  # Should be 24pt for blue bars
        
        # 3. Transform Y coordinate
        y = PAGE_HEIGHT - y1_bottom  # Bottom edge in ReportLab space
        
        # 4. Render
        canvas.setFillColorRGB(*shape['color'])
        canvas.rect(x0, y, width, height, stroke=0, fill=1)
```

### Stage 3: Text Rendering

```python
for element in coordinates:
    # 1. Transform coordinates
    x = element['x']
    y = PAGE_HEIGHT - element['y']
    
    # 2. Apply corrections
    if x > 380:  # Right-aligned dates
        x -= 1.5
    
    # 3. Bullet injection
    text = element['text']
    if should_inject_bullet(element):
        text = "• " + text
        x -= 8.5
    
    # 4. Hyperlink detection
    url = detect_hyperlink(text, element['y'])
    if url:
        width = canvas.stringWidth(text, font, size)
        canvas.linkURL(url, (x, y-2, x+width, y+size))
    
    # 5. Render text
    canvas.setFont(font, size)
    canvas.setFillColorRGB(*rgb_from_int(element['color']))
    canvas.drawString(x, y, text)
```

### Stage 4: Finalization

```python
canvas.save()
```

## Precision Corrections

### Global Transformations

Applied to ALL elements:

1. **Vertical Upshift**: +8pt (addresses top margin drift)
2. **Name Gap Reduction**: -3pt for elements below name section
3. **Sidebar Alignment**: -2pt horizontal for left column

### Element-Specific Adjustments

- **Blue Bars**: Enforce uniform 24pt height
- **Bullets**: -8.5pt horizontal offset
- **Right Dates**: -1.5pt horizontal correction
- **Link Disambiguation**: Y < 150 threshold

## Font Handling

### TrebuchetMS Family

| Font File | Internal Name | Use Case |
|-----------|---------------|----------|
| `trebuc.ttf` | TrebuchetMS | Regular body text |
| `trebucbd.ttf` | TrebuchetMS-Bold | Headers, job titles |
| `trebucit.ttf` | TrebuchetMS-Italic | Emphasized text |

### Registration

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('TrebuchetMS', 'fonts/trebuc.ttf'))
pdfmetrics.registerFont(TTFont('TrebuchetMS-Bold', 'fonts/trebucbd.ttf'))
pdfmetrics.registerFont(TTFont('TrebuchetMS-Italic', 'fonts/trebucit.ttf'))
```

## Color System

### RGB Conversion

Coordinates JSON stores colors as packed integers:

```python
def rgb_from_int(color_int):
    """
    Converts packed integer to normalized RGB tuple.
    
    Args:
        color_int: RGB packed as (R << 16) | (G << 8) | B
    
    Returns:
        (r, g, b): Normalized 0-1 floats
    
    Example:
        color_int = 1048346  # RGB(15, 251, 202)
        rgb = rgb_from_int(color_int)
        # Returns: (0.059, 0.318, 0.792)
    """
    r = ((color_int >> 16) & 0xFF) / 255.0
    g = ((color_int >> 8) & 0xFF) / 255.0
    b = (color_int & 0xFF) / 255.0
    return (r, g, b)
```

### Blue Bar Color

```python
BLUE_COLOR = (0.059, 0.318, 0.792)  # RGB(15, 81, 202)
```

This exact shade is filtered during shape rendering to ensure only blue header bars are drawn.

## Error Handling

### Font Loading

```python
try:
    canvas.drawString(x, y, text)
except Exception as e:
    print(f"⚠️ Error drawing '{text}': {e}")
    # Continue rendering remaining elements
```

### Graceful Degradation

- Missing fonts: Falls back to default ReportLab fonts
- Invalid coordinates: Skips element, logs warning
- Malformed JSON: Raises explicit error before rendering

## Performance Characteristics

- **Rendering Time**: ~100-200ms for single-page CV
- **Memory Usage**: ~10MB peak (font loading + canvas)
- **File Size**: ~25KB output PDF

## Future Enhancement Opportunities

1. **Multi-Page Support**: Extend coordinate transformation for page breaks
2. **Template System**: Parameterize colors/fonts for multiple CV styles
3. **Validation Layer**: JSON schema validation before rendering
4. **Compression**: Optimize PDF output size with ReportLab compression flags

---

**Architecture designed and implemented by Nicolás Ignacio Fredes Franco.**
