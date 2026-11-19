# regras-videos — canal Manual da Madrugada

Motor de vídeo (pycairo + ffmpeg) e episódios do canal de YouTube **Manual da Madrugada** (terror de regras, modelado no
Lullorin e adaptado ao Brasil). Para produzir um episódio, siga **PRODUCAO.md** do começo ao fim.

- `engine/` — personagens (`chars.py`), cenários (`scenes.py`), render (`render.py`), legenda (`srt.py`), thumbnail (`thumb.py` → `mm()`), marca (`branding.py`).
- `episodes/` — roteiros (`epNN_<slug>.py`), `temas.md` (fila), `agenda.md` (datas), `epNN/` (tts.tsv, youtube.md).
- `media/` — áudios gerados pela GitHub Action `tts` (API do HeyGen; o shell não acessa o HeyGen).
- `tools/` — `tts_jobs.py` (pedido de vozes), `tts_api.py` (roda na Action), `vertical.py` (TikTok), `verify_audio.py`, `produce.sh`, `catalogo.py`.
- `branding/` — foto de perfil, banner e descrição do canal.
- `build/` — saídas (fora do git).

Não altere episódios já publicados no YouTube (veja `episodes/agenda.md`). Commits com a atribuição padrão do Claude.
