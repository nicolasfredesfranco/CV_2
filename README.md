# Professional CV Generator

A high-precision, Python-based CV generation engine designed to programmatically replicate and customize Curriculum Vitae PDFs with pixel-perfect accuracy.

## 🚀 Overview

This project renders a minimalist, professional CV by strictly adhering to a target design layout. It uses a unique **Objective-Driven Architecture** where elements are positioned based on exact coordinates extracted from a "Gold Standard" PDF.

Key features:
- **Pixel-Perfect Renderer**: Uses ReportLab to draw vector graphics and text with sub-point precision.
- **OCR-based Alignment**: Includes a mastering tool that extracts a coordinate dictionary from a target PDF to align sections and indentation exactly.
- **JSON-Driven Content**: separation of content (`coordinates.json`) from logic.
- **Automated Quality Verification**: Scripts to visually compare the output against the objective.

## 📂 Project Structure

```
├── data/
│   ├── coordinates.json        # Main content source (text, phones, emails)
│   ├── shapes.json             # Geometric elements (blue header backgrounds)
│   ├── objective_dictionary.json # OCR-extracted ground truth coordinates
│   └── assets/                 # Fonts and static resources
├── src/
│   ├── renderer.py             # Core PDF generation logic
│   ├── validators.py           # Data integrity checks
│   ├── transformations.py      # Coordinate system math (PDF vs ReportLab)
│   └── config.py               # Global constants (Colors, Fonts)
├── scripts/                    # Utility tools for maintenance
│   ├── verify_cv_quality.py    # Comparison tool
│   └── ...
├── pdfs/
│   ├── objective/              # The target PDF to replicate
│   └── generated/              # Output files
└── main.py                     # Entry point
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/nicolasfredesfranco/CV_2.git
   cd CV_2
   ```

2. **Set up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   *System Dependencies (Linux/Ubuntu):*
   ```bash
   sudo apt-get install poppler-utils  # Required for pdf2image verification
   ```

## 🏃 Usage

### Generate CV
Run the main engine to generate the PDF:
```bash
python3 main.py
```
Output will be saved to `outputs/Nicolas_Fredes_CV.pdf`.

### Update Alignment
If the objective PDF changes, you can re-sync the alignment using the dictionary extractor (located in `scripts/legacy` or by running the generation check):
*The alignment logic now uses `data/objective_dictionary.json` as the source of truth for indentation and section header positions.*

## 📐 Architecture Details

### The "Objective Dictionary" System
To ensure the generated CV looks identical to the original design, the system uses `data/objective_dictionary.json`. This file acts as a map, containing:
- Exact `(x, y)` centroids for every word in the original PDF.
- Font sizes and families detected via analysis.

The generator uses this map to:
1. Center section backgrounds (Experience, Education, etc.) perfectly behind their labels.
2. Indent company names (e.g., "JOBSITY") to match the exact vertical guide of the original design.

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
