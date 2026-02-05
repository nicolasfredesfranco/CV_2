#!/usr/bin/env python3
"""
Script mejorado para calcular y distribuir espacios de manera casi homogénea
para que las líneas toquen exactamente X=587
"""

import json

TARGET_X = 587.0

# Factor de corrección empírico (ajustable basado en observaciones)
# Para Trebuchet MS 10pt, aproximadamente:
CHAR_AVG_WIDTH = 4.8  # Ancho promedio por carácter (ajuste fino)
SPACE_WIDTH = 2.5     # Ancho de un espacio

def estimate_current_width(text):
    """Estima el ancho actual del texto en puntos"""
    # Contar caracteres y espacios
    char_count = len(text.replace(' ', ''))
    space_count = text.count(' ')
    
    estimated_width = (char_count * CHAR_AVG_WIDTH) + (space_count * SPACE_WIDTH)
    return estimated_width

def calculate_total_spaces_needed(text, left_x):
    """
    Calcula el número TOTAL de espacios que necesitamos agregar
    """
    current_width = estimate_current_width(text)
    current_right_edge = left_x + current_width
    gap_in_points = TARGET_X - current_right_edge
    
    # Convertir gap en puntos a número de espacios necesarios
    total_spaces_needed = int(gap_in_points / SPACE_WIDTH)
    
    return total_spaces_needed, gap_in_points

def distribute_spaces_optimally(text, total_spaces):
    """
    Distribuye espacios de manera casi homogénea entre palabras
    
    Si total_spaces es POSITIVO: agrega espacios
    Si total_spaces es NEGATIVO: quita espacios
    """
    words = text.split()
    num_gaps = len(words) - 1
    
    if num_gaps == 0:
        return text
    
    if total_spaces == 0:
        # No hay cambios necesarios - mantener espaciado actual
        return ' '.join(words)
    
    elif total_spaces > 0:
        # AGREGAR espacios
        base_spaces = total_spaces // num_gaps
        extra_spaces = total_spaces % num_gaps
        
        # Crear lista de espacios por gap
        spaces_per_gap = []
        for i in range(num_gaps):
            if i < extra_spaces:
                spaces_per_gap.append(base_spaces + 1)
            else:
                spaces_per_gap.append(base_spaces)
        
        # Construir texto con espacios distribuidos
        result_parts = []
        for i, word in enumerate(words):
            result_parts.append(word)
            if i < num_gaps:
                total_gap_spaces = 1 + spaces_per_gap[i]  # 1 base + extras
                result_parts.append(' ' * total_gap_spaces)
        
        return ''.join(result_parts)
    
    else:
        # QUITAR espacios (total_spaces es negativo)
        # Contar cuántos espacios EXTRA tiene el texto actual
        current_extra_spaces = 0
        for i in range(len(text) - 1):
            if text[i] == ' ' and i > 0 and text[i-1] == ' ':
                current_extra_spaces += 1
        
        # Calcular cuántos espacios debemos quitar
        spaces_to_remove = abs(total_spaces)
        spaces_to_remove = min(spaces_to_remove, current_extra_spaces)  # No podemos quitar más de los que hay
        
        if spaces_to_remove == 0:
            return ' '.join(words)  # Ya está en espaciado simple
        
        # Distribución de qué gaps perderán espacios
        base_remove = spaces_to_remove // num_gaps
        extra_remove = spaces_to_remove % num_gaps
        
        # Crear lista: cuántos espacios EXTRAS debe tener cada gap (puede ser 0)
        current_spaces = []
        # Primero detectar cuántos espacios extra tiene cada gap actualmente
        parts = text.split()
        for i in range(len(parts) - 1):
            # Encontrar cuántos espacios hay entre parts[i] y parts[i+1]
            idx = text.find(parts[i])
            next_idx = text.find(parts[i+1], idx + len(parts[i]))
            gap_size = next_idx - (idx + len(parts[i]))
            current_spaces.append(max(0, gap_size - 1))  # espacios extra (sin contar el básico)
        
        # Calcular nueva distribución
        new_extra_spaces = []
        for i in range(num_gaps):
            remove_from_this_gap = base_remove if i >= extra_remove else base_remove + 1
            new_extra = max(0, current_spaces[i] - remove_from_this_gap)
            new_extra_spaces.append(new_extra)
        
        # Construir texto
        result_parts = []
        for i, word in enumerate(words):
            result_parts.append(word)
            if i < num_gaps:
                total_gap_spaces = 1 + new_extra_spaces[i]  # 1 base + extras
                result_parts.append(' ' * total_gap_spaces)
        
        return ''.join(result_parts)

