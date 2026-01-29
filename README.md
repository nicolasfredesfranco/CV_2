# Professional CV Generator

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-success.svg)](test_main.py)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](#)

**Automated CV/Resume Generator** with vector-perfect PDF output, modular architecture, and professional quality rendering.

<p align="center">
  <img src="examples/cv_preview.png" alt="Generated CV Preview" width="600">
</p>

<p align="center">
  <a href="outputs/Nicolas_Fredes_CV.pdf">📄 Download Latest CV (PDF)</a>
</p>

---

## ✨ Features

- **Vector PDF Output** - Searchable text, clickable hyperlinks, perfect zoom quality
- **Modular Architecture** - Clean separation: config, rendering, validation, transformations  
- **Automated Testing** - Comprehensive test suite ensuring reliability
- **Professional Quality** - Production-ready output suitable for job applications
- **Easy Customization** - JSON-based data, centralized configuration

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

---

##  📁 Project Structure

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
├── outputs/               # Generated PDFs
├── examples/              # Sample outputs & previews
├── tools/                 # Analysis & optimization utilities
├── test_main.py          # Test suite
└── README.md             # This file
```

---

## 🔧 Configuration

All parameters centralized in [`src/config.py`](src/config.py):

```python
class CVConfig:
    # Page dimensions
    PAGE_WIDTH: float = 623.0
    PAGE_HEIGHT: float = 806.0
    
    # Corporate blue
    COLOR_PRIMARY_BLUE = (0.168627, 0.450980, 0.701961)
    
    # Global Y-axis offset
    Y_GLOBAL_OFFSET: float = 32.6
```

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install pytest

# Run all tests
pytest test_main.py -v

# Expected: 25 passed, 1 skipped
```

---

## 📊 Technical Specifications

| Feature | Specification |
|---------|--------------|
| **Output Format** | PDF 1.4 (Vector) |
| **File Size** | ~68 KB |
| **Page Size** | Letter (8.66" x 11.22") |
| **Fonts** | TrueType (embedded) |
| **Links** | Fully clickable |
| **Text** | Searchable & selectable |
| **Generation Time** | < 1 second |

---

## 🎨 Customization

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

Modify global offset in [`src/config.py`](src/config.py):

```python
Y_GLOBAL_OFFSET: float = 32.6  # Fine-tune vertical alignment
```

---

## 🛠️ Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest test_main.py -v --cov=src

# Format code
black src/ main.py

# Type checking
mypy src/
```

---

## 📝 Documentation

- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guidelines & workflow
- **[CHANGELOG.md](CHANGELOG.md)** - Version history & release notes
- **[tools/](tools/)** - Analysis & optimization utilities

---

## 🔗 Author

**Nicolás Ignacio Fredes Franco**

- 📧 Email: nicofredesfranco@gmail.com
- 💼 LinkedIn: [nicolasfredesfranco](https://www.linkedin.com/in/nicolasfredesfranco/)
- 🐙 GitHub: [nicolasfredesfranco](https://github.com/nicolasfredesfranco)

---

## 📄 License

This project is proprietary software created by and for Nicolás Ignacio Fredes Franco.

---

## 🙏 Acknowledgments

Built with:
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [pdf2image](https://github.com/Belval/pdf2image) - PDF rendering  
- [Pillow](https://python-pillow.org/) - Image processing

---

<p align="center">
  Made with ❤️ by Nicolás Fredes Franco
</p>

<p align="center">
  <a href="outputs/Nicolas_Fredes_CV.pdf">📥 Download My CV</a>
</p>
