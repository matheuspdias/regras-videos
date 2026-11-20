"""Thumbnail do ep01: 'só 3%..' — protagonista em choque, tia Marta com 3%, linha neon ligando os dois."""
import sys
import math
import cairo
from .chars import draw_char, Pose, TAU
from .scenes import bg_jantar, fg_jantar, text, W, H, vignette
from .render import neon_bar, heart


def neon_line(ctx, pts, glow=(1, 0.25, 0.7)):
    for lw, a in ((60, 0.06), (40, 0.1), (24, 0.18), (12, 0.6), (5, 1.0)):
        ctx.set_line_width(lw)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        if lw == 5:
            ctx.set_source_rgba(1, 0.92, 0.98, 1)
        else:
            ctx.set_source_rgba(glow[0], glow[1], glow[2], a)
        ctx.move_to(*pts[0])
        ctx.curve_to(*pts[1], *pts[2], *pts[3])
        ctx.stroke()


def main(out):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    ctx.save()
    # fundo: casa da vó, mais escuro e quente
    ctx.translate(W / 2, H / 2)
    ctx.scale(1.35, 1.35)
    ctx.translate(-W / 2, -H / 2 - 40)
    bg_jantar(ctx, 0)
    ctx.restore()
    ctx.rectangle(0, 0, W, H)
    ctx.set_source_rgba(0.1, 0.0, 0.15, 0.6)
    ctx.fill()
    # tia (direita), sorrindo
    tia = draw_char(ctx, 'tia', 1420, 1330, 1.55, Pose(mouth='grin', eyes='happy', arms='wave', facing=-1))
    # protagonista (esquerda), em choque
    voce = draw_char(ctx, 'voce', 520, 1370, 1.75, Pose(eyes='wide', mouth='o', arms='face', sweat=True, facing=1))
    # linha neon do protagonista até a tia
    hx, hy = voce['head']
    tx, ty = tia['head']
    neon_line(ctx, [(hx + 120, hy - 10), (hx + 400, hy - 260), (tx - 420, ty - 300), (tx - 150, ty - 120)])
    # barra 3%
    neon_bar(ctx, tx, tia['top'][1] - 70, 2.0, 3)
    # texto
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(190)
    w1 = ctx.text_extents('só ').x_advance
    w2 = ctx.text_extents('3%..').x_advance
    x0 = W / 2 - (w1 + w2) / 2
    text(ctx, 'só ', x0, 230, 190, '#FFFFFF', align='left', outline='#120018', lw=24)
    text(ctx, '3%..', x0 + w1, 230, 190, '#FFD23F', align='left', outline='#120018', lw=24)
    vignette(ctx, 0.45)
    surf.write_to_png(out)


def ep02(out):
    from .scenes import bg_classe
    from .render import rings, thought_bubble
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    ctx.save()
    ctx.translate(W / 2, H / 2); ctx.scale(1.3, 1.3); ctx.translate(-W / 2, -H / 2 - 30)
    bg_classe(ctx, 0)
    ctx.restore()
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.1, 0.0, 0.15, 0.55); ctx.fill()
    voce = draw_char(ctx, 'voce', 560, 1380, 1.7, Pose(eyes='wide', mouth='wavy', arms='face', sweat=True, blush=True, facing=1))
    hx, hy = voce['head']
    rings(ctx, hx, hy, voce['head_r'], 0.15)
    rings(ctx, hx, hy, voce['head_r'], 0.5)
    bia = draw_char(ctx, 'bia', 1450, 1380, 1.6, Pose(eyes='wide', mouth='o', blush=True, arms='face', facing=-1))
    # balão de pensamento com coração
    bx, by = 1000, 380
    for k, (fx_, r) in enumerate(((0.3, 16), (0.55, 26))):
        ctx.arc(hx + (bx - hx) * fx_, hy - 150 + (by - hy + 150) * fx_, r, 0, TAU); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
    ctx.save(); ctx.translate(bx, by); ctx.scale(1.4, 1.0); ctx.arc(0, 0, 110, 0, TAU); ctx.restore()
    ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
    heart(ctx, bx, by + 20, 80, (1, 0.25, 0.6, 1))
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(180)
    w1 = ctx.text_extents('ela ').x_advance
    w2 = ctx.text_extents('ouviu..').x_advance
    x0 = W / 2 - (w1 + w2) / 2
    text(ctx, 'ela ', x0, 200, 180, '#FFFFFF', align='left', outline='#120018', lw=24)
    text(ctx, 'ouviu..', x0 + w1, 200, 180, '#FFD23F', align='left', outline='#120018', lw=24)
    vignette(ctx, 0.45)
    surf.write_to_png(out)




