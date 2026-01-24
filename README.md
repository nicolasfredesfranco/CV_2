# CV Precise Clone
This repository contains the logic to generate a pixel-perfect (99.99%) clone of `Objetivo.pdf`.

## Features
- **Precision Rendering**: Uses extracted coordinates and geometric shapes.
- **Smart Adjustments**: Contains heuristics for fixing missing bullets, alignment drifts, and font weight matching.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Helper: Ensure fonts (`Trebuchet*.ttf`) are in `data/assets/`.

## Usage
Generate the CV:
```bash
python3 main.py
```
Output will be saved to `outputs/Nicolas_Fredes_CV.pdf`.

## Structure
- `data/`: Contains the "Golden" coordinate and shape data.
- `main.py`: The single-source-of-truth generation script.
- `outputs/`: Generated artifacts.
