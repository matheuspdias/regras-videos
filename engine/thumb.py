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


def mm_banheiro(spec, out):
    """Capa 'no banheiro' (noite 04): o box de vidro embaçado à direita, com a criatura de pé lá dentro, as mãos
    espalmadas no vidro e o rosto aparecendo numa faixa que ela limpou no vapor; protagonista apavorado à esquerda;
    balão vermelho. spec: ordem, criatura, balao, cena='banheiro'"""
    from .render import rich_text
    from .scenes import bg_mm_banheiro, vapor
    from .chars import rrect, setc
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    q = spec.get('criatura', 'coisa')
    z = spec.get('zoom', 1.3)
    ctx.save()
    ctx.translate(1230, 660); ctx.scale(z, z); ctx.translate(-1430, -560)
    bg_mm_banheiro(ctx, 0.0)
    ctx.save(); ctx.translate(1430, 862)
    info = draw_char(ctx, q, 0, 0, spec.get('cs', 0.84), Pose(mouth='grin', facing=-1, arms='down'))
    hx_, hy_ = info['head']; hr = info['head_r']
    ctx.restore()
    hx_, hy_ = hx_ + 1430, hy_ + 862
    # vidro embaçado com uma faixa limpa na altura do rosto
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    ctx.rectangle(1080, 210, 720, 640)
    ctx.save(); ctx.translate(hx_, hy_ + hr * 0.15); ctx.rotate(-0.12); ctx.scale(1.0, 0.62)
    ctx.arc(0, 0, hr * 1.35, 0, TAU); ctx.restore()
    ctx.set_source_rgba(0.72, 0.75, 0.8, 0.3); ctx.fill()
    ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    vapor(ctx, 1090, 760, 700, 0.0, a=0.18, n=7)
    # marcas de mão no vidro
    for mx, my, a in ((hx_ - hr * 2.3, hy_ + hr * 0.9, -0.3), (hx_ + hr * 2.1, hy_ - hr * 0.1, 0.25)):
        ctx.save(); ctx.translate(mx, my); ctx.rotate(a)
        ctx.set_source_rgba(0.08, 0.08, 0.1, 0.4)
        ctx.save(); ctx.scale(1, 1.15); ctx.arc(0, 0, hr * 0.42, 0, TAU); ctx.restore(); ctx.fill()
        for k in range(5):
            ang = -2.4 + k * 0.42
            ctx.save(); ctx.translate(math.cos(ang) * hr * 0.6, math.sin(ang) * hr * 0.7); ctx.rotate(ang + math.pi / 2)
            ctx.scale(0.35, 1); ctx.arc(0, 0, hr * 0.32, 0, TAU); ctx.restore(); ctx.fill()
        ctx.restore()
    ctx.set_source_rgba(0.9, 0.92, 0.96, 0.4); ctx.set_line_width(3)
    for k, x in enumerate((1130, 1250, 1540, 1700)):
        ctx.move_to(x, 300 + k * 60); ctx.line_to(x + 4, 470 + k * 60); ctx.stroke()
    ctx.set_source_rgba(0.78, 0.78, 0.82, 1); ctx.set_line_width(7)
    ctx.rectangle(1070, 200, 740, 660); ctx.stroke()
    top_dev = ctx.user_to_device(hx_, hy_ - hr)
    head_dev = ctx.user_to_device(hx_, hy_)
    ctx.restore()
    # escurece bordas
    g = cairo.RadialGradient(1230, H / 2 + 60, 280, 1230, H / 2 + 60, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.8)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    g2 = cairo.LinearGradient(0, 0, 0, 300)
    g2.add_color_stop_rgba(0, 0.02, 0.02, 0.025, 0.95); g2.add_color_stop_rgba(1, 0.02, 0.02, 0.025, 0)
    ctx.rectangle(0, 0, W, 300); ctx.set_source(g2); ctx.fill()
    # protagonista em primeiro plano, à esquerda
    draw_char(ctx, 'voce', 380, 1250, 1.45, Pose(eyes='wide', mouth='flat', arms='point', sweat=True, facing=1, look=1))
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
        hx, top = head_dev
        bx, by = max(w_ / 2 + 40, min(hx - 560, W - w_ / 2 - 40)), top_dev[1] + 40
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(bx + w_ / 2 - 110, by + 30); ctx.line_to(hx - 170, top_dev[1] + 130); ctx.line_to(bx + w_ / 2 - 40, by + 20); ctx.fill()
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


