"""Gera o pedido de vozes (tts_in/*.json) para a Action `tts` gerar pela API do HeyGen.

uso: python3 tools/tts_jobs.py episodes.epNN_slug epNN
Inclui só as falas que ainda não têm linha em episodes/epNN/tts.tsv. Depois: commit + push e espere a Action
(ela gera os mp3 em media/epNN/audio/, preenche o tts.tsv e apaga o pedido). Erros ficam em tts_out/.
"""
import importlib
import json
import os
import sys
import time

mod, ep = sys.argv[1], sys.argv[2]
sys.path.insert(0, '.')
m = importlib.import_module(mod)
done = set()
tsv = f'episodes/{ep}/tts.tsv'
if os.path.exists(tsv):
    done = {int(r.split('\t')[0]) for r in open(tsv) if r.strip()}
jobs = []
for i, line in enumerate(m.LINES):
    if i in done:
        continue
    sp, text = line[0], line[1]
    jobs.append({'i': i, 'voice': m.VOICES[sp], 'text': text})
os.makedirs('tts_in', exist_ok=True)
out = f'tts_in/{ep}_{int(time.time())}.json'
json.dump({'ep': ep, 'jobs': jobs}, open(out, 'w'), ensure_ascii=False, indent=0)
print(out, len(jobs), 'falas')
