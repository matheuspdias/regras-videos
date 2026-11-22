#!/usr/bin/env python3
"""Envia um episódio ao YouTube como Programado (roda na Action `publicar`).

Pedido de publicação: publicar/epNN.json
    {"ep": "ep05", "mod": "episodes.ep05_slug", "publicar_em": "2026-11-24T20:00:00-03:00"}
Título, descrição e tags saem de episodes/epNN/youtube.md. O vídeo, a thumb e a legenda saem de build/epNN/
(gerados pelo tools/produce.sh no próprio runner).

Depois do envio o JSON ganha "video_id", "status" e "avisos", e a agenda passa de `entregue` para `agendado`.

Modos:
  python3 tools/publicar.py publicar/ep09.json   envia o episódio
  python3 tools/publicar.py --teste              sobe um vídeo de 5 s como NÃO LISTADO, confere se o YouTube
                                                 respeitou (projeto não travado) e apaga o vídeo de teste
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUSO = dt.timezone(dt.timedelta(hours=-3))
CATEGORIA = '24'  # Entretenimento


def log(*a):
    print('[publicar]', *a, flush=True)


def youtube():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    cred = Credentials(None, refresh_token=os.environ['YT_REFRESH_TOKEN'], token_uri='https://oauth2.googleapis.com/token',
                       client_id=os.environ['YT_CLIENT_ID'], client_secret=os.environ['YT_CLIENT_SECRET'])
    return build('youtube', 'v3', credentials=cred, cache_discovery=False)


def secao(md, nome):
    m = re.search(r'\*\*' + nome + r'\*\*\s*\n(.*?)(?=\n\*\*[^*\n]+\*\*\s*\n|\Z)', md, re.S)
    return m.group(1).strip() if m else ''


def metadados(ep):
    md = open(os.path.join(RAIZ, 'episodes', ep, 'youtube.md'), encoding='utf-8').read()
    titulo, desc, tags = secao(md, 'Título'), secao(md, 'Descrição'), secao(md, 'Tags')
    if not titulo or not desc:
        sys.exit(f'youtube.md de {ep} sem Título ou Descrição')
    tags = [t.strip() for t in tags.replace('\n', ',').split(',') if t.strip()]
    # o YouTube aceita até 500 caracteres somando as tags
    out, tot = [], 0
    for t in tags:
        if tot + len(t) + 2 > 480:
            break
        out.append(t)
        tot += len(t) + 2
    desc = desc.replace('<', '‹').replace('>', '›')  # a API recusa < e > na descrição
    return titulo[:100], desc[:5000], out


def subir(yt, arquivo, corpo):
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload
    media = MediaFileUpload(arquivo, mimetype='video/mp4', chunksize=16 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part='snippet,status', body=corpo, media_body=media, notifySubscribers=True)
    resp, tent = None, 0
    while resp is None:
        try:
            st, resp = req.next_chunk()
            if st:
                log(f'enviando: {int(st.progress() * 100)}%')
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504) and tent < 6:
                tent += 1
                time.sleep(2 ** tent)
                continue
            raise
    return resp


def corpo_video(titulo, desc, tags, privacidade, quando=None):
    status = dict(privacyStatus=privacidade, selfDeclaredMadeForKids=False, containsSyntheticMedia=True,
                  embeddable=True)
    if quando:
        status['publishAt'] = quando.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    return dict(snippet=dict(title=titulo, description=desc, tags=tags, categoryId=CATEGORIA,
                             defaultLanguage='pt-BR', defaultAudioLanguage='pt-BR'), status=status)


def publicar(caminho):
    from googleapiclient.http import MediaFileUpload
    pedido = json.load(open(caminho, encoding='utf-8'))
    ep = pedido['ep']
    if pedido.get('video_id'):
        log(f'{ep} já enviado ({pedido["video_id"]}); nada a fazer')
        return
    quando = dt.datetime.fromisoformat(pedido['publicar_em'])
    if quando < dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=30):
        sys.exit(f'{ep}: publicar_em {quando} já passou (ou falta menos de 30 min); corrija a data no JSON')
    titulo, desc, tags = metadados(ep)
    video = os.path.join(RAIZ, 'build', ep, f'{ep}.mp4')
    yt = youtube()
    log(f'{ep}: enviando "{titulo}" para {quando.astimezone(FUSO):%d/%m %H:%M}')
    resp = subir(yt, video, corpo_video(titulo, desc, tags, 'private', quando))
    vid = resp['id']
    log(f'enviado: https://youtu.be/{vid}')
    avisos = []
    st = resp.get('status', {})
    if not st.get('publishAt'):
        avisos.append('o YouTube não manteve o agendamento (vídeo travado como privado?): agende à mão no Studio')
    thumb = os.path.join(RAIZ, 'build', ep, 'thumb.jpg')
    try:
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb, mimetype='image/jpeg')).execute()
        log('thumbnail definida')
    except Exception as e:  # noqa: BLE001
        avisos.append(f'thumbnail não foi aceita: {e}')
    srt = os.path.join(RAIZ, 'build', ep, f'{ep}_legenda_pt.srt')
    try:
        yt.captions().insert(part='snippet', body=dict(snippet=dict(videoId=vid, language='pt-BR', name='Português',
                                                                     isDraft=False)),
                             media_body=MediaFileUpload(srt, mimetype='application/octet-stream')).execute()
        log('legenda enviada')
    except Exception as e:  # noqa: BLE001
        avisos.append(f'legenda não foi aceita: {e}')
    for a in avisos:
        log('AVISO:', a)
    pedido.update(video_id=vid, link=f'https://youtu.be/{vid}', status='agendado' if not avisos else 'enviado com avisos',
                  enviado_em=dt.datetime.now(FUSO).isoformat(timespec='seconds'), avisos=avisos)
    json.dump(pedido, open(caminho, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ag = os.path.join(RAIZ, 'episodes', 'agenda.md')
    linhas = open(ag, encoding='utf-8').read().split('\n')
    for i, l in enumerate(linhas):
        if l.startswith(f'| {ep} |'):
            linhas[i] = re.sub(r'\|\s*entregue\s*\|\s*$', '| agendado (auto) |', l)
    open(ag, 'w', encoding='utf-8').write('\n'.join(linhas))
    resumo(f'**{ep}** enviado: https://youtu.be/{vid} — publica {quando.astimezone(FUSO):%d/%m às %H:%M}'
           + ''.join(f'\n- ⚠️ {a}' for a in avisos))


def teste():
    arq = '/tmp/teste.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=0x1b1f3b:s=1280x720:d=5',
                    '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', arq], check=True)
    yt = youtube()
    resp = subir(yt, arq, corpo_video('teste do publicador (será apagado)', 'teste automático', [], 'unlisted'))
    vid = resp['id']
    time.sleep(5)
    st = yt.videos().list(part='status', id=vid).execute()['items'][0]['status']
    log('status devolvido:', json.dumps(st))
    ok = st.get('privacyStatus') == 'unlisted'
    yt.videos().delete(id=vid).execute()
    log('vídeo de teste apagado')
    msg = ('✅ projeto LIBERADO: o YouTube aceitou o vídeo como não listado' if ok else
           '❌ projeto TRAVADO: o YouTube forçou o vídeo para privado (precisa de auditoria ou de outro projeto)')
    log(msg)
    resumo(msg)


def resumo(txt):
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        open(os.environ['GITHUB_STEP_SUMMARY'], 'a', encoding='utf-8').write(txt + '\n')


if __name__ == '__main__':
    if sys.argv[1:] == ['--teste']:
        teste()
    else:
        for c in sys.argv[1:]:
            publicar(c)