def mm_atras(spec, out):
    """Capa 'atrás de você' (noite 05): no corredor, o protagonista em primeiro plano, de frente pra câmera,
    paralisado; a criatura enorme logo atrás dele, debruçada por cima do ombro, cabeça torta, sorrindo de olhos
    fechados, a mão comprida quase no ombro; o guarda-roupa da vó ao fundo; balão vermelho.
    spec: ordem, criatura, balao, cena='atras'"""
    from .render import rich_text
    from .scenes import bg_mm_corredor_vo
    from .chars import rrect
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    q = spec.get('criatura', 'coisa')
    z = spec.get('zoom', 1.25)
    ctx.save()
    ctx.translate(W / 2, H / 2 + 80); ctx.scale(z, z); ctx.translate(-1150, -560)
    bg_mm_corredor_vo(ctx, 0.0)
    ctx.restore()
    # escurece tudo e as bordas
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, 0.35); ctx.fill()
    g = cairo.RadialGradient(1000, H / 2 + 80, 300, 1000, H / 2 + 80, 1200)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.8)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    # a criatura atrás, debruçada por cima do ombro direito do protagonista
    ctx.save(); ctx.translate(spec.get('cx', 1230), 1560); ctx.rotate(spec.get('incl', -0.28))
    info = draw_char(ctx, q, 0, 0, spec.get('cs', 1.7), Pose(mouth='grin', facing=-1, arms='point'))
    hd = ctx.user_to_device(*info['head']); tp = ctx.user_to_device(info['head'][0], info['top'][1])
    ctx.restore()
    # luz fria vinda de baixo no rosto do protagonista
    g3 = cairo.RadialGradient(700, 700, 50, 700, 700, 520)
    g3.add_color_stop_rgba(0, 0.6, 0.65, 0.8, 0.10); g3.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g3); ctx.fill()
    draw_char(ctx, 'voce', 600, 1330, 1.5, Pose(eyes='wide', mouth='flat', arms='down', sweat=True, facing=1))
    # linhas de susto
    ctx.set_source_rgba(0.9, 0.9, 0.92, 1); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (-0.9, -0.5, -0.1):
        ctx.move_to(470 + math.cos(a - 1.9) * 260, 620 + math.sin(a - 1.9) * 260)
        ctx.line_to(470 + math.cos(a - 1.9) * 310, 620 + math.sin(a - 1.9) * 310)
        ctx.stroke()
    g2 = cairo.LinearGradient(0, 0, 0, 300)
    g2.add_color_stop_rgba(0, 0.02, 0.02, 0.025, 0.95); g2.add_color_stop_rgba(1, 0.02, 0.02, 0.025, 0)
    ctx.rectangle(0, 0, W, 300); ctx.set_source(g2); ctx.fill()
    if spec.get('balao'):
        msg = spec['balao']
        ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(66)
        w_ = ctx.text_extents(msg).width + 80
        hx, top = tp
        bx, by = min(hx + 470, W - w_ / 2 - 40), max(top + 60, 380)
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(bx - w_ / 2 + 40, by + 20); ctx.line_to(hx + 150, top + 140); ctx.line_to(bx - w_ / 2 + 110, by + 30); ctx.fill()
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


