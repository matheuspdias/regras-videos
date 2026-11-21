"""Personagens do canal: cabeça redonda preta brilhante, olhos grandes, corpo simples.
Tudo desenhado com pycairo. Coordenadas: (x, y) = ponto entre os pés, escala s (1.0 ~ 520px de altura).
"""
import math
import cairo

TAU = math.tau


def hexc(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def setc(ctx, c, a=None):
    if isinstance(c, str):
        c = hexc(c)
    if a is not None:
        c = (c[0], c[1], c[2], a)
    ctx.set_source_rgba(*c)


def darker(h, f=0.75):
    r, g, b, _ = hexc(h)
    return (r * f, g * f, b * f, 1)


def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -TAU / 4, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, TAU / 4)
    ctx.arc(x + r, y + h - r, r, TAU / 4, TAU / 2)
    ctx.arc(x + r, y + r, r, TAU / 2, 3 * TAU / 4)
    ctx.close_path()


OUT = (0.07, 0.07, 0.09, 1)  # cor do contorno
LW = 7  # espessura do contorno (em unidades do personagem)
FACE = (0.16, 0.09, 0.07, 1)
CAST_FACE_DARK = True  # canal monocromático  # traços do rosto (boca, sobrancelha, olho fechado)


def fill_stroke(ctx, fill, lw=LW):
    setc(ctx, fill)
    ctx.fill_preserve()
    ctx.set_source_rgba(*OUT)
    ctx.set_line_width(lw)
    ctx.stroke()


# ---------------------------------------------------------------- elenco
CAST = {
    'voce':  dict(skin='#ECECEC', name='Você', shirt='#D6D6D6', pants='#8A8A8A', shoes='#F2F2F2', kind='hoodie', hair='short', hair_c='#5A5A5A', extra=None, face='min', h=1.0),
    'mae':   dict(skin='#ECECEC', name='Mãe', shirt='#CFCFCF', pants='#7A7A7A', shoes='#3A3A3A', kind='tee', hair='ponytail', hair_c='#4A4A4A', extra=None, face='min', h=1.0),
    'coisa': dict(skin='#E4E4E4', name='A coisa', shirt='#CFCFCF', pants='#CFCFCF', shoes='#3A3A3A', kind='dress', hair='ponytail', hair_c='#4A4A4A', extra='presilha_red', face='creature', h=1.42),
    'irmao': dict(skin='#ECECEC', name='Irmão', shirt='#DADADA', pants='#8A8A8A', shoes='#F2F2F2', kind='tee', hair='short', hair_c='#6A6A6A', extra=None, face='min', h=0.7),
    'pai':   dict(tie='#6A6A6A', skin='#ECECEC', name='Pai', shirt='#C4C4C4', pants='#6A6A6A', shoes='#2A2A2A', kind='shirt', hair='short', hair_c='#3A3A3A', extra=None, face='min', h=1.06),
    'vo':    dict(skin='#ECECEC', name='Vó', shirt='#CFCFCF', pants='#CFCFCF', shoes='#3A3A3A', kind='dress', hair='bun', hair_c='#BDBDBD', extra='oculos', face='min', h=0.9),
    # variantes da criatura: a coisa copia quem ela imita, sempre alta, olhos amarelos e UM detalhe vermelho
    'coisa_vo':     dict(skin='#E4E4E4', name='A coisa (vó)', shirt='#CFCFCF', pants='#CFCFCF', shoes='#3A3A3A', kind='dress', hair='bun', hair_c='#BDBDBD', extra='laco_red', face='creature', h=1.36),
    'coisa_pai':    dict(tie='#E5262B', skin='#E4E4E4', name='A coisa (pai)', shirt='#C4C4C4', pants='#5A5A5A', shoes='#2A2A2A', kind='shirt', hair='short', hair_c='#3A3A3A', extra=None, face='creature', h=1.55),
    'coisa_irmao':  dict(skin='#E4E4E4', name='A coisa (irmão)', shirt='#DADADA', pants='#8A8A8A', shoes='#E5262B', kind='tee', hair='short', hair_c='#6A6A6A', extra=None, face='creature', h=1.05),
    'coisa_vizinho': dict(skin='#E4E4E4', name='A coisa (vizinho)', shirt='#BDBDBD', pants='#5A5A5A', shoes='#2A2A2A', kind='tee', hair='cap', hair_c='#E5262B', extra=None, face='creature', h=1.55),
    'coisa_crianca': dict(skin='#E4E4E4', name='A coisa (criança)', shirt='#D6D6D6', pants='#D6D6D6', shoes='#3A3A3A', kind='dress', hair='pigtails', hair_c='#4A4A4A', extra='presilha_red', face='creature', h=0.95),
    # noite 03: imita o pai, pescoço comprido demais (espia por cima do muro), olhos vazios, braços longos; gravata vermelha
    'coisa_ep03':   dict(tie='#E5262B', skin='#E4E4E4', name='A coisa (pai, noite 03)', shirt='#C4C4C4', pants='#4A4A4A', shoes='#2A2A2A', kind='shirt', hair='short', hair_c='#3A3A3A', extra=None, face='creature', h=1.6, pescoco=0.3, olhos='vazios', bracos=2.1, inclina=0.12),
    # noite 04: imita a irmã de camisola, cabelo molhado cobrindo metade do rosto, cabeça torta, boca vertical, braços compridos; xuxinha vermelha
    'coisa_ep04':   dict(skin='#E4E4E4', name='A coisa (irmã, noite 04)', shirt='#D2D2D4', pants='#D2D2D4', shoes='#3A3A3A', kind='dress', hair='mecha', hair_c='#2E2E33', extra='xuxinha_red', face='creature', h=1.55, boca='vertical', bracos=2.25, inclina=0.38),
    'coisa_sombra': dict(skin='#2E2E33', name='A coisa (sombra)', shirt='#1E1E22', pants='#1E1E22', shoes='#111113', kind='tee', hair='none', hair_c='#1E1E22', extra='olhos_red', face='creature', h=1.85),
    'irma':  dict(skin='#ECECEC', name='Irmã', shirt='#D8D8DA', pants='#7E7E84', shoes='#F2F2F2', kind='tee', hair='long', hair_c='#3A3A3E', extra=None, face='min', h=0.95),
    'vizinho': dict(skin='#ECECEC', name='Vizinho', shirt='#BDBDBD', pants='#6A6A6A', shoes='#2A2A2A', kind='tee', hair='cap', hair_c='#5A5A5A', extra=None, face='min', h=1.02),
}


