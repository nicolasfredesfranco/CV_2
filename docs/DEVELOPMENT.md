# Development Guide

## Setting Up Development Environment

### Prerequisites

- Python 3.8+
- Git
- Virtual environment (recommended)

### Initial Setup

```bash
# Clone repository
git clone https://github.com/nicolasfredesfranco/CV_2.git
cd CV_2

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development tools

# Verify installation
python3 main.py --validate-only
```

## Development Workflow

### 1. Making Changes

#### Modifying Content

**Update personal information:**

Edit `data/coordinates.json`:
```json
{
  "text": "Your Name Here",
  "x": 231.63,
  "y": 83.94,
  "font": "TrebuchetMS-Bold",
  "size": 24.01,
  "color": 2978739,
  "bold": true,
  "italic": false
}
```

**Adjust section headers:**

Edit `data/shapes.json`:
```json
[
  {
    "x": 228,
    "y": 725.64,
    "width": 382,
    "height": 18.34
  }
]
```

#### Testing Changes

```bash
# Generate PDF
python3 main.py

# Verify alignment
python3 tools/verify_alignment.py

# Check colors
python3 tools/compare_colors.py

# Run quality checks
python3 verify_cv_quality.py
```

### 2. Code Standards

#### Python Style

- **PEP 8** compliant
- **Type hints** for all functions
- **Docstrings** for modules, classes, and public functions
- **Line length**: Max 100 characters

#### Formatting

Use Black for consistent formatting:
```bash
black src/ tools/ scripts/
```

#### Linting

```bash
# Flake8
flake8 src/ tools/ scripts/

# pylint
pylint src/ tools/ scripts/
```

### 3. Testing

#### Running Tests

```bash
# All tests
python3 -m pytest tests/

# With coverage
python3 -m pytest --cov=src tests/

# Specific test file
python3 -m pytest tests/test_main.py

# Verbose output
python3 -m pytest -v tests/
```

#### Writing Tests

Example test structure:
```python
import pytest
from src.renderer import CVRenderer

def test_renderer_initialization():
    """Test CVRenderer initializes correctly."""
    renderer = CVRenderer()
    assert renderer is not None
    assert renderer.canvas is not None

def test_invalid_data_raises_error():
    """Test validation catches invalid coordinates."""
    with pytest.raises(ValueError):
        # Test invalid data
        pass
```

## Tools Reference

### Alignment Verification

```bash
python3 tools/verify_alignment.py

# JSON output
python3 tools/verify_alignment.py --json

# Custom PDF
python3 tools/verify_alignment.py --pdf path/to/cv.pdf
```

### Color Comparison

```bash
python3 tools/compare_colors.py
```

Validates that all 4 job title colors match the objective PDF.

### Quality Verification

```bash
python3 verify_cv_quality.py
```

Comprehensive checks including:
- Data validation
- Font verification
- Color accuracy
- Layout consistency

## Modifying Positions

### Understanding Coordinates

**Coordinate system:**
- Origin: Bottom-left corner
- X-axis: Increases right
- Y-axis: Increases upward
- Units: Points (1/72 inch)

**Example positioning:**

```python
{
  "text": "JOBSITY",
  "x": 213.08,    # 213 points from left edge
  "y": 131.69,    # 132 points from bottom
  "size": 14.01   # 14pt font
}
```

### Adjusting Rectangle Alignment

If a section header is misaligned:

1. **Find the text center:**
   ```python
   python3 tools/verify_alignment.py
   ```

2. **Calculate required adjustment:**
   ```
   If text center = 390.62
   And rect center = 388.50
   Delta = +2.12 pixels
   ```

3. **Update `shapes.json`:**
   ```json
   {
     "y": 381.68,  // Move up by 2.12
     "height": 17.88
   }
   ```

4. **Verify:**
   ```bash
   python3 main.py
   python3 tools/verify_alignment.py
   ```

## Color Management

### Color Format

Colors are stored as **decimal RGB**:

```
Hex: #2B73B3
RGB: (43, 115, 179)
Decimal: 2847667
```

**Conversion:**
```python
decimal = (R << 16) | (G << 8) | B
decimal = (43 << 16) | (115 << 8) | 179
decimal = 2847667
```

### Standard Colors

```python
# Name blue
COLOR_NAME = 2978739      # #2D73B3

# Job title blue
COLOR_JOB_TITLE = 2847667  # #2B73B3

# Section header background
COLOR_SECTION_BG = 15790320  # #F0F0F0

# Hyperlinks
COLOR_LINK = 1070028       # #1050CC
```

## Debugging

### Enable Debug Logging

```bash
python3 main.py --debug
```

### Common Issues

#### Fonts Not Loading

**Symptom:** Error: "Font not found"

**Solution:**
```bash
# Verify fonts exist
ls -l data/assets/*.ttf

# Check font paths in fonts.py
```

#### Alignment Issues

**Symptom:** Text not centered in rectangles

**Solution:**
```bash
# Check current alignment
python3 tools/verify_alignment.py

# Compare coordinates
python3 tools/detailed_pdf_comparison.py
```

#### Colors Wrong

**Symptom:** Job titles incorrect color

**Solution:**
```bash
# Verify colors
python3 tools/compare_colors.py

# Check coordinates.json for color values
grep -A2 "Lead Artificial" data/coordinates.json
```

## Git Workflow

### Branch Strategy

```bash
# Create feature branch
git checkout -b feature/update-contact-info

# Make changes
# ... edit files ...

# Stage changes
git add data/coordinates.json

# Commit with descriptive message
git commit -m "Update email address and phone number"

# Push to remote
git push origin feature/update-contact-info
```

### Commit Messages

Follow conventional commits:

```
feat: Add new project to experience section
fix: Correct alignment of SKILLS header
docs: Update README with new examples
refactor: Simplify coordinate validation logic
test: Add tests for color conversion
```

## Performance Profiling

### Measure Generation Time

```bash
time python3 main.py
```

### Profile Code

```python
import cProfile
import pstats

cProfile.run('main()', 'profile_stats')
p = pstats.Stats('profile_stats')
p.sort_stats('cumulative').print_stats(10)
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: CV Generation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest tests/
      - name: Generate CV
        run: python3 main.py
      - name: Verify alignment
        run: python3 tools/verify_alignment.py
```

## Release Process

1. **Update version** in `main.py`
2. **Run all tests**: `pytest tests/`
3. **Verify output**: `python3 main.py && python3 tools/verify_alignment.py`
4. **Update CHANGELOG.md**
5. **Tag release**: `git tag v3.0.0`
6. **Push**: `git push --tags`

## Troubleshooting

### PDF Generation Fails

```bash
# Check data validity
python3 main.py --validate-only

# Enable debug mode
python3 main.py --debug 2>&1 | less
```

### Tests Failing

```bash
# Run specific test with verbose output
python3 -m pytest -vv tests/test_main.py::test_name

# Show print statements
python3 -m pytest -s tests/
```

## Resources

- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)

---

For architecture details, see [ARCHITECTURE.md](ARCHITECTURE.md).