def mm_olho(spec, out):
    """Capa 'olho mágico' (noite 06): de dentro de casa, no escuro, a lente redonda e enorme do olho mágico à direita
    com a criatura curvada colada nela lá fora (capacete vermelho, quatro olhos); à esquerda o protagonista encostado
    na porta, apavorado, e o cachorro em primeiro plano rosnando pra porta; balão vermelho.
    spec: ordem, criatura, balao, cena='olho'"""
    from .render import rich_text, draw_monstro, dog
    from .chars import rrect, setc
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    q = spec.get('criatura', 'coisa')
    R = spec.get('r', 400)
    c0 = spec.get('centro', (1360, 650))
    top = draw_monstro(ctx, {'monstro': 'olho', 'quem': q, 'perto': spec.get('perto', 0.95), 'incl': spec.get('incl', -0.28),
                             'centro': c0, 'r': R, 'escuro': spec.get('escuro', 0.18)}, 0.0, 1.0, 0.0)
    # madeira da porta em volta da lente (de dentro, quase preta) e o batente à esquerda
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.35); ctx.set_line_width(5)
    ctx.rectangle(760, 120, 1200, 1100); ctx.stroke()
    ctx.move_to(760, 120); ctx.line_to(760, H); ctx.stroke()
    # protagonista encostado na porta, à esquerda
    draw_char(ctx, 'voce', 350, 1260, 1.5, Pose(eyes='wide', mouth='o', arms='face', sweat=True, facing=1))
    ctx.set_source_rgba(0.9, 0.9, 0.92, 1); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (-0.9, -0.5, -0.1):
        ctx.move_to(360 + math.cos(a - 1.2) * 270, 600 + math.sin(a - 1.2) * 270)
        ctx.line_to(360 + math.cos(a - 1.2) * 320, 600 + math.sin(a - 1.2) * 320)
        ctx.stroke()
    # cachorro rosnando em primeiro plano
    dog(ctx, spec.get('cao_x', 640), 1095, 'rosna', 0.3)
    g2 = cairo.LinearGradient(0, 0, 0, 300)
    g2.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.9); g2.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0)
    ctx.rectangle(0, 0, W, 300); ctx.set_source(g2); ctx.fill()
    if spec.get('balao'):
        msg = spec['balao']
        ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(66)
        w_ = ctx.text_extents(msg).width + 80
        bx, by = c0[0] - R * 0.95, c0[1] - R * 0.82
        bx = min(max(bx, w_ / 2 + 40), W - w_ / 2 - 40)
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(bx + w_ / 2 - 150, by + 30); ctx.line_to(c0[0] - R * 0.35, c0[1] - R * 0.35); ctx.line_to(bx + w_ / 2 - 60, by + 30); ctx.fill()
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


def mm_vassoura(spec, out):
    """Capa 'vassoura' (noite 07): no quartinho da casa da vó, o protagonista encolhido em cima da cama de ferro,
    abraçando os joelhos, com o chinelo no chão; a criatura enorme e curvada à direita, varrendo debaixo da cama com a
    vassoura de palha, boca costurada de vermelho e olhos vazios; balão vermelho.
    spec: ordem, criatura, balao, cena='vassoura'"""
    from .render import rich_text
    from .scenes import mm_room, cama_ferro, chinelo, wood_window, amber
    from .chars import rrect
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    q = spec.get('criatura', 'coisa')
    mm_room(ctx, wall_c='#151413', fy=860)
    wood_window(ctx, 1000, 330, 240, 220)
    amber(ctx, 1120, 440, 420, 0.10)
    ctx.save(); ctx.translate(-60, 60); ctx.scale(1.25, 1.25)
    cama_ferro(ctx, 60, 690, 700)
    ctx.restore()
    chinelo(ctx, 1030, 990, 1.1)
    # a criatura curvada à direita, varrendo pra baixo da cama
    ctx.save(); ctx.translate(spec.get('cx', 1440), 1020); ctx.rotate(spec.get('incl', -0.2))
    info = draw_char(ctx, q, 0, 0, spec.get('cs', 0.92), Pose(mouth='grin', facing=-1, arms='hold', varre=spec.get('varre', 0.9)))
    tp = ctx.user_to_device(info['head'][0], info['top'][1])
    ctx.restore()
    # escurece as bordas
    g = cairo.RadialGradient(900, H / 2 + 60, 300, 900, H / 2 + 60, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.8)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    # protagonista encolhido em cima da cama
    draw_char(ctx, 'voce', spec.get('vx', 560), 935, 1.35, Pose(eyes='wide', mouth='o', arms='face', sweat=True, sit=True, facing=1))
    ctx.set_source_rgba(0.9, 0.9, 0.92, 1); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (-0.9, -0.5, -0.1):
        ctx.move_to(520 + math.cos(a - 1.5) * 280, 460 + math.sin(a - 1.5) * 280)
        ctx.line_to(520 + math.cos(a - 1.5) * 330, 460 + math.sin(a - 1.5) * 330)
        ctx.stroke()
    g2 = cairo.LinearGradient(0, 0, 0, 300)
    g2.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.92); g2.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0)
    ctx.rectangle(0, 0, W, 300); ctx.set_source(g2); ctx.fill()
    if spec.get('balao'):
        msg = spec['balao']
        ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(58)
        w_ = ctx.text_extents(msg).width + 80
        hx, top = tp
        bx, by = spec.get('bx', 1040), spec.get('by', 720)
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(bx + w_ / 2 - 150, by - 60); ctx.line_to(hx - 70, top + 250); ctx.line_to(bx + w_ / 2 - 70, by - 60); ctx.fill()
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