# ---------------------------------------------------------------- thumbnail genérica (usada pela automação)
def generic(spec, out):
    """spec (THUMB no arquivo do episódio):
    bg: chave de engine.scenes.BG
    text: (parte_branca, parte_amarela)   ex.: ('só', '3%..')
    left: (cid, dict_pose)   protagonista em reação, normalmente 'voce'
    right: (cid, dict_pose) ou None
    link: 'bar' | 'neon' | 'thought' | 'rings' | None
    bar: valor da barra neon sobre o personagem da direita (se link='bar')
    """
    from .scenes import BG
    from .render import rings
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    bgf, fgf = BG[spec['bg']]
    ctx.save()
    ctx.translate(W / 2, H / 2); ctx.scale(1.3, 1.3); ctx.translate(-W / 2, -H / 2 - 30)
    bgf(ctx, 0)
    ctx.restore()
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.1, 0.0, 0.15, 0.55); ctx.fill()
    lid, lpose = spec['left']
    lp = dict(lpose); lp.setdefault('facing', 1)
    L = draw_char(ctx, lid, 560, 1380, 1.7, Pose(**lp))
    R = None
    if spec.get('right'):
        rid, rpose = spec['right']
        rp = dict(rpose); rp.setdefault('facing', -1)
        R = draw_char(ctx, rid, 1450, 1380, 1.6, Pose(**rp))
    hx, hy = L['head']
    link = spec.get('link')
    if link in ('rings', 'thought'):
        rings(ctx, hx, hy, L['head_r'], 0.15)
        rings(ctx, hx, hy, L['head_r'], 0.5)
    if link == 'thought':
        bx, by = 1000, 380
        for fx_, r in ((0.3, 16), (0.55, 26)):
            ctx.arc(hx + (bx - hx) * fx_, hy - 150 + (by - hy + 150) * fx_, r, 0, TAU); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
        ctx.save(); ctx.translate(bx, by); ctx.scale(1.4, 1.0); ctx.arc(0, 0, 110, 0, TAU); ctx.restore()
        ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
        heart(ctx, bx, by + 20, 80, (1, 0.25, 0.6, 1))
    if link in ('neon', 'bar') and R:
        tx, ty = R['head']
        neon_line(ctx, [(hx + 120, hy - 10), (hx + 400, hy - 260), (tx - 420, ty - 300), (tx - 150, ty - 120)])
    if link == 'bar' and R:
        neon_bar(ctx, R['head'][0], R['top'][1] - 70, 2.0, spec.get('bar', 50))
    a, b = spec['text']
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    size = 180
    while True:
        ctx.set_font_size(size)
        w1 = ctx.text_extents(a + ' ').x_advance if a else 0
        w2 = ctx.text_extents(b).x_advance
        if w1 + w2 < W - 160 or size < 90:
            break
        size -= 10
    x0 = W / 2 - (w1 + w2) / 2
    if a:
        text(ctx, a + ' ', x0, 200, size, '#FFFFFF', align='left', outline='#120018', lw=24)
    text(ctx, b, x0 + w1, 200, size, '#FFD23F', align='left', outline='#120018', lw=24)
    vignette(ctx, 0.45)
    surf.write_to_png(out)


