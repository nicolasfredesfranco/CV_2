#!/usr/bin/env python3
"""
Grid Search para optimización automática
Prueba múltiples configuraciones y elige la mejor
"""

import subprocess
import json
import re
import shutil

def get_score():
    """Ejecuta comparación y extrae score"""
    result = subprocess.run(['python3', 'compare_pdf.py'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        match = re.search(r'(\d+\.\d+)/100', line)
        if match:
            return float(match.group(1))
    return None

def modify_code(sort_reverse=False, gap_threshold=10, tolerance=0.8):
    """Modifica generate_cv_from_python.py con los parámetros dados"""
    with open('generate_cv_from_python.py', 'r') as f:
        content = f.read()
    
    # Modificar sort_reverse en la línea de ordenamiento
    if sort_reverse:
        content = content.replace(
            'block_spans.sort(key=lambda s: (s[\'y\'], s[\'x\']))',
            'block_spans.sort(key=lambda s: (s[\'y\'], s[\'x\']), reverse=True)'
        )
    else:
        content = content.replace(
            'block_spans.sort(key=lambda s: (s[\'y\'], s[\'x\']), reverse=True)',
            'block_spans.sort(key=lambda s: (s[\'y\'], s[\'x\']))'
        )
    
    with open('generate_cv_from_python.py', 'w') as f:
        f.write(content)

def run_variation(name, **params):
    """Ejecuta una variación y devuelve el score"""
    print(f"  Testing: {name:30s} ", end='', flush=True)
    
    # Modificar código
    modify_code(**params)
    
    # Generar PDF
    result = subprocess.run(['python3', 'generate_cv_from_python.py'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Error en generación")
        return None
    
    # Comparar
    score = get_score()
    if score:
        print(f"→ {score:.2f}/100")
        return score
    else:
        print("❌ Error en comparación")
        return None

# Configuraciones a probar
configurations = [
    {'name': 'Baseline', 'sort_reverse': False, 'gap_threshold': 10, 'tolerance': 0.8},
    {'name': 'Orden inverso', 'sort_reverse': True, 'gap_threshold': 10, 'tolerance': 0.8},
    {'name': 'Gap threshold 15', 'sort_reverse': False, 'gap_threshold': 15, 'tolerance': 0.8},
    {'name': 'Gap threshold 8', 'sort_reverse': False, 'gap_threshold': 8, 'tolerance': 0.8},
    {'name': 'Gap threshold 12', 'sort_reverse': False, 'gap_threshold': 12, 'tolerance': 0.8},
    {'name': 'Gap threshold 20', 'sort_reverse': False, 'gap_threshold': 20, 'tolerance': 0.8},
    {'name': 'Gap threshold 5', 'sort_reverse': False, 'gap_threshold': 5, 'tolerance': 0.8},
    {'name': 'Orden inv + Gap 15', 'sort_reverse': True, 'gap_threshold': 15, 'tolerance': 0.8},
    {'name': 'Orden inv + Gap 8', 'sort_reverse': True, 'gap_threshold': 8, 'tolerance': 0.8},
    {'name': 'Orden inv + Gap 20', 'sort_reverse': True, 'gap_threshold': 20, 'tolerance': 0.8},
    {'name': 'Orden inv + Gap 5', 'sort_reverse': True, 'gap_threshold': 5, 'tolerance': 0.8},
    {'name': 'Orden inv + Gap 12', 'sort_reverse': True, 'gap_threshold': 12, 'tolerance': 0.8},
]

if __name__ == '__main__':
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          GRID SEARCH - 12 CONFIGURACIONES                   ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    # Guardar versión original
    shutil.copy('generate_cv_from_python.py', 'generate_cv_backup.py')
    
    results = []
    
    for config in configurations:
        score = run_variation(**config)
        if score:
            results.append((score, config['name'], config))
    
    # Ordenar por score
    results.sort(reverse=True)
    
    print(f"\n{'='*70}")
    print("📊 RESULTADOS (ordenados por score):")
    print(f"{'='*70}")
    
    for i, (score, name, config) in enumerate(results[:5], 1):
        status = "🏆" if i == 1 else "✅"
        print(f"{status} #{i}: {score:.2f}/100 - {name}")
    
    if results:
        best_score, best_name, best_config = results[0]
        print(f"\n🏆 MEJOR CONFIGURACIÓN: {best_name}")
        print(f"   Score: {best_score:.2f}/100")
        print(f"   Config: {best_config}")
        
        # Aplicar la mejor configuración
        modify_code(**best_config)
        subprocess.run(['python3', 'generate_cv_from_python.py'], capture_output=True)
        
        print(f"\n✅ Mejor configuración aplicada")
    
    # Limpiar
    import os
    os.remove('generate_cv_backup.py')