def mm_cafe(spec, out):
    """Capa 'cafe' (noite 08): a cozinha acesa de madrugada, a mesa posta com as xícaras fumegando em primeiro plano;
    a criatura enorme de avental vermelho atrás da mesa, curvada debaixo da lâmpada, com o bule na mão e o olho único
    aceso; à esquerda, o protagonista espiando da porta escura do corredor, apavorado; balão vermelho.
    spec: ordem, criatura, balao, cena='cafe'"""
    from .render import rich_text
    from .scenes import bg_mm_cozinha_cafe, xicara, vapor
    from .chars import rrect
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    q = spec.get('criatura', 'coisa')
    ctx.save(); ctx.translate(-260, -120); ctx.scale(1.22, 1.22)
    bg_mm_cozinha_cafe(ctx, 0.0, xicaras=0)
    ctx.restore()
    # a criatura atrás da mesa, curvada, servindo
    ctx.save(); ctx.translate(spec.get('cx', 1220), 1100); ctx.rotate(spec.get('incl', -0.2))
    info = draw_char(ctx, q, 0, 0, spec.get('cs', 1.08), Pose(mouth='grin', facing=-1, arms='hold'))
    tp = ctx.user_to_device(info['head'][0], info['top'][1])
    ctx.restore()
    # mesa em primeiro plano com toalha xadrez e as xícaras
    ctx.move_to(560, 860); ctx.line_to(1560, 860); ctx.line_to(1640, 1080); ctx.line_to(480, 1080); ctx.close_path()
    ctx.set_source_rgba(0.17, 0.15, 0.15, 1); ctx.fill_preserve(); ctx.set_source_rgba(0.6, 0.6, 0.64, 1); ctx.set_line_width(5); ctx.stroke()
    ctx.save(); ctx.move_to(560, 860); ctx.line_to(1560, 860); ctx.line_to(1640, 1080); ctx.line_to(480, 1080); ctx.close_path(); ctx.clip()
    for k in range(460, 1660, 56):
        ctx.rectangle(k, 860, 28, 220)
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.12); ctx.fill()
    ctx.restore()
    for k, x in enumerate((700, 920, 1140)):
        xicara(ctx, x, 950, 1.25, 0.5 + k * 1.3)
        vapor(ctx, x - 60, 860, 120, 0.9 + k, a=0.22, n=3)
    # escurece as bordas
    g = cairo.RadialGradient(1100, H / 2 + 40, 300, 1100, H / 2 + 40, 1250)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.75)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    # a porta escura do corredor à esquerda, com o protagonista espiando
    ctx.rectangle(0, 0, 470, H); ctx.set_source_rgba(0.035, 0.035, 0.04, 1); ctx.fill()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 1); ctx.set_line_width(8); ctx.move_to(470, 0); ctx.line_to(470, H); ctx.stroke()
    gl = cairo.LinearGradient(470, 0, 260, 0)
    gl.add_color_stop_rgba(0, 1, 0.72, 0.32, 0.22); gl.add_color_stop_rgba(1, 1, 0.72, 0.32, 0)
    ctx.rectangle(260, 0, 210, H); ctx.set_source(gl); ctx.fill()
    draw_char(ctx, 'voce', spec.get('vx', 330), 1140, 1.4, Pose(eyes='wide', mouth='o', arms='face', sweat=True, facing=1))
    ctx.set_source_rgba(0.9, 0.9, 0.92, 1); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (-0.9, -0.5, -0.1):
        ctx.move_to(330 + math.cos(a - 1.2) * 300, 560 + math.sin(a - 1.2) * 300)
        ctx.line_to(330 + math.cos(a - 1.2) * 350, 560 + math.sin(a - 1.2) * 350)
        ctx.stroke()
    g2 = cairo.LinearGradient(0, 0, 0, 300)
    g2.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.92); g2.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0)
    ctx.rectangle(0, 0, W, 300); ctx.set_source(g2); ctx.fill()
    if spec.get('balao'):
        msg = spec['balao']
        ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(58)
        w_ = ctx.text_extents(msg).width + 80
        hx, top = tp
        bx, by = spec.get('bx', 1450), spec.get('by', 640)
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(bx - w_ / 2 + 120, by - 60); ctx.line_to(hx + 60, top + 200); ctx.line_to(bx - w_ / 2 + 220, by - 60); ctx.fill()
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


