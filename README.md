# 📄 CV PDF Replication System

Sistema automatizado de replicación y comparación de CV en PDF usando Python y ReportLab.

---

## ⚠️ **ARCHIVOS PROTEGIDOS - NO MODIFICAR**

Los siguientes archivos **NO DEBEN SER MODIFICADOS BAJO NINGUNA CIRCUNSTANCIA**:

```
❌ EN_NicolasFredes_CV.pdf  - PDF ORIGINAL (Ground Truth)
❌ compare_pdf.py           - Comparador Ultra-Detallado
```

Estos archivos son la base del sistema y cualquier modificación romperá el flujo de trabajo.

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Workflow del Sistema](#workflow-del-sistema)
4. [Instalación](#instalación)
5. [Uso](#uso)
6. [Sistema de Comparación](#sistema-de-comparación)
7. [Métrica Unificada](#métrica-unificada)
8. [Iteración y Mejora](#iteración-y-mejora)
9. [Resultados Actuales](#resultados-actuales)
10. [Contribuir](#contribuir)

---

## 🎯 Descripción General

Este proyecto replica un CV profesional existente usando Python y ReportLab, con un sistema avanzado de comparación que mide la similitud entre el PDF original y el generado.

### Objetivos

- ✅ Generar un PDF idéntico al original usando código Python
- ✅ Comparar ambos PDFs con máximo detalle (como lo haría el ojo humano)
- ✅ Iterar automáticamente hasta lograr > 95% de similitud
- ✅ Mantener el CV como código versionable

### Ventajas

- **Versionamiento:** CV bajo control de versiones (Git)
- **Actualización rápida:** Cambiar contenido en Python y regenerar
- **Portabilidad:** Funciona en cualquier sistema con Python
- **Profesionalismo:** Formato consistente y preciso
- **Automatización:** Loop de mejora guiado por métricas

---

## 📁 Estructura del Proyecto

```
CV/
├── 📘 README.md                       # Documentación completa del proyecto
├── 📋 PLAN.md                         # Plan de ejecución iterativa (pseudocódigo)
│
├── ❌ EN_NicolasFredes_CV.pdf        # [PROTEGIDO] PDF original - Ground Truth
├── ❌ compare_pdf.py                  # [PROTEGIDO] Comparador ultra-detallado
│
├── ✅ generate_cv_from_python.py     # ⭐ ARCHIVO PRINCIPAL - Generador de PDF
├── 📄 generated.pdf                   # Output del generador (auto-generado)
│
├── 📊 detailed_comparison.json        # Reporte de comparación (auto-generado)
│
├── 🔧 install_fonts.sh                # Script para instalar TrebuchetMS
├── 🔧 VERIFY.sh                       # Script de verificación
├── 📦 requirements.txt                # Dependencias Python
├── 📜 LICENSE                         # Licencia MIT
├── 🚫 .gitignore                      # Control de versiones
│
└── 📁 fonts/                          # Fuentes alternativas
    ├── dejavu-fonts-ttf-2.37.tar.bz2
    └── trebuc32.exe
```

### ⭐ Archivo Principal

**`generate_cv_from_python.py`** es el archivo principal que debes modificar para:
- Cambiar contenido del CV
- Ajustar layout y espaciado
- Mejorar similitud con el original
- Actualizar información personal

### Archivos Clave

#### **🔒 Archivos Protegidos (NO MODIFICAR)**

| Archivo | Descripción | ¿Por qué no modificar? |
|---------|-------------|------------------------|
| `EN_NicolasFredes_CV.pdf` | PDF original del CV | Es el ground truth contra el que se compara todo |
| `compare_pdf.py` | Sistema de comparación ultra-detallado | Sistema optimizado y calibrado |

#### **✅ Archivo Principal (MODIFICABLE)**

| Archivo | Descripción | Score Actual |
|---------|-------------|--------------|
| **`generate_cv_from_python.py`** ⭐ | **Generador principal del PDF** | **48.39/100** |

Este es el **único archivo Python que debes modificar** para mejorar el CV.

#### **🔧 Scripts de Soporte**

| Archivo | Descripción |
|---------|-------------|
| `install_fonts.sh` | Instala TrebuchetMS (ejecutar una vez) |
| `VERIFY.sh` | Verifica integridad del repositorio |

#### **📄 Outputs Auto-generados**

| Archivo | Descripción | Se Regenera |
|---------|-------------|-------------|
| `generated.pdf` | PDF creado por el generador | Cada ejecución |
| `detailed_comparison.json` | Análisis ultra-detallado (380KB) | Cada comparación |

---

## 🔄 Workflow del Sistema

```
┌─────────────────────────────────────────────────────────┐
│     EN_NicolasFredes_CV.pdf (ORIGINAL)                  │
│     ❌ NO MODIFICAR                                      │
└────────────────┬────────────────────────────────────────┘
                 │ (ground truth)
                 ↓
┌─────────────────────────────────────────────────────────┐
│     generate_cv_from_python.py                          │
│     (Genera PDF usando ReportLab)                       │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│     generated.pdf                                        │
│     (Output a comparar)                                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│     compare_pdf.py (COMPARADOR)                         │
│     ❌ NO MODIFICAR                                      │
│     • Analiza 16 categorías                             │
│     • Genera métricas detalladas                        │
│     • Score 0-100                                        │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│     detailed_comparison.json + Reporte                  │
│     • Score actual                                       │
│     • Recomendaciones específicas                       │
│     • Breakdown detallado                               │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓ (analizar y ajustar)
                 │
         ┌───────┴────────┐
         │ Modificar solo │
         │ generate_cv... │
         └───────┬────────┘
                 │
                 └──────→ Loop hasta Score > 95%
```

---

## 🚀 Instalación

### 1. Requisitos

```bash
# Python 3.8+
python3 --version

# Dependencias Python
pip install reportlab PyMuPDF numpy
```

### 2. Instalar Fuentes (Opcional pero Recomendado)

Para obtener la mejor similitud, instala Trebuchet MS:

```bash
# Método 1: Script incluido
chmod +x install_fonts.sh
./install_fonts.sh

# Método 2: Manual (Ubuntu/Debian)
sudo apt-get install ttf-mscorefonts-installer
sudo fc-cache -f
```

**Nota:** El generador tiene fallbacks a Liberation Sans y DejaVu Sans si Trebuchet MS no está disponible.

### 3. Verificar Instalación

```bash
# Listar archivos
ls -lh

# Verificar que existen los archivos protegidos
ls EN_NicolasFredes_CV.pdf compare_pdf.py
```

---

## 💻 Uso

### Generar PDF

```bash
python3 generate_cv_from_python.py
```

**Output:** `generated.pdf`

### Comparar PDFs

```bash
python3 compare_pdf.py
```

**Output:**
- Reporte en consola (detallado)
- `detailed_comparison.json` (164KB de datos)

### Ver Score Rápido

```bash
python3 compare_pdf.py 2>&1 | grep -A 20 "SIMILARITY SCORE"
```

### Workflow Completo

```bash
# 1. Generar PDF
python3 generate_cv_from_python.py

# 2. Comparar
python3 compare_pdf.py

# 3. Revisar recomendaciones en el reporte

# 4. Modificar SOLO generate_cv_from_python.py

# 5. Repetir hasta Score > 95%
```

---

## 🔬 Sistema de Comparación

El comparador (`compare_pdf.py` - **NO MODIFICAR**) realiza un análisis ultra-detallado de **16 categorías**.

### Categorías Analizadas

| # | Categoría | Peso | Descripción |
|---|-----------|------|-------------|
| 1 | **Geometría de página** | 3% | Dimensiones exactas y área |
| 2 | **Márgenes** | 8% | Top, Bottom, Left, Right |
| 3 | **Columnas & Layout** | 12% | Estructura de 2 columnas, gutter |
| 4 | **Font Sizes** | 12% | Todos los tamaños de fuente |
| 5 | **Font Distribution** | 10% | Frecuencia de uso de cada tamaño |
| 6 | **Font Families** | 8% | Fuentes usadas (TrebuchetMS, etc.) |
| 7 | **Colors** | 10% | Paleta completa y distribución |
| 8 | **Line Spacing** | 7% | Interlineado |
| 9 | **Block Spacing** | 8% | Espaciado vertical entre bloques |
| 10 | **Content** | 6% | Texto, palabras, similitud |
| 11 | **Sections** | 5% | Detección de secciones del CV |
| 12 | **Alignment** | 3% | Left, Right, Center |
| 13 | **Density** | 4% | Uso de espacio en la página |
| 14 | **Ratios** | 4% | Proporciones y balance |
| 15 | **Exact Positions** | 2% | Posiciones exactas |
| 16 | **Global Document** | 8% | Análisis completo del documento |

### ¿Qué Analiza "Global Document"?

Esta categoría analiza el documento **como un conjunto completo**, no solo por partes:

- **Límites globales:** Top, Bottom, Left, Right del contenido completo
- **Whitespace:** Porcentaje de espacio en blanco (legibilidad)
- **Leading:** Ratio line spacing / font size (tipografía)
- **Section Weights:** Peso visual de cada sección (EDUCATION, EXPERIENCE, etc.)
- **Visual Hierarchy:** Jerarquía completa de tamaños de fuente
- **Global Spacing:** Espaciado entre todos los elementos
- **Document Balance:** Centro de masa y simetría
- **Bounds:** Límites exactos del contenido

### Precisión del Análisis

- **Precisión:** 0.01 puntos
- **Métricas totales:** 50+
- **Estadísticas:** Mean, Median, Std, Percentiles
- **Análisis visual:** Como lo haría el ojo humano
- **Output:** 164KB de datos en JSON

---

## 📊 Métrica Unificada

### Score: 0 a 100

El comparador genera una **métrica única unificada** de 0 a 100:

- **100** = PDFs idénticos
- **95-99** = Prácticamente idénticos (imperceptible)
- **90-94** = Muy similares (diferencias menores)
- **80-89** = Similares (diferencias visibles)
- **70-79** = Parecidos (diferencias significativas)
- **60-69** = Algo parecidos
- **0-59** = Diferentes

### Interpretación del Score

```
Score = 100 - Σ(penalizaciones)

Penalizaciones ponderadas por importancia visual:
- Fuente diferente: hasta -10 pts (muy visible)
- Columnas mal alineadas: hasta -12 pts (estructura crítica)
- Colores incorrectos: hasta -10 pts (muy visible)
- Espaciado incorrecto: hasta -8 pts (legibilidad)
- etc.
```

### Breakdown Detallado

El sistema muestra exactamente qué afecta el score:

```
📉 PENALTIES BREAKDOWN:
   • Margins: -4.47
   • Columns & layout: -11.00
   • Font families: -10.00
   • Colors: -4.45
   • Block spacing: -8.00
   • Global document: -5.67
   • ... más categorías
   ─────────────────────────
   TOTAL PENALTIES: -63.10 pts
```

---

## 🔄 Iteración y Mejora

### Proceso de Mejora

1. **Ejecutar comparador:**
   ```bash
   python3 compare_pdf.py
   ```

2. **Revisar el reporte:**
   - Score actual
   - Critical Issues (❌)
   - Recommendations (⚠️)
   - Minor Issues (➖)

3. **Modificar SOLO `generate_cv_from_python.py`:**
   ```python
   # Ejemplo: Ajustar márgenes
   MARGIN_TOP = 31.39  # Cambiar según recomendación
   MARGIN_BOTTOM = 32.66
   ```

4. **Regenerar y comparar:**
   ```bash
   python3 generate_cv_from_python.py
   python3 compare_pdf.py
   ```

5. **Repetir hasta Score > 95%**

### Recomendaciones por Prioridad

El comparador categoriza problemas por severidad:

#### 🚨 **Critical Issues** (Arreglar primero)
- Font family incorrecta
- Colores faltantes
- Page size incorrecto

#### ⚠️ **Recommendations** (Arreglar después)
- Márgenes desviados > 2pts
- Columnas > 2% diferencia
- Espaciado > 1-2pts diferencia

#### ℹ️ **Minor Issues** (Opcionales)
- Posiciones ligeramente diferentes
- Similitud textual < 95%
- Alineación menor

---

## 📈 Resultados Actuales

### Score Actual: **36.90/100**

#### Problemas Principales

1. ❌ **Font family:** Usando LiberationSans en lugar de TrebuchetMS (-10 pts)
2. ⚠️ **Right column width:** 111.02pt debería ser 311.02pt (64.3% diff) (-11 pts)
3. ⚠️ **Block spacing:** 10.55pt debería ser 6.82pt (-8 pts)
4. ⚠️ **Margins bottom:** 43.76pt debería ser 32.66pt (34% diff) (-4.5 pts)
5. ⚠️ **Font distribution:** Faltan instancias de varios tamaños (-4.3 pts)
6. ⚠️ **Global document:** Whitespace, leading, section weights (-5.7 pts)

#### Próximos Pasos

1. **Prioridad 1:** Instalar y usar TrebuchetMS → +10 pts esperados
2. **Prioridad 2:** Corregir ancho de columna derecha → +11 pts
3. **Prioridad 3:** Ajustar espaciado entre bloques → +8 pts
4. **Prioridad 4:** Corregir márgenes → +4.5 pts
5. **Prioridad 5:** Mejorar distribución de fuentes → +4.3 pts

**Score esperado después de fixes:** ~85-90/100

---

## 🛠️ Troubleshooting

### Problema: Fuentes no se ven correctas

**Solución:**
```bash
# Instalar MS Core Fonts
sudo apt-get install ttf-mscorefonts-installer
sudo fc-cache -f

# O usar el script incluido
./install_fonts.sh
```

### Problema: compare_pdf.py da error

**NO MODIFICAR `compare_pdf.py`**

Verifica:
```bash
# Dependencias instaladas
pip install PyMuPDF numpy

# Archivos existen
ls EN_NicolasFredes_CV.pdf generated.pdf
```

### Problema: Score muy bajo

**Normal al principio.** Sigue el proceso de iteración:
1. Lee las recomendaciones
2. Modifica SOLO `generate_cv_from_python.py`
3. Regenera y compara
4. Repite

### Problema: JSON muy grande

**Es normal.** El archivo `detailed_comparison.json` contiene ~164KB de datos detallados. Si solo necesitas el score:

```bash
python3 compare_pdf.py 2>&1 | grep "SIMILARITY SCORE" -A 20
```

---

## 📝 Notas Importantes

### ⚠️ Archivos que NO SE DEBEN MODIFICAR

```
❌ EN_NicolasFredes_CV.pdf
❌ compare_pdf.py
```

**¿Por qué?**

- **`EN_NicolasFredes_CV.pdf`**: Es el ground truth. Si se modifica, toda la comparación pierde sentido.
- **`compare_pdf.py`**: Sistema optimizado y calibrado. Modificarlo puede romper las métricas.

### ✅ Archivo que SÍ SE DEBE MODIFICAR

```
✅ generate_cv_from_python.py
```

**Este es el único archivo que debes editar para mejorar la similitud.**

### 🔒 Protección de Archivos (Opcional)

Para prevenir modificaciones accidentales:

```bash
# Hacer archivos de solo lectura
chmod 444 EN_NicolasFredes_CV.pdf
chmod 444 compare_pdf.py

# Verificar
ls -l EN_NicolasFredes_CV.pdf compare_pdf.py
```

Para volver a hacerlos editables (si realmente necesitas):

```bash
chmod 644 EN_NicolasFredes_CV.pdf
chmod 644 compare_pdf.py
```

---

## 🎓 Casos de Uso

### Actualizar CV

```bash
# 1. Editar contenido en generate_cv_from_python.py
vim generate_cv_from_python.py

# 2. Regenerar
python3 generate_cv_from_python.py

# 3. Verificar cambios
evince generated.pdf
```

### Mejorar Similitud

```bash
# 1. Comparar
python3 compare_pdf.py > report.txt

# 2. Leer recomendaciones
less report.txt

# 3. Ajustar parámetros en generate_cv_from_python.py

# 4. Repetir
```

### Versionamiento

```bash
# Git workflow
git add generate_cv_from_python.py
git commit -m "Adjust margins to improve similarity"
git push
```

---

## 📚 Recursos Adicionales

### Documentación ReportLab

- [ReportLab User Guide](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [ReportLab API](https://www.reportlab.com/documentation/)

### PyMuPDF (fitz)

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)

### Fuentes

- [MS Core Fonts](https://mscorefonts2.sourceforge.net/)
- [Liberation Fonts](https://github.com/liberationfonts/liberation-fonts)

---

## 🤝 Contribuir

### Reglas Básicas

1. **NUNCA** modificar `EN_NicolasFredes_CV.pdf`
2. **NUNCA** modificar `compare_pdf.py`
3. Solo modificar `generate_cv_from_python.py` para mejorar similitud
4. Probar cambios antes de commit:
   ```bash
   python3 generate_cv_from_python.py
   python3 compare_pdf.py
   ```

### Workflow de Contribución

1. Fork del repositorio
2. Crear branch: `git checkout -b mejora-margenes`
3. Modificar SOLO `generate_cv_from_python.py`
4. Probar: `python3 compare_pdf.py`
5. Commit: `git commit -m "Mejora márgenes (+5 pts)"`
6. Push: `git push origin mejora-margenes`
7. Pull Request con el nuevo score

---

## 📄 Licencia

Este proyecto es para uso personal/educativo.

---

## 👤 Autor

**Nicolás Fredes**  
CV Template Owner & System Developer

---

## 🎯 Objetivo Final

**Lograr Score > 95/100**

Una vez alcanzado, el sistema genera PDFs prácticamente idénticos al original, permitiendo:
- ✅ CV profesional como código
- ✅ Actualizaciones rápidas
- ✅ Versionamiento completo
- ✅ Portabilidad total
- ✅ Automatización completa

---

**Última actualización:** Octubre 2025  
**Versión del comparador:** 2.0 Ultra-Detailed  
**Score actual:** 36.90/100  
**Objetivo:** > 95/100

