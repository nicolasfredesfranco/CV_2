#!/usr/bin/env python3
"""
Environment Setup Script
========================
Initializes directory structure and validates configuration.

@author: Nicolás Ignacio Fredes Franco
"""

import os
import json
from pathlib import Path

def setup_environment():
    """Inicializa la estructura de directorios y archivos de configuración base."""
    base_dir = Path.cwd()
    data_dir = base_dir / 'data'
    assets_dir = data_dir / 'assets'
    output_dir = base_dir / 'outputs'
    
    # 1. Crear jerarquía de directorios
    print(f"📁 Verificando estructura en: {base_dir}")
    for d in [data_dir, assets_dir, output_dir]:
        d.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Directorio listo: {d.name}/")

    print("\n⚠️  IMPORTANTE:")
    print("   1. Coloca tus fuentes (trebuc.ttf, etc.) en 'data/assets/'")
    print("   2. Asegúrate de que 'coordinates.json' y 'shapes.json' estén en 'data/'")
    print("   3. Ejecuta 'python main.py' para generar el CV.")

if __name__ == "__main__":
    setup_environment()
