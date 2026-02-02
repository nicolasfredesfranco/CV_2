# 🔒 POSICIONES PERFECTAS DE RECTÁNGULOS - NO MODIFICAR 🔒

## ⚠️ ADVERTENCIA CRÍTICA ⚠️

Este documento registra las posiciones **PERFECTAS** de los 4 rectángulos de la columna izquierda del CV.
Estas posiciones fueron ajustadas meticulosamente a través de múltiples iteraciones hasta lograr
alineación visual perfecta con sus headers respectivos.

**CUALQUIER MODIFICACIÓN A ESTAS POSICIONES EMPEORARÁ LA ALINEACIÓN.**

## Estado Actual (Perfecto)

```
🔒 EDUCATION:          Y = 644.32  (PERFECTO - BLOQUEADO)
🔒 PAPERS & WORKSHOPS: Y = 463.00  (PERFECTO - BLOQUEADO)
🔒 SKILLS:             Y = 373.93  (PERFECTO - BLOQUEADO)
🔒 LANGUAGES:          Y =  78.59  (PERFECTO - BLOQUEADO)
```

## Características de la Alineación

- ✅ Cada rectángulo está perfectamente centrado vertical con su header
- ✅ Espaciado superior e inferior del texto es idéntico dentro del rectángulo
- ✅ Alineación consistente con el estilo del header "EXPERIENCE" en columna derecha
- ✅ Dimensiones idénticas (Width=155.91, Height=18.0039)
- ✅ Posición X idéntica (X=42.00)

## Backup de Seguridad

Un backup permanente fue creado:
- `data/shapes.json.PERFECT_ALIGNMENT_BACKUP_20260202_173454`

## Git Commit de Referencia

```
commit 25d9160
Author: Nicolás Fredes
Date:   Sun Feb 2 17:34:54 2026

🔒 PUNTO DE INFLEXIÓN: Alineación perfecta de todos los rectángulos
```

## Sistema de Coordenadas

- **Sistema PDF**: Y=0 está en la parte inferior, Y aumenta hacia arriba
- **Altura de página**: 806.0 puntos
- **Conversión desde coordinates.json**: `Y_pdf = 806.0 - Y_texto`
- **Offset aplicado**: Aproximadamente +35-39 puntos desde la posición calculada

## Historia de Ajustes

### EDUCATION
- Posición inicial: Variable (pre-ajustes)
- Ajustes aplicados: +13 puntos desde backup original
- **Posición final: Y=644.32** ✅

### PAPERS & WORKSHOPS
- Creado como copia exacta de EDUCATION
- Ajustes iterativos: múltiples incrementos pequeños
- **Posición final: Y=463.00** ✅

### SKILLS
- Base calculada: Y=334.93 (desde coordinates.json)
- Offset total aplicado: +39 puntos
- **Posición final: Y=373.93** ✅

### LANGUAGES
- Base calculada: Y=39.59 (desde coordinates.json)
- Offset total aplicado: +39 puntos
- **Posición final: Y=78.59** ✅

## Instrucciones para el Futuro

### ❌ NUNCA hacer:
- Modificar las coordenadas Y de estos 4 rectángulos
- "Optimizar" o "mejorar" las posiciones
- Aplicar fórmulas matemáticas para "corregir" alineación
- Confiar solo en cálculos automáticos sin verificación visual

### ✅ SIEMPRE hacer:
- Si se necesita modificar shapes.json, preservar las posiciones Y de estos 4 rectángulos
- Verificar visualmente en el PDF después de cualquier cambio en el sistema
- Usar el backup en caso de modificaciones accidentales
- Consultar este documento antes de cualquier cambio

## Restauración desde Backup

Si las posiciones se modifican accidentalmente:

```bash
# Restaurar desde backup
cp data/shapes.json.PERFECT_ALIGNMENT_BACKUP_20260202_173454 data/shapes.json

# Regenerar PDF
python main.py

# Verificar visualmente
```

## Fecha de Creación

**2 de Febrero de 2026, 17:34 hrs**

---

**⚠️ RECUERDA: ESTAS POSICIONES ESTÁN PERFECTAS. NO LAS MODIFIQUES. ⚠️**
