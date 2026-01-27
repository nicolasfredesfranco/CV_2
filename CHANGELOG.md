# Changelog

All notable changes to the Precision CV Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Automated test suite (pytest)
- CI/CD pipeline configuration
- Type hints throughout codebase
- Multi-language CV support
- Template system for different CV styles

---

## [1.0.0] - 2026-01-27

### 🎉 Major Release: Professional Repository Structure

This release marks the transition to a professionally structured, GitHub-optimized repository.

### Added
- **Comprehensive documentation suite**
  - Enhanced `README.md` with badges, diagrams, and detailed sections
  - `ARCHITECTURE.md` with system design and technical deep dives
  - `DEVELOPMENT.md` with development guidelines and troubleshooting
  - `CONTRIBUTING.md` with contribution process and coding standards
  - `CHANGELOG.md` (this file) for version tracking

- **Professional repository structure**
  - `config/` directory for configuration files
  - `pdfs/` with subdirectories (objective/, generated/, versions/)
  - `scripts/` organized by function (compression/, verification/, extraction/)
  - `analysis/` for active analysis reports
  - `archive/` for historical data (large files)
  - `docs/development/` for development documentation

- **GitHub-optimized features**
  - Multiple mermaid diagrams (architecture, flow charts, timelines)
  - Collapsible sections for better readability
  - Tables for structured data
  - Alerts and callouts for important information
  - Center-aligned sections for visual hierarchy

### Changed
- **Moved LICENSE from `docs/` to repository root** (standard location)
- **Reorganized 23 files** into logical directory structure
- **Updated .gitignore** to reflect new structure
- **Relocated documentation** for better organization
  - `ESTADO_ACTUAL.md` to `docs/`
  - `docs/README.md` to `docs/development/README_legacy.md`

### Removed
- **Deleted backup files** (`objetivo_coords.json.bak`, `objetivo_shapes.json.bak`)
- **Removed `nueva_version/` directory** (consolidated into `pdfs/versions/`)
- **Cleaned root directory** (now only 4 essential files)

### Performance
- Generation time: **< 500ms**
- Similarity score: **93.25%** (maximum achievable)
- PDF output size: **68 KB**

---

## [0.9.0] - 2026-01-23

### 🎯Achieved Maximum Similarity

### Added
- **Section-specific offset configuration**
  - Granular Y-offsets per CV section
  - Configuration files: `generation_config.json`, `generation_config_best.json`
  
- **Advanced precision techniques**
  - Font weight simulation (Fill + Stroke rendering mode)
  - Heuristic bullet point injection
  - Date alignment correction (-1.5px)
  - Context-aware hyperlink mapping

### Changed
- Evolved from global offsets to section-based corrections
- Iterative optimization supports up to 10,000 iterations
- Adaptive learning rates based on current score

### Fixed
- Coordinate transformation accuracy
- Blue header color matching
- Interactive link positioning

### Performance
- **Global Similarity:** 93.06% → 93.25%
- **Pixel Score:** 94.66%
- **Structural Score:** 91.45%

---

## [0.8.0] - 2026-01-22

### 🔄 Iterative Optimization System

### Added
- `legacy/iterate_master.py` - Orchestrator for iterative refinement
- Gradient descent optimization with anti-divergence logic
- Detailed gap analysis reporting (`gap_analysis_100.md`)
- Side-by-side visual comparison tool

### Changed
- Refactored generation pipeline for modularity
- Improved coordinate extraction accuracy

### Fixed
- Edge case handling in text positioning
- Font loading fallback mechanism

---

## [0.7.0] - 202 6-01-21

### ⚡ Performance Enhancements

### Added
- PDF compression strategies
  - `compress_multi_strategy.py` (qpdf, mutool, pikepdf)
  - Target size compression (`compress_to_1_9mb.py`)
  - Link preservation during compression

### Changed
- Optimized rendering pipeline
- Reduced memory footprint

### Performance
- Compressed PDF from 4.2 MB → 1.9 MB (55% reduction)
- Maintained visual fidelity and interactive links

---

## [0.6.0] - 2026-01-20

### 🔗 Interactive Hyperlinks

### Added
- Context-aware link detection
- Y-coordinate disambiguation for duplicate text
- 5 interactive links:
  - Email: `mailto:nico.fredes.franco@gmail.com`
  - GitHub: `https://github.com/nicolasfredesfranco`
  - LinkedIn: `http://www.linkedin.com/in/nicolasfredesfranco`
  - Twitter: `https://twitter.com/NicoFredesFranc`
  - DOI: `https://doi.org/10.1109/ACCESS.2021.3094723`

### Changed
- Link mapping logic centralized in `_draw_elements()`

### Fixed
- Hitbox calculation for clickable areas

---

## [0.5.0] - 2026-01-19

### 🎨 Precision Rendering Techniques

### Added
- Font weight simulation via `setTextRenderMode(2)`
- Adaptive stroke widths (0.05pt body, 0.3pt headers)
- Chromatic synchronization for color accuracy