class Pose:
    """Estado de um personagem num frame."""

    def __init__(self, **kw):
        self.eyes = kw.get('eyes', 'normal')     # normal, wide, happy, sad, angry, closed, side, half
        self.look = kw.get('look', 0.0)          # -1 esquerda .. 1 direita
        self.mouth = kw.get('mouth', 'smile')    # smile, open, flat, frown, o, grin, wavy, talk
        self.talk = kw.get('talk', 0.0)          # 0..1 abertura da boca quando falando
        self.arms = kw.get('arms', 'down')       # down, wave, face, point, hip, up, hold, cross, shrug
        self.facing = kw.get('facing', 1)        # 1 para a direita, -1 para a esquerda
        self.sweat = kw.get('sweat', False)
        self.blush = kw.get('blush', False)
        self.blink = kw.get('blink', False)
        self.bob = kw.get('bob', 0.0)
        self.extra_prop = kw.get('prop', None)   # objeto na mão: 'lanche', 'caneta', 'celular', 'veu', 'escova', 'pudim', 'controle'
        self.veil = kw.get('veil', False)
        self.mustache = kw.get('mustache', False)
        self.sit = kw.get('sit', False)
        self.lie = kw.get('lie', False)          # deitado (cabeça para a esquerda, pés no ponto do slot)


def draw_char(ctx, cid, x, y, s=1.0, pose=None):
    c = CAST[cid]
    p = pose or Pose()
    ctx.save()
    ctx.translate(x, y)
    hs = c['h']
    ctx.scale(s, s)
    if p.lie:
        ctx.rotate(-math.pi / 2)
    f = p.facing
    by = -p.bob * 6
    H = 520 * hs  # altura total
    head_r = 118 * (0.92 + 0.08 * hs) if cid != 'lari' else 104
    body_h = H * 0.36
    leg_h = H * 0.22 if not p.sit else H * 0.12
    hip_y = -leg_h + by
    sh_y = hip_y - body_h
    head_cy = sh_y - head_r * 0.82
    neck = c.get('pescoco', 0) * H          # criatura: pescoço comprido demais (fração da altura)
    head_cy -= neck
    body_w_top = 120 * (0.9 + 0.1 * hs)
    body_w_bot = 140 * (0.9 + 0.1 * hs)

    # sombra
    ctx.save()
    ctx.scale(1, 0.18)
    ctx.arc(0, 0, 110 * hs, 0, TAU)
    ctx.restore()
    ctx.set_source_rgba(0, 0, 0, 0.18)
    ctx.fill()
    # pernas
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for side in (-1, 1):
        lx = side * 34
        ctx.set_source_rgba(*OUT)
        ctx.set_line_width(46)
        ctx.move_to(lx, hip_y - 10)
        if p.sit:
            ctx.line_to(lx + 60 * f, hip_y + 4)
        else:
            ctx.line_to(lx, -22)
        ctx.stroke()
        setc(ctx, c['pants'])
        ctx.set_line_width(32)
        ctx.move_to(lx, hip_y - 10)
        if p.sit:
            ctx.line_to(lx + 60 * f, hip_y + 4)
        else:
            ctx.line_to(lx, -22)
        ctx.stroke()
        # sapato
        sx = lx + (60 * f if p.sit else 0)
        sy = hip_y + 4 if p.sit else -18
        ctx.save()
        ctx.translate(sx + 10 * f, sy)
        ctx.scale(1.0, 0.62)
        ctx.arc(0, 0, 30, 0, TAU)
        ctx.restore()
        fill_stroke(ctx, c['shoes'], 6)

    if c['kind'] == 'dress':
        # vestido: trapézio até perto do joelho
        ctx.move_to(-body_w_top / 2, sh_y + 10)
        ctx.line_to(body_w_top / 2, sh_y + 10)
        ctx.line_to(body_w_bot / 2 + 34, hip_y + leg_h * 0.45)
        ctx.line_to(-body_w_bot / 2 - 34, hip_y + leg_h * 0.45)
        ctx.close_path()
        fill_stroke(ctx, c['shirt'])

    # braços (atrás do tronco quando para baixo)
    arm_color = c['shirt']

    def arm(side, kind):
        ax = side * (body_w_top / 2 - 6)
        ay = sh_y + 26
        pts = []
        ak = c.get('bracos', 1.6) if c.get('face') == 'creature' else 1.0
        if kind == 'down':
            pts = [(ax, ay), (ax + side * 34, ay + 70), (ax + side * 30, ay + 140)]
        elif kind == 'hip':
            pts = [(ax, ay), (ax + side * 70, ay + 70), (ax + side * 30, ay + 130)]
        elif kind == 'wave':
            if side == f:
                pts = [(ax, ay), (ax + side * 80, ay - 30), (ax + side * 110, ay - 130)]
            else:
                pts = [(ax, ay), (ax + side * 22, ay + 80), (ax + side * 18, ay + 150)]
        elif kind == 'up':
            pts = [(ax, ay), (ax + side * 60, ay - 70), (ax + side * 70, ay - 170)]
        elif kind == 'face':
            pts = [(ax, ay), (ax + side * 60, ay + 30), (side * 50, head_cy + head_r * 0.45)]
        elif kind == 'point':
            if side == f:
                pts = [(ax, ay), (ax + side * 90, ay + 10), (ax + side * 180, ay - 10)]
            else:
                pts = [(ax, ay), (ax + side * 22, ay + 80), (ax + side * 18, ay + 150)]
        elif kind == 'hold':
            if side == f:
                pts = [(ax, ay), (ax + side * 40, ay + 80), (ax + side * 110, ay + 70)]
            else:
                pts = [(ax, ay), (ax + side * 22, ay + 80), (ax + side * 18, ay + 150)]
        elif kind == 'shrug':
            pts = [(ax, ay), (ax + side * 70, ay + 40), (ax + side * 100, ay - 20)]
        elif kind == 'cross':
            pts = [(ax, ay), (ax + side * 20, ay + 70), (-side * 30, ay + 60)]
        else:
            pts = [(ax, ay), (ax + side * 22, ay + 80), (ax + side * 18, ay + 150)]
        if ak != 1.0:
            pts = [pts[0], (pts[1][0], ay + (pts[1][1] - ay) * ak), (pts[2][0] + side * 20, ay + (pts[2][1] - ay) * ak)]
        for lw, col in ((38, OUT), (26, None)):
            ctx.set_line_width(lw)
            if col:
                ctx.set_source_rgba(*col)
            else:
                setc(ctx, arm_color)
            ctx.move_to(*pts[0])
            ctx.curve_to(pts[1][0], pts[1][1], pts[1][0], pts[1][1], pts[2][0], pts[2][1])
            ctx.stroke()
        # mão
        ctx.arc(pts[2][0], pts[2][1], 19, 0, TAU)
        fill_stroke(ctx, c['skin'], 5)
        return pts[2]

    hands = {}
    front_kinds = ('face', 'cross', 'hold', 'point', 'wave', 'up', 'shrug', 'down', 'hip')
    for side in (-1, 1):
        if p.arms not in front_kinds:
            hands[side] = arm(side, p.arms)

    # tronco
    if c['kind'] != 'dress':
        ctx.move_to(-body_w_top / 2, sh_y + 10)
        ctx.curve_to(-body_w_top / 2 - 10, sh_y + 40, -body_w_bot / 2, hip_y - 30, -body_w_bot / 2, hip_y)
        ctx.line_to(body_w_bot / 2, hip_y)
        ctx.curve_to(body_w_bot / 2, hip_y - 30, body_w_top / 2 + 10, sh_y + 40, body_w_top / 2, sh_y + 10)
        ctx.close_path()
        fill_stroke(ctx, c['shirt'])
    if c['kind'] == 'hoodie':
        # bolso canguru e cordões
        rrect(ctx, -46, hip_y - 70, 92, 46, 16)
        ctx.set_source_rgba(*darker(c['shirt'], 0.82))
        ctx.fill_preserve()
        ctx.set_source_rgba(*OUT)
        ctx.set_line_width(4)
        ctx.stroke()
        ctx.set_line_width(5)
        ctx.set_source_rgba(1, 1, 1, 0.9)
        for dx in (-16, 16):
            ctx.move_to(dx, sh_y + 20)
            ctx.line_to(dx, sh_y + 70)
            ctx.stroke()
    if c['kind'] == 'shirt':
        ctx.set_source_rgba(*OUT)
        ctx.set_line_width(4)
        ctx.move_to(0, sh_y + 20)
        ctx.line_to(0, hip_y)
        ctx.stroke()
        # gravata
        ctx.move_to(0, sh_y + 18)
        ctx.line_to(-12, sh_y + 40)
        ctx.line_to(0, sh_y + 100)
        ctx.line_to(12, sh_y + 40)
        ctx.close_path()
        fill_stroke(ctx, c.get('tie', '#C1121F'), 4)
    if cid == 'voce' and not c.get('face'):
        star(ctx, -30 * f, sh_y + 52, 16, '#FFD23F')

    for side in (-1, 1):
        if p.arms in front_kinds:
            hands[side] = arm(side, p.arms)

    # ---- cabeça
    if p.lie:   # cabeça quase em pé no travesseiro, rosto virado para a câmera
        ctx.save(); ctx.translate(0, head_cy); ctx.rotate(math.pi / 2 - 0.22); ctx.translate(0, -head_cy)
        draw_head(ctx, cid, c, p, 0, head_cy, head_r)
        ctx.restore()
    else:
        if neck > 0:
            ctx.set_line_cap(cairo.LINE_CAP_BUTT)
            ctx.set_source_rgba(*OUT); ctx.set_line_width(46)
            ctx.move_to(0, sh_y + 12); ctx.line_to(0, head_cy + head_r * 0.7); ctx.stroke()
            setc(ctx, c['skin']); ctx.set_line_width(34)
            ctx.move_to(0, sh_y + 14); ctx.line_to(0, head_cy + head_r * 0.72); ctx.stroke()
        tilt = c.get('inclina', 0)              # criatura: cabeça torta (radianos)
        if tilt:
            ctx.save(); ctx.translate(0, head_cy + head_r * 0.8); ctx.rotate(tilt * f); ctx.translate(0, -(head_cy + head_r * 0.8))
        draw_head(ctx, cid, c, p, 0, head_cy, head_r)
        if tilt:
            ctx.restore()

    # props
    if p.extra_prop and (1 in hands or -1 in hands):
        hx, hy = hands.get(f, hands.get(1))
        draw_prop(ctx, p.extra_prop, hx, hy, f)
    ctx.restore()
    if p.lie:
        return dict(head=(x + head_cy * s, y), head_r=head_r * s, top=(x + head_cy * s, y - head_r * s))
    return dict(head=(x, y + head_cy * s), head_r=head_r * s, top=(x, y + (head_cy - head_r) * s))


