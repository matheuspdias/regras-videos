"""Confere se cada fala do episódio tem o áudio certo (existência + duração igual à do HeyGen).

uso: python3 tools/verify_audio.py episodes.ep03_xxx ep03
Sai com código 1 se algo estiver errado.
"""
import importlib
import subprocess
import sys

mod, ep = sys.argv[1], sys.argv[2]
sys.path.insert(0, '.')
lines = importlib.import_module(mod).LINES
rows = {int(r.split('\t')[0]): r.rstrip('\n').split('\t') for r in open(f'episodes/{ep}/tts.tsv') if r.strip()}
bad = []
for i, line in enumerate(lines):
    if i not in rows:
        bad.append(f'{i}: sem áudio gerado ({line[1][:40]})')
        continue
    exp = float(rows[i][3])
    try:
        d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f'media/{ep}/audio/{i:03d}.mp3']))
    except Exception:
        bad.append(f'{i}: arquivo ausente')
        continue
    if abs(d - exp) > 0.2:
        bad.append(f'{i}: duração {d:.2f}s, esperado {exp:.2f}s ({line[1][:40]})')
extra = [k for k in rows if k >= len(lines)]
if extra:
    bad.append(f'tts.tsv tem índices além do roteiro: {extra}')
if bad:
    print('ERRO NOS ÁUDIOS:\n' + '\n'.join(bad))
    sys.exit(1)
print(f'ok: {len(lines)} falas, todos os áudios conferem')
