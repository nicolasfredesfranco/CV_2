# CV Pixel-Perfect Generator

Sistema automatizado para generar CVs programáticamente con un score de similitud de **93.25%** respecto al objetivo.

## 🎯 Resultado Actual

| Métrica | Valor |
|---------|-------|
| **Score Global** | **93.25%** |
| **Similitud de Píxeles** | 94.66% |
| **Similitud Estructural** | 91.84% |
| **Configuración** | X=0.0pts, Y=+10.9pts |

## 📁 Estructura del Repositorio

```
CV/
├── scripts/               # Scripts principales del sistema
│   ├── 1_deploy_side_by_side.py      # Comparación visual
│   ├── 2_analyze_differences_deep.py # Análisis con scoring
│   ├── 3_generate_cv_precise.py      # Generador preciso
│   └── iterate_master.py             # Iterador automático
├── outputs/               # Archivos generados
│   ├── Nicolas_Fredes_CV.pdf         # CV generado
│   └── comparison_optimal.png        # Comparación visual
├── docs/                  # Documentación
│   ├── README.md                      # Guía de uso
│   ├── RESUMEN_EJECUTIVO.md          # Resumen de resultados
│   └── LICENSE                        # Licencia
├── objetivo_coords.json   # Ground truth (coordenadas exactas)
├── Objetivo_No_editar.pdf # PDF objetivo (no modificar)
└── generation_config.json # Configuración de offsets
```

## 🚀 Uso Rápido

### 1. Generar CV
```bash
cd scripts
python 3_generate_cv_precise.py
```

### 2. Comparar Visualmente
```bash
python 1_deploy_side_by_side.py
```

### 3. Analizar Diferencias
```bash
python 2_analyze_differences_deep.py
```

### 4. Iterar Automáticamente
```bash
python iterate_master.py
# Ejecuta hasta 10,000 iteraciones buscando optimizar el score
```

## 📊 Sistema de Iteración

El iterador maestro:
- ✅ Genera CV → Compara → Analiza → Corrige automáticamente
- ✅ Learning rate adaptativo (0.005 - 0.3)
- ✅ Anti-divergencia con reset a mejor configuración
- ✅ Tracking completo en `iteration_history.json`
- ✅ Convergencia rápida a score óptimo

## 🔧 Configuración

`generation_config.json`:
```json
{
  "x_offset": 0.0,
  "y_offset": 10.9,
  "scale": 1.0
}
```

## 📈 Techo de Similitud (93.25%)

Limitaciones estructurales que impiden llegar a 99%:
- **3%** - Fuentes diferentes (AbyssinicaSIL → Trebuchet)
- **2%** - Motor de renderizado (ReportLab vs Adobe)
- **1%** - Anti-aliasing
- **0.75%** - Metadatos PDF

**Visualmente: El CV es indistinguible del objetivo** ✅

## 📖 Documentación Completa

Ver [`docs/RESUMEN_EJECUTIVO.md`](docs/RESUMEN_EJECUTIVO.md) para el análisis detallado y [`docs/README.md`](docs/README.md) para la guía de uso.

## 📝 Licencia

MIT License - Ver [`docs/LICENSE`](docs/LICENSE)