def star(ctx, x, y, r, col):
    ctx.move_to(x, y - r)
    for i in range(1, 10):
        a = -TAU / 4 + i * TAU / 10
        rr = r if i % 2 == 0 else r * 0.45
        ctx.line_to(x + rr * math.cos(a), y + rr * math.sin(a))
    ctx.close_path()
    fill_stroke(ctx, col, 3)


def draw_head(ctx, cid, c, p, hx, hy, r):
    f = p.facing
    hair = c.get('hair')
    hc = c.get('hair_c', '#222')
    # cabelo atrás
    if hair in ('long', 'mecha'):
        ctx.move_to(hx - r * 1.02, hy - r * 0.1)
        ctx.curve_to(hx - r * 1.15, hy + r * 0.9, hx - r * 0.9, hy + r * 1.45, hx - r * 0.55, hy + r * 1.4)
        ctx.line_to(hx + r * 0.55, hy + r * 1.4)
        ctx.curve_to(hx + r * 0.9, hy + r * 1.45, hx + r * 1.15, hy + r * 0.9, hx + r * 1.02, hy - r * 0.1)
        ctx.close_path()
        fill_stroke(ctx, hc)
    if hair == 'ponytail':
        ctx.save()
        ctx.translate(hx - f * r * 0.95, hy - r * 0.2)
        ctx.rotate(-f * 0.5)
        ctx.scale(0.55, 1.0)
        ctx.arc(0, r * 0.45, r * 0.55, 0, TAU)
        ctx.restore()
        fill_stroke(ctx, hc)
    if hair == 'pigtails':
        for side in (-1, 1):
            ctx.arc(hx + side * r * 1.05, hy + r * 0.05, r * 0.38, 0, TAU)
            fill_stroke(ctx, hc)
            ctx.arc(hx + side * r * 0.88, hy - r * 0.1, r * 0.12, 0, TAU)
            fill_stroke(ctx, '#FF6B9A', 4)
    if hair == 'bigcurls':
        for i in range(11):
            a = math.pi * (0.95 + i * 0.11)
            ctx.arc(hx + math.cos(a) * r * 1.05, hy + math.sin(a) * r * 1.0 + r * 0.15, r * 0.36, 0, TAU)
            fill_stroke(ctx, hc, 5)
        for side in (-1, 1):
            ctx.arc(hx + side * r * 1.05, hy + r * 0.55, r * 0.33, 0, TAU)
            fill_stroke(ctx, hc, 5)
    if hair == 'bun':
        ctx.arc(hx, hy - r * 1.02, r * 0.38, 0, TAU)
        fill_stroke(ctx, hc)

    if p.veil:
        ctx.move_to(hx - r * 0.85, hy - r * 0.6)
        ctx.curve_to(hx - r * 1.6, hy + r * 0.4, hx - r * 1.4, hy + r * 1.6, hx - r * 1.1, hy + r * 1.9)
        ctx.line_to(hx + r * 1.1, hy + r * 1.9)
        ctx.curve_to(hx + r * 1.4, hy + r * 1.6, hx + r * 1.6, hy + r * 0.4, hx + r * 0.85, hy - r * 0.6)
        ctx.curve_to(hx + r * 0.4, hy - r * 1.15, hx - r * 0.4, hy - r * 1.15, hx - r * 0.85, hy - r * 0.6)
        ctx.close_path()
        ctx.set_source_rgba(1, 1, 1, 0.7)
        ctx.fill_preserve()
        ctx.set_source_rgba(1, 1, 1, 0.9)
        ctx.set_line_width(4)
        ctx.stroke()

    # cabeça
    ctx.arc(hx, hy, r, 0, TAU)
    fill_stroke(ctx, c['skin'], LW + 1)
    # brilho (glossy)
    g = cairo.RadialGradient(hx - r * 0.35, hy - r * 0.45, r * 0.05, hx - r * 0.2, hy - r * 0.3, r * 1.0)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.22)
    g.add_color_stop_rgba(0.35, 1, 1, 1, 0.08)
    g.add_color_stop_rgba(1, 1, 1, 1, 0.0)
    ctx.arc(hx, hy, r - 4, 0, TAU)
    ctx.set_source(g)
    ctx.fill()
    ctx.save()
    ctx.translate(hx - r * 0.42, hy - r * 0.52)
    ctx.rotate(-0.6)
    ctx.scale(1.0, 0.55)
    ctx.arc(0, 0, r * 0.2, 0, TAU)
    ctx.restore()
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.fill()

    # cabelo na frente
    if hair in ('long', 'ponytail', 'mecha'):
        ctx.move_to(hx - r * 0.98, hy - r * 0.15)
        ctx.curve_to(hx - r * 0.9, hy - r * 1.15, hx + r * 0.9, hy - r * 1.15, hx + r * 0.98, hy - r * 0.15)
        ctx.curve_to(hx + r * 0.6, hy - r * 0.62, hx + r * 0.1, hy - r * 0.5, hx - r * 0.2 * f, hy - r * 0.78)
        ctx.curve_to(hx - r * 0.4, hy - r * 0.45, hx - r * 0.8, hy - r * 0.5, hx - r * 0.98, hy - r * 0.15)
        ctx.close_path()
        fill_stroke(ctx, hc)
    if hair == 'pigtails' or hair == 'bun':
        ctx.move_to(hx - r * 0.97, hy - r * 0.2)
        ctx.curve_to(hx - r * 0.9, hy - r * 1.12, hx + r * 0.9, hy - r * 1.12, hx + r * 0.97, hy - r * 0.2)
        ctx.curve_to(hx + r * 0.5, hy - r * 0.55, hx - r * 0.5, hy - r * 0.55, hx - r * 0.97, hy - r * 0.2)
        ctx.close_path()
        fill_stroke(ctx, hc)
    if hair == 'curly':
        for i in range(9):
            a = math.pi * (1.0 + i * 0.125)
            ctx.arc(hx + math.cos(a) * r * 0.86, hy + math.sin(a) * r * 0.86, r * 0.3, 0, TAU)
            fill_stroke(ctx, hc, 5)
        ctx.arc(hx, hy - r * 0.85, r * 0.35, 0, TAU)
        fill_stroke(ctx, hc, 5)
    if hair == 'short':
        ctx.move_to(hx - r * 0.99, hy - r * 0.1)
        ctx.curve_to(hx - r * 1.0, hy - r * 1.18, hx + r * 1.0, hy - r * 1.18, hx + r * 0.99, hy - r * 0.1)
        ctx.curve_to(hx + r * 0.7, hy - r * 0.6, hx + r * 0.3, hy - r * 0.62, hx, hy - r * 0.55)
        ctx.curve_to(hx - r * 0.3, hy - r * 0.62, hx - r * 0.7, hy - r * 0.6, hx - r * 0.99, hy - r * 0.1)
        ctx.close_path()
        fill_stroke(ctx, hc)
    if hair == 'bigcurls':
        for i in range(6):
            a = math.pi * (1.15 + i * 0.14)
            ctx.arc(hx + math.cos(a) * r * 0.8, hy + math.sin(a) * r * 0.8, r * 0.3, 0, TAU)
            fill_stroke(ctx, hc, 5)
    if hair == 'cap':
        ctx.move_to(hx - r * 1.0, hy - r * 0.2)
        ctx.curve_to(hx - r * 1.0, hy - r * 1.2, hx + r * 1.0, hy - r * 1.2, hx + r * 1.0, hy - r * 0.2)
        ctx.close_path()
        fill_stroke(ctx, hc)
        ctx.save()
        ctx.translate(hx + f * r * 0.85, hy - r * 0.22)
        ctx.scale(1.0, 0.28)
        ctx.arc(0, 0, r * 0.62, 0, TAU)
        ctx.restore()
        fill_stroke(ctx, hc, 5)
    if hair == 'bald':
        for side in (-1, 1):
            ctx.arc(hx + side * r * 0.95, hy - r * 0.05, r * 0.2, 0, TAU)
            fill_stroke(ctx, hc, 4)

    if c.get('face'):
        _face_custom(ctx, c, p, hx, hy, r)
    else:
        _face_std(ctx, cid, c, p, f, hx, hy, r)
    if hair == 'mecha':                         # noite 04: cabelo molhado caindo por cima de metade do rosto
        ctx.move_to(hx - r * 1.04, hy - r * 0.2)
        ctx.curve_to(hx - r * 0.7, hy - r * 1.1, hx + r * 0.1, hy - r * 1.05, hx + r * 0.05, hy - r * 0.5)
        ctx.curve_to(hx - r * 0.02, hy + r * 0.2, hx - r * 0.12, hy + r * 1.0, hx - r * 0.05, hy + r * 1.75)
        ctx.line_to(hx - r * 0.3, hy + r * 1.6)
        ctx.line_to(hx - r * 0.5, hy + r * 1.8)
        ctx.line_to(hx - r * 0.72, hy + r * 1.55)
        ctx.line_to(hx - r * 0.95, hy + r * 1.7)
        ctx.curve_to(hx - r * 1.15, hy + r * 0.9, hx - r * 1.12, hy + r * 0.3, hx - r * 1.04, hy - r * 0.2)
        ctx.close_path()
        fill_stroke(ctx, hc)
        ctx.set_source_rgba(0.6, 0.6, 0.64, 0.35); ctx.set_line_width(3)   # fios molhados
        for k in (0.25, 0.5, 0.75):
            ctx.move_to(hx - r * (0.15 + k * 0.8), hy - r * 0.6)
            ctx.curve_to(hx - r * (0.1 + k * 0.8), hy + r * 0.3, hx - r * (0.2 + k * 0.75), hy + r * 0.9, hx - r * (0.15 + k * 0.75), hy + r * 1.5)
            ctx.stroke()
    # bigode
    if c.get('extra') == 'bigode' or p.mustache:
        ctx.save()
        ctx.translate(mx, my - r * 0.14)
        for side in (-1, 1):
            ctx.save()
            ctx.scale(side, 1)
            ctx.move_to(0, 0)
            ctx.curve_to(mw * 0.6, -mw * 0.5, mw * 1.4, -mw * 0.2, mw * 1.6, mw * 0.25)
            ctx.curve_to(mw * 1.1, mw * 0.05, mw * 0.5, mw * 0.25, 0, mw * 0.2)
            ctx.close_path()
            ctx.restore()
        ctx.restore()
        ctx.set_source_rgba(0.55, 0.36, 0.2, 1) if p.mustache else ctx.set_source_rgba(0.85, 0.85, 0.85, 1)
        ctx.fill()

    if p.blush:
        for side in (-1, 1):
            ctx.save()
            ctx.translate(hx + side * r * 0.55 + f * r * 0.08, hy + r * 0.3)
            ctx.scale(1, 0.5)
            ctx.arc(0, 0, r * 0.16, 0, TAU)
            ctx.restore()
            ctx.set_source_rgba(1, 0.42, 0.55, 0.75)
            ctx.fill()

    # extras
    ext = c.get('extra')
    if ext == 'fone':
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.set_line_width(12)
        ctx.arc(hx, hy + r * 0.62, r * 0.78, 0.15 * math.pi, 0.85 * math.pi)
        ctx.stroke()
        for side in (-1, 1):
            rrect(ctx, hx + side * r * 0.72 - 18, hy + r * 0.78, 36, 30, 10)
            fill_stroke(ctx, '#F2F2F2', 4)
    if ext == 'presilha_red':
        ctx.save()
        ctx.translate(hx + r * 0.55, hy - r * 0.62)
        ctx.rotate(0.5)
        rrect(ctx, -26, -9, 52, 18, 9)
        ctx.restore()
        fill_stroke(ctx, '#E5262B', 4)
    if ext == 'xuxinha_red':                   # xuxinha vermelha (a que a irmã perdeu no ralo)
        ctx.save(); ctx.translate(hx + r * 0.9, hy + r * 0.55); ctx.scale(0.7, 1.0)
        ctx.arc(0, 0, r * 0.2, 0, TAU); ctx.restore()
        fill_stroke(ctx, '#E5262B', 4)
        ctx.save(); ctx.translate(hx + r * 0.9, hy + r * 0.55); ctx.scale(0.7, 1.0)
        ctx.arc(0, 0, r * 0.08, 0, TAU); ctx.restore()
        fill_stroke(ctx, '#7A1012', 3)
    if ext == 'laco_red':                      # laço vermelho no coque
        for side in (-1, 1):
            ctx.move_to(hx, hy - r * 1.32)
            ctx.line_to(hx + side * r * 0.42, hy - r * 1.5)
            ctx.line_to(hx + side * r * 0.42, hy - r * 1.14)
            ctx.close_path()
            fill_stroke(ctx, '#E5262B', 4)
        ctx.arc(hx, hy - r * 1.32, r * 0.1, 0, TAU)
        fill_stroke(ctx, '#E5262B', 4)
    if ext == 'presilha':
        ctx.save()
        ctx.translate(hx + r * 0.55, hy - r * 0.62)
        ctx.rotate(0.5)
        rrect(ctx, -26, -9, 52, 18, 9)
        ctx.restore()
        fill_stroke(ctx, '#FFD23F', 4)
    if ext == 'brinco':
        for side in (-1, 1):
            ctx.arc(hx + side * r * 0.98, hy + r * 0.45, r * 0.12, 0, TAU)
            ctx.set_source_rgba(1, 0.82, 0.25, 1)
            ctx.set_line_width(6)
            ctx.stroke()
    if p.veil:
        for i in range(5):
            ctx.arc(hx - r * 0.6 + i * r * 0.3, hy - r * 0.9 + abs(i - 2) * r * 0.06, r * 0.13, 0, TAU)
            fill_stroke(ctx, ['#FFFFFF', '#FFB3C6', '#FFFFFF', '#FFB3C6', '#FFFFFF'][i], 3)
    if p.sweat:
        sx = hx + f * r * 0.95
        sy = hy - r * 0.55
        ctx.move_to(sx, sy - 34)
        ctx.curve_to(sx + 22, sy, sx + 18, sy + 22, sx, sy + 22)
        ctx.curve_to(sx - 18, sy + 22, sx - 22, sy, sx, sy - 34)
        ctx.close_path()
        fill_stroke(ctx, '#7CC6FE' if not CAST_FACE_DARK else '#BFC7CC', 4)



