#!/usr/bin/env python3
"""Puxa os números do canal (YouTube Data + Analytics + Reporting API) e grava em analytics/.

Roda na GitHub Action `analytics` (o shell do Claude não acessa googleapis).
Secrets: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (token do canal deste repo).

Saídas:
  analytics/AAAA-MM-DD.json  — snapshot completo (canal, vídeos, retenção, impressões/CTR)
  analytics/ultimo.md        — resumo legível do snapshot mais recente
  analytics/reach/*.csv      — relatórios brutos de impressões/CTR já baixados (cache)
"""
import csv, datetime as dt, io, json, os, sys, urllib.error, urllib.parse, urllib.request

OUT = 'analytics'
REACH = os.path.join(OUT, 'reach')
TODAY = dt.date.today()


def http(method, url, token=None, data=None, form=None, raw=False):
    headers = {}
    body = None
    if token:
        headers['Authorization'] = f'Bearer {token}'
    if form is not None:
        body = urllib.parse.urlencode(form).encode()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    elif data is not None:
        body = json.dumps(data).encode()
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            b = r.read()
            return b if raw else json.loads(b or b'{}')
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors='replace')[:600]
        raise RuntimeError(f'{method} {url.split("?")[0]} -> {e.code}: {msg}')


def get(url, token, **params):
    return http('GET', url + '?' + urllib.parse.urlencode(params), token)


def access_token():
    r = http('POST', 'https://oauth2.googleapis.com/token', form=dict(
        client_id=os.environ['YT_CLIENT_ID'], client_secret=os.environ['YT_CLIENT_SECRET'],
        refresh_token=os.environ['YT_REFRESH_TOKEN'], grant_type='refresh_token'))
    print('escopos do token:', r.get('scope'))
    return r['access_token']


DATA = 'https://www.googleapis.com/youtube/v3'
ANA = 'https://youtubeanalytics.googleapis.com/v2/reports'
REP = 'https://youtubereporting.googleapis.com/v1'


def rows(r):
    cols = [h['name'] for h in r.get('columnHeaders', [])]
    return [dict(zip(cols, x)) for x in r.get('rows', []) or []]


def canal_e_videos(tk):
    ch = get(f'{DATA}/channels', tk, part='id,snippet,statistics,contentDetails', mine='true')['items'][0]
    uploads = ch['contentDetails']['relatedPlaylists']['uploads']
    ids, page = [], None
    while True:
        p = dict(part='contentDetails', playlistId=uploads, maxResults=50)
        if page:
            p['pageToken'] = page
        r = get(f'{DATA}/playlistItems', tk, **p)
        ids += [i['contentDetails']['videoId'] for i in r.get('items', [])]
        page = r.get('nextPageToken')
        if not page:
            break
    vids = []
    for i in range(0, len(ids), 50):
        r = get(f'{DATA}/videos', tk, part='snippet,statistics,contentDetails,status', id=','.join(ids[i:i + 50]))
        for v in r.get('items', []):
            vids.append(dict(
                id=v['id'], titulo=v['snippet']['title'],
                publicado=v['snippet']['publishedAt'], status=v['status'].get('privacyStatus'),
                agendado=v['status'].get('publishAt'), duracao=v['contentDetails']['duration'],
                views=int(v['statistics'].get('viewCount', 0)), likes=int(v['statistics'].get('likeCount', 0)),
                comentarios=int(v['statistics'].get('commentCount', 0))))
    canal = dict(id=ch['id'], nome=ch['snippet']['title'],
                 inscritos=int(ch['statistics'].get('subscriberCount', 0)),
                 views=int(ch['statistics'].get('viewCount', 0)), videos=int(ch['statistics'].get('videoCount', 0)))
    return canal, vids


def analytics(tk, inicio):
    base = dict(ids='channel==MINE', startDate=inicio, endDate=TODAY.isoformat())
    porvideo = rows(get(ANA, tk, **base, dimensions='video', sort='-views', maxResults=200,
                        metrics='views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,'
                                'subscribersGained,subscribersLost,likes,comments,shares'))
    diario = rows(get(ANA, tk, **base, dimensions='day', sort='day',
                      metrics='views,estimatedMinutesWatched,averageViewDuration,subscribersGained'))
    trafego = rows(get(ANA, tk, **base, dimensions='insightTrafficSourceType', sort='-views',
                       metrics='views,estimatedMinutesWatched'))
    return porvideo, diario, trafego


def retencao(tk, vid, inicio):
    r = get(ANA, tk, ids='channel==MINE', startDate=inicio, endDate=TODAY.isoformat(),
            dimensions='elapsedVideoTimeRatio', filters=f'video=={vid}',
            metrics='audienceWatchRatio,relativeRetentionPerformance')
    return [[round(x['elapsedVideoTimeRatio'], 2), round(x['audienceWatchRatio'], 3),
             round(x['relativeRetentionPerformance'], 3)] for x in rows(r)]


def trafego_video(tk, vid, inicio):
    r = get(ANA, tk, ids='channel==MINE', startDate=inicio, endDate=TODAY.isoformat(),
            dimensions='insightTrafficSourceType', filters=f'video=={vid}', sort='-views', metrics='views')
    return {x['insightTrafficSourceType']: x['views'] for x in rows(r)}


