#!/usr/bin/env python3
"""Troca título e/ou thumbnail de um vídeo já publicado (roda na Action `atualizar`). Serve para os testes A/B.

Pedido: ajustes/<nome>.json
    {"video_id": "...", "ep": "ep01",
     "titulo": "novo título",                                    (opcional)
     "thumb": {"mod": "episodes.ep01_nome_completo",                   (opcional: THUMB do módulo +
               "override": {"ordem": "NÃO RESPONDA"}}        campos trocados)
     "motivo": "uma linha"}

Depois de aplicar, o JSON ganha "antes" (título antigo), "aplicado_em" e "avisos". Pedidos com "aplicado_em" são pulados.
Para desfazer um teste, crie outro pedido com o título/thumb antigos.
"""
import datetime as dt
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
FUSO = dt.timezone(dt.timedelta(hours=-3))


def log(*a):
    print('[atualizar]', *a, flush=True)


def render_thumb(spec_pedido, saida):
    import importlib
    from engine import thumb
    m = importlib.import_module(spec_pedido['mod'])
    spec = dict(m.THUMB)
    for k, v in spec_pedido.get('override', {}).items():
        spec[k] = tuple(v) if isinstance(v, list) else v
    png = saida.replace('.jpg', '.png')
    # mesma escolha do engine.thumb._cli: capa própria mm_<cena>, senão mm() (com 'ordem') ou generic()
    fn = getattr(thumb, f"mm_{spec.get('cena')}", None) if spec.get('cena') else None
    (fn or (thumb.mm if 'ordem' in spec else thumb.generic))(spec, png)
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', png, '-vf', 'scale=1280:720', '-q:v', '2', saida])
    return saida


def aplicar(caminho):
    pedido = json.load(open(caminho, encoding='utf-8'))
    if pedido.get('aplicado_em'):
        log(caminho, 'já aplicado; pulando')
        return
    from publicar import youtube
    from googleapiclient.http import MediaFileUpload
    yt = youtube()
    vid = pedido['video_id']
    avisos = []
    item = yt.videos().list(part='snippet', id=vid).execute()['items'][0]
    sn = item['snippet']
    pedido['antes'] = {'titulo': sn['title']}
    if pedido.get('titulo'):
        novo = {k: sn[k] for k in ('title', 'description', 'categoryId', 'tags', 'defaultLanguage') if k in sn}
        novo['title'] = pedido['titulo'][:100]
        yt.videos().update(part='snippet', body={'id': vid, 'snippet': novo}).execute()
        log(vid, 'título:', sn['title'], '->', novo['title'])
    if pedido.get('thumb'):
        os.makedirs(os.path.join(RAIZ, 'build', 'ajustes'), exist_ok=True)
        jpg = render_thumb(pedido['thumb'], os.path.join(RAIZ, 'build', 'ajustes', f'{vid}.jpg'))
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(jpg, mimetype='image/jpeg')).execute()
            log(vid, 'thumbnail trocada')
        except Exception as e:  # noqa: BLE001
            avisos.append(f'thumbnail não foi aceita: {e}')
    pedido['aplicado_em'] = dt.datetime.now(FUSO).isoformat(timespec='seconds')
    pedido['avisos'] = avisos
    json.dump(pedido, open(caminho, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    sys.path.insert(0, os.path.join(RAIZ, 'tools'))
    for c in sys.argv[1:]:
        aplicar(c)