def _face_std(ctx, cid, c, p, f, hx, hy, r):
    # olhos
    ex = r * 0.34
    ey = hy - r * 0.02
    er = r * 0.27 if cid != 'lari' else r * 0.3
    look = p.look * er * 0.35 + f * er * 0.12
    for side in (-1, 1):
        cx = hx + side * ex + f * r * 0.08
        if p.blink or p.eyes == 'closed':
            ctx.set_source_rgba(*FACE)
            ctx.set_line_width(9)
            ctx.move_to(cx - er * 0.8, ey + er * 0.2)
            ctx.curve_to(cx - er * 0.3, ey + er * 0.55, cx + er * 0.3, ey + er * 0.55, cx + er * 0.8, ey + er * 0.2)
            ctx.stroke()
            continue
        if p.eyes == 'happy':
            ctx.set_source_rgba(*FACE)
            ctx.set_line_width(11)
            ctx.move_to(cx - er * 0.8, ey + er * 0.3)
            ctx.curve_to(cx - er * 0.4, ey - er * 0.6, cx + er * 0.4, ey - er * 0.6, cx + er * 0.8, ey + er * 0.3)
            ctx.stroke()
            continue
        sc = 1.25 if p.eyes == 'wide' else 1.0
        ctx.save()
        ctx.translate(cx, ey)
        ctx.scale(sc * 0.86, sc * 1.08)
        ctx.arc(0, 0, er, 0, TAU)
        ctx.restore()
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgba(*FACE)
        ctx.set_line_width(4)
        ctx.stroke()
        pr = er * (0.42 if p.eyes == 'wide' else 0.55)
        ctx.arc(cx + look, ey + er * 0.08, pr, 0, TAU)
        ctx.set_source_rgba(0.06, 0.06, 0.08, 1)
        ctx.fill()
        ctx.arc(cx + look - pr * 0.35, ey - pr * 0.3, pr * 0.32, 0, TAU)
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.fill()
        # pálpebras para emoções
        if p.eyes in ('half', 'sad', 'angry'):
            ctx.save()
            ctx.translate(cx, ey)
            ctx.scale(0.9, 1.12)
            ctx.arc(0, 0, er + 2, 0, TAU)
            ctx.restore()
            ctx.save()
            ctx.clip()
            ctx.set_source_rgba(*darker(c['skin'], 0.82))
            if p.eyes == 'half':
                ctx.rectangle(cx - er * 1.2, ey - er * 1.4, er * 2.4, er * 1.25)
            elif p.eyes == 'sad':
                ctx.move_to(cx - er * 1.2, ey - er * 1.4)
                ctx.line_to(cx + er * 1.2, ey - er * 1.4)
                ctx.line_to(cx + er * 1.2 * side, ey - er * 0.9)
                ctx.line_to(cx - er * 1.2 * side, ey - er * 0.2)
                ctx.close_path()
            else:
                ctx.move_to(cx - er * 1.2, ey - er * 1.4)
                ctx.line_to(cx + er * 1.2, ey - er * 1.4)
                ctx.line_to(cx - er * 1.2 * side, ey - er * 0.9)
                ctx.line_to(cx + er * 1.2 * side, ey - er * 0.15)
                ctx.close_path()
            ctx.fill()
            ctx.restore()
    # sobrancelhas
    if p.eyes in ('angry', 'sad', 'wide'):
        ctx.set_source_rgba(*FACE)
        ctx.set_line_width(8)
        for side in (-1, 1):
            cx = hx + side * ex + f * r * 0.08
            by = ey - er * 1.45
            if p.eyes == 'angry':
                ctx.move_to(cx - side * er * 0.8, by - er * 0.15)
                ctx.line_to(cx + side * er * 0.6, by + er * 0.3)
            elif p.eyes == 'sad':
                ctx.move_to(cx - side * er * 0.7, by + er * 0.3)
                ctx.line_to(cx + side * er * 0.6, by - er * 0.1)
            else:
                ctx.move_to(cx - er * 0.6, by - er * 0.25)
                ctx.curve_to(cx - er * 0.2, by - er * 0.5, cx + er * 0.2, by - er * 0.5, cx + er * 0.6, by - er * 0.25)
            ctx.stroke()

    # óculos
    if c.get('extra') == 'oculos':
        ctx.set_source_rgba(0.85, 0.75, 0.4, 1)
        ctx.set_line_width(6)
        for side in (-1, 1):
            cx = hx + side * ex + f * r * 0.08
            ctx.arc(cx, ey, er * 1.12, 0, TAU)
            ctx.stroke()
        ctx.move_to(hx - ex + f * r * 0.08 + er * 1.12, ey)
        ctx.line_to(hx + ex + f * r * 0.08 - er * 1.12, ey)
        ctx.stroke()

    # boca
    mx = hx + f * r * 0.1
    my = hy + r * 0.48
    mw = r * 0.26
    ctx.set_source_rgba(*FACE)
    ctx.set_line_width(8)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    m = p.mouth
    if p.talk > 0.05 and m not in ('o',):
        oh = r * 0.08 + p.talk * r * 0.2
        ctx.save()
        ctx.translate(mx, my)
        ctx.scale(1.0, oh / (mw * 0.8))
        ctx.arc(0, 0, mw * 0.8, 0, TAU)
        ctx.restore()
        ctx.set_source_rgba(0.85, 0.25, 0.3, 1)
        ctx.fill_preserve()
        ctx.set_source_rgba(*FACE)
        ctx.set_line_width(6)
        ctx.stroke()
    elif m == 'smile':
        ctx.move_to(mx - mw, my - mw * 0.2)
        ctx.curve_to(mx - mw * 0.4, my + mw * 0.55, mx + mw * 0.4, my + mw * 0.55, mx + mw, my - mw * 0.2)
        ctx.stroke()
    elif m == 'grin':
        ctx.move_to(mx - mw * 1.2, my - mw * 0.3)
        ctx.curve_to(mx - mw * 0.6, my + mw * 1.1, mx + mw * 0.6, my + mw * 1.1, mx + mw * 1.2, my - mw * 0.3)
        ctx.close_path()
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.fill_preserve()
        ctx.set_source_rgba(*FACE)
        ctx.set_line_width(6)
        ctx.stroke()
    elif m == 'flat':
        ctx.move_to(mx - mw * 0.7, my + 4)
        ctx.line_to(mx + mw * 0.7, my + 4)
        ctx.stroke()
    elif m == 'frown':
        ctx.move_to(mx - mw * 0.8, my + mw * 0.35)
        ctx.curve_to(mx - mw * 0.3, my - mw * 0.3, mx + mw * 0.3, my - mw * 0.3, mx + mw * 0.8, my + mw * 0.35)
        ctx.stroke()
    elif m == 'o':
        ctx.arc(mx, my + 4, mw * 0.45, 0, TAU)
        ctx.set_source_rgba(0.85, 0.25, 0.3, 1)
        ctx.fill_preserve()
        ctx.set_source_rgba(*FACE)
        ctx.set_line_width(6)
        ctx.stroke()
    elif m == 'wavy':
        ctx.move_to(mx - mw, my)
        for i in range(1, 7):
            ctx.line_to(mx - mw + i * mw / 3, my + (6 if i % 2 else -6))
        ctx.stroke()



