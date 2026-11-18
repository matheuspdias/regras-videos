"""Corta um episódio em partes verticais (1080x1920) para o TikTok.

Uso:  MM_VERT=1 python3 -m engine.render episodes.epNN_slug epNN     # render sem legenda/HUD -> build/epNN_v/epNN.mp4
      python3 tools/vertical.py episodes.epNN_slug epNN [corte1,corte2,...]

Os cortes (segundos) entram ANTES de um cartão de regra ou logo depois de um susto; sem cortes, usa CORTES_TIKTOK do
episódio ou corta em cartões de regra a cada ~2 min. Cada parte tem de 1 a 3,5 min (o TikTok só paga acima de 1 min).
Saída: build/epNN_v/tiktok/ (parteN.mp4, parteN_capa.jpg, legendas.md)
"""
import importlib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cairo  # noqa: E402
from engine.render import build, caption_chunks, rich_text  # noqa: E402
from engine.scenes import text  # noqa: E402
from engine.chars import rrect  # noqa: E402

VW, VH = 1080, 1920
CROP_X, CROP_W = 240, 1440          # pedaço do quadro 16:9 que entra no vertical
SCENE_Y, SCENE_H = 430, 810         # onde a cena fica no vertical
RED = '&H2B26E5&'                   # #E5262B em BGR do ASS
CAPRED = '&H4B4BFF&'


def ts(t):
    t = max(t, 0)
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'


def ass_rich(s_):
    """**palavra** -> vermelho"""
    return re.sub(r'\*\*([^*]+)\*\*', lambda m: '{\\c' + RED + '}' + m.group(1) + '{\\c&HF2F2F2&}', s_)


def card_shot(shots, t):
    for s in shots:
        if s['t0'] <= t < s['t1']:
            return any(isinstance(i, dict) and ('regra' in i or 'cta_mm' in i) for i in s['scene'].get('fx', []))
    return False


def make_ass(path, ep, clips, shots, a, b, n, N):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {VW}
PlayResY: {VH}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,88,&H00F2F2F2,&H00F2F2F2,&H00050505,&H00000000,1,0,0,0,100,100,0,0,1,6,0,8,50,50,1330,1
Style: Ordem,Poppins,112,&H00F2F2F2,&H00F2F2F2,&H00050505,&H00000000,1,0,0,0,100,100,0,0,1,7,0,8,40,40,215,1
Style: Parte,Poppins,46,&H008E8E93,&H008E8E93,&H00050505,&H00000000,1,0,0,0,100,100,6,0,1,3,0,8,40,40,150,1
Style: Fim,Poppins,70,&H00FFFFFF,&H00FFFFFF,&H002B26E5,&H002B26E5,1,0,0,0,100,100,0,0,3,18,0,8,60,60,1640,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    dur = b - a
    ordem = ep.THUMB['ordem']
    ev.append(f'Dialogue: 0,{ts(0)},{ts(dur)},Parte,,0,0,0,,P A R T E   {n} / {N}')
    ev.append(f'Dialogue: 0,{ts(0)},{ts(dur)},Ordem,,0,0,0,,{ass_rich(ordem)}')
    for c in clips:
        if c['t1'] <= a or c['t0'] >= b or card_shot(shots, c['t0'] + 0.05):
            continue
        ch = caption_chunks(c['text'], maxw=4)
        lens = [len(x) + 3 for x in ch]
        tot = sum(lens); acc = 0
        cd = c['t1'] - c['t0']
        for x, ln in zip(ch, lens):
            s0 = c['t0'] + acc / tot * cd
            acc += ln
            s1 = c['t0'] + acc / tot * cd
            if s1 <= a or s0 >= b:
                continue
            col = '{\\c' + CAPRED + '}' if c['sp'] == 'coisa' else ''
            ev.append(f'Dialogue: 1,{ts(s0 - a)},{ts(min(s1, b) - a)},Cap,,0,0,0,,{col}{x.upper()}')
    if n < N:
        ev.append(f'Dialogue: 2,{ts(dur - 3.2)},{ts(dur)},Fim,,0,0,0,,{{\\fad(250,0)}}PARTE {n + 1} NO PERFIL')
    with open(path, 'w') as fh:
        fh.write(head + '\n'.join(ev) + '\n')


