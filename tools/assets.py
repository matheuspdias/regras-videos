"""Gera a lista de download (assets_in/*.json) dos áudios de um episódio que ainda não estão em media/.

uso: python3 tools/assets.py ep03
Lê episodes/<ep>/tts.tsv  (linhas: indice<TAB>voice_id<TAB>audio_id<TAB>duracao)
"""
import json
import os
import sys
import time

ep = sys.argv[1]
base = 'https://resource2.heygen.ai/text_to_speech/cdea5e656a244864a1032edcb4fae01d'
rows = [l.rstrip('\n').split('\t') for l in open(f'episodes/{ep}/tts.tsv') if l.strip()]
files = []
for r in rows:
    idx, voice, aid = int(r[0]), r[1], r[2]
    dest = f'media/{ep}/audio/{idx:03d}.mp3'
    if not os.path.exists(dest):
        files.append({'url': f'{base}/{voice}/id={aid}.mp3', 'dest': dest})
os.makedirs('assets_in', exist_ok=True)
out = f'assets_in/{ep}_{int(time.time())}.json'
json.dump({'files': files}, open(out, 'w'), indent=0)
print(out, len(files), 'arquivos')