def mm_parede(spec, out):
    """Capa 'parede' (noite 09): a casa em corte, dividida pela parede da sua porta trancada. À esquerda, o seu quarto
    escuro, com o protagonista encolhido na cama, apavorado; no meio, a porta vista de dentro com o trinco fechado e a
    sombra de dois pés na fresta; à direita, no corredor, a criatura enorme imitando a irmã (maria-chiquinha, travesseiro
    vermelho) curvada encostada na porta, batendo; balão vermelho.
    spec: ordem, criatura, balao, cena='parede'"""
    from .render import rich_text
    from .scenes import mm_room, bed, trinco, estrelinhas, lr
    from .chars import rrect
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    q = spec.get('criatura', 'coisa')
    # o quarto (esq.) e o corredor (dir.)
    mm_room(ctx, fy=900)
    ctx.rectangle(1010, 0, W - 1010, H); ctx.set_source_rgba(0.075, 0.07, 0.065, 1); ctx.fill()
    g = cairo.RadialGradient(1500, 380, 20, 1500, 380, 700)                  # luz amarela fraca do corredor
    g.add_color_stop_rgba(0, 1, 0.75, 0.35, 0.22); g.add_color_stop_rgba(1, 1, 0.75, 0.35, 0)
    ctx.rectangle(1010, 0, W - 1010, H); ctx.set_source(g); ctx.fill()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 1); ctx.set_line_width(5)
    ctx.move_to(1010, 900); ctx.line_to(W, 900); ctx.stroke()
    # cama e estrelinhas
    ctx.save(); ctx.translate(-120, 80); ctx.scale(1.05, 1.05)
    bed(ctx, 60, 860, 640, made=False)
    ctx.restore()
    estrelinhas(ctx, 60, 470, 520, 120, n=9, seed=4)
    # a parede em corte com a porta
    ctx.rectangle(940, 0, 70, H); ctx.set_source_rgba(0.13, 0.13, 0.15, 1); ctx.fill()
    ctx.set_source_rgba(0.75, 0.75, 0.8, 1); ctx.set_line_width(6)
    ctx.move_to(940, 0); ctx.line_to(940, H); ctx.move_to(1010, 0); ctx.line_to(1010, H); ctx.stroke()
    lr(ctx, 700, 330, 240, 570, fill='#1A1A1E')                              # porta, de dentro
    ctx.arc(905, 640, 8, 0, TAU); ctx.set_source_rgba(0.75, 0.75, 0.8, 1); ctx.fill()
    trinco(ctx, 840, 560, fechado=True)
    for xx in (760, 860):                                                    # sombra dos pés na fresta
        ctx.rectangle(xx, 893, 50, 7); ctx.set_source_rgba(0, 0, 0, 1); ctx.fill()
    gf = cairo.LinearGradient(0, 900, 0, 960)
    gf.add_color_stop_rgba(0, 1, 0.75, 0.35, 0.35); gf.add_color_stop_rgba(1, 1, 0.75, 0.35, 0)
    ctx.rectangle(700, 900, 240, 60); ctx.set_source(gf); ctx.fill()
    # a criatura no corredor, curvada, encostada na porta, batendo
    ctx.save(); ctx.translate(spec.get('cx', 1330), 1050); ctx.rotate(spec.get('incl', -0.12))
    info = draw_char(ctx, q, 0, 0, spec.get('cs', 0.84), Pose(mouth='grin', facing=-1, arms='point'))
    tp = ctx.user_to_device(info['head'][0], info['top'][1])
    ctx.restore()
    # escurece as bordas
    gv = cairo.RadialGradient(960, H / 2 + 60, 350, 960, H / 2 + 60, 1250)
    gv.add_color_stop_rgba(0, 0, 0, 0, 0); gv.add_color_stop_rgba(1, 0, 0, 0, 0.75)
    ctx.rectangle(0, 0, W, H); ctx.set_source(gv); ctx.fill()
    # protagonista encolhido na cama
    draw_char(ctx, 'voce', spec.get('vx', 420), 980, 1.22, Pose(eyes='wide', mouth='o', arms='face', sweat=True, sit=True, facing=1))
    ctx.set_source_rgba(0.9, 0.9, 0.92, 1); ctx.set_line_width(8); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (-0.9, -0.5, -0.1):
        ctx.move_to(420 + math.cos(a - 1.2) * 250, 600 + math.sin(a - 1.2) * 250)
        ctx.line_to(420 + math.cos(a - 1.2) * 300, 600 + math.sin(a - 1.2) * 300)
        ctx.stroke()
    g2 = cairo.LinearGradient(0, 0, 0, 300)
    g2.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.92); g2.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0)
    ctx.rectangle(0, 0, W, 300); ctx.set_source(g2); ctx.fill()
    if spec.get('balao'):
        msg = spec['balao']
        ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(56)
        w_ = ctx.text_extents(msg).width + 80
        hx, top = tp
        bx, by = spec.get('bx', 1480), spec.get('by', 285)
        bx = min(bx, W - w_ / 2 - 20)
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(hx - 40, by + 30); ctx.line_to(hx - 10, top + 40); ctx.line_to(hx + 50, by + 30); ctx.fill()
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