def _face_custom(ctx, c, p, hx, hy, r):
    f = p.facing
    style = c['face']
    if style == 'min':
        # rosto mínimo: dois pontinhos e um traço
        for side in (-1, 1):
            ex = hx + side * r * 0.3 + f * r * 0.1 + p.look * r * 0.06
            ey = hy - r * 0.02
            if p.blink or p.eyes == 'closed':
                ctx.set_source_rgba(*FACE); ctx.set_line_width(6)
                ctx.move_to(ex - r * 0.1, ey); ctx.line_to(ex + r * 0.1, ey); ctx.stroke()
                continue
            er = r * (0.13 if p.eyes == 'wide' else 0.095)
            ctx.arc(ex, ey, er, 0, TAU); ctx.set_source_rgba(0.06, 0.06, 0.07, 1); ctx.fill()
            ctx.arc(ex - er * 0.3, ey - er * 0.35, er * 0.3, 0, TAU); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
            if p.eyes in ('sad', 'angry', 'wide'):
                ctx.set_source_rgba(*FACE); ctx.set_line_width(5)
                by = ey - r * 0.25
                if p.eyes == 'sad':
                    ctx.move_to(ex - side * r * 0.13, by + r * 0.05); ctx.line_to(ex + side * r * 0.1, by - r * 0.03)
                elif p.eyes == 'angry':
                    ctx.move_to(ex - side * r * 0.13, by - r * 0.04); ctx.line_to(ex + side * r * 0.1, by + r * 0.05)
                else:
                    ctx.move_to(ex - r * 0.1, by - r * 0.04); ctx.line_to(ex + r * 0.1, by - r * 0.04)
                ctx.stroke()
        mx = hx + f * r * 0.1
        my = hy + r * 0.4
        ctx.set_source_rgba(*FACE); ctx.set_line_width(6)
        if p.talk > 0.05 or p.mouth == 'o':
            oh = r * (0.06 + 0.12 * max(p.talk, 0.5 if p.mouth == 'o' else 0))
            ctx.save(); ctx.translate(mx, my); ctx.scale(1, oh / (r * 0.08)); ctx.arc(0, 0, r * 0.08, 0, TAU); ctx.restore()
            ctx.set_source_rgba(0.1, 0.1, 0.12, 1); ctx.fill()
        elif p.mouth in ('smile', 'grin'):
            ctx.arc(mx, my - r * 0.08, r * 0.14, 0.2 * math.pi, 0.8 * math.pi); ctx.stroke()
        elif p.mouth == 'frown':
            ctx.arc(mx, my + r * 0.1, r * 0.12, 1.2 * math.pi, 1.8 * math.pi); ctx.stroke()
        elif p.mouth == 'wavy':
            ctx.move_to(mx - r * 0.14, my)
            for i in range(1, 5):
                ctx.line_to(mx - r * 0.14 + i * r * 0.07, my + (4 if i % 2 else -4))
            ctx.stroke()
        else:
            ctx.move_to(mx - r * 0.1, my); ctx.line_to(mx + r * 0.1, my); ctx.stroke()
    elif style == 'creature':
        # olhos: 'dois' (padrão) | 'quatro' | 'um' | 'vazios' | 'fechados' ; boca: 'sorriso' | 'vertical' | 'costurada' | 'aberta'
        olhos = c.get('olhos', 'dois')

        def glow_eye(ex, ey, rr, a=1.0):
            for k in range(6, 0, -1):
                ctx.arc(ex, ey, rr * (1 + k * 0.35), 0, TAU)
                ctx.set_source_rgba(1, 0.85, 0.2, 0.05 * a); ctx.fill()
            ctx.arc(ex, ey, rr, 0, TAU); ctx.set_source_rgba(1, 0.88, 0.25, a); ctx.fill()
            ctx.arc(ex, ey, rr * 0.33, 0, TAU); ctx.set_source_rgba(0.1, 0.05, 0, a); ctx.fill()
        if olhos == 'quatro':
            for side in (-1, 1):
                glow_eye(hx + side * r * 0.36, hy - r * 0.22, r * 0.12)
                glow_eye(hx + side * r * 0.22, hy + r * 0.05, r * 0.09)
        elif olhos == 'um':
            glow_eye(hx, hy - r * 0.12, r * 0.26)
        elif olhos == 'vazios':
            for side in (-1, 1):
                ex, ey = hx + side * r * 0.33, hy - r * 0.08
                ctx.save(); ctx.translate(ex, ey); ctx.scale(1, 1.35); ctx.arc(0, 0, r * 0.19, 0, TAU); ctx.restore()
                ctx.set_source_rgba(0.02, 0.02, 0.025, 1); ctx.fill()
                glow_eye(ex, ey + r * 0.03, r * 0.035)
        elif olhos == 'fechados':
            ctx.set_source_rgba(*FACE); ctx.set_line_width(7)
            for side in (-1, 1):
                ex, ey = hx + side * r * 0.33, hy - r * 0.08
                ctx.arc(ex, ey - r * 0.06, r * 0.13, 0.15 * math.pi, 0.85 * math.pi); ctx.stroke()
        else:
            for side in (-1, 1):
                glow_eye(hx + side * r * 0.33, hy - r * 0.08, r * 0.15)
        boca = c.get('boca', 'sorriso')
        if p.mouth == 'flat' and boca == 'sorriso':
            ctx.set_source_rgba(*FACE); ctx.set_line_width(6)
            ctx.move_to(hx - r * 0.1, hy + r * 0.4); ctx.line_to(hx + r * 0.1, hy + r * 0.4); ctx.stroke()
        elif boca == 'vertical':
            my = hy + r * 0.45
            ctx.save(); ctx.translate(hx, my); ctx.scale(0.32, 1); ctx.arc(0, 0, r * 0.42, 0, TAU); ctx.restore()
            ctx.set_source_rgba(0.05, 0.05, 0.06, 1); ctx.fill()
            ctx.set_source_rgba(0.95, 0.95, 0.9, 1); ctx.set_line_width(3)
            for i in range(-4, 5):
                yy = my + i * r * 0.085
                ww = r * 0.13 * (1 - abs(i) / 5.5)
                ctx.move_to(hx - ww, yy); ctx.line_to(hx - ww * 0.3, yy); ctx.stroke()
                ctx.move_to(hx + ww, yy); ctx.line_to(hx + ww * 0.3, yy); ctx.stroke()
        elif boca == 'costurada':
            w = r * 0.62; my = hy + r * 0.42
            ctx.set_source_rgba(*FACE); ctx.set_line_width(6)
            ctx.move_to(hx - w, my - r * 0.08); ctx.curve_to(hx - w * 0.4, my + r * 0.12, hx + w * 0.4, my + r * 0.12, hx + w, my - r * 0.08); ctx.stroke()
            ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.set_line_width(4)
            for i in range(-5, 6):
                x = hx + i * w / 6
                ctx.move_to(x, my - r * 0.04); ctx.line_to(x, my + r * 0.14); ctx.stroke()
        elif boca == 'aberta':
            ctx.save(); ctx.translate(hx, hy + r * 0.5); ctx.scale(1, 1.25); ctx.arc(0, 0, r * 0.3, 0, TAU); ctx.restore()
            ctx.set_source_rgba(0.03, 0.03, 0.035, 1); ctx.fill()
        else:
            w = r * 0.72
            my = hy + r * 0.36
            ctx.move_to(hx - w, my - r * 0.1)
            ctx.curve_to(hx - w * 0.5, my + r * 0.42, hx + w * 0.5, my + r * 0.42, hx + w, my - r * 0.1)
            ctx.curve_to(hx + w * 0.5, my + r * 0.12, hx - w * 0.5, my + r * 0.12, hx - w, my - r * 0.1)
            ctx.close_path()
            ctx.set_source_rgba(0.05, 0.05, 0.06, 1); ctx.fill()
            ctx.set_source_rgba(0.95, 0.95, 0.9, 1); ctx.set_line_width(3)
            for i in range(-6, 7):
                x = hx + i * w / 7
                ctx.move_to(x, my + r * 0.02); ctx.line_to(x, my + r * 0.16 - abs(i) * r * 0.012); ctx.stroke()