# ---------------------------------------------------------------- Manual da Madrugada
def mm(spec, out):
    """spec (THUMB do episódio):
    ordem: 'NÃO **RESPONDA**'   (palavra entre ** fica vermelha)
    esquerda: (cid, pose) protagonista com medo
    criatura_porta: True -> criatura espiando de uma porta à direita
    balao: texto do balão vermelho saindo da porta (opcional)
    """
    from .render import rich_text
    from .scenes import lr
    from .chars import rrect
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.03, 0.03, 0.035, 1); ctx.fill()
    # chão
    ctx.set_source_rgba(0.75, 0.75, 0.78, 1); ctx.set_line_width(8)
    ctx.move_to(0, 1010); ctx.line_to(W, 1010); ctx.stroke()
    if spec.get('criatura_porta'):
        # porta entreaberta com a criatura espiando
        dx, dy, dw, dh = 1260, 330, 420, 690
        ctx.rectangle(dx, dy, dw, dh); ctx.set_source_rgba(0.01, 0.01, 0.012, 1); ctx.fill()
        ctx.save()
        ctx.rectangle(dx, dy, dw, dh); ctx.clip()
        draw_char(ctx, spec.get('criatura', 'coisa'), dx + 105, dy + dh + 10, 0.95, Pose(mouth='grin', facing=-1, arms='down'))
        ctx.restore()
        ctx.rectangle(dx + 170, dy, dw - 170, dh); ctx.set_source_rgba(0.14, 0.14, 0.16, 1); ctx.fill()
        ctx.set_source_rgba(0.85, 0.85, 0.88, 1); ctx.set_line_width(9)
        ctx.rectangle(dx, dy, dw, dh); ctx.stroke()
        ctx.move_to(dx + 170, dy); ctx.line_to(dx + 170, dy + dh); ctx.stroke()
        if spec.get('balao'):
            msg = spec['balao']
            ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(54)
            w_ = ctx.text_extents(msg).width + 70
            bx, by = dx + 40, dy - 30
            rrect(ctx, bx - w_ / 2, by - 60, w_, 92, 34)
            ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
            ctx.move_to(bx + 10, by + 30); ctx.line_to(bx + 40, by + 70); ctx.line_to(bx + 50, by + 30); ctx.fill()
            ctx.move_to(bx - w_ / 2 + 35, by + 5); ctx.set_source_rgba(1, 1, 1, 1); ctx.show_text(msg)
    lid, lp = spec['esquerda']
    lp = dict(lp); lp.setdefault('facing', 1)
    draw_char(ctx, lid, 520, 1120, 1.55, Pose(**lp))
    # linhas de susto
    ctx.set_source_rgba(0.9, 0.9, 0.92, 1); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (-0.9, -0.5, -0.1):
        ctx.move_to(520 + math.cos(a - 1.2) * 250, 520 + math.sin(a - 1.2) * 250)
        ctx.line_to(520 + math.cos(a - 1.2) * 300, 520 + math.sin(a - 1.2) * 300)
        ctx.stroke()
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    fs = 170
    while fs > 90:
        ctx.set_font_size(fs)
        if ctx.text_extents(spec['ordem'].replace('*', '')).x_advance < W - 160:
            break
        fs -= 8
    if not spec.get('sem_ordem'):
        rich_text(ctx, spec['ordem'], 960, 190, fs)
    surf.write_to_png(out)


def _cli():
    out = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if arg == 'ep02':
        ep02(out)
    elif arg and arg.startswith('episodes.'):
        import importlib
        spec = importlib.import_module(arg).THUMB
        fn = globals().get(f"mm_{spec.get('cena')}") if spec.get('cena') else None   # capa própria: def mm_<cena>(spec, out)
        (fn or (mm if 'ordem' in spec else generic))(spec, out)
    else:
        main(out)



def mm_cama(spec, out):
    """Capa 'na cama': protagonista fingindo que dorme e a criatura ao lado da cama, com balão vermelho.
    spec: ordem, criatura, balao, cena='cama', zoom (opcional)"""
    from .render import rich_text
    from .scenes import BG
    from .chars import rrect
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    bg, fg = BG['cama']
    z = spec.get('zoom', 1.22)
    cx, cy = spec.get('foco', (1080, 640))
    ctx.save()
    ctx.translate(W / 2, H / 2 + 200); ctx.scale(z, z); ctx.translate(-cx, -cy)
    bg(ctx, 0.0)
    q = spec.get('criatura', 'coisa')
    # a criatura atrás da cama, debruçada sobre o travesseiro (pés escondidos pela colcha)
    fx_, fy_ = spec.get('pos', (1180, 880))
    ctx.save(); ctx.rectangle(-500, -500, 4000, 500 + 740); ctx.clip()   # pernas somem atrás da cama
    ctx.translate(fx_, fy_); ctx.rotate(spec.get('incl', -0.16))
    info = draw_char(ctx, q, 0, 0, spec.get('cs', 1.0), Pose(mouth='grin', facing=-1, arms='point'))
    hl = ctx.user_to_device(*info['head']); tl = ctx.user_to_device(info['head'][0], info['top'][1])
    ctx.restore()
    from .scenes import big_bed
    big_bed(ctx)                                   # a cama na frente: a criatura fica atrás dela
    draw_char(ctx, 'voce', 1250, 625, 0.85, Pose(lie=True, eyes='closed', mouth='flat', sweat=True))
    if fg:
        fg(ctx, 0.0)
    ctx.restore()
    hx, top = hl[0], tl[1]
    # escurece as bordas e deixa a cena mais sinistra
    g = cairo.RadialGradient(W / 2, H / 2 + 120, 320, W / 2, H / 2 + 120, 1150)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.75)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    g2 = cairo.LinearGradient(0, 0, 0, 330)
    g2.add_color_stop_rgba(0, 0.02, 0.02, 0.025, 0.95); g2.add_color_stop_rgba(1, 0.02, 0.02, 0.025, 0)
    ctx.rectangle(0, 0, W, 330); ctx.set_source(g2); ctx.fill()
    # posição da cabeça da criatura no quadro final
    sx, sy = hx, top
    if spec.get('balao'):
        msg = spec['balao']
        ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(66)
        w_ = ctx.text_extents(msg).width + 80
        bx, by = sx + 400, sy + 250
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(bx - w_ / 2 + 40, by + 20); ctx.line_to(sx + 70, sy + 60); ctx.line_to(bx - w_ / 2 + 110, by + 30); ctx.fill()
        ctx.move_to(bx - w_ / 2 + 40, by + 8); ctx.set_source_rgba(1, 1, 1, 1); ctx.show_text(msg)
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    fs = 170
    while fs > 90:
        ctx.set_font_size(fs)
        if ctx.text_extents(spec['ordem'].replace('*', '')).x_advance < W - 160:
            break
        fs -= 8
    rich_text(ctx, spec['ordem'], 960, 170, fs)
    surf.write_to_png(out)


