#!/usr/bin/env bash
# Renderiza e empacota um episódio já com áudios baixados.
# uso: tools/produce.sh episodes.ep03_xxx ep03
set -euo pipefail
MOD=$1; EP=$2
cd "$(dirname "$0")/.."
python3 tools/verify_audio.py "$MOD" "$EP"
mkdir -p "build/$EP"
python3 -m engine.render "$MOD" "$EP" | tee "build/$EP/render.log"
python3 -m engine.srt "$MOD" "$EP" "build/$EP/${EP}_legenda_pt.srt"
python3 -m engine.thumb "build/$EP/thumb.png" "$MOD"
ffmpeg -v error -y -i "build/$EP/thumb.png" -vf scale=1280:720 -q:v 2 "build/$EP/thumb.jpg"
TITLE=$(python3 -c "import importlib,sys; sys.path.insert(0,'.'); print(importlib.import_module('$MOD').TITLE)")
SAFE=$(python3 -c "import unicodedata,re,sys; t=unicodedata.normalize('NFKD',sys.argv[1]).encode('ascii','ignore').decode(); print(re.sub(r'[^A-Za-z0-9 ]','',t).strip())" "$TITLE")
OUT="build/$EP/entrega"; rm -rf "$OUT"; mkdir -p "$OUT"
# cópia de entrega com bitrate limitado (o envio pelo chat aceita até 400 MiB; ~10 min de vídeo dá ~340 MB)
ffmpeg -v error -y -i "build/$EP/$EP.mp4" -c:v libx264 -preset veryfast -b:v 4400k -maxrate 4800k -bufsize 9600k \
  -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT/$SAFE.mp4"
cp "build/$EP/thumb.jpg" "$OUT/${EP}_thumb.jpg"
cp "build/$EP/${EP}_legenda_pt.srt" "$OUT/"
cp "episodes/$EP/youtube.md" "$OUT/${EP}_titulo_descricao.md"
# quadros de conferência
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "build/$EP/$EP.mp4")
python3 - "$EP" "$DUR" <<'PY'
import subprocess, sys
ep, dur = sys.argv[1], float(sys.argv[2])
sel = '+'.join(f'eq(n\\,{int(dur*24*k/13)})' for k in range(1, 13))
subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', f'build/{ep}/{ep}.mp4', '-vf', f"select='{sel}',scale=480:270,tile=4x3:padding=4", '-vsync', 'vfr', '-frames:v', '1', f'build/{ep}/conferencia.png'])
PY
echo "duração: $DUR s"
ls -la "$OUT"
