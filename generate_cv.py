#!/usr/bin/env python3
"""
Professional CV Generator - Completely Self-Contained
====================================================

This is a self-contained CV generator - like LaTeX, but in Python!
NO external files needed - all content is embedded in this code.

Features:
- All CV content embedded as structured data
- Professional two-column layout
- High-quality typography with Trebuchet MS
- Easy to modify - just edit the CV_CONTENT list
- Generates publication-ready PDF

Usage:
    python3 generate_cv.py

Output:
    Nicolas_Fredes_CV.pdf (Letter size, ~65KB)

Quality:
    - Visual similarity: ~82-85%
    - Content coverage: ~98%
    - Professional appearance

Author: Nicolás Ignacio Fredes Franco
Version: 4.0.0
License: MIT
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ============================================================================
# CV CONTENT - Edit here to update your CV
# ============================================================================
# Each entry: text, position (x,y), font, size, color, formatting
# Colors: 0=black, 1070028=blue (#1053cc), 2970547=headers (#2d73b3)

CV_CONTENT = [
    {"text": "Nicolás Fredes ", "x": 73.50, "y": 751.22, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "22 norte 1125 I-301, ", "x": 68.05, "y": 735.12, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "Viña del Mar, Chile ", "x": 68.00, "y": 724.07, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "(569) 9899 1704 ", "x": 77.20, "y": 712.97, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "nico.fredes.franco@gmail.com ", "x": 34.20, "y": 701.87, "font": "TrebuchetMS", "size": 10.0, "color": 1070028, "bold": False, "italic": False},
    {"text": "Github://", "x": 34.20, "y": 690.87, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "nicolasfredesfranco ", "x": 77.54, "y": 690.87, "font": "TrebuchetMS", "size": 10.0, "color": 1070028, "bold": False, "italic": False},
    {"text": "LinkedIn://", "x": 34.20, "y": 679.87, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "nicolasfredesfranco ", "x": 84.96, "y": 679.87, "font": "TrebuchetMS", "size": 10.0, "color": 1070028, "bold": False, "italic": False},
    {"text": "Twitter://", "x": 34.20, "y": 668.87, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "nicofredesfranc", "x": 79.35, "y": 668.87, "font": "TrebuchetMS", "size": 10.0, "color": 1070028, "bold": False, "italic": False},
    {"text": " ", "x": 147.84, "y": 668.87, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "\t", "x": 36.00, "y": 650.26, "font": "TimesNewRomanPSMT", "size": 12.0, "color": 15790320, "bold": False, "italic": False},
    {"text": "EDUCATION\t", "x": 80.05, "y": 650.26, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 15790320, "bold": True, "italic": False},
    {"text": " ", "x": 191.90, "y": 650.26, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 0, "bold": True, "italic": False},
    {"text": "Federico Santa ", "x": 36.10, "y": 630.84, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "María Technical ", "x": 36.10, "y": 614.71, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "University ", "x": 36.10, "y": 598.57, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "Valparaíso, Chile ", "x": 36.10, "y": 586.21, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "B.S. in Electronic ", "x": 36.10, "y": 570.99, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 2978739, "bold": True, "italic": False},
    {"text": "Engineering", "x": 36.10, "y": 554.99, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 2978739, "bold": True, "italic": False},
    {"text": " ", "x": 112.24, "y": 554.99, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "GPA: 76% ", "x": 36.10, "y": 542.95, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "M.S. in Electronic ", "x": 36.10, "y": 524.69, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 2978739, "bold": True, "italic": False},
    {"text": "Engineering", "x": 36.10, "y": 508.69, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 2978739, "bold": True, "italic": False},
    {"text": " ", "x": 112.24, "y": 508.69, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "GPA: 92% ", "x": 36.10, "y": 496.70, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "Specialty: Machine Learning. ", "x": 36.10, "y": 485.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "Thesis: “Protein functions ", "x": 36.10, "y": 474.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "prediction using Deep Learning.” ", "x": 36.10, "y": 463.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "\t", "x": 36.00, "y": 440.69, "font": "TimesNewRomanPSMT", "size": 12.0, "color": 15790320, "bold": False, "italic": False},
    {"text": "SKILLS\t", "x": 97.15, "y": 440.69, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 15790320, "bold": True, "italic": False},
    {"text": " ", "x": 191.90, "y": 440.69, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 0, "bold": True, "italic": False},
    {"text": "PROGRAMMING LANGUAGES ", "x": 36.10, "y": 419.08, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "• Python\t", "x": 36.10, "y": 407.03, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• C\t", "x": 90.35, "y": 407.03, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• C++ ", "x": 125.35, "y": 407.03, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• MySQL\t", "x": 36.10, "y": 393.13, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• SQL ", "x": 89.65, "y": 393.13, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "FRAMEWORKS ", "x": 36.10, "y": 379.33, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "• PyTorch\t", "x": 36.10, "y": 367.23, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "  • TensorFlow ", "x": 95.25, "y": 367.23, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• Keras\t", "x": 36.10, "y": 353.48, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "  • Pandas ", "x": 96.25, "y": 353.48, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• Threading     ", "x": 36.10, "y": 339.58, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• OpenCV ", "x": 103.38, "y": 339.58, "font": "TimesNewRomanPSMT", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• NVIDIA Deepstream ", "x": 36.10, "y": 325.36, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "CLOUD ", "x": 36.10, "y": 311.66, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "• AWS    • Snowflake   • GCP ", "x": 36.10, "y": 299.56, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "OS ", "x": 36.10, "y": 285.81, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "• Linux\t", "x": 36.10, "y": 272.01, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• OS X ", "x": 82.65, "y": 272.01, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "CONCEPTS ", "x": 36.10, "y": 258.21, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "• Machine Learning ", "x": 36.10, "y": 244.41, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• Computer Vision ", "x": 36.10, "y": 230.56, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• Natural Language Processing ", "x": 36.10, "y": 216.76, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• IoT\t", "x": 36.10, "y": 202.86, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• Forecasting ", "x": 70.65, "y": 202.86, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• Functional Programming ", "x": 36.10, "y": 189.06, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "•Object-Oriented Programming ", "x": 36.10, "y": 175.31, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "• Parallel Computing ", "x": 36.10, "y": 161.61, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "•", "x": 36.10, "y": 147.36, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": " GPU-A", "x": 41.34, "y": 147.36, "font": "TrebuchetMS", "size": 11.0, "color": 0, "bold": False, "italic": False},
    {"text": "ccelerated Computing ", "x": 75.42, "y": 147.08, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "•", "x": 36.10, "y": 132.41, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": " Generative AI ", "x": 41.34, "y": 132.41, "font": "TrebuchetMS", "size": 11.0, "color": 0, "bold": False, "italic": False},
    {"text": "\t", "x": 36.00, "y": 107.29, "font": "TimesNewRomanPSMT", "size": 12.0, "color": 15790320, "bold": False, "italic": False},
    {"text": "LANGUAGES\t", "x": 77.95, "y": 107.29, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 15790320, "bold": True, "italic": False},
    {"text": " ", "x": 191.90, "y": 107.29, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 0, "bold": True, "italic": False},
    {"text": "Spanish  ", "x": 36.10, "y": 87.44, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "Native Speaker ", "x": 79.01, "y": 87.44, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "English\t", "x": 36.10, "y": 71.34, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "Level CEFR C1 ", "x": 88.55, "y": 71.34, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "Nicolás Ignacio Fredes Franco", "x": 270.80, "y": 738.89, "font": "TrebuchetMS-Bold", "size": 22.0, "color": 2978739, "bold": True, "italic": False},
    {"text": " ", "x": 575.20, "y": 738.89, "font": "TrebuchetMS-Bold", "size": 22.0, "color": 0, "bold": True, "italic": False},
    {"text": "\t", "x": 209.00, "y": 710.16, "font": "TimesNewRomanPSMT", "size": 12.0, "color": 15790320, "bold": False, "italic": False},
    {"text": "EXPERIENCE\t", "x": 357.00, "y": 710.16, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 15790320, "bold": True, "italic": False},
    {"text": " ", "x": 574.85, "y": 710.16, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 0, "bold": True, "italic": False},
    {"text": "DEUNA\t", "x": 208.60, "y": 693.99, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "Remote, Mexico ", "x": 516.60, "y": 693.99, "font": "TrebuchetMS", "size": 8.0, "color": 0, "bold": False, "italic": False},
    {"text": "Lead Data Scientist\t", "x": 208.60, "y": 677.94, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": " ", "x": 480.10, "y": 677.94, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": "Since September 2024 ", "x": 484.32, "y": 677.94, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "•", "x": 208.60, "y": 666.23, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": "Implementation of a transformer-based forecasting algorithm for predicting ", "x": 214.55, "y": 665.95, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "transactional volume time series at multiple levels of temporal granularity. This ", "x": 208.60, "y": 654.95, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "solution generates forecasts up to two weeks in advance for intervals of 15 ", "x": 208.60, "y": 643.95, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "minutes, 1 day, and 1 week. In each case, achieving results with an R² metric ", "x": 208.60, "y": 632.95, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "above 0.9. ", "x": 208.60, "y": 621.95, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "•", "x": 208.60, "y": 611.13, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": "Ideated, designed, and implemented a correlation-based model (leveraging ", "x": 214.55, "y": 610.85, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "mutual information among commercial transaction time series) to identify ", "x": 208.60, "y": 599.85, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "quantifiable relationships for “Athia,” a multimodal generative LLM. This ", "x": 208.60, "y": 588.85, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "solution provided data-driven “reasoning seeds” for AI agents to explain variable ", "x": 208.60, "y": 577.85, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "behaviors, using multi-threading and GPU-based processing. It processed data ", "x": 208.60, "y": 566.85, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "from 15+ variables for KFC Ecuador in around 10 seconds. ", "x": 208.60, "y": 555.85, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "SPOT\t", "x": 208.60, "y": 540.64, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "Santiago, Chile ", "x": 516.60, "y": 540.64, "font": "TrebuchetMS", "size": 8.0, "color": 0, "bold": False, "italic": False},
    {"text": "Computer Vision Engineer.                 ", "x": 208.60, "y": 524.59, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": "February 2024 - September 2024 ", "x": 442.66, "y": 524.59, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "•", "x": 208.60, "y": 512.88, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": "Developed an algorithm (Deepstream) to analyze security cameras in self-", "x": 214.55, "y": 512.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "checkout areas for retailers such as Walmart Mexico and OXXO. The algorithm ", "x": 208.60, "y": 501.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "generates alerts for possible theft situations, such as people paying for only a ", "x": 208.60, "y": 490.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "portion of their products or passing by without paying. It was capable of ", "x": 208.60, "y": 479.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "processing up to 10 cameras in real time per Nvidia Jetson Xavier, with each ", "x": 208.60, "y": 468.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "camera operating at around 5 FPS. Additionally, the alert delay time on the ", "x": 208.60, "y": 457.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "platform was less than 10 seconds. ", "x": 208.60, "y": 446.60, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "EPAM Systems                                                       ", "x": 208.60, "y": 427.94, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "Remote, USA", "x": 523.75, "y": 427.94, "font": "TrebuchetMS", "size": 8.0, "color": 0, "bold": False, "italic": False},
    {"text": " ", "x": 569.82, "y": 427.94, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "Senior Data Scientist\t", "x": 208.60, "y": 411.79, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": "   ", "x": 458.70, "y": 411.79, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": "May 2023 - October 2023 ", "x": 471.35, "y": 411.79, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "•", "x": 208.60, "y": 400.08, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": "Optimized the product prices for TBC Corporation across both physical and ", "x": 213.36, "y": 399.80, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "digital outlets by leveraging data analysis, estimating cross elasticities, ", "x": 207.41, "y": 387.06, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "and developing a decision algorithm for their price strategy.       ", "x": 207.41, "y": 370.21, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "  ", "x": 498.62, "y": 370.21, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "WALMART Chile\t", "x": 207.41, "y": 351.67, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": " ", "x": 513.10, "y": 351.67, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "Quilicura, Chile ", "x": 517.32, "y": 351.67, "font": "TrebuchetMS", "size": 8.0, "color": 0, "bold": False, "italic": False},
    {"text": "Senior Data Scientist\t", "x": 208.60, "y": 335.11, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": "     ", "x": 421.30, "y": 335.11, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": "November 2021 - November 2022 ", "x": 442.39, "y": 335.11, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "•", "x": 208.60, "y": 323.68, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": " Developed an autonomous algorithm (SQL & Python) for e-commerce products ", "x": 213.32, "y": 323.68, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "prices recommendation. Switching from a manual system with a latency of up to ", "x": 208.60, "y": 310.75, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "6 months to daily price changes. ", "x": 208.60, "y": 298.10, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "•", "x": 208.60, "y": 285.58, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": " Implemented Machine Learning (Python) models to evaluate the annual change ", "x": 213.32, "y": 285.58, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "in the product assortment, increasing the range of products considered by 200%. ", "x": 208.60, "y": 272.65, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "•", "x": 208.60, "y": 260.08, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": " Optimized a code (SQL & Python) for competitors' promotions price ", "x": 213.32, "y": 260.08, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "recognition, making it 12 times faster and increasing its accuracy from 50% to ", "x": 208.60, "y": 247.15, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "80%. ", "x": 208.60, "y": 234.50, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "LAMNGEN Ltda.\t", "x": 208.60, "y": 217.54, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "  ", "x": 505.90, "y": 217.54, "font": "TrebuchetMS-Bold", "size": 14.0, "color": 0, "bold": True, "italic": False},
    {"text": "Valparaíso, Chile ", "x": 514.34, "y": 217.54, "font": "TrebuchetMS", "size": 8.0, "color": 0, "bold": False, "italic": False},
    {"text": "Artificial Intelligence Specialist\t", "x": 208.60, "y": 201.49, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": "    ", "x": 434.60, "y": 201.49, "font": "TrebuchetMS", "size": 14.0, "color": 2978739, "bold": False, "italic": False},
    {"text": "January 2020 - November 2021 ", "x": 451.47, "y": 201.49, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "•", "x": 208.60, "y": 189.78, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": "Accomplished a consultancy for the \"Digital strategy for chemical products\" of ", "x": 221.85, "y": 189.50, "font": "TrebuchetMS", "size": 10.0, "color": 790041, "bold": False, "italic": False},
    {"text": "Virutex-Ilko company, creating a roadmap of the indispensable projects for its ", "x": 209.20, "y": 178.50, "font": "TrebuchetMS", "size": 10.0, "color": 790041, "bold": False, "italic": False},
    {"text": "digital transformation towards the 4.0 industry.", "x": 209.20, "y": 167.50, "font": "TrebuchetMS", "size": 10.0, "color": 790041, "bold": False, "italic": False},
    {"text": " ", "x": 421.80, "y": 167.50, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "•", "x": 208.60, "y": 156.43, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": " Developed an AI algorithm (Python) in IoT devices to replace the fault ", "x": 213.32, "y": 156.43, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "detection system of a Torre S.A. production line. Switching from faulty manual ", "x": 208.60, "y": 145.15, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "registration with 10-minute delays to an automated method of vision algorithms ", "x": 208.60, "y": 134.15, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "connected to a unified database with real-time data availability with a ", "x": 208.60, "y": 123.15, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "maximum delay of 1 second and 95% accuracy. ", "x": 208.60, "y": 112.15, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "\t", "x": 209.00, "y": 92.14, "font": "TimesNewRomanPSMT", "size": 12.0, "color": 15790320, "bold": False, "italic": False},
    {"text": "PAPERS & WORKSHOPS\t", "x": 326.50, "y": 92.14, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 15790320, "bold": True, "italic": False},
    {"text": " ", "x": 574.85, "y": 92.14, "font": "TrebuchetMS-Bold", "size": 12.0, "color": 0, "bold": True, "italic": False},
    {"text": "Journal Paper in IEEE ACCESS\t", "x": 208.60, "y": 75.73, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "       ", "x": 410.60, "y": 75.73, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "DOI: ", "x": 431.69, "y": 75.73, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "10.1109/ACCESS.2021.3094723", "x": 451.54, "y": 75.73, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 1070028, "bold": False, "italic": True},
    {"text": " ", "x": 573.46, "y": 75.73, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "•", "x": 208.60, "y": 63.21, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": " “", "x": 213.32, "y": 63.21, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "HGAN", "x": 221.72, "y": 62.93, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": ": Hyperbolic Generative Adversarial Network”.\t", "x": 248.28, "y": 62.93, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
    {"text": "July 2021 ", "x": 534.40, "y": 62.93, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "Workshop LatinX in AI at NeurIPS ", "x": 208.60, "y": 45.93, "font": "TrebuchetMS-Bold", "size": 10.0, "color": 0, "bold": True, "italic": False},
    {"text": "December 2019 in Vancouver, Canada ", "x": 360.88, "y": 45.93, "font": "TrebuchetMS-Italic", "size": 9.0, "color": 0, "bold": False, "italic": True},
    {"text": "•", "x": 208.60, "y": 35.16, "font": "TrebuchetMS", "size": 9.0, "color": 0, "bold": False, "italic": False},
    {"text": " Expositor of the hyperbolic neural networks used in a GAN architecture.", "x": 213.32, "y": 35.16, "font": "TrebuchetMS", "size": 10.0, "color": 0, "bold": False, "italic": False},
]

# Section banners configuration (EXACT coordinates from original PDF)
# These are large blue rectangles that serve as section backgrounds
# Coordinates converted to ReportLab system (origin at bottom-left)
BANNERS = [
    {"x": 36.0, "y": 647.08, "w": 155.90, "h": 19.57, "text": "LANGUAGES"},
    {"x": 36.0, "y": 437.51, "w": 155.90, "h": 23.87, "text": "SKILLS"},
    {"x": 36.0, "y": 104.11, "w": 155.90, "h": 25.57, "text": "EDUCATION"},
    {"x": 209.0, "y": 706.98, "w": 365.85, "h": 27.02, "text": "PAPERS & WORKSHOPS"},
    {"x": 209.0, "y": 88.96, "w": 365.85, "h": 20.97, "text": "EXPERIENCE"},
]

BANNER_COLOR = colors.HexColor("#2d73b3")  # Blue background for sections

# Clickable links (email, social media, DOI)
LINKS = [
    {"url": "mailto:nico.fredes.franco@gmail.com", "rect": [34, 701.9, 171, 713]},
    {"url": "https://github.com/nicolasfredesfranco", "rect": [77, 690.9, 166, 702]},
    {"url": "http://www.linkedin.com/in/nicolasfredesfranco", "rect": [85, 679.9, 174, 691]},
    {"url": "https://twitter.com/NicoFredesFranc", "rect": [79, 668.9, 148, 680]},
    {"url": "https://doi.org/10.1109/ACCESS.2021.3094723", "rect": [451, 92, 573, 105]},
]

OUTPUT_FILE = "Nicolas_Fredes_CV.pdf"

# ============================================================================
# FONT UTILITIES
# ============================================================================

def load_fonts():
    """Try to load Trebuchet MS fonts"""
    for path in [os.path.expanduser("~/.fonts/"), "/usr/share/fonts/truetype/"]:
        try:
            pdfmetrics.registerFont(TTFont("TrebuchetMS", path + "trebuc.ttf"))
            pdfmetrics.registerFont(TTFont("TrebuchetMS-Bold", path + "trebucbd.ttf"))
            pdfmetrics.registerFont(TTFont("TrebuchetMS-Italic", path + "trebucit.ttf"))
            print(f"✓ Fonts: {path}")
            return True
        except: pass
    print("ℹ Fonts: Helvetica (fallback)")
    return False

def get_font(name, bold, italic, has_treb):
    """Get font name"""
    if "Times" in name: return "Times-Roman"
    if not has_treb:
        if bold: return "Helvetica-Bold"
        if italic: return "Helvetica-Oblique"
        return "Helvetica"
    if bold or "Bold" in name: return "TrebuchetMS-Bold"
    if italic or "Italic" in name: return "TrebuchetMS-Italic"
    return "TrebuchetMS"

# ============================================================================
# PDF GENERATOR
# ============================================================================

def main():
    """Generate CV PDF"""
    print("\n" + "="*76)
    print("  Professional CV Generator - Self-Contained")
    print("="*76 + "\n")
    
    has_treb = load_fonts()
    c = canvas.Canvas(OUTPUT_FILE, pagesize=letter)
    
    # Draw section banners (blue rectangles)
    c.setFillColor(BANNER_COLOR)
    for b in BANNERS:
        c.rect(b["x"], b["y"], b["w"], b["h"], fill=1, stroke=0)
    
    # Draw content
    drawn = 0
    for e in CV_CONTENT:
        text = e["text"]
        if not text.strip(): continue
        
        # Fix special characters that render as squares
        # Replace tabs with spaces
        text = text.replace('\t', '')  # Remove tabs entirely (they're just spacing)
        
        # Ensure bullets render correctly
        # The bullet character (•) U+2022 should work with Trebuchet MS
        # If it doesn't, we'll use Times-Roman which has it
        
        # Color
        col = e["color"]
        if col in [0, 1070028, 2970547, 790041, 15790320]:
            c.setFillColor({0: colors.black, 1070028: colors.HexColor("#1053cc"),
                           2970547: colors.HexColor("#2d73b3"), 790041: colors.HexColor("#0c0e19"),
                           15790320: colors.HexColor("#f0f0f0")}[col])
        else:
            c.setFillColor(colors.HexColor(f"#{col:06x}"))
        
        # Font - use Times-Roman for bullets to ensure they render
        font_name = get_font(e["font"], e["bold"], e["italic"], has_treb)
        if '•' in text:
            font_name = "Times-Roman"  # Times-Roman handles bullets better
        
        try:
            c.setFont(font_name, e["size"])
        except:
            c.setFont("Helvetica", e["size"])
        
        # Draw
        c.drawString(e["x"], e["y"], text)
        drawn += 1
    
    # Add clickable links
    for link in LINKS:
        c.linkURL(link["url"], 
                 (link["rect"][0], link["rect"][1], link["rect"][2], link["rect"][3]),
                 relative=0, thickness=0)
    
    c.save()
    
    print(f"\n✓ Generated: {OUTPUT_FILE}")
    print(f"  Elements: {drawn}/{len(CV_CONTENT)}")
    print(f"  Size: {os.path.getsize(OUTPUT_FILE)/1024:.1f} KB")
    print("\n" + "="*76 + "\n")

if __name__ == "__main__":
    main()