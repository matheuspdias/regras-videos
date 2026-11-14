# regras-videos — canal Manual da Madrugada

Motor de vídeo (pycairo + ffmpeg) e episódios do canal de YouTube **Manual da Madrugada** (terror de regras, modelado no
Lullorin e adaptado ao Brasil). Para produzir um episódio, siga **PRODUCAO.md** do começo ao fim.

- `engine/` — personagens (`chars.py`), cenários (`scenes.py`), render (`render.py`), legenda (`srt.py`), thumbnail (`thumb.py` → `mm()`), marca (`branding.py`).
- `episodes/` — roteiros (`epNN_<slug>.py`), `temas.md` (fila), `agenda.md` (datas), `epNN/` (tts.tsv, youtube.md).
- `media/` — áudios baixados pelo GitHub Action `fetch-assets` (o shell não acessa o HeyGen).
- `tools/` — `assets.py`, `verify_audio.py`, `produce.sh`, `catalogo.py`.
- `branding/` — foto de perfil, banner e descrição do canal.
- `build/` — saídas (fora do git).

Não altere `episodes/ep01_*` (já entregue). Commits com a atribuição padrão do Claude.