# Cargar coordinates.json
with open('data/coordinates.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Patrones para identificar las 5 líneas (buscar sin importar espacios)
patterns = [
    ("Ideated", "designed", "implemented"),
    ("mutual", "information", "commercial"),
    ("Athia",),
    ("solution", "provided", "data-driven"),
    ("behaviors", "multi-threading")
]

target_lines = []

# Encontrar las líneas
for i, item in enumerate(data):
    if 'text' in item:
        # Normalizar espacios para buscar
        normalized_text = ' '.join(item['text'].split())
        
        for pattern_words in patterns:
            # Verificar si todas las palabras del patrón están en el texto
            if all(word in normalized_text for word in pattern_words):
                # Evitar duplicados
                if not any(tl['index'] == i for tl in target_lines):
                    target_lines.append({
                        'index': i,
                        'text': item['text'],
                        'x': item['x'],
                        'pattern': ' '.join(pattern_words)
                    })
                    break

print("=" * 80)
print("CÁLCULO OPTIMIZADO DE ESPACIADO PARA 5 LÍNEAS")
print("=" * 80)

if len(target_lines) != 5:
    print(f"ERROR: Se encontraron {len(target_lines)} líneas en lugar de 5")
    exit(1)

# Procesar cada línea
results = []
for idx, target in enumerate(target_lines, 1):
    text = target['text']
    left_x = target['x']
    
    # Calcular espacios totales necesarios
    total_spaces, gap_pts = calculate_total_spaces_needed(text, left_x)
    
    # Distribuir espacios
    new_text = distribute_spaces_optimally(text, total_spaces)
    
    # Calcular nueva estimación
    new_width = estimate_current_width(new_text)
    new_right_edge = left_x + new_width
    final_gap = TARGET_X - new_right_edge
    
    print(f"\nLínea {idx}: {target['pattern']}")
    print(f"  Left X: {left_x}")
    print(f"  Gap actual: {gap_pts:.1f} pts")
    print(f"  Espacios totales a agregar: {total_spaces}")
    
    words = text.split()
    num_gaps = len(words) - 1
    if total_spaces > 0 and num_gaps > 0:
        base = total_spaces // num_gaps
        extra = total_spaces % num_gaps
        print(f"  Distribución: {base} espacios base, {extra} gap(s) con +1 extra")
    
    print(f"  Gap final estimado: {final_gap:.1f} pts")
    print(f"  Texto original: {text[:50]}...")
    print(f"  Texto nuevo:    {new_text[:50]}...")
    
    # Actualizar en data
    data[target['index']]['text'] = new_text
    
    results.append({
        'line': idx,
        'total_spaces': total_spaces,
        'gap': gap_pts,
        'final_gap': final_gap
    })

print("\n" + "=" * 80)
print("RESUMEN:")
for r in results:
    status = "✓ OK" if abs(r['final_gap']) < 5 else "⚠ Revisar"
    print(f"  Línea {r['line']}: {r['total_spaces']:2d} espacios | Gap final: {r['final_gap']:+6.1f}pts {status}")

print("\nGuardando cambios...")
with open('data/coordinates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Cambios guardados en coordinates.json")
print("=" * 80)
print("\nSiguientes pasos:")
print("  1. python3 main.py")
print("  2. Desplegar en browser a 500% zoom")
print("  3. Verificar visualmente que los bordes TOQUEN (no crucen) la línea vertical")
print("=" * 80)
