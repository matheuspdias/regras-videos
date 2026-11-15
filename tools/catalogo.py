"""Imprime o catálogo atual: cenários e posições, elenco, poses, objetos e efeitos.
uso: python3 tools/catalogo.py
"""
import re
import sys
sys.path.insert(0, '.')
from engine.scenes import BG, SLOTS
from engine.chars import CAST

print('# CENÁRIOS (bg) e posições (slots: x, y_pés, escala)')
for k in BG:
    print(f'- {k}: ' + (', '.join(SLOTS.get(k, {}).keys()) or '(sem personagens: tela de efeito)'))
print('\n# ELENCO (id: nome)')
for k, v in CAST.items():
    print(f'- {k}: {v["name"]}')
print('\n# POSE (kwargs de C)')
print("eyes: normal wide happy sad angry closed half | mouth: smile grin flat frown o wavy | arms: down wave face point hip up hold cross shrug")
print("facing: 1/-1 | look: -1..1 | sweat, blush, sit, lie, veil, mustache: True | prop: " + ', '.join(sorted(set(re.findall(r"prop == '(\w+)'", open('engine/chars.py').read())))))
print('\n# EFEITOS (fx)')
src = open('engine/render.py').read()
print(', '.join(sorted(set(re.findall(r"'(\w+)' in fx", src)))))
print('\n# CÂMERA (cam): zoom, to, focus=<id>, cx, cy')
