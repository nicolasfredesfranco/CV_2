# CV Output Directory

This directory contains the generated PDF resume.

## Generated Files

- **Nicolas_Fredes_CV.pdf** - The production-ready CV in PDF format

## Archive

The `archive/` subdirectory contains historical versions and test outputs from the development process. These files are kept for reference but are not part of the production build.

## Regenerating the CV

To regenerate the PDF from the source data, run:

```bash
python3 main.py
```

The new PDF will be created at `outputs/Nicolas_Fredes_CV.pdf`.

## PDF Specifications

- **Format**: PDF 1.4 (ReportLab)
- **Page Size**: A4 (595.28 × 841.89 points)
- **Font**: TrebuchetMS family (Regular, Bold, Italic)
- **File Size**: ~67KB
- **Features**: Interactive hyperlinks, vector graphics

## Version Information

See `../CHANGELOG.md` for detailed version history and alignment specifications.