def alcance(tk):
    """Impressões e CTR por vídeo (YouTube Reporting API, relatório channel_reach_basic_a1).
    Cria o job na primeira execução; os relatórios diários aparecem com ~1-2 dias de atraso."""
    os.makedirs(REACH, exist_ok=True)
    jobs = http('GET', f'{REP}/jobs', tk).get('jobs', [])
    job = next((j for j in jobs if j['reportTypeId'] == 'channel_reach_basic_a1'), None)
    if not job:
        job = http('POST', f'{REP}/jobs', tk, data=dict(reportTypeId='channel_reach_basic_a1', name='alcance'))
        print('job de alcance criado; impressões/CTR chegam nas próximas execuções')
    page = None
    while True:
        url = f'{REP}/jobs/{job["id"]}/reports' + (f'?pageToken={page}' if page else '')
        r = http('GET', url, tk)
        for rep in r.get('reports', []):
            dia = rep['startTime'][:10]
            fn = os.path.join(REACH, f'{dia}_{rep["id"]}.csv')
            if not os.path.exists(fn):
                open(fn, 'wb').write(http('GET', rep['downloadUrl'], tk, raw=True))
        page = r.get('nextPageToken')
        if not page:
            break
    # um relatório por dia; se houver reprocessamento, fica só o mais recente de cada dia
    pordia = {}
    for f in sorted(os.listdir(REACH)):
        pordia[f[:10]] = f
    tot = {}
    for f in pordia.values():
        for x in csv.DictReader(io.StringIO(open(os.path.join(REACH, f), encoding='utf-8').read())):
            imp = float(x.get('video_thumbnail_impressions') or 0)
            ctr = float(x.get('video_thumbnail_impressions_ctr') or 0)
            t = tot.setdefault(x['video_id'], [0.0, 0.0])
            t[0] += imp
            t[1] += imp * ctr
    return {v: dict(impressoes=int(i), ctr=round(100 * c / i, 2) if i else None) for v, (i, c) in tot.items()}


def mmss(s):
    s = int(round(float(s or 0)))
    return f'{s // 60}:{s % 60:02d}'


def resumo(snap):
    c = snap['canal']
    L = [f'# {c["nome"]} — {snap["data"]}', '',
         f'Inscritos: {c["inscritos"]} · views totais: {c["views"]} · vídeos: {c["videos"]}', '',
         '| Vídeo | Publicado | Views | Impr. | CTR | Média | % visto | Inscr. | Retém 30s |',
         '|---|---|---|---|---|---|---|---|---|']
    for v in snap['videos']:
        a = v.get('analytics', {})
        al = v.get('alcance', {})
        ret = v.get('retencao') or []
        r30 = '—'
        if ret and v.get('segundos'):
            alvo = 30 / v['segundos']
            p = min(ret, key=lambda x: abs(x[0] - alvo))
            r30 = f'{round(100 * p[1])}%'
        ctr = f'{al["ctr"]}%' if al.get('ctr') is not None else '—'
        L.append(f'| {v["titulo"][:60]} | {v["publicado"][:10]} | {a.get("views", v["views"])} | '
                 f'{al.get("impressoes", "—")} | {ctr} | '
                 f'{mmss(a.get("averageViewDuration"))} | {round(a.get("averageViewPercentage", 0))}% | '
                 f'{a.get("subscribersGained", 0)} | {r30} |')
    L += ['', '## Fontes de tráfego (canal)', '']
    for t in snap['trafego']:
        L.append(f'- {t["insightTrafficSourceType"]}: {t["views"]} views')
    if snap.get('erros'):
        L += ['', '## Avisos', ''] + [f'- {e}' for e in snap['erros']]
    return '\n'.join(L) + '\n'


def segundos(iso):
    import re
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    return sum(int(x or 0) * k for x, k in zip(m.groups(), (3600, 60, 1))) if m else 0


def main():
    os.makedirs(OUT, exist_ok=True)
    tk = access_token()
    canal, vids = canal_e_videos(tk)
    publicados = [v for v in vids if v['status'] == 'public']
    inicio = min([v['publicado'][:10] for v in publicados] or [TODAY.isoformat()])
    erros = []
    porvideo, diario, trafego = analytics(tk, inicio)
    pv = {x['video']: x for x in porvideo}
    try:
        alc = alcance(tk)
    except Exception as e:
        alc = {}
        erros.append(f'impressões/CTR indisponíveis: {e}')
    for v in vids:
        v['segundos'] = segundos(v['duracao'])
        v['analytics'] = pv.get(v['id'], {})
        v['alcance'] = alc.get(v['id'], {})
        if v['status'] == 'public':
            try:
                v['retencao'] = retencao(tk, v['id'], v['publicado'][:10])
                v['trafego'] = trafego_video(tk, v['id'], v['publicado'][:10])
            except Exception as e:
                erros.append(f'{v["id"]}: {e}')
    vids.sort(key=lambda v: v['publicado'])
    snap = dict(data=TODAY.isoformat(), canal=canal, videos=vids, diario=diario, trafego=trafego, erros=erros,
                legenda=dict(retencao='[fração do vídeo, audienceWatchRatio, relativeRetentionPerformance]',
                             ctr='% de cliques nas impressões da thumbnail (Reporting API)'))
    json.dump(snap, open(os.path.join(OUT, f'{TODAY.isoformat()}.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(OUT, 'ultimo.md'), 'w').write(resumo(snap))
    print(resumo(snap))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('ERRO:', e, file=sys.stderr)
        sys.exit(1)