def make_cover(path, ep, bdir_h, n, N):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, VW, VH)
    ctx = cairo.Context(surf)
    ctx.rectangle(0, 0, VW, VH); ctx.set_source_rgba(0.03, 0.03, 0.035, 1); ctx.fill()
    from engine.thumb import mm
    tmp = path + '.base.png'
    mm(dict(ep.THUMB, sem_ordem=True), tmp)
    th = cairo.ImageSurface.create_from_png(tmp)
    os.remove(tmp)
    sc = VW * 1.25 / th.get_width()
    ctx.save(); ctx.rectangle(0, 560, VW, VH - 560); ctx.clip()
    ctx.translate((VW - th.get_width() * sc) / 2, 560 - 200 * sc); ctx.scale(sc, sc)
    ctx.set_source_surface(th, 0, 0); ctx.paint(); ctx.restore()
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    fs = 120
    while fs > 70:
        ctx.set_font_size(fs)
        if ctx.text_extents(ep.THUMB['ordem'].replace('*', '')).x_advance < VW - 80:
            break
        fs -= 6
    rich_text(ctx, ep.THUMB['ordem'], VW / 2, 420, fs)
    tag = f'PARTE {n}'
    ctx.set_font_size(78); e = ctx.text_extents(tag)
    rrect(ctx, VW / 2 - e.x_advance / 2 - 46, 1430, e.x_advance + 92, 130, 30)
    ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
    text(ctx, tag, VW / 2, 1520, 78, '#FFFFFF')
    surf.write_to_png(path + '.png')
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', path + '.png', '-q:v', '2', path])
    os.remove(path + '.png')


def auto_cuts(shots, end):
    cards = [s['t0'] for s in shots if any(isinstance(i, dict) and 'regra' in i for i in s['scene'].get('fx', []))]
    cuts, last = [], 0.0
    for c in cards:
        if c - last >= 95 and end - c >= 70:
            cuts.append(c); last = c
    return cuts


def main():
    mod, eid = sys.argv[1], sys.argv[2]
    ep, clips, shots, total = build(mod, eid)
    importlib.import_module(mod)
    end = total - ep.TAIL + 1.0
    if len(sys.argv) > 3:
        cuts = [float(x) for x in sys.argv[3].split(',')]
    else:
        cuts = list(getattr(ep, 'CORTES_TIKTOK', None) or auto_cuts(shots, end))
    t0s = [s_['t0'] for s_ in shots]
    cuts = [min(t0s, key=lambda x: abs(x - c)) for c in cuts]      # corta sempre no início de um plano
    bounds = [0.0] + cuts + [end]
    N = len(bounds) - 1
    bdir = f'build/{eid}_v'
    src = f'{bdir}/{eid}.mp4'
    out = f'{bdir}/tiktok'
    os.makedirs(out, exist_ok=True)
    md = [f'# {ep.TITLE} — TikTok ({N} partes)\n']
    for k in range(N):
        a, b = bounds[k], bounds[k + 1]
        n = k + 1
        so = os.environ.get('SO_PARTES')            # ex.: SO_PARTES=4 refaz só a parte 4
        if not so or str(n) in so.split(','):
            ass = f'{out}/parte{n}.ass'
            make_ass(ass, ep, clips, shots, a, b, n, N)
            vf = (f'crop={CROP_W}:1080:{CROP_X}:0,scale={VW}:{SCENE_H},pad={VW}:{VH}:0:{SCENE_Y}:color=0x080809,'
                  f'ass={ass}')
            subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', src,
                                   '-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p',
                                   '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', f'{out}/parte{n}.mp4'])
            make_cover(f'{out}/parte{n}_capa.jpg', ep, f'build/{eid}', n, N)
        titulo = ep.TITLE
        md.append(f'## Parte {n}/{N} — {b - a:.0f} s\n')
        md.append(f'{titulo} (parte {n}/{N}) 🌙\n')
        if n < N:
            md.append(f'A parte {n + 1} já tá no perfil. Qual regra você quebraria primeiro?\n')
        else:
            md.append('Fim da noite. Qual regra você quebraria primeiro?\n')
        md.append('Todas as histórias deste perfil são ficção.\n')
        md.append('#terror #historiasdeterror #creepypasta #regrasdeterror #manualdamadrugada\n')
        print(f'parte {n}/{N}: {a:.1f}-{b:.1f} ({b - a:.0f} s)')
    with open(f'{out}/legendas.md', 'w') as fh:
        fh.write('\n'.join(md))
    print('ok', out)


if __name__ == '__main__':
    main()
