#!/usr/bin/env python3
"""
Reset de espaciado para las 5 líneas de DEUNA + recálculo preciso
"""

import json

# Cargar coordinates.json
with open('data/coordinates.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Patrones para identificar las 5 líneas únicas
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
        normalized_text = ' '.join(item['text'].split())
        
        for pattern_words in patterns:
            if all(word in normalized_text for word in pattern_words):
                if not any(tl['index'] == i for tl in target_lines):
                    target_lines.append({
                        'index': i,
                        'text': item['text'],
                        'pattern': ' '.join(pattern_words)
                    })
                    break

print("=" * 80)
print("RESET DE ESPACIADO A SIMPLE")
print("=" * 80)

if len(target_lines) != 5:
    print(f"ERROR: Se encontraron {len(target_lines)} líneas")
    exit(1)

# RESET: Normalizar todos los espacios múltiples a espacios simples
for idx, target in enumerate(target_lines, 1):
    old_text = target['text']
    new_text = ' '.join(old_text.split())  # Normalize all spaces to single
    
    print(f"\nLínea {idx}: {target['pattern']}")
    print(f"  ANTES: {old_text[:60]}...")
    print(f"  DESPUÉS: {new_text[:60]}...")
    
    data[target['index']]['text'] = new_text

print("\n" + "=" * 80)
print("Guardando...")
with open('data/coordinates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Reseteo completado")
print("=" * 80)
print("\nAhora ejecuta:")
print("  python3 main.py")
print("  Verifica visualmente la posición de las líneas")
print("  Luego podemos calcular el espaciado necesario correctamente")
print("=" * 80)
