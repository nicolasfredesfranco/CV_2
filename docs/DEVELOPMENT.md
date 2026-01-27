# 💻 Development Guide

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Code Guidelines](#code-guidelines)
- [Testing](#testing)
- [Debugging](#debugging)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)
- [Release Process](#release-process)

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed
- **Git** for version control
- **pip** package manager
- **virtualenv** (recommended)

**Check versions:**
```bash
python3 --version  # Should be >= 3.8
git --version
pip --version
```

### Quick Setup

```bash
# 1. Clone repository
git clone https://github.com/nicolasfredesfranco/CV.git
cd CV

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run generation test
python3 main.py

# 5. Verify output
ls -lh outputs/Nicolas_Fredes_CV.pdf
```

---

## Development Environment Setup

### Recommended IDE Setup

#### VS Code

**Extensions:**
- Python (Microsoft)
- Pylance
- autoDocstring
- GitLens
- Markdown All in One

**Settings (`.vscode/settings.json`):**
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "editor.formatOnSave": true,
  "editor.rulers": [100],
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  }
}
```

#### PyCharm

**Configuration:**
1. File → Settings → Project → Python Interpreter
2. Add virtualenv interpreter
3. Enable Flake8 inspection
4. Set line length to 100

### Development Dependencies

Install additional development tools:

```bash
pip install black flake8 mypy pytest pytest-cov
```

**Tools:**
- **black**: Code formatter
- **flake8**: Linter
- **mypy**: Type checker
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting

---

## Project Structure

### File Organization

```
CV/
├── main.py                    # 🎯 CORE: Main generation engine
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies (optional)
│
├── data/                      # 🔒 IMMUTABLE: Golden data
│   ├── coordinates.json       # ⚠️ DO NOT EDIT manually
│   ├── shapes.json            # ⚠️ DO NOT EDIT manually
│   └── assets/                # Font files
│
├── config/                    # Configuration files
│   ├── generation_config.json      # Current config
│   └── generation_config_best.json # Best achieved
│
├── outputs/                   # Generated files (gitignored)
├── pdfs/                      # Organized PDFs
├── scripts/                   # Utility scripts
├── legacy/                    # Legacy/development scripts
├── docs/                      # Documentation
├── analysis/                  # Analysis reports
└── archive/                   # Historical data
```

### Key Files to Know

| File | Purpose | Modify? |
|------|---------|---------|
| `main.py` | Core engine | ✅ Yes |
| `data/coordinates.json` | Golden data | ❌ No (regenerate if needed) |
| `data/shapes.json` | Golden data | ❌ No (regenerate if needed) |
| `config/generation_config.json` | Offset config | ✅ Yes (via iteration) |
| `requirements.txt` | Dependencies | ✅ Yes (carefully) |
| `README.md` | Main docs | ✅ Yes |

---

## Code Guidelines

### Style Guide

This project follows **PEP 8** with modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes preferred (`"text"`)
- **Docstrings**: Google style

### Formatting with Black

```bash
# Format single file
black main.py

# Format all Python files
black .

# Check without modifying
black --check main.py
```

### Linting with Flake8

```bash
# Lint main.py
flake8 main.py --max-line-length=100

# Lint all files
flake8 . --max-line-length=100 --exclude=venv,legacy

# Common useful flags
flake8 main.py --max-line-length=100 --ignore=E203,W503
```

**Ignored Warnings:**
- `E203`: Whitespace before ':' (conflicts with black)
- `W503`: Line break before binary operator (PEP 8 update)

### Type Hints

**Encouraged but not required.** Example:

```python
from typing import List, Dict, Tuple

def rgb_from_int(color_int: int) -> Tuple[float, float, float]:
    """Convert integer color to RGB tuple."""
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return (r/255.0, g/255.0, b/255.0)
```

### Docstring Format

Use **Google style** docstrings:

```python
def transform_coordinate(x: float, y: float, page_height: float) -> Tuple[float, float]:
    """Transform PDF coordinates to ReportLab space.
    
    Args:
        x: X coordinate in PDF space
        y: Y coordinate in PDF space (top-down)
        page_height: Height of page in points
    
    Returns:
        Tuple of (x, y_reportlab) in ReportLab space (bottom-up)
    
    Example:
        >>> transform_coordinate(100, 50, 841.89)
        (100, 791.89)
    """
    return (x, page_height - y)
```

---

## Testing

### Manual Testing

**Basic smoke test:**
```bash
python3 main.py
ls -lh outputs/Nicolas_Fredes_CV.pdf
# Expected: File exists, ~68KB
```

**Link verification:**
```bash
python3 scripts/verification/verify_links.py
# Expected: All 5 links found
```

**Visual comparison:**
```bash
cd legacy
python3 1_deploy_side_by_side.py
# Opens side-by-side comparison
```

### Automated Testing (Future)

**Test structure (proposed):**
```
tests/
├── test_coordinate_transform.py
├── test_rgb_conversion.py
├── test_font_loading.py
└── test_generation.py
```

**Example test:**
```python
import pytest
from main import rgb_from_int

def test_rgb_from_int():
    assert rgb_from_int(0) == (0.0, 0.0, 0.0)  # Black
    assert rgb_from_int(16777215) == (1.0, 1.0, 1.0)  # White
    
    # Blue header color
    result = rgb_from_int(2978739)
    assert result[0] == pytest.approx(0.176, abs=0.001)
    assert result[1] == pytest.approx(0.451, abs=0.001)
    assert result[2] == pytest.approx(0.702, abs=0.001)
```

**Run tests:**
```bash
pytest
pytest --cov=main  # With coverage
```

---

## Debugging

### Common Debugging Techniques

#### 1. **Print Debugging**

Add temporary print statements:

```python
def _draw_elements(self, c, page_height):
    for elem in self.elements:
        print(f"DEBUG: Rendering {elem['text']} at ({elem['x']}, {elem['y']})")
        # ... rendering logic
```

#### 2. **Interactive Debugging (pdb)**

```python
import pdb

def _draw_elements(self, c, page_height):
    for elem in self.elements:
        if elem['text'] == "PROBLEMATIC TEXT":
            pdb.set_trace()  # Breakpoint here
        # ... rendering logic
```

**In debugger:**
```
(Pdb) print(elem)
(Pdb) print(page_height)
(Pdb) n  # Next line
(Pdb) c  # Continue
```

#### 3. **Visual Debugging**

Render bounding boxes for elements:

```python
# Add before drawing text
c.setStrokeColorRGB(1, 0, 0)  # Red
c.setLineWidth(0.5)
c.rect(x, y, 50, size, stroke=1, fill=0)  # Hitbox visualization
```

### Logging

**Enable detailed logging:**

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def _draw_elements(self, c, page_height):
    logger.debug(f"Processing {len(self.elements)} elements")
    for elem in self.elements:
        logger.debug(f"Element: {elem['text']}")
        # ... logic
```

---

## Common Tasks

### Task 1: Add a New Precision Patch

**Example:** Add italic text compensation

```python
def _draw_elements(self, c, page_height):
    for elem in self.elements:
        # ... existing code
        
        # NEW PATCH: Italic compensation
        is_italic = elem.get('italic', False)
        if is_italic:
            x += 0.5  # Slight right shift for italics
        
        c.drawString(x, y, text)
```

**Steps:**
1. Identify the issue (e.g., italics render off)
2. Add detection logic
3. Apply correction
4. Test visually
5. Measure impact on score

### Task 2: Extract Coordinates from New PDF

```bash
cd scripts/extraction

# Using pdfminer
python3 extract_text_coords.py new_target.pdf > new_coords.json

# Manually review and clean
# Replace data/coordinates.json with new_coords.json
```

### Task 3: Update Font Mapping

**Edit `main.py`:**

```python
FONT_PATHS = {
    'TrebuchetMS': 'data/assets/trebuc.ttf',
    'TrebuchetMS-Bold': 'data/assets/trebucbd.ttf',
    'TrebuchetMS-Italic': 'data/assets/trebucit.ttf',
    'AbyssinicaSIL-Regular': '/usr/share/fonts/truetype/abyssinica/AbyssinicaSIL-Regular.ttf',  # NEW
}

FONT_MAPPING = {
    'AbyssinicaSIL-Regular': 'AbyssinicaSIL-Regular',  # Use exact font
    # ... existing mappings
}
```

### Task 4: Run Iterative Optimization

```bash
cd legacy

# Run 100 iterations targeting 93.5%
python3 iterate_master.py 100 0.935

# Monitor progress
tail -f iteration.log
```

### Task 5: Compress PDF to Target Size

```bash
cd scripts/compression

# Compress to 1.9 MB
python3 compress_to_1_9mb.py

# Multi-strategy compression
python3 compress_multi_strategy.py input.pdf
```

---

## Troubleshooting

### Issue: "Font not found"

**Symptoms:**
```
⚠️ Warning: Could not load font TrebuchetMS-Bold
```

**Solution:**
```bash
# Verify font file exists
ls -lh data/assets/trebucbd.ttf

# Check file permissions
chmod 644 data/assets/*.ttf

# Verify path in main.py FONT_PATHS
```

### Issue: "PDF not generated"

**Symptoms:**
```
Generating CV to /path/to/outputs/Nicolas_Fredes_CV.pdf...
(no output file created)
```

**Debugging:**
```bash
# Check outputs directory exists
ls -ld outputs/

# Create if missing
mkdir -p outputs

# Check write permissions
ls -ld outputs/
```

### Issue: "Coordinates seem offset"

**Symptoms:** All text renders but appears shifted

**Diagnosis:**
1. Check page size: `pdfinfo pdfs/objective/Objetivo_No_editar.pdf`
2. Verify PAGE_HEIGHT matches in `main.py`
3. Confirm coordinate transformation logic

**Solution:**
```python
# Adjust PAGE_HEIGHT if different from A4
PAGE_HEIGHT = 841.89  # Standard A4
# PAGE_HEIGHT = 792.0  # Letter size

# Update transformation
y = PAGE_HEIGHT - elem['y']
```

### Issue: "Similarity score stuck at X%"

**Diagnosis:**
- Stuck < 85%: Coordinate extraction errors or wrong page size
- Stuck 85-90%: Section offset misalignment
- Stuck 90-93%: Font/rendering differences
- Stuck >93%: Structural limit reached

**Solutions:**
- < 90%: Run iterative optimization (`iterate_master.py`)
- 90-93%: Fine-tune section offsets manually
- > 93%: Install exact fonts or accept limit

---

## Release Process

### Versioning

This project uses **Semantic Versioning** (SemVer):

- **MAJOR**: Breaking changes (e.g., data format change)
- **MINOR**: New features (e.g., new precision patch)
- **PATCH**: Bug fixes (e.g., coordinate calculation fix)

**Example:** `v1.2.3` = Major 1, Minor 2, Patch 3

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `main.py` (if version constant exists)
- [ ] Git tag created: `git tag v1.2.3`
- [ ] Tag pushed: `git push origin v1.2.3`
- [ ] GitHub release created with notes

### Creating a Release

```bash
# 1. Update version
# Edit main.py or VERSION file

# 2. Update CHANGELOG.md
# Add new section for version

# 3. Commit changes
git add .
git commit -m "Release v1.2.3"

# 4. Create tag
git tag -a v1.2.3 -m "Version 1.2.3: Description"

# 5. Push
git push origin main
git push origin v1.2.3

# 6. Create GitHub release
# Use GitHub web UI or gh CLI
```

---

## Best Practices

### Do's ✅

- **Do** test changes locally before committing
- **Do** write descriptive commit messages
- **Do** update documentation when changing behavior
- **Do** use meaningful variable names
- **Do** add comments for complex logic
- **Do** maintain backward compatibility when possible

### Don'ts ❌

- **Don't** commit `outputs/` directory contents
- **Don't** modify `data/coordinates.json` manually
- **Don't** hard-code paths (use `os.path.join`)
- **Don't** commit credentials or sensitive data
- **Don't** break existing functionality without strong reason

---

## Resources

### Documentation

- [README.md](../README.md) - Project overview
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

### External Resources

- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [PDF Reference](https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)

### Tools

- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- [pdfminer.six](https://pdfminer-docs.readthedocs.io/)
- [pikepdf](https://pikepdf.readthedocs.io/)

---

## Getting Help

### Community

- **GitHub Issues**: [Open an issue](https://github.com/nicolasfredesfranco/CV/issues)
- **Discussions**: [GitHub Discussions](https://github.com/nicolasfredesfranco/CV/discussions)

### Contact

- **Email**: nico.fredes.franco@gmail.com
- **LinkedIn**: [nicolasfredesfranco](https://www.linkedin.com/in/nicolasfredesfranco)

---

**Happy Coding! 🚀**