### Changed
- Rendering pipeline to support precision patches

### Fixed
- Visual weight discrepancy between target and generated PDF

---

## [0.4.0] - 2026-01-18

### 📐 Coordinate Space Transformation

### Added
- Correct Y-axis inversion (PDF top-down → ReportLab bottom-up)
- Page height constants for A4 (595.27 x 841.89 pts)

### Changed
- Complete rewrite of coordinate transformation logic

### Fixed
- Major positioning errors resolved
- Similarity score improved from ~70% to ~85%

---

## [0.3.0] - 2026-01-17

### 📦 Golden Data Extraction

### Added
- Scripts for PDF data extraction
  - `extract_text_coords.py` using pdfminer
  - `find_colored_paths.py` for geometric shapes
- `data/coordinates.json` (1,581 lines)
- `data/shapes.json` (594 lines)

### Changed
- Transitioned from manual positioning to data-driven approach

---

## [0.2.0] - 2026-01-16

### 🏗️ Core Engine Development

### Added
- `CVGenerator` class for PDF generation
- Font loading system with TTF support
- Basic shape rendering (rectangles)
- Text rendering with font families

### Changed
- Architecture refactored to class-based design

---

## [0.1.0] - 2026-01-15

### 🚀 Initial Release

### Added
- Proof of concept for programmatic PDF generation
- ReportLab integration
- Basic coordinate mapping
- Simple text rendering

### Notes
- Initial exploration phase
- Manual positioning of elements
- Similarity score: ~50%

---

## Version Comparison

| Version | Similarity | Key Feature |
|---------|------------|-------------|
| 0.1.0 | ~50% | Initial proof of concept |
| 0.2.0 | ~60% | Core engine architecture |
| 0.3.0 | ~70% | Golden data extraction |
| 0.4.0 | ~85% | Correct coordinate transformation |
| 0.5.0 | ~88% | Precision rendering techniques |
| 0.6.0 | ~90% | Interactive hyperlinks |
| 0.7.0 | ~90% | Performance optimization |
| 0.8.0 | ~92% | Iterative optimization |
| 0.9.0 | **93.25%** | Maximum similarity achieved |
| **1.0.0** | **93.25%** | **Professional structure & docs** |

---

## Similarity Score Evolution

```
100% ┤
     │
95%  ┤                         ╭──────────────── Maximum Achievable (93.25%)
     │                    ╭────╯
90%  ┤              ╭─────╯
     │         ╭────╯
85%  ┤    ╭────╯
     │╭───╯
80%  ┼╯
     │
75%  ┤
     │
70%  ┤╮
     │ ╲
65%  ┤  ╲
     │   ╲
60%  ┤    ╲╮
     │      ╲
55%  ┤       ╲
     │        ╲╮
50%  ┤          ╰─────────────────────────────────────────
     └┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬
      0.1  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9  1.0
```

---

## Breaking Changes

### [1.0.0] - Repository Structure

**Migration Guide:**

If you have scripts referencing old paths:

```python
# Old paths (< 1.0.0)
"Objetivo_No_editar.pdf"
"generation_config.json"
"compress_multi_strategy.py"

# New paths (>= 1.0.0)
"pdfs/objective/Objetivo_No_editar.pdf"
"config/generation_config.json"
"scripts/compression/compress_multi_strategy.py"
```

**Update your scripts:**
```python
# Before
objective_path = "Objetivo_No_editar.pdf"

# After
objective_path = "pdfs/objective/Objetivo_No_editar.pdf"
```

**`main.py` is unchanged** - no migration needed for core generation.

---

## Security

### [1.0.0] - No Security Issues

This project:
- ✅ Does not execute external code
- ✅ Does not make network requests
- ✅ Does not access system resources beyond file I/O
- ✅ Does not store credentials
- ✅ MIT Licensed with clear attribution requirements

**Reported Vulnerabilities:** None

---

## Deprecated Features

### None

All features are actively maintained. Legacy scripts in `legacy/` are preserved for historical reference but are not deprecated (they remain functional).

---

## Contributors

### [1.0.0]
- **Nicolás Ignacio Fredes Franco** - Initial work and maintenance

### Special Thanks
- **Google DeepMind Antigravity Team** - Development assistance
- **Open Source Community** - For tools and libraries (ReportLab, PyMuPDF, pdfminer, etc.)

---

## Links

- **Repository**: [https://github.com/nicolasfredesfranco/CV](https://github.com/nicolasfredesfranco/CV)
- **Issues**: [https://github.com/nicolasfredesfranco/CV/issues](https://github.com/nicolasfredesfranco/CV/issues)
- **Documentation**: [README.md](README.md), [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

**Note:** Dates are in YYYY-MM-DD format. All changes are documented from version 1.0.0 onward. Earlier versions are reconstructed from git history and may be approximate.

[Unreleased]: https://github.com/nicolasfredesfranco/CV/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nicolasfredesfranco/CV/releases/tag/v1.0.0
