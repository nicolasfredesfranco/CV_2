#!/usr/bin/env python3
"""
Aplicar espaciado de 3 espacios (reducido desde 4)
"""

import json

with open('data/coordinates.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

patterns = [
    ("Ideated", "designed", "implemented"),
    ("mutual", "information", "commercial"),
    ("Athia",),
    ("solution", "provided", "data-driven"),
    ("behaviors", "multi-threading")
]

target_lines = []

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
print("APLICANDO ESPACIADO DE 3 ESPACIOS")
print("=" * 80)

if len(target_lines) != 5:
    print(f"ERROR: {len(target_lines)} líneas")
    exit(1)

for idx, target in enumerate(target_lines, 1):
    words = target['text'].split()
    new_text = '   '.join(words)  # 3 espacios
    
    print(f"\nLínea {idx}: {target['pattern']}")
    print(f"  Espacios: 3 entre {len(words)} palabras")
    
    data[target['index']]['text'] = new_text

print("\n" + "=" * 80)
with open('data/coordinates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✓ 3 espacios aplicado")
print("=" * 80)