def mm_sofa(spec, out):
    """Capa 'sofa' (noite 10): visto de trás do sofá da sala. Em primeiro plano, enorme, a criatura (o tio de chapéu)
    sentada no sofá com o encosto cobrindo o corpo, o pescoço comprido esticado e a cabeça torta virada pro fundo, com a
    mala vermelha em cima do encosto; lá no fundo, pequeno, no vão escuro do corredor, o protagonista na ponta dos pés,
    apavorado, a caminho do quarto; balão vermelho. spec: ordem, criatura, balao, cena='sofa'"""
    from .render import rich_text
    from .scenes import mm_room, door, amber, lr
    from .chars import rrect, draw_prop
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    q = spec.get('criatura', 'coisa')
    # fundo: a parede da sala com o vão do corredor e as portas lá dentro
    mm_room(ctx, fy=840)
    ctx.rectangle(180, 260, 560, 580); ctx.set_source_rgba(0.015, 0.015, 0.02, 1); ctx.fill()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 1); ctx.set_line_width(6); ctx.rectangle(180, 260, 560, 580); ctx.stroke()
    ctx.set_line_width(3)
    ctx.move_to(180, 840); ctx.line_to(330, 640); ctx.line_to(590, 640); ctx.line_to(740, 840); ctx.stroke()
    for x in (350, 480):
        lr(ctx, x, 430, 100, 210, fill='#0D0D10')
    amber(ctx, 1700, 520, 520, 0.3, 0)
    draw_char(ctx, 'voce', spec.get('vx', 470), 860, 0.62, Pose(eyes='wide', mouth='o', arms='face', sweat=True, facing=1))
    ctx.set_source_rgba(0.9, 0.9, 0.92, 1); ctx.set_line_width(6); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a in (-0.9, -0.5, -0.1):
        ctx.move_to(470 + math.cos(a - 1.2) * 140, 600 + math.sin(a - 1.2) * 140)
        ctx.line_to(470 + math.cos(a - 1.2) * 170, 600 + math.sin(a - 1.2) * 170)
        ctx.stroke()
    # a criatura sentada, enorme, inclinada na direção do corredor
    ctx.save(); ctx.translate(spec.get('cx', 1400), 1200); ctx.rotate(spec.get('incl', -0.5))
    info = draw_char(ctx, q, 0, 0, spec.get('cs', 1.25), Pose(mouth='grin', facing=-1, arms='down', sit=True))
    tp = ctx.user_to_device(info['head'][0], info['top'][1])
    ctx.restore()
    # o encosto do sofá, de costas, em primeiro plano
    rrect(ctx, 760, 860, 1300, 320, 70)
    ctx.set_source_rgba(0.12, 0.12, 0.135, 1); ctx.fill_preserve()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 1); ctx.set_line_width(7); ctx.stroke()
    draw_prop(ctx, 'mala', spec.get('mx', 1640), 712, -1)
    # escurece as bordas
    gv = cairo.RadialGradient(900, H / 2 + 40, 320, 900, H / 2 + 40, 1250)
    gv.add_color_stop_rgba(0, 0, 0, 0, 0); gv.add_color_stop_rgba(1, 0, 0, 0, 0.8)
    ctx.rectangle(0, 0, W, H); ctx.set_source(gv); ctx.fill()
    g2 = cairo.LinearGradient(0, 0, 0, 300)
    g2.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0.92); g2.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0)
    ctx.rectangle(0, 0, W, 300); ctx.set_source(g2); ctx.fill()
    if spec.get('balao'):
        msg = spec['balao']
        ctx.select_font_face('Courier New', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(58)
        w_ = ctx.text_extents(msg).width + 80
        hx, top = tp
        bx, by = spec.get('bx', 1480), spec.get('by', 330)
        bx = min(bx, W - w_ / 2 - 20)
        rrect(ctx, bx - w_ / 2, by - 70, w_, 108, 40)
        ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
        ctx.move_to(bx - w_ / 2 + 60, by + 30); ctx.line_to(hx + 60, top + 200); ctx.line_to(bx - w_ / 2 + 170, by + 30); ctx.fill()
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