def draw_prop(ctx, prop, x, y, f):
    ctx.save()
    ctx.translate(x, y)
    if prop == 'lanche':
        ctx.save()
        ctx.scale(1, 0.6)
        ctx.arc(0, -10, 42, math.pi, TAU)
        ctx.restore()
        fill_stroke(ctx, '#E9B872', 5)
        rrect(ctx, -44, -12, 88, 12, 5)
        fill_stroke(ctx, '#7FB800', 4)
        rrect(ctx, -42, 0, 84, 16, 8)
        fill_stroke(ctx, '#E9B872', 5)
    elif prop == 'caneta':
        ctx.rotate(-0.6 * f)
        rrect(ctx, -6, -60, 12, 80, 5)
        fill_stroke(ctx, '#2F7DE1', 4)
    elif prop == 'celular':
        rrect(ctx, -26, -60, 52, 92, 10)
        fill_stroke(ctx, '#222831', 5)
        rrect(ctx, -19, -52, 38, 74, 6)
        ctx.set_source_rgba(0.82, 0.88, 0.96, 1)
        ctx.fill()
    elif prop == 'controle':
        rrect(ctx, -50, -22, 100, 44, 20)
        fill_stroke(ctx, '#3A3A48', 5)
        for dx, col in ((26, '#E63946'), (38, '#2A9D8F')):
            ctx.arc(dx - 6, -4, 7, 0, TAU)
            setc(ctx, col)
            ctx.fill()
    elif prop == 'pudim':
        ctx.save()
        ctx.scale(1, 0.35)
        ctx.arc(0, 0, 70, 0, TAU)
        ctx.restore()
        fill_stroke(ctx, '#FFFFFF', 4)
        ctx.move_to(-38, -2)
        ctx.line_to(-28, -52)
        ctx.line_to(28, -52)
        ctx.line_to(38, -2)
        ctx.close_path()
        fill_stroke(ctx, '#F4C95D', 5)
        rrect(ctx, -29, -60, 58, 16, 8)
        fill_stroke(ctx, '#8C4A1C', 4)
    elif prop == 'escova':
        ctx.rotate(-0.9 * f)
        rrect(ctx, -6, -70, 12, 90, 5)
        fill_stroke(ctx, '#4CC9F0', 4)
        rrect(ctx, -9, -88, 18, 22, 4)
        fill_stroke(ctx, '#FFFFFF', 3)
    elif prop == 'caderno':
        rrect(ctx, -50, -70, 100, 130, 8)
        fill_stroke(ctx, '#F8F4E3', 5)
        ctx.set_source_rgba(0.5, 0.6, 0.9, 1)
        ctx.set_line_width(2)
        for i in range(6):
            ctx.move_to(-40, -45 + i * 18)
            ctx.line_to(40, -45 + i * 18)
            ctx.stroke()
    elif prop == 'frango':
        ctx.save()
        ctx.rotate(-0.4 * f)
        ctx.save()
        ctx.scale(1, 0.75)
        ctx.arc(0, -30, 34, 0, TAU)
        ctx.restore()
        fill_stroke(ctx, '#C46A2B', 5)
        rrect(ctx, -6, -6, 12, 40, 6)
        fill_stroke(ctx, '#FFF4DC', 4)
        ctx.restore()
    elif prop == 'sacola':
        ctx.move_to(-40, -10)
        ctx.line_to(40, -10)
        ctx.line_to(34, 70)
        ctx.line_to(-34, 70)
        ctx.close_path()
        fill_stroke(ctx, '#F1FAEE', 4)
        for dx in (-18, 4, 20):
            ctx.arc(dx, -16, 16, 0, TAU)
            fill_stroke(ctx, '#E63946', 3)
        ctx.arc(-8, -28, 14, 0, TAU)
        fill_stroke(ctx, '#2A9D8F', 3)
    elif prop == 'bolo':
        ctx.save(); ctx.scale(1, 0.32); ctx.arc(0, 0, 80, 0, TAU); ctx.restore()
        fill_stroke(ctx, '#FFFFFF', 4)
        ctx.move_to(-60, -4); ctx.line_to(-60, -56); ctx.line_to(60, -56); ctx.line_to(60, -4); ctx.close_path()
        fill_stroke(ctx, '#F4C430', 5)
        ctx.save(); ctx.translate(0, -56); ctx.scale(1, 0.3); ctx.arc(0, 0, 60, 0, TAU); ctx.restore()
        fill_stroke(ctx, '#F9D55B', 4)
        ctx.arc(0, -58, 10, 0, TAU)
        fill_stroke(ctx, '#FFFFFF', 3)
    elif prop == 'microfone':
        ctx.rotate(-0.4 * f)
        rrect(ctx, -9, -10, 18, 70, 6)
        fill_stroke(ctx, '#343A40', 4)
        ctx.arc(0, -24, 20, 0, TAU)
        fill_stroke(ctx, '#ADB5BD', 4)
    elif prop == 'coxinha':
        ctx.move_to(0, -50); ctx.curve_to(40, -10, 40, 30, 0, 32); ctx.curve_to(-40, 30, -40, -10, 0, -50); ctx.close_path()
        fill_stroke(ctx, '#D98E32', 4)
    elif prop == 'bola':
        ctx.arc(0, -10, 34, 0, TAU); fill_stroke(ctx, '#FFFFFF', 4)
        for k in range(5):
            a = k * TAU / 5
            ctx.arc(math.cos(a) * 21, -10 + math.sin(a) * 21, 7, 0, TAU)
            ctx.set_source_rgba(0.1, 0.1, 0.12, 1); ctx.fill()
    elif prop == 'caneca':
        rrect(ctx, -26, -50, 52, 60, 8)
        fill_stroke(ctx, '#D8D8D8', 4)
        ctx.arc(30, -20, 16, -1.4, 1.4); ctx.set_source_rgba(*OUT); ctx.set_line_width(6); ctx.stroke()
    elif prop == 'veu':
        ctx.save()
        ctx.scale(1, 0.6)
        ctx.arc(0, -40, 50, 0, TAU)
        ctx.restore()
        ctx.set_source_rgba(1, 1, 1, 0.75)
        ctx.fill()
    ctx.restore()
