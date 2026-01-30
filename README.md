# Professional CV Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A high-precision, Python-based CV/Resume generation engine designed to programmatically create professional PDF documents with pixel-perfect accuracy.

## 🌟 Features

- **🎯 Pixel-Perfect Rendering**: Sub-pixel precision positioning using ReportLab
- **📐 Coordinate-Driven Layout**: JSON-based configuration for ultimate flexibility
- **✅ Quality Verification**: Automated tools to validate alignment and color accuracy
- **🎨 Professional Design**: Clean, minimalist aesthetic with blue accent colors
- **🔧 Modular Architecture**: Separated concerns for easy maintenance and customization
- **📊 Data Validation**: Comprehensive checks for data integrity
- **🚀 Fast Generation**: Optimized rendering with LRU caching

## 📖 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Virtual environment tool

### System Dependencies

For Linux/Ubuntu users:
```bash
sudo apt-get install python3-pip python3-venv
```

### Project Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/nicolasfredesfranco/CV_2.git
   cd CV_2
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python3 main.py --version
   ```

## 🚀 Quick Start

### Generate Your CV

```bash
python3 main.py
```

The generated PDF will be saved to `outputs/Nicolas_Fredes_CV.pdf`.

### Validate Data Only

```bash
python3 main.py --validate-only
```

### Custom Output Path

```bash
python3 main.py --output /path/to/custom_cv.pdf
```

### Enable Debug Logging

```bash
python3 main.py --debug
```

## 📂 Project Structure

```
CV_2/
├── main.py                      # Entry point
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Development dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guidelines
│
├── src/                         # Core application code
│   ├── __init__.py
│   ├── config.py                # Configuration and constants
│   ├── fonts.py                 # Font registration and management
│   ├── renderer.py              # PDF rendering engine
│   ├── shapes.py                # Geometric shape handling
│   └── text.py                  # Text rendering logic
│
├── data/                        # Data files
│   ├── coordinates.json         # Text element coordinates
│   ├── shapes.json              # Rectangle/shape definitions
│   ├── objective_reference.pdf  # Reference design PDF
│   └── assets/                  # Fonts and static files
│       ├── Trebuchet-MS.ttf
│       ├── Trebuchet-MS-Bold.ttf
│       └── Trebuchet-MS-Italic.ttf
│
├── outputs/                     # Generated PDFs
│   └── Nicolas_Fredes_CV.pdf    # Default output
│
├── tools/                       # Development utilities
│   ├── verify_alignment.py      # Rectangle alignment checker
│   ├── compare_colors.py        # Color validation tool
│   └── verify_cv_quality.py     # Overall quality checks
│
├── scripts/                     # Setup and build scripts
│   └── setup_env.py             # Environment configuration
│
├── tests/                       # Unit and integration tests
│   └── test_main.py
│
└── docs/                        # Documentation
    ├── ARCHITECTURE.md          # System architecture (see below)
    ├── DEVELOPMENT.md           # Development guide
    └── API.md                   # API documentation
```

## 💻 Usage

### Command-Line Interface

```bash
usage: main.py [-h] [--output PATH] [--data-dir DIR] [--validate-only] [--debug] [--version]

CV Generator - Professional PDF generation with pixel-perfect precision

optional arguments:
  -h, --help            Show this help message and exit
  --output PATH, -o PATH
                        Custom output PDF file path
  --data-dir DIR, -d DIR
                        Custom data directory path
  --validate-only, -v   Validate JSON data without generating PDF
  --debug               Enable debug logging for detailed output
  --version             Show program's version number and exit
```

### Examples

```bash
# Basic generation
python3 main.py

# Custom output location
python3 main.py --output ~/Documents/resume.pdf

# Validate data integrity
python3 main.py --validate-only

# Debug mode for troubleshooting
python3 main.py --debug
```

## ⚙️ Configuration

### Data Files

#### `data/coordinates.json`

Contains all text elements with precise positioning:

```json
[
  {
    "text": "Nicol\u00e1s Ignacio Fredes Franco",
    "x": 231.63,
    "y": 83.94,
    "font": "TrebuchetMS-Bold",
    "size": 24.01,
    "color": 2978739,
    "bold": true,
    "italic": false
  },
  ...
]
```

#### `data/shapes.json`

Defines blue section header rectangles:

```json
[
  {
    "x": 228,
    "y": 725.64,
    "width": 382,
    "height": 18.34
  },
  ...
]
```

### Colors

- **Primary Blue** (`#2D73B3`, RGB: 43, 115, 179, Decimal: 2978739): Main name, degrees
- **Job Title Blue** (`#2B73B3`, RGB: 43, 115, 179, Decimal: 2847667): Job positions
- **Section Header Blue** (`#F0F0F0`, RGB: 240, 240, 240, Decimal: 15790320): Section backgrounds
- **Link Blue** (`#1050CC`, RGB: 16, 80, 204, Decimal: 1070028): URLs and hyperlinks

## 🔧 Development

### Tools and Verification

#### Verify Rectangle Alignment

```bash
python3 tools/verify_alignment.py
```

Expected output:
```
[EXPERIENCE]     ✅ PERFECT (Δ0.06px)
[EDUCATION]      ✅ PERFECT (Δ0.45px)
[PAPERS & WORKSHOPS] ✅ PERFECT (Δ0.00px) 🏆
[SKILLS]         ✅ PERFECT (Δ0.00px) 🏆
[LANGUAGES]      ✅ PERFECT (Δ0.00px) 🏆
```

#### Compare Colors

```bash
python3 tools/compare_colors.py
```

Validates job title colors against objective PDF.

#### Quality Verification

```bash
python3 verify_cv_quality.py
```

Comprehensive quality checks including layout, fonts, and colors.

### Making Changes

1. **Update Content**: Edit `data/coordinates.json`
2. **Adjust Layout**: Modify `data/shapes.json` for rectangle positions
3. **Change Colors**: Update color values in coordinate entries
4. **Test Changes**: Run `python3 main.py` and verify with tools

## 🧪 Testing

Run the test suite:

```bash
python3 -m pytest tests/
```

Run with coverage:

```bash
python3 -m pytest --cov=src tests/
```

## 🏗️ Architecture

The system uses a **coordinate-driven architecture** where every element's position is explicitly defined:

```
┌─────────────────┐
│  coordinates.   │──┐
│     json        │  │
└─────────────────┘  │
                     │  ┌──────────────┐      ┌──────────────┐
┌─────────────────┐  ├─▶│   renderer   │─────▶│   PDF Out    │
│   shapes.json   │──┘  │      .py     │      │              │
└─────────────────┘     └──────────────┘      └──────────────┘
                              ▲
                              │
                         ┌────┴─────┐
                         │  fonts.  │
                         │    py    │
                         └──────────┘
```

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Code of conduct
- Development workflow
- Pull request process
- Coding standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Nicolás Ignacio Fredes Franco**
- GitHub: [@nicolasfredesfranco](https://github.com/nicolasfredesfranco)
- LinkedIn: [nicolasfredesfranco](https://linkedin.com/in/nicolasfredesfranco)
- Email: nico.fredes.franco@gmail.com

## 🙏 Acknowledgments

- ReportLab library for PDF generation
- PyMuPDF (fitz) for PDF analysis
- The open-source community

---

**Note**: This generator is designed for personal CV creation. Ensure any fonts and assets you use are properly licensed for your use case.
