# Professional CV Generator

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-25/25%20passing-success.svg)](test_main.py)
[![Visual Match](https://img.shields.io/badge/visual%20match-100%25-brightgreen.svg)](#visual-fidelity)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](#)

**Professional CV/Resume Generator** with 100% visual fidelity, vector-perfect PDF output, and automated quality assurance.

<p align="center">
  <img src="examples/cv_preview.png" alt="Generated CV Preview" width="700">
</p>

<p align="center">
  <a href="outputs/Nicolas_Fredes_CV.pdf">📄 Download CV (PDF)</a> •
  <a href="#quick-start">🚀 Quick Start</a> •
  <a href="#documentation">📖 Documentation</a>
</p>

---

## ✨ Key Features

- ✅ **100% Visual Match** - Generated output matches reference PDF exactly
- ✅ **Vector PDF** - Searchable text, clickable hyperlinks, perfect zoom quality
- ✅ **Modular Architecture** - Clean, maintainable, extensible codebase
- ✅ **Automated Testing** - 25/25 tests passing, continuous validation
- ✅ **Professional Quality** - Production-ready for job applications
- ✅ **Easy Customization** - JSON-based data, centralized configuration

---

## 🎯 Visual Fidelity

The generator achieves **100% visual match** with the reference PDF:

<p align="center">
  <img src="outputs/FINAL_100PCT_MATCH.png" alt="100% Match Verification" width="800">
</p>

**Verification Method**: Pixel-by-pixel comparison of rendered PDFs at 200 DPI  
**Result**: Perfect visual equality

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/nicolasfredesfranco/CV.git
cd CV

# Install dependencies
pip install -r requirements.txt

# Generate CV
python main.py

# Output: outputs/Nicolas_Fredes_CV.pdf
```

**Generated in < 1 second** ⚡

---

## 📁 Project Structure

```
CV/
├── main.py                # Entry point - generates CV
├── src/                   # Source code modules
│   ├── config.py         # Configuration & constants
│   ├── renderer.py       # PDF rendering engine
│   ├── transformer.py    # Coordinate transformations
│   ├── validator.py      # Data validation
│   ├── font_manager.py   # Font loading & caching
│   ├── hyperlink_handler.py  # Link management
│   └── logger.py         # Structured logging
├── data/                  # Input data
│   ├── coordinates.json  # Text positions & content
│   ├── shapes.json       # Background shapes
│   └── fonts/            # TrueType fonts
├── pdfs/objective/        # Reference PDF
├── outputs/               # Generated PDFs
├── examples/              # Sample outputs & previews
├── tools/                 # Analysis & optimization utilities
├── test_main.py          # Test suite (25 tests)
└── README.md             # This file
```

---

## 🔧 Configuration

All parameters centralized in [`src/config.py`](src/config.py):

```python
class CVConfig:
    # Page dimensions (PDF points)
    PAGE_WIDTH: float = 623.0
    PAGE_HEIGHT: float = 806.0
    
    # Corporate blue RGB(43,115,179)
    COLOR_PRIMARY_BLUE = (0.168627, 0.450980, 0.701961)
    
    # Global Y-axis offset (fine-tuned)
    Y_GLOBAL_OFFSET: float = 32.6
```

---

## 🧪 Testing & Quality Assurance

```bash
# Install dev dependencies
pip install pytest

# Run all tests
pytest test_main.py -v

# Expected output: ✅ 25 passed, 1 skipped
```

**Test Coverage**:
- ✅ Configuration validation  
- ✅ Data loading & validation
- ✅ Coordinate transformations
- ✅ PDF generation
- ✅ Font management
- ✅ Hyperlink handling

---

## 📊 Technical Specifications

| Feature | Specification |
|---------|--------------|
| **Output Format** | PDF 1.4 (Vector) |
| **File Size** | 67 KB |
| **Page Size** | 623 × 806 points |
| **Fonts** | TrueType (embedded) |
| **Links** | Fully clickable ✅ |
| **Text** | Searchable & selectable ✅ |
| **Generation Time** | < 1 second ⚡ |
| **Visual Match** | 100% ✅ |

---

## 🎨 Customization Guide

### Update Content

Edit [`data/coordinates.json`](data/coordinates.json):

```json
{
  "text": "Your Name",
  "x": 100.0,
  "y": 50.0,
  "fontname": "OpenSans-Bold",
  "fontsize": 24.0
}
```

### Modify Colors

Update [`src/config.py`](src/config.py):

```python
COLOR_PRIMARY_BLUE = (0.168627, 0.450980, 0.701961)  # RGB(43,115,179)
```

### Adjust Layout

Fine-tune vertical alignment in [`src/config.py`](src/config.py):

```python
Y_GLOBAL_OFFSET: float = 32.6  # Adjust as needed
```

---

## 🛠️ Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest test_main.py -v

# Format code
black src/ main.py

# Type checking
mypy src/
```

---

## 📚 Documentation

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines & workflow
- **[CHANGELOG.md](CHANGELOG.md)** - Version history & release notes
- **[tools/](tools/)** - Analysis & optimization utilities

### Tools Available

- `visual_human_compare.py` - Human-perceptible difference analysis
- `smart_visual_corrector.py` - Automated parameter optimization
- `compare_precise.py` - Pixel-perfect comparison utilities

---

## 🔗 Author

**Nicolás Ignacio Fredes Franco**

- 📧 Email: nicofredesfranco@gmail.com
- 💼 LinkedIn: [nicolasfredesfranco](https://www.linkedin.com/in/nicolasfredesfranco/)
- 🐙 GitHub: [nicolasfredesfranco](https://github.com/nicolasfredesfranco)
- 📍 Location: Viña del Mar, Chile

---

## 📄 License

This project is proprietary software created by Nicolás Ignacio Fredes Franco.

---

## 🙏 Acknowledgments

Built with professional-grade libraries:

- [ReportLab](https://www.reportlab.com/) - Industry-standard PDF generation
- [pdf2image](https://github.com/Belval/pdf2image) - High-quality PDF rendering
- [Pillow](https://python-pillow.org/) - Advanced image processing
- [pdfplumber](https://github.com/jsvine/pdfplumber) - PDF analysis

---

<p align="center">
  <strong>Professional CV Generator v3.0.2</strong>
</p>

<p align="center">
  Developed by <a href="https://www.linkedin.com/in/nicolasfredesfranco/">Nicolás Fredes Franco</a>
</p>

<p align="center">
  <a href="outputs/Nicolas_Fredes_CV.pdf">📥 Download My CV</a>
</p>
