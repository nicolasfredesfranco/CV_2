#!/usr/bin/env python3
"""
Aplicar espaciado homogéneo de 4 espacios (como ZENTA GROUP que funciona perfecto)
"""

import json

# Cargar
with open('data/coordinates.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Los patrones
patterns = [
    ("Ideated", "designed", "implemented"),
    ("mutual", "information", "commercial"),
    ("Athia",),
    ("solution", "provided", "data-driven"),
    ("behaviors", "multi-threading")
]

target_lines = []

# Encontrar
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
print("APLICANDO ESPACIADO DE 4 ESPACIOS (como ZENTA GROUP)")
print("=" * 80)

if len(target_lines) != 5:
    print(f"ERROR: {len(target_lines)} líneas encontradas")
    exit(1)

# Aplicar 4 espacios entre palabras
for idx, target in enumerate(target_lines, 1):
    words = target['text'].split()
    # Unir con 4 espacios
    new_text = '    '.join(words)  # 4 espacios
    
    print(f"\nLínea {idx}: {target['pattern']}")
    print(f"  Palabras: {len(words)}")
    print(f"  ANTES: {target[' text'][:50]}...")
    print(f"  DESPUÉS: {new_text[:50]}...")
    
    data[target['index']]['text'] = new_text

print("\n" + "=" * 80)
with open('data/coordinates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ Espaciado de 4 espacios aplicado")
print("=" * 80)