def mm_portao(spec, out):
    """Capa 'no portão' (noite 03): visto de dentro, protagonista espiando pela cortina em primeiro plano;
    lá fora, a criatura alta atrás da grade, pescoço por cima do muro, batendo palma; balão vermelho.
    spec: ordem, criatura, balao, cena='portao'"""
    from .render import rich_text
    from .scenes import muro_portao, grade_portao, fg_mm_cortina, DARK, DARK3, lr
    from .chars import rrect, setc
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    q = spec.get('criatura', 'coisa')
    # quintal ao fundo, com o portão à direita
    ctx.save()
    z = spec.get('zoom', 1.05)
    ctx.translate(1150, 745); ctx.scale(z, z); ctx.translate(-1000, -560)
    muro_portao(ctx, 0.0)
    ctx.save(); ctx.translate(960, 830)
    info = draw_char(ctx, q, 0, 0, spec.get('cs', 0.86), Pose(mouth='grin', facing=-1, arms='up'))
    hl = ctx.user_to_device(*info['head']); tl = ctx.user_to_device(info['head'][0], info['top'][1])
    ctx.restore()
    grade_portao(ctx, 0.0)
    ctx.restore()
    hx, top = hl[0], tl[1]
    # escurece bordas
    g = cairo.RadialGradient(1150, H / 2 + 60, 280, 1150, H / 2 + 60, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.8)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    g2 = cairo.LinearGradient(0, 0, 0, 300)
    g2.add_color_stop_rgba(0, 0.02, 0.02, 0.025, 0.95); g2.add_color_stop_rgba(1, 0.02, 0.02, 0.025, 0)
    ctx.rectangle(0, 0, W, 300); ctx.set_source(g2); ctx.fill()
    # cortina (de dentro de casa) e o protagonista na frente dela, espiando
    ctx.move_to(-20, 0); ctx.line_to(330, 0)
    ctx.curve_to(290, 400, 360, 760, 300, H); ctx.line_to(-20, H); ctx.close_path()
    setc(ctx, '#1F1D22'); ctx.fill_preserve(); ctx.set_source_rgba(0.6, 0.6, 0.64, 1); ctx.set_line_width(5); ctx.stroke()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.35); ctx.set_line_width(3)
    for k in (90, 200):
        ctx.move_to(k, 0); ctx.curve_to(k - 20, 400, k + 40, 760, k, H); ctx.stroke()
    draw_char(ctx, 'voce', 400, 1230, 1.45, Pose(eyes='wide', mouth='o', arms='face', sweat=True, facing=1))
    # linhas de susto
    ctx.set_source_rgba(0.9, 0.9, 0.92, 1); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (-0.9, -0.5, -0.1):
        ctx.move_to(400 + math.cos(a - 1.2) * 270, 640 + math.sin(a - 1.2) * 270)
        ctx.line_to(400 + math.cos(a - 1.2) * 320, 640 + math.sin(a - 1.2) * 320)
        ctx.stroke()
    if spec.get('balao'):
        msg = spec['balao']
        ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(66)
        w_ = ctx.text_extents(msg).width + 80
        bx, by = min(hx + 420, W - w_ / 2 - 40), top + 170
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(bx - w_ / 2 + 40, by + 20); ctx.line_to(hx + 110, top + 110); ctx.line_to(bx - w_ / 2 + 110, by + 30); ctx.fill()
        ctx.move_to(bx - w_ / 2 + 40, by + 8); ctx.set_source_rgba(1, 1, 1, 1); ctx.show_text(msg)
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    fs = 170
    while fs > 90:
        ctx.set_font_size(fs)
        if ctx.text_extents(spec['ordem'].replace('*', '')).x_advance < W - 160:
            break
        fs -= 8
    rich_text(ctx, spec['ordem'], 960, 170, fs)
    surf.write_to_png(out)


if __name__ == '__main__':
    _cli()
