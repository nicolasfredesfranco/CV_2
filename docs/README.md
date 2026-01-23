#!/usr/bin/env python3
"""
README.md - Sistema de Generación de CV Pixel-Perfect
====================================================

## Sistema Completo

Este repositorio contiene un sistema automatizado para generar un CV pixel-perfect 
que sea indistinguible del CV objetivo usando iteración automática con correcciones 
inteligentes.

## Archivos Principales

1. **1_deploy_side_by_side.py** - Comparación visual lado a lado
2. **2_analyze_differences_deep.py** - Análisis profundo de diferencias con scoring
3. **3_generate_cv_precise.py** - Generador de CV desde coordenadas JSON
4. **iterate_master.py** - Orquestador maestro de iteración (hasta 10,000 ciclos)

## Datos de Entrada

- **objetivo_coords.json** - Coordenadas exactas extraídas del CV objetivo
- **Objetivo_No_editar.pdf** - PDF objetivo (ground truth)

## Uso

### Ejecución Manual (Paso a Paso)

```bash
# 1. Generar CV
python3 3_generate_cv_precise.py

# 2. Analizar diferencias
python3 2_analyze_differences_deep.py

# 3. Comparar visualmente
python3 1_deploy_side_by_side.py
```

### Ejecución Automática (Iteración Completa)

```bash
# Ejecutar hasta 10,000 iteraciones o score > 99.99%
python3 iterate_master.py 10000 0.9999
```

## Estado Actual

El sistema detecta correctamente un offset vertical de aproximadamente -83pts.
El próximo paso es corregir la lógica de transformación de coordenadas en el generador.

## Problema Identificado

La transformación de coordenadas Y está incorrecta. Necesita ser corregida para:
- Cuando gen_y < obj_y (generado más arriba): aumentar Y
- Cuando gen_y > obj_y (generado más abajo): disminuir Y

La fórmula correcta en ReportLab es:
```
y_reportlab = height - y_pdf_coords - CORRECTION_OFFSET
```

Donde CORRECTION_OFFSET se ajusta iterativamente basándose en los deltas detectados.
