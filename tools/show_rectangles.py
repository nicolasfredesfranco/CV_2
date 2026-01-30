#!/usr/bin/env python3
"""
Ajustador iterativo de rectángulos - uno por uno
"""

import json
from pathlib import Path

SHAPES_JSON = Path("data/shapes.json")

# Cargar shapes actuales
with open(SHAPES_JSON, 'r') as f:
    shapes = json.load(f)

print("=== AJUSTE MANUAL DE RECTÁNGULOS ===\n")
print("Rectángulos actuales:\n")

for i, shape in enumerate(shapes, 1):
    print(f"{i}. y={shape['y']:8.2f}, x={shape['x']:8.2f}, w={shape['width']:8.2f}, h={shape['height']:7.4f}")

print("\n" + "="*60)
print("Edita el archivo data/shapes.json para ajustar las posiciones Y")
print("Luego ejecuta: python main.py")
print("="*60)
