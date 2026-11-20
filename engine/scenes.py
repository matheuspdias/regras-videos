"""Cenários (fundo + primeiro plano) e posições (slots) dos personagens."""
import math
import random
import cairo
from .chars import hexc, setc, rrect, fill_stroke, OUT, TAU, star

W, H = 1920, 1080


def rect(ctx, x, y, w, h, col, outline=True, lw=5):
    ctx.rectangle(x, y, w, h)
    if outline:
        fill_stroke(ctx, col, lw)
    else:
        setc(ctx, col)
        ctx.fill()


def rr(ctx, x, y, w, h, r, col, lw=5):
    rrect(ctx, x, y, w, h, r)
    fill_stroke(ctx, col, lw)


def window(ctx, x, y, w, h, sky='#9ED8F5', night=False):
    rr(ctx, x - 14, y - 14, w + 28, h + 28, 10, '#FFFFFF')
    g = cairo.LinearGradient(0, y, 0, y + h)
    if night:
        g.add_color_stop_rgb(0, 0.08, 0.1, 0.25)
        g.add_color_stop_rgb(1, 0.2, 0.18, 0.4)
    else:
        a = hexc(sky)
        g.add_color_stop_rgb(0, a[0], a[1], a[2])
        g.add_color_stop_rgb(1, 0.85, 0.95, 1)
    ctx.rectangle(x, y, w, h)
    ctx.set_source(g)
    ctx.fill()
    if night:
        ctx.arc(x + w * 0.7, y + h * 0.3, 26, 0, TAU)
        ctx.set_source_rgba(1, 0.97, 0.8, 1)
        ctx.fill()
    else:
        # nuvem
        for dx, dy, r in ((0.3, 0.35, 26), (0.38, 0.3, 32), (0.47, 0.36, 24)):
            ctx.arc(x + w * dx, y + h * dy, r, 0, TAU)
            ctx.set_source_rgba(1, 1, 1, 0.95)
            ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.set_line_width(10)
    ctx.move_to(x + w / 2, y)
    ctx.line_to(x + w / 2, y + h)
    ctx.move_to(x, y + h / 2)
    ctx.line_to(x + w, y + h / 2)
    ctx.stroke()
    ctx.rectangle(x, y, w, h)
    ctx.set_source_rgba(*OUT)
    ctx.set_line_width(5)
    ctx.stroke()


def frame_pic(ctx, x, y, w, h, col):
    rr(ctx, x, y, w, h, 4, '#8B5E3C')
    rect(ctx, x + 10, y + 10, w - 20, h - 20, col, lw=3)


def floor(ctx, y, col, col2=None, tiles=False):
    rect(ctx, 0, y, W, H - y, col, outline=False)
    ctx.set_source_rgba(*OUT)
    ctx.set_line_width(5)
    ctx.move_to(0, y)
    ctx.line_to(W, y)
    ctx.stroke()
    if tiles:
        ctx.set_source_rgba(0, 0, 0, 0.08)
        ctx.set_line_width(3)
        for i in range(-10, 30):
            ctx.move_to(W / 2 + i * 140 - (H - y) * 1.2 * (i - 10) / 10, H)
            ctx.line_to(W / 2 + (i - 10) * 70 + 700, y)
            ctx.stroke()
        for k in range(1, 5):
            yy = y + (H - y) * (k / 5) ** 1.4
            ctx.move_to(0, yy)
            ctx.line_to(W, yy)
            ctx.stroke()


def wall(ctx, col, y1, col2=None, ybreak=None):
    rect(ctx, 0, 0, W, y1, col, outline=False)
    if col2 and ybreak:
        rect(ctx, 0, ybreak, W, y1 - ybreak, col2, outline=False)
        ctx.set_source_rgba(0, 0, 0, 0.35)
        ctx.set_line_width(6)
        ctx.move_to(0, ybreak)
        ctx.line_to(W, ybreak)
        ctx.stroke()


def vignette(ctx, a=0.28):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, H * 1.05)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, a)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()


def text(ctx, s, x, y, size, col='#FFFFFF', align='center', bold=True, outline=None, lw=10, font='Poppins'):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)
    ext = ctx.text_extents(s)
    if align == 'center':
        tx = x - ext.width / 2 - ext.x_bearing
    elif align == 'right':
        tx = x - ext.width - ext.x_bearing
    else:
        tx = x
    ty = y
    ctx.move_to(tx, ty)
    ctx.text_path(s)
    if outline:
        setc(ctx, outline)
        ctx.set_line_width(lw)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.stroke_preserve()
    setc(ctx, col)
    ctx.fill()
    return ext


# ---------------------------------------------------------------- cenários
def bg_jantar(ctx, t):
    wall(ctx, '#F6E7C8', 760, '#E9C99A', 520)
    window(ctx, 1480, 120, 300, 260)
    frame_pic(ctx, 250, 140, 200, 150, '#7FB3D5')
    frame_pic(ctx, 520, 170, 130, 170, '#F5B7B1')
    # relógio
    ctx.arc(1080, 200, 60, 0, TAU)
    fill_stroke(ctx, '#FFFFFF')
    ctx.set_source_rgba(*OUT)
    ctx.set_line_width(6)
    ctx.move_to(1080, 200); ctx.line_to(1080, 160); ctx.move_to(1080, 200); ctx.line_to(1110, 210); ctx.stroke()
    # filtro de barro
    rr(ctx, 120, 560, 120, 200, 40, '#C8763E')
    floor(ctx, 760, '#B9855A')


def fg_jantar(ctx, t):
    # mesa com toalha xadrez
    rr(ctx, 160, 760, 1600, 90, 12, '#FFFFFF')
    ctx.save()
    rrect(ctx, 160, 760, 1600, 90, 12)
    ctx.clip()
    ctx.set_source_rgba(0.85, 0.2, 0.2, 0.55)
    for i in range(0, 1600, 60):
        ctx.rectangle(160 + i, 760, 30, 90)
    ctx.fill()
    ctx.restore()
    rrect(ctx, 160, 760, 1600, 90, 12)
    ctx.set_source_rgba(*OUT)
    ctx.set_line_width(5)
    ctx.stroke()
    rect(ctx, 180, 850, 1560, 230, '#8B5A2B')
    # comida
    for x, col in ((420, '#F4D35E'), (760, '#FFFFFF'), (1130, '#C46A2B'), (1460, '#7FB800')):
        ctx.save(); ctx.translate(x, 752); ctx.scale(1, 0.32); ctx.arc(0, 0, 90, 0, TAU); ctx.restore()
        fill_stroke(ctx, '#FFFFFF', 4)
        ctx.save(); ctx.translate(x, 735); ctx.scale(1, 0.45); ctx.arc(0, 0, 56, math.pi, TAU); ctx.restore()
        fill_stroke(ctx, col, 4)
    # jarra de suco
    rr(ctx, 560, 700, 56, 70, 12, '#FFB347')


def bg_sala(ctx, t):
    wall(ctx, '#CDE7E3', 780)
    window(ctx, 200, 140, 320, 280)
    # TV
    rr(ctx, 1260, 240, 460, 280, 16, '#1E1E24')
    g = cairo.LinearGradient(0, 260, 0, 500)
    g.add_color_stop_rgb(0, 0.3, 0.6, 1)
    g.add_color_stop_rgb(1, 0.6, 0.3, 0.9)
    ctx.rectangle(1280, 260, 420, 240)
    ctx.set_source(g)
    ctx.fill()
    text(ctx, 'GOL!', 1490, 410, 90, '#FFD23F', outline='#1E1E24', lw=12)
    rect(ctx, 1240, 520, 500, 260, '#8B5E3C')
    floor(ctx, 780, '#D9B38C', tiles=True)
    rr(ctx, 240, 560, 1000, 280, 40, '#E76F51')


def fg_sala(ctx, t):
    rr(ctx, 200, 640, 90, 280, 40, '#E76F51')
    rr(ctx, 1190, 640, 90, 280, 40, '#E76F51')
    rr(ctx, 260, 810, 960, 110, 30, '#C65A3F')


def bg_portao(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 700)
    g.add_color_stop_rgb(0, 0.55, 0.8, 0.98)
    g.add_color_stop_rgb(1, 0.85, 0.94, 1)
    ctx.rectangle(0, 0, W, 700)
    ctx.set_source(g)
    ctx.fill()
    # prédio da escola
    rect(ctx, 0, 180, W, 560, '#F2C14E')
    rect(ctx, 0, 560, W, 180, '#2A9D8F', outline=False)
    for i in range(6):
        window(ctx, 120 + i * 300, 250, 170, 140)
    text(ctx, 'E.E. PROF. ANTÔNIO CARLOS', 960, 230, 44, '#FFFFFF', outline='#1E1E24', lw=10)
    # muro + portão
    rect(ctx, 0, 600, W, 160, '#D9D9D9')
    rect(ctx, 600, 520, 720, 260, '#6C757D')
    ctx.set_source_rgba(*OUT)
    ctx.set_line_width(10)
    for i in range(16):
        ctx.move_to(620 + i * 46, 530); ctx.line_to(620 + i * 46, 770)
    ctx.stroke()
    # guarita
    rr(ctx, 1450, 420, 300, 360, 10, '#FFFFFF')
    window(ctx, 1490, 470, 220, 130)
    text(ctx, 'PORTARIA', 1600, 700, 38, '#1E1E24')
    floor(ctx, 760, '#A3A3A3')
    ctx.set_source_rgba(0, 0, 0, 0.12)
    for i in range(0, W, 160):
        ctx.rectangle(i, 760, 6, 320)
    ctx.fill()


def bg_classe(ctx, t):
    wall(ctx, '#FDF1D6', 720, '#7FB069', 500)
    # quadro verde
    rr(ctx, 520, 110, 880, 330, 10, '#2D6A4F', 8)
    rect(ctx, 520, 430, 880, 20, '#B08968')
    ctx.set_source_rgba(1, 1, 1, 0.85)
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(54)
    ctx.move_to(600, 220); ctx.show_text('2x + 6 = 14')
    ctx.move_to(600, 320); ctx.show_text('x = ?')
    window(ctx, 1560, 140, 260, 300)
    window(ctx, 100, 140, 260, 300)
    floor(ctx, 720, '#C9A27E', tiles=True)
    # mesa do professor
    rr(ctx, 120, 640, 320, 140, 8, '#8B5E3C')


def fg_classe(ctx, t):
    for x in (700, 1100, 1500):
        rr(ctx, x - 150, 820, 300, 40, 8, '#D4A373')
        rect(ctx, x - 130, 860, 18, 220, '#6C757D', lw=3)
        rect(ctx, x + 112, 860, 18, 220, '#6C757D', lw=3)


def bg_patio(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 600)
    g.add_color_stop_rgb(0, 0.5, 0.78, 0.98)
    g.add_color_stop_rgb(1, 0.82, 0.93, 1)
    ctx.rectangle(0, 0, W, 760)
    ctx.set_source(g)
    ctx.fill()
    for x, y, r in ((300, 140, 50), (360, 120, 64), (430, 145, 46), (1400, 100, 40), (1450, 90, 54)):
        ctx.arc(x, y, r, 0, TAU)
        ctx.set_source_rgba(1, 1, 1, 0.95)
        ctx.fill()
    rect(ctx, 0, 330, W, 450, '#F4A261')
    rect(ctx, 0, 600, W, 180, '#E76F51', outline=False)
    # cantina
    rr(ctx, 760, 380, 420, 240, 8, '#FFFFFF')
    rect(ctx, 790, 420, 360, 160, '#3D405B')
    text(ctx, 'CANTINA', 970, 370, 46, '#FFFFFF', outline='#1E1E24', lw=10)
    for i in range(7):
        ctx.move_to(780 + i * 60, 380)
        ctx.line_to(810 + i * 60, 330)
        ctx.line_to(840 + i * 60, 380)
        ctx.close_path()
        fill_stroke(ctx, '#E63946' if i % 2 else '#FFFFFF', 4)
    # árvore
    rect(ctx, 260, 420, 60, 360, '#8B5E3C')
    for dx, dy, r in ((0, 0, 140), (-90, 50, 100), (100, 50, 110)):
        ctx.arc(290 + dx, 380 + dy, r, 0, TAU)
        fill_stroke(ctx, '#52B788')
    floor(ctx, 780, '#BFBFBF')
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.set_line_width(8)
    ctx.move_to(0, 900); ctx.line_to(W, 900); ctx.stroke()
    # banco
    rr(ctx, 1450, 720, 360, 40, 8, '#8B5E3C')


def bg_corredor(ctx, t):
    wall(ctx, '#FFFFFF', 760, '#3A86FF', 500)
    for x in (180, 1520):
        rr(ctx, x, 230, 220, 530, 6, '#8B5E3C')
        ctx.arc(x + 190, 500, 12, 0, TAU)
        fill_stroke(ctx, '#FFD23F', 3)
        rr(ctx, x + 40, 260, 140, 90, 6, '#BDE0FE')
    # mural
    rr(ctx, 620, 160, 680, 300, 8, '#DDA15E')
    for i, col in enumerate(('#FFFFFF', '#FFD6A5', '#CAFFBF', '#9BF6FF', '#FFC6FF')):
        ctx.save(); ctx.translate(680 + i * 125, 220 + (i % 2) * 40); ctx.rotate((i % 3 - 1) * 0.08)
        rect(ctx, 0, 0, 100, 120, col, lw=3); ctx.restore()
    text(ctx, 'FESTA JUNINA - SÁB', 960, 430, 40, '#9D0208')
    floor(ctx, 760, '#E9D8A6', tiles=True)


def fx_estojo(ctx, t):
    random.seed(4)
    for i in range(9):
        x = 760 + random.random() * 520
        y = 960 + random.random() * 80
        ctx.save(); ctx.translate(x, y); ctx.rotate(random.random() * 3)
        rrect(ctx, -6, -40, 12, 80, 5)
        fill_stroke(ctx, random.choice(['#E63946', '#2F7DE1', '#2A9D8F', '#FFB703', '#9B5DE5']), 3)
        ctx.restore()


def bg_biblioteca(ctx, t):
    wall(ctx, '#E9EDC9', 760)
    for sx in (60, 1360):
        rect(ctx, sx, 120, 500, 640, '#7F5539')
        for row in range(5):
            y = 150 + row * 120
            rect(ctx, sx + 20, y + 90, 460, 14, '#5C3D2E', lw=3)
            random.seed(row + sx)
            x = sx + 30
            while x < sx + 460:
                w = 20 + random.random() * 22
                h = 60 + random.random() * 28
                rect(ctx, x, y + 90 - h, w, h, random.choice(['#E63946', '#457B9D', '#F4A261', '#2A9D8F', '#E9C46A', '#8338EC']), lw=3)
                x += w + 3
    text(ctx, 'SILÊNCIO', 960, 200, 64, '#9D0208', outline='#FFFFFF', lw=10)
    floor(ctx, 760, '#B08968')


def fg_biblioteca(ctx, t):
    rr(ctx, 380, 800, 640, 40, 8, '#A47148')
    rect(ctx, 420, 840, 20, 240, '#6C584C', lw=3)
    rect(ctx, 960, 840, 20, 240, '#6C584C', lw=3)


def bg_quarto(ctx, t):
    wall(ctx, '#BDB2FF', 780)
    window(ctx, 1300, 140, 360, 300, night=False)
    # pôster
    rr(ctx, 260, 140, 260, 340, 6, '#FFD166')
    star(ctx, 390, 260, 70, '#EF476F')
    text(ctx, 'FUTEBOL', 390, 420, 40, '#073B4C')
    # cama
    rr(ctx, 1150, 620, 680, 160, 20, '#118AB2')
    rr(ctx, 1170, 590, 200, 70, 30, '#FFFFFF')
    floor(ctx, 780, '#C9A27E')


def bg_banheiro(ctx, t):
    wall(ctx, '#E0FBFC', 780)
    # azulejos
    ctx.set_source_rgba(0.6, 0.75, 0.8, 0.5)
    ctx.set_line_width(3)
    for x in range(0, W, 90):
        ctx.move_to(x, 0); ctx.line_to(x, 780)
    for y in range(0, 780, 90):
        ctx.move_to(0, y); ctx.line_to(W, y)
    ctx.stroke()
    # espelho (moldura); o reflexo é desenhado pelo render
    rr(ctx, 1010, 120, 460, 600, 30, '#C9ADA7', 8)
    floor(ctx, 780, '#9DB4C0', tiles=True)


MIRROR = (1040, 150, 400, 540)  # área do reflexo


def fg_banheiro(ctx, t):
    # pia
    rr(ctx, 980, 740, 520, 70, 20, '#FFFFFF')
    rect(ctx, 1180, 810, 120, 270, '#FFFFFF')
    rr(ctx, 1210, 700, 60, 50, 10, '#ADB5BD')


def bg_sofa_vo(ctx, t):
    wall(ctx, '#FFE5D9', 780, '#F4ACB7', 560)
    frame_pic(ctx, 300, 160, 240, 180, '#B5E48C')
    frame_pic(ctx, 1380, 150, 200, 240, '#FFCAD4')
    # santo / crucifixo simples e paninho de crochê
    rr(ctx, 860, 160, 200, 200, 100, '#FFFFFF')
    ctx.set_source_rgba(0.9, 0.6, 0.7, 0.6)
    for i in range(12):
        a = i * TAU / 12
        ctx.arc(960 + math.cos(a) * 80, 260 + math.sin(a) * 80, 14, 0, TAU)
        ctx.fill()
    floor(ctx, 780, '#A98467')
    rr(ctx, 420, 560, 1080, 290, 40, '#6D597A')
    rr(ctx, 860, 540, 200, 40, 8, '#FFFFFF')


def fg_sofa_vo(ctx, t):
    rr(ctx, 380, 650, 90, 270, 40, '#6D597A')
    rr(ctx, 1450, 650, 90, 270, 40, '#6D597A')
    rr(ctx, 440, 810, 1040, 110, 30, '#56445D')


def bg_festa(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 760)
    g.add_color_stop_rgb(0, 0.05, 0.06, 0.2)
    g.add_color_stop_rgb(1, 0.25, 0.15, 0.35)
    ctx.rectangle(0, 0, W, 760)
    ctx.set_source(g)
    ctx.fill()
    random.seed(7)
    for i in range(70):
        ctx.arc(random.random() * W, random.random() * 420, 1.5 + random.random() * 2.5, 0, TAU)
        ctx.set_source_rgba(1, 1, 1, 0.5 + 0.5 * math.sin(t * 2 + i))
        ctx.fill()
    ctx.arc(1650, 140, 60, 0, TAU)
    ctx.set_source_rgba(1, 0.97, 0.85, 1)
    ctx.fill()
    # barracas
    for x, name, col in ((120, 'PESCARIA', '#E63946'), (720, 'PIPOCA', '#FFB703'), (1340, 'FANTASIA', '#2A9D8F')):
        rect(ctx, x, 420, 460, 340, '#FFF3E0')
        for i in range(8):
            ctx.move_to(x - 20 + i * 62.5, 420)
            ctx.line_to(x + 11 + i * 62.5, 340)
            ctx.line_to(x + 42 + i * 62.5, 420)
            ctx.close_path()
            fill_stroke(ctx, col if i % 2 else '#FFFFFF', 4)
        rr(ctx, x + 60, 450, 340, 70, 10, col)
        text(ctx, name, x + 230, 503, 46, '#FFFFFF', outline='#1E1E24', lw=8)
        rect(ctx, x + 30, 600, 400, 30, '#8B5E3C')
    floor(ctx, 760, '#7A6A53')
    ctx.set_source_rgba(1, 1, 1, 0.35)
    ctx.set_line_width(8)
    ctx.arc(960, 1250, 420, math.pi * 1.1, math.pi * 1.9)
    ctx.stroke()


def fg_festa(ctx, t):
    # bandeirinhas
    random.seed(3)
    for k, (y0, sag) in enumerate(((60, 120), (150, 90))):
        pts = []
        for i in range(0, 41):
            x = i * W / 40
            y = y0 + sag * math.sin(math.pi * i / 40) + 4 * math.sin(t * 2 + i + k)
            pts.append((x, y))
        ctx.set_source_rgba(0.9, 0.9, 0.9, 0.9)
        ctx.set_line_width(3)
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        ctx.stroke()
        cols = ['#E63946', '#FFB703', '#2A9D8F', '#8338EC', '#06D6A0', '#FF006E']
        for i, (x, y) in enumerate(pts[:-1]):
            ctx.move_to(x, y)
            ctx.line_to(x + 40, y)
            ctx.line_to(x + 40, y + 46)
            ctx.line_to(x + 20, y + 34)
            ctx.line_to(x, y + 46)
            ctx.close_path()
            fill_stroke(ctx, cols[(i + k) % len(cols)], 3)
    # fogueira
    fx = 1780
    for i in range(4):
        ctx.save(); ctx.translate(fx, 1010); ctx.rotate((i - 1.5) * 0.4)
        rr(ctx, -110, -14, 220, 28, 12, '#7F4F24')
        ctx.restore()
    for i, col in enumerate(('#E85D04', '#FAA307', '#FFD60A')):
        s = 1 - i * 0.28
        fl = 1 + 0.08 * math.sin(t * 9 + i)
        ctx.move_to(fx - 90 * s, 1000)
        ctx.curve_to(fx - 100 * s, 900, fx - 20 * s, 860 - 60 * s * fl, fx, 760 + 80 * i - 40 * fl)
        ctx.curve_to(fx + 20 * s, 860 - 60 * s * fl, fx + 100 * s, 900, fx + 90 * s, 1000)
        ctx.close_path()
        setc(ctx, col)
        ctx.fill()


def bg_meiofio(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 760)
    g.add_color_stop_rgb(0, 0.04, 0.05, 0.16)
    g.add_color_stop_rgb(1, 0.18, 0.12, 0.3)
    ctx.rectangle(0, 0, W, 800)
    ctx.set_source(g)
    ctx.fill()
    random.seed(11)
    for i in range(90):
        ctx.arc(random.random() * W, random.random() * 500, 1.2 + random.random() * 2.4, 0, TAU)
        ctx.set_source_rgba(1, 1, 1, 0.4 + 0.6 * abs(math.sin(t * 1.5 + i)))
        ctx.fill()
    # casas ao fundo
    for i, col in enumerate(('#3D348B', '#7678ED', '#5E548E', '#3D348B', '#7678ED')):
        rect(ctx, i * 400 - 40, 470, 380, 300, col)
        window(ctx, i * 400 + 60, 540, 110, 90, night=True)
        ctx.rectangle(i * 400 + 60, 540, 110, 90)
        ctx.set_source_rgba(1, 0.85, 0.4, 0.55)
        ctx.fill()
    # poste
    rect(ctx, 1600, 200, 26, 600, '#4A4E69')
    ctx.arc(1613, 200, 40, 0, TAU)
    ctx.set_source_rgba(1, 0.92, 0.6, 1)
    ctx.fill()
    g2 = cairo.RadialGradient(1613, 260, 10, 1613, 600, 500)
    g2.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.35)
    g2.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g2)
    ctx.fill()
    # calçada e rua
    rect(ctx, 0, 770, W, 120, '#8D99AE')
    rect(ctx, 0, 870, W, 30, '#EDF2F4')
    rect(ctx, 0, 900, W, 180, '#2B2D42', outline=False)
    ctx.set_source_rgba(1, 0.85, 0.2, 0.9)
    for i in range(0, W, 220):
        ctx.rectangle(i, 1000, 120, 14)
    ctx.fill()


def bg_ciencia(ctx, t):
    g = cairo.LinearGradient(0, 0, W, H)
    g.add_color_stop_rgb(0, 0.12, 0.16, 0.32)
    g.add_color_stop_rgb(1, 0.22, 0.1, 0.35)
    ctx.rectangle(0, 0, W, H)
    ctx.set_source(g)
    ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.set_line_width(2)
    for x in range(0, W, 60):
        ctx.move_to(x, 0); ctx.line_to(x, H)
    for y in range(0, H, 60):
        ctx.move_to(0, y); ctx.line_to(W, y)
    ctx.stroke()
    floor(ctx, 860, '#2B2D42')


def bg_plain(col1, col2):
    def f(ctx, t):
        g = cairo.LinearGradient(0, 0, 0, H)
        a, b = hexc(col1), hexc(col2)
        g.add_color_stop_rgb(0, a[0], a[1], a[2])
        g.add_color_stop_rgb(1, b[0], b[1], b[2])
        ctx.rectangle(0, 0, W, H)
        ctx.set_source(g)
        ctx.fill()
    return f


def bg_feira(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 700)
    g.add_color_stop_rgb(0, 0.52, 0.8, 0.98)
    g.add_color_stop_rgb(1, 0.85, 0.94, 1)
    ctx.rectangle(0, 0, W, 780); ctx.set_source(g); ctx.fill()
    for x, y, r in ((260, 120, 46), (320, 100, 60), (390, 125, 44), (1500, 90, 40), (1560, 80, 52)):
        ctx.arc(x, y, r, 0, TAU); ctx.set_source_rgba(1, 1, 1, 0.95); ctx.fill()
    # prédios ao fundo
    for i, col in enumerate(('#F4A261', '#E9C46A', '#E76F51', '#2A9D8F', '#F4A261', '#E9C46A')):
        rect(ctx, i * 330 - 20, 220 + (i % 2) * 60, 320, 560, col)
        for k in range(3):
            window(ctx, i * 330 + 50 + k * 90, 300 + (i % 2) * 60, 50, 60)
    floor(ctx, 780, '#9C9C9C')
    # barracas
    for x, col, prod in ((80, '#E63946', '#E63946'), (720, '#2A9D8F', '#F4A261'), (1360, '#FFB703', '#8AC926')):
        rect(ctx, x + 20, 430, 14, 360, '#6C757D', lw=3)
        rect(ctx, x + 446, 430, 14, 360, '#6C757D', lw=3)
        ctx.move_to(x - 20, 470); ctx.line_to(x + 240, 380); ctx.line_to(x + 500, 470); ctx.close_path()
        fill_stroke(ctx, col)
        for k in range(6):
            ctx.move_to(x - 20 + k * 87, 470); ctx.line_to(x + 23 + k * 87, 500); ctx.line_to(x + 67 + k * 87, 470); ctx.close_path()
            fill_stroke(ctx, '#FFFFFF' if k % 2 else col, 3)
        rr(ctx, x, 640, 480, 70, 8, '#8B5E3C')
        random.seed(x)
        for k in range(14):
            ctx.arc(x + 30 + k * 32 + random.random() * 6, 625 - (k % 2) * 18, 20, 0, TAU)
            fill_stroke(ctx, prod, 3)
    rr(ctx, 1500, 540, 200, 70, 8, '#FFFFFF')
    text(ctx, 'R$ 5', 1600, 592, 46, '#C1121F')


def bg_quadra(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, 600)
    g.add_color_stop_rgb(0, 0.5, 0.78, 0.98)
    g.add_color_stop_rgb(1, 0.85, 0.94, 1)
    ctx.rectangle(0, 0, W, 700); ctx.set_source(g); ctx.fill()
    # alambrado
    ctx.set_source_rgba(0.35, 0.4, 0.45, 0.55); ctx.set_line_width(3)
    for i in range(-40, 80):
        ctx.move_to(i * 40, 160); ctx.line_to(i * 40 + 540, 700)
        ctx.move_to(i * 40, 160); ctx.line_to(i * 40 - 540, 700)
    ctx.stroke()
    rect(ctx, 0, 150, W, 14, '#6C757D', lw=3)
    rect(ctx, 0, 680, W, 780 - 680, '#5C677D')
    floor(ctx, 760, '#4D908E')
    ctx.set_source_rgba(1, 1, 1, 0.85); ctx.set_line_width(8)
    ctx.move_to(0, 960); ctx.line_to(W, 960); ctx.stroke()
    ctx.arc(1000, 1100, 260, math.pi, TAU); ctx.stroke()
    # gol à direita
    ctx.set_source_rgba(1, 1, 1, 1); ctx.set_line_width(16)
    ctx.move_to(1560, 1000); ctx.line_to(1560, 640); ctx.line_to(1880, 640); ctx.line_to(1880, 1000); ctx.stroke()
    ctx.set_source_rgba(1, 1, 1, 0.35); ctx.set_line_width(2)
    for k in range(1600, 1880, 24):
        ctx.move_to(k, 640); ctx.line_to(k, 1000)
    for k in range(660, 1000, 24):
        ctx.move_to(1560, k); ctx.line_to(1880, k)
    ctx.stroke()


def bg_salao(ctx, t):
    wall(ctx, '#FFF1E6', 780, '#E8C2CA', 560)
    # faixa
    rr(ctx, 460, 70, 1000, 120, 16, '#C9184A')
    text(ctx, '80 ANOS DA VÓ CIDA', 960, 152, 66, '#FFFFFF', outline='#590D22', lw=10)
    # balões dourados e rosa
    for k, (x, y) in enumerate(((150, 160), (260, 120), (1660, 150), (1780, 110), (360, 230), (1560, 230))):
        bob = 8 * math.sin(t * 1.5 + k)
        ctx.set_source_rgba(0.4, 0.4, 0.4, 0.8); ctx.set_line_width(2)
        ctx.move_to(x, y + 70 + bob); ctx.line_to(x + 10, y + 260); ctx.stroke()
        ctx.save(); ctx.translate(x, y + bob); ctx.scale(0.85, 1.0); ctx.arc(0, 0, 70, 0, TAU); ctx.restore()
        fill_stroke(ctx, '#F4C430' if k % 2 == 0 else '#FF8FAB', 4)
    floor(ctx, 780, '#C9A27E', tiles=True)
    # mesa com bolo
    rr(ctx, 1440, 640, 420, 140, 10, '#FFFFFF')
    ctx.save(); ctx.translate(1650, 640); ctx.scale(1, 0.3); ctx.arc(0, 0, 110, 0, TAU); ctx.restore()
    fill_stroke(ctx, '#FFFFFF', 4)
    rect(ctx, 1570, 520, 160, 120, '#FFB5C2')
    text(ctx, '80', 1650, 610, 70, '#C9184A')


def bg_quarto_noite(ctx, t):
    wall(ctx, '#3C3A6B', 780)
    window(ctx, 1300, 140, 360, 300, night=True)
    rr(ctx, 260, 140, 260, 340, 6, '#5A5891')
    star(ctx, 390, 260, 70, '#8D8BC4')
    rr(ctx, 1150, 620, 680, 160, 20, '#2B2D5E')
    rr(ctx, 1170, 590, 200, 70, 30, '#8D8BC4')
    floor(ctx, 780, '#2E2C52')
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.05, 0.05, 0.2, 0.25); ctx.fill()


def bg_onibus(ctx, t):
    wall(ctx, '#DDE5ED', 780)
    # janelas com paisagem passando
    for k in range(4):
        x = 120 + k * 450
        rr(ctx, x - 10, 130, 380, 300, 16, '#ADB5BD')
        ctx.save(); rrect(ctx, x, 140, 360, 280, 12); ctx.clip()
        g = cairo.LinearGradient(0, 140, 0, 420)
        g.add_color_stop_rgb(0, 0.95, 0.75, 0.55); g.add_color_stop_rgb(1, 0.98, 0.9, 0.75)
        ctx.rectangle(x, 140, 360, 280); ctx.set_source(g); ctx.fill()
        off = (t * 400) % 300
        for b in range(-1, 4):
            bx = x - off + b * 150
            ctx.rectangle(bx, 260 + (b % 2) * 30, 110, 200); ctx.set_source_rgba(0.45, 0.4, 0.55, 0.9); ctx.fill()
        ctx.restore()
    # barra de apoio
    ctx.set_source_rgba(0.75, 0.76, 0.78, 1); ctx.set_line_width(14)
    ctx.move_to(0, 90); ctx.line_to(W, 90); ctx.stroke()
    for k in range(6):
        ctx.arc(150 + k * 330, 130, 26, 0, TAU); ctx.set_source_rgba(0.95, 0.75, 0.2, 1); ctx.set_line_width(8); ctx.stroke()
    floor(ctx, 780, '#495057')
    # bancos
    for x in (420, 1150):
        rr(ctx, x - 230, 560, 460, 260, 30, '#1D3557')


def fg_onibus(ctx, t):
    for x in (420, 1150):
        rr(ctx, x - 250, 800, 500, 90, 20, '#274472')


BG = {
    'jantar': (bg_jantar, fg_jantar),
    'sala': (bg_sala, fg_sala),
    'portao': (bg_portao, None),
    'classe': (bg_classe, fg_classe),
    'patio': (bg_patio, None),
    'corredor': (bg_corredor, None),
    'biblioteca': (bg_biblioteca, fg_biblioteca),
    'quarto': (bg_quarto, None),
    'banheiro': (bg_banheiro, fg_banheiro),
    'sofa_vo': (bg_sofa_vo, fg_sofa_vo),
    'festa': (bg_festa, fg_festa),
    'meiofio': (bg_meiofio, None),
    'ciencia': (bg_ciencia, None),
    'caderno': (bg_plain('#3D405B', '#22223B'), None),
    'ranking': (bg_plain('#1B1B3A', '#3A0CA3'), None),
    'placar': (bg_plain('#10002B', '#3C096C'), None),
    'whatsapp': (bg_plain('#0B3D2E', '#081C15'), None),
    'final': (bg_plain('#3A0CA3', '#7209B7'), None),
    'feira': (bg_feira, None),
    'onibus': (bg_onibus, fg_onibus),
    'quadra': (bg_quadra, None),
    'salao': (bg_salao, None),
    'quarto_noite': (bg_quarto_noite, None),
    'desenho': (bg_plain('#6D4C41', '#4E342E'), None),
    'lista': (bg_plain('#1B1B3A', '#3A0CA3'), None),
}

# slots: (x, y_pés, escala)
SLOTS = {
    'jantar': dict(m1=(380, 850, 0.8), m2=(680, 840, 0.8), m3=(960, 850, 0.8), m4=(1250, 850, 0.8), m5=(1560, 850, 0.84)),
    'sala': dict(a=(560, 875, 0.9), b=(960, 875, 0.9)),
    'portao': dict(a=(1300, 1000, 0.95), b=(700, 1000, 0.95)),
    'classe': dict(prof=(330, 980, 0.85), d1=(700, 930, 0.8), d2=(1100, 930, 0.8), d3=(1500, 930, 0.8)),
    'patio': dict(a=(620, 1010, 0.95), b=(1250, 1010, 0.95), c=(960, 1010, 0.95), d=(330, 1010, 0.9)),
    'corredor': dict(a=(700, 1000, 0.95), b=(1220, 1000, 0.95)),
    'biblioteca': dict(a=(700, 930, 0.85), b=(1300, 1010, 0.95)),
    'quarto': dict(a=(760, 1010, 1.0)),
    'banheiro': dict(a=(650, 1050, 1.05)),
    'sofa_vo': dict(a=(760, 875, 0.9), b=(1160, 875, 0.9)),
    'festa': dict(f1=(380, 1010, 0.85), f2=(1240, 1010, 0.9), c=(840, 1010, 0.9), f4=(1460, 1010, 0.85)),
    'meiofio': dict(a=(760, 960, 0.9), b=(1130, 960, 0.9)),
    'ciencia': dict(a=(620, 1000, 0.9), b=(1300, 1000, 0.9)),
    'final': dict(c=(560, 1020, 1.0)),
    'feira': dict(a=(560, 1010, 0.95), b=(980, 1010, 0.95), c=(1560, 1010, 0.95)),
    'quadra': dict(a=(500, 1010, 0.9), b=(1000, 1010, 0.95), gol=(1720, 1000, 0.85), gol2=(1640, 980, 0.85)),
    'salao': dict(a=(330, 1010, 0.9), b=(700, 1010, 0.9), c=(1060, 1010, 0.95), d=(1400, 1010, 0.8), e=(1700, 1010, 0.9)),
    'quarto_noite': dict(a=(760, 1010, 1.0)),
    'onibus': dict(a=(300, 870, 0.85), b=(1030, 870, 0.9), c=(1290, 870, 0.9)),
}


# ======================================================================
# MANUAL DA MADRUGADA — cenários escuros em traço claro
# ======================================================================
LINE = (0.60, 0.60, 0.64, 1)
DARK = '#141416'
DARK2 = '#1C1C1F'
DARK3 = '#242428'


def lr(ctx, x, y, w, h, fill=DARK2, lw=4, r=0):
    if r:
        rrect(ctx, x, y, w, h, r)
    else:
        ctx.rectangle(x, y, w, h)
    setc(ctx, fill)
    ctx.fill_preserve()
    ctx.set_source_rgba(*LINE)
    ctx.set_line_width(lw)
    ctx.stroke()


def amber(ctx, x, y, r=120, a=0.35, t=0, flick=False):
    k = 1.0
    if flick:
        k = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 23) * math.sin(t * 7.3))
    g = cairo.RadialGradient(x, y, 4, x, y, r)
    g.add_color_stop_rgba(0, 1, 0.72, 0.3, a * k)
    g.add_color_stop_rgba(1, 1, 0.72, 0.3, 0)
    ctx.rectangle(x - r, y - r, 2 * r, 2 * r)
    ctx.set_source(g)
    ctx.fill()


def mm_room(ctx, wall_c=DARK, floor_c=DARK3, fy=800):
    ctx.rectangle(0, 0, W, H); setc(ctx, wall_c); ctx.fill()
    ctx.rectangle(0, fy, W, H - fy); setc(ctx, floor_c); ctx.fill()
    ctx.set_source_rgba(*LINE); ctx.set_line_width(5)
    ctx.move_to(0, fy); ctx.line_to(W, fy); ctx.stroke()


def door(ctx, x, y, w, h, open_frac=0.0, light=False, t=0):
    lr(ctx, x, y, w, h, fill='#0B0B0C')
    if light:
        g = cairo.LinearGradient(0, y + h - 14, 0, y + h + 60)
        g.add_color_stop_rgba(0, 1, 0.75, 0.35, 0.55)
        g.add_color_stop_rgba(1, 1, 0.75, 0.35, 0)
        ctx.rectangle(x - 20, y + h - 6, w + 40, 70); ctx.set_source(g); ctx.fill()
    if open_frac < 0.98:
        lw_ = w * (1 - open_frac)
        lr(ctx, x, y, lw_, h, fill=DARK2)
        ctx.arc(x + lw_ - 22, y + h * 0.55, 7, 0, TAU)
        ctx.set_source_rgba(*LINE); ctx.fill()


def moon_window(ctx, x, y, w, h):
    lr(ctx, x, y, w, h, fill='#0F1218')
    ctx.arc(x + w * 0.68, y + h * 0.32, 26, 0, TAU)
    ctx.set_source_rgba(0.85, 0.86, 0.9, 0.9); ctx.fill()
    g = cairo.RadialGradient(x + w * 0.68, y + h * 0.32, 10, x + w * 0.68, y + h * 0.32, 150)
    g.add_color_stop_rgba(0, 0.8, 0.85, 1, 0.12); g.add_color_stop_rgba(1, 0.8, 0.85, 1, 0)
    ctx.rectangle(x, y, w, h); ctx.set_source(g); ctx.fill()
    ctx.set_source_rgba(*LINE); ctx.set_line_width(4)
    ctx.move_to(x + w / 2, y); ctx.line_to(x + w / 2, y + h)
    ctx.move_to(x, y + h / 2); ctx.line_to(x + w, y + h / 2); ctx.stroke()


def bed(ctx, x, y, w, made=True):
    lr(ctx, x, y - 160, 40, 220, r=6)                    # cabeceira
    lr(ctx, x, y - 30, w, 90, r=10)                       # colchão
    lr(ctx, x + 50, y - 70, 180, 50, fill='#2A2A2E', r=22)  # travesseiro
    if made:
        lr(ctx, x + 250, y - 40, w - 250, 70, fill='#26262A', r=12)
    else:
        ctx.move_to(x + 250, y - 40); ctx.curve_to(x + 400, y - 90, x + 520, y - 10, x + w, y - 50)
        ctx.line_to(x + w, y + 30); ctx.line_to(x + 250, y + 30); ctx.close_path()
        setc(ctx, '#26262A'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    lr(ctx, x, y + 60, 26, 60); lr(ctx, x + w - 26, y + 60, 26, 60)


def bg_mm_quarto(ctx, t):
    mm_room(ctx)
    moon_window(ctx, 220, 160, 300, 280)
    door(ctx, 760, 260, 230, 540)
    bed(ctx, 1180, 780, 640, made=False)
    lr(ctx, 1060, 640, 100, 160, r=6)                     # criado-mudo
    lr(ctx, 1085, 560, 50, 80, fill='#2C2C30')            # abajur
    ctx.move_to(1070, 560); ctx.line_to(1150, 560); ctx.line_to(1130, 520); ctx.line_to(1090, 520); ctx.close_path()
    setc(ctx, '#3A3A40'); ctx.fill()


def bg_mm_corredor(ctx, t):
    mm_room(ctx, fy=820)
    for k, x in enumerate((240, 820, 1400)):
        door(ctx, x, 280, 240, 540)
    for x in (630, 1210):
        ctx.arc(x, 380, 18, 0, TAU); ctx.set_source_rgba(1, 0.75, 0.35, 0.8); ctx.fill()
        amber(ctx, x, 380, 110, 0.45, t)


def bg_mm_corredor_luz(ctx, t):
    """corredor com luz acesa por baixo da porta do meio (quarto da mãe)"""
    mm_room(ctx, fy=820)
    for k, x in enumerate((240, 820, 1400)):
        door(ctx, x, 280, 240, 540, light=(k == 1), t=t)
    for x in (630, 1210):
        ctx.arc(x, 380, 18, 0, TAU); ctx.set_source_rgba(1, 0.75, 0.35, 0.8); ctx.fill()
        amber(ctx, x, 380, 110, 0.45, t)


def bg_mm_quarto_mae(ctx, t):
    mm_room(ctx, wall_c='#121214')
    moon_window(ctx, 1450, 160, 280, 260)
    bed(ctx, 260, 780, 760, made=True)
    lr(ctx, 1100, 480, 260, 320, r=6)                    # cômoda
    for k in range(3):
        lr(ctx, 1120, 500 + k * 100, 220, 80, fill=DARK3)
    lr(ctx, 1150, 330, 160, 130, fill='#101012')          # porta-retrato
    door(ctx, 1500, 460, 180, 340, open_frac=0.6)


def bg_mm_sala(ctx, t):
    mm_room(ctx)
    moon_window(ctx, 140, 170, 280, 250)
    lr(ctx, 520, 600, 640, 140, r=30)                    # sofá
    lr(ctx, 520, 520, 640, 110, r=30)
    lr(ctx, 1260, 380, 360, 220, fill='#08080A')         # TV desligada
    lr(ctx, 1240, 600, 400, 200)
    door(ctx, 1700, 260, 200, 540)


def bg_mm_sala_manha(ctx, t):
    bg_mm_sala(ctx, t)
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.12); ctx.fill()


def bg_mm_cozinha(ctx, t):
    mm_room(ctx)
    lr(ctx, 120, 520, 1000, 280)                          # balcão
    for k in range(4):
        lr(ctx, 140 + k * 245, 560, 225, 220, fill=DARK3)
    lr(ctx, 120, 200, 600, 200)                           # armário alto
    moon_window(ctx, 780, 200, 280, 220)
    lr(ctx, 1260, 260, 300, 540, r=14)                    # geladeira
    ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.move_to(1260, 460); ctx.line_to(1560, 460); ctx.stroke()
    lr(ctx, 1640, 520, 160, 280)                          # fogão


def bg_mm_porta(ctx, t):
    mm_room(ctx)
    lr(ctx, 700, 140, 520, 660, fill='#0E0E10')           # porta de entrada grande
    ctx.arc(1160, 470, 14, 0, TAU); ctx.set_source_rgba(*LINE); ctx.fill()
    lr(ctx, 1130, 500, 60, 90, fill='#2A2A2E', r=8)       # fechadura
    ctx.arc(960, 300, 12, 0, TAU); ctx.set_source_rgba(0.75, 0.75, 0.8, 1); ctx.fill()   # olho mágico
    lr(ctx, 300, 240, 260, 360, fill='#0F1218')           # janela lateral
    lr(ctx, 1380, 600, 320, 200)                          # aparador


def bg_mm_preto(ctx, t):
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.03, 0.03, 0.035, 1); ctx.fill()



# ---------------------------------------------------------------- casa da vó (noite 02)
def wood_window(ctx, x, y, w, h, open_=True):
    """janela de madeira de casa do interior: duas folhas, a da direita entreaberta mostrando a lua"""
    lr(ctx, x - 14, y - 14, w + 28, h + 28, fill=DARK3)
    moon_window(ctx, x, y, w, h)
    if open_:
        lr(ctx, x, y, w * 0.5, h, fill='#1E1A17')                     # folha esquerda fechada
        for k in range(1, 5):
            ctx.move_to(x + 10, y + k * h / 5); ctx.line_to(x + w * 0.5 - 10, y + k * h / 5)
        ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.stroke()
        ctx.move_to(x + w, y); ctx.line_to(x + w + 70, y + 26); ctx.line_to(x + w + 70, y + h - 26); ctx.line_to(x + w, y + h)
        ctx.close_path(); setc(ctx, '#1E1A17'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()


def oratorio(ctx, x, y, t, lit=True):
    """oratório de madeira numa prateleira, com uma velinha"""
    lr(ctx, x - 90, y + 150, 180, 16, fill=DARK3)                      # prateleira
    ctx.move_to(x - 60, y + 150); ctx.line_to(x - 60, y + 20); ctx.line_to(x, y - 30); ctx.line_to(x + 60, y + 20)
    ctx.line_to(x + 60, y + 150); ctx.close_path()
    setc(ctx, '#1A1714'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    lr(ctx, x - 40, y + 40, 80, 100, fill='#0C0B0A', r=30)             # nicho
    lr(ctx, x + 70, y + 110, 18, 40, fill='#D9D4C8')                   # vela
    if lit:
        fl = 0.85 + 0.15 * math.sin(t * 17) * math.sin(t * 5.1)
        ctx.save(); ctx.translate(x + 79, y + 98); ctx.scale(0.55, 1.0 * fl)
        ctx.arc(0, 0, 13, 0, TAU); ctx.restore(); ctx.set_source_rgba(1, 0.78, 0.35, 0.95); ctx.fill()
        amber(ctx, x + 79, y + 98, 260, 0.30, t, flick=True)
    else:
        ctx.set_source_rgba(0.6, 0.6, 0.64, 0.5); ctx.set_line_width(3)
        ctx.move_to(x + 79, y + 104); ctx.curve_to(x + 70, y + 80, x + 95, y + 60, x + 82, y + 30); ctx.stroke()


def arruda_copo(ctx, x, y):
    lr(ctx, x - 22, y - 60, 44, 60, fill='#1A1D22', r=6)               # copo d'água
    ctx.set_source_rgba(0.55, 0.62, 0.55, 1); ctx.set_line_width(4)
    for a in (-0.35, 0.0, 0.3):
        ctx.move_to(x, y - 40); ctx.line_to(x + math.sin(a) * 70, y - 40 - math.cos(a) * 70); ctx.stroke()
        for k in (0.45, 0.75, 1.0):
            ctx.arc(x + math.sin(a) * 70 * k, y - 40 - math.cos(a) * 70 * k, 7, 0, TAU); ctx.fill()


def bg_mm_quarto_vo(ctx, t, lit=True, manha=False):
    mm_room(ctx, wall_c='#151413')
    wood_window(ctx, 200, 170, 280, 260)
    door(ctx, 760, 260, 230, 540)
    oratorio(ctx, 1300, 300, t, lit=lit)
    bed(ctx, 1180, 780, 640, made=False)
    lr(ctx, 1060, 640, 100, 160, r=6)                                  # criado-mudo
    arruda_copo(ctx, 1110, 640)
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.13); ctx.fill()
    elif not lit:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, 0.45); ctx.fill()


def ramo_seco(ctx, x, y):
    """raminho de arruda seco e escuro, amarrado com linha vermelha"""
    for col, lw, rr_ in ((LINE, 11, 11), ((0.07, 0.065, 0.06, 1), 5, 7)):
        ctx.set_source_rgba(*col); ctx.set_line_width(lw)
        for a in (-0.5, -0.15, 0.2):
            ctx.move_to(x, y); ctx.line_to(x + math.cos(a) * 110, y + math.sin(a) * 40); ctx.stroke()
            for k in (0.5, 0.75, 1.0):
                ctx.arc(x + math.cos(a) * 110 * k, y + math.sin(a) * 40 * k - 6, rr_, 0, TAU); ctx.fill()
    ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.set_line_width(6)
    ctx.move_to(x + 18, y - 16); ctx.line_to(x + 22, y + 14); ctx.stroke()
    ctx.move_to(x + 20, y + 10); ctx.curve_to(x - 10, y + 30, x - 30, y + 20, x - 40, y + 40); ctx.stroke()


def big_bed(ctx):
    lr(ctx, 600, 400, 50, 420, r=8)                                    # cabeceira de madeira
    for k in range(3):
        lr(ctx, 612, 440 + k * 120, 26, 90, fill=DARK3, r=6)
    lr(ctx, 640, 640, 1140, 130, r=14)                                 # colchão
    lr(ctx, 690, 575, 300, 85, fill='#2C2C30', r=40)                   # travesseiro
    lr(ctx, 660, 770, 34, 110); lr(ctx, 1730, 770, 34, 110)            # pés da cama


def bg_mm_cama(ctx, t, lit=True):
    mm_room(ctx, wall_c='#151413', fy=880)
    wood_window(ctx, 900, 120, 260, 230)
    oratorio(ctx, 1560, 170, t, lit=lit)
    big_bed(ctx)


def fg_mm_cama(ctx, t, lit=True):
    # colcha de retalhos cobrindo o corpo (o protagonista deitado tem os pés em ~1250)
    ctx.move_to(975, 760); ctx.line_to(975, 600)
    ctx.curve_to(1020, 500, 1200, 505, 1330, 560)
    ctx.curve_to(1450, 600, 1600, 590, 1760, 610)
    ctx.line_to(1790, 800); ctx.line_to(990, 800); ctx.close_path()
    setc(ctx, '#2A2724'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(5); ctx.stroke()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.35); ctx.set_line_width(3)
    for x in range(1080, 1760, 140):                                   # costuras dos retalhos
        ctx.move_to(x, 600); ctx.line_to(x - 20, 795); ctx.stroke()
    ctx.move_to(985, 700); ctx.curve_to(1200, 690, 1500, 710, 1780, 700); ctx.stroke()
    if not lit:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, 0.45); ctx.fill()


# ---------------------------------------------------------------- quintal e portão (noite 03)
def muro_portao(ctx, t, manha=False):
    """céu, casas do outro lado da rua, poste, muro com cacos de vidro e portão de grade (as grades vão no fg)"""
    g = cairo.LinearGradient(0, 0, 0, 470)
    if manha:
        g.add_color_stop_rgba(0, 0.16, 0.2, 0.3, 1); g.add_color_stop_rgba(1, 0.42, 0.42, 0.48, 1)
    else:
        g.add_color_stop_rgba(0, 0.03, 0.035, 0.05, 1); g.add_color_stop_rgba(1, 0.07, 0.075, 0.09, 1)
    ctx.rectangle(0, 0, W, 480); ctx.set_source(g); ctx.fill()
    if not manha:
        ctx.arc(330, 130, 30, 0, TAU); ctx.set_source_rgba(0.85, 0.86, 0.9, 0.85); ctx.fill()
    # casas do outro lado da rua (silhuetas com telhado)
    for x, w, h in ((-20, 360, 170), (380, 300, 210), (1240, 330, 190), (1600, 360, 160)):
        y = 470 - h
        ctx.move_to(x, y + 40); ctx.line_to(x + w / 2, y - 10); ctx.line_to(x + w, y + 40); ctx.line_to(x + w, 470); ctx.line_to(x, 470); ctx.close_path()
        setc(ctx, '#101012'); ctx.fill_preserve(); ctx.set_source_rgba(0.6, 0.6, 0.64, 0.5); ctx.set_line_width(3); ctx.stroke()
    lr(ctx, 1290, 360, 70, 60, fill='#0A0A0C')                                # janela da vizinha da frente
    # poste com luz âmbar
    lr(ctx, 1505, 120, 18, 360, fill=DARK3)
    lr(ctx, 1460, 110, 110, 22, fill=DARK3, r=8)
    ctx.arc(1480, 140, 13, 0, TAU); ctx.set_source_rgba(1, 0.75, 0.35, 0.95 if not manha else 0.3); ctx.fill()
    if not manha:
        amber(ctx, 1480, 150, 330, 0.32, t)
    # chão do quintal (cimento)
    ctx.rectangle(0, 820, W, H - 820); setc(ctx, DARK3); ctx.fill()
    # muro
    for x0, x1 in ((0, 760), (1160, W)):
        lr(ctx, x0 - 6, 470, x1 - x0 + 12, 350, fill='#19191C')
        ctx.set_source_rgba(0.6, 0.6, 0.64, 0.22); ctx.set_line_width(2)
        for yy in range(530, 820, 60):
            ctx.move_to(x0, yy); ctx.line_to(x1, yy)
        ctx.stroke()
        # cacos de vidro em cima do muro
        random.seed(x0 + 3)
        x = x0 + 10
        while x < x1 - 20:
            hh = 14 + random.random() * 22
            ctx.move_to(x, 470); ctx.line_to(x + 7 + random.random() * 6, 470 - hh); ctx.line_to(x + 18, 470); ctx.close_path()
            ctx.set_source_rgba(0.62, 0.68, 0.66, 0.85); ctx.fill()
            x += 26 + random.random() * 22
    # vão do portão: rua escura
    ctx.rectangle(760, 470, 400, 350); setc(ctx, '#0B0B0D'); ctx.fill()
    ctx.set_source_rgba(*LINE); ctx.set_line_width(5); ctx.move_to(0, 820); ctx.line_to(W, 820); ctx.stroke()
    # casinha da Paçoca
    ctx.move_to(170, 760); ctx.line_to(290, 660); ctx.line_to(410, 760); ctx.close_path()
    setc(ctx, '#232326'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    lr(ctx, 190, 760, 200, 140, fill='#1E1E21')
    lr(ctx, 250, 800, 80, 100, fill='#060607', r=30)
    # vaso de espada-de-são-jorge
    lr(ctx, 1640, 840, 90, 80, fill='#202024', r=6)
    ctx.set_source_rgba(0.5, 0.56, 0.5, 1); ctx.set_line_width(7)
    for a in (-0.3, -0.1, 0.12, 0.3):
        ctx.move_to(1685, 840); ctx.line_to(1685 + math.sin(a) * 150, 840 - math.cos(a) * 150); ctx.stroke()
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.12); ctx.fill()


def grade_portao(ctx, t, manha=False):
    """grades do portão por cima de quem está atrás dele, com corrente e cadeado"""
    ctx.set_source_rgba(0.68, 0.68, 0.72, 1)
    ctx.set_line_width(9)
    ctx.rectangle(760, 440, 400, 380); ctx.stroke()
    ctx.set_line_width(7)
    for x in range(800, 1160, 40):
        ctx.move_to(x, 440); ctx.line_to(x, 820)
    ctx.move_to(760, 560); ctx.line_to(1160, 560)
    ctx.move_to(760, 700); ctx.line_to(1160, 700)
    ctx.stroke()
    for x in range(800, 1160, 40):                                           # pontas de lança
        ctx.move_to(x - 9, 446); ctx.line_to(x, 418); ctx.line_to(x + 9, 446); ctx.close_path(); ctx.fill()
    ctx.move_to(960, 440); ctx.line_to(960, 820); ctx.set_line_width(10); ctx.stroke()   # junção das folhas
    # corrente + cadeado
    ctx.set_line_width(5)
    for k in range(6):
        ctx.save(); ctx.translate(925 + k * 14, 640 + (k % 2) * 4); ctx.scale(1.0, 0.6)
        ctx.arc(0, 0, 9, 0, TAU); ctx.restore(); ctx.stroke()
    lr(ctx, 948, 652, 40, 46, fill='#4A4A50', r=6)
    ctx.arc(968, 652, 13, math.pi, 0); ctx.set_line_width(5); ctx.set_source_rgba(0.68, 0.68, 0.72, 1); ctx.stroke()


def bg_mm_quintal(ctx, t):
    muro_portao(ctx, t)


def bg_mm_quintal_manha(ctx, t):
    muro_portao(ctx, t, manha=True)


def bg_mm_cortina(ctx, t):
    """de dentro da sala: janela da frente grande, com o quintal e o portão lá fora (o fg põe as cortinas)"""
    ctx.rectangle(0, 0, W, H); setc(ctx, DARK); ctx.fill()
    ctx.save()
    ctx.rectangle(520, 140, 880, 620); ctx.clip()
    ctx.translate(520, 140); ctx.scale(880 / W, 880 / W); ctx.translate(0, -150)
    muro_portao(ctx, t)
    grade_portao(ctx, t)
    ctx.restore()
    ctx.rectangle(0, 860, W, H - 860); setc(ctx, DARK3); ctx.fill()
    ctx.set_source_rgba(*LINE); ctx.set_line_width(5); ctx.move_to(0, 860); ctx.line_to(W, 860); ctx.stroke()
    lr(ctx, 500, 120, 920, 660, fill=(0, 0, 0, 0), lw=10)                   # batente
    ctx.set_source_rgba(*LINE); ctx.set_line_width(6)
    ctx.move_to(960, 140); ctx.line_to(960, 760); ctx.stroke()
    lr(ctx, 470, 770, 980, 30, fill=DARK3)                                   # parapeito
    lr(ctx, 1560, 620, 260, 240, r=6)                                        # aparador
    lr(ctx, 1610, 520, 70, 100, fill='#2C2C30', r=8)                         # telefone fixo / rádio


def fg_mm_cortina(ctx, t):
    sw = 8 * math.sin(t * 0.7)
    for x0, side in ((430, 1), (1490, -1)):
        ctx.move_to(x0 - side * 30, 90)
        ctx.line_to(x0 + side * 150 + sw, 90)
        ctx.curve_to(x0 + side * 120 + sw, 400, x0 + side * 170 + sw, 650, x0 + side * 130 + sw, 840)
        ctx.line_to(x0 - side * 30, 840); ctx.close_path()
        setc(ctx, '#1F1D22'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
        ctx.set_source_rgba(0.6, 0.6, 0.64, 0.3); ctx.set_line_width(3)
        for k in (40, 85):
            ctx.move_to(x0 + side * k, 100); ctx.curve_to(x0 + side * (k - 10), 400, x0 + side * (k + 20), 650, x0 + side * k, 830); ctx.stroke()
    lr(ctx, 360, 78, 1200, 18, fill=DARK3, r=8)                               # varão


BG = {
    'quarto': (bg_mm_quarto, None),
    'corredor': (bg_mm_corredor, None),
    'corredor_luz': (bg_mm_corredor_luz, None),
    'quarto_mae': (bg_mm_quarto_mae, None),
    'sala': (bg_mm_sala, None),
    'sala_manha': (bg_mm_sala_manha, None),
    'cozinha': (bg_mm_cozinha, None),
    'porta': (bg_mm_porta, None),
    'preto': (bg_mm_preto, None),
    'quarto_vo': (bg_mm_quarto_vo, None),
    'quarto_vo_escuro': (lambda c, t: bg_mm_quarto_vo(c, t, lit=False), None),
    'quarto_vo_manha': (lambda c, t: bg_mm_quarto_vo(c, t, manha=True), None),
    'quarto_vo_ramo': (lambda c, t: (bg_mm_quarto_vo(c, t, manha=True), ramo_seco(c, 1260, 735)), None),
    'cama': (bg_mm_cama, fg_mm_cama),
    'cama_escuro': (lambda c, t: bg_mm_cama(c, t, lit=False), lambda c, t: fg_mm_cama(c, t, lit=False)),
    'quintal': (bg_mm_quintal, grade_portao),
    'quintal_manha': (bg_mm_quintal_manha, lambda c, t: grade_portao(c, t, manha=True)),
    'cortina': (bg_mm_cortina, fg_mm_cortina),
}

SLOTS = {
    'quarto': dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'corredor': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), p3=(1520, 1000, 0.9), meio=(650, 1010, 0.95)),
    'corredor_luz': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), p3=(1520, 1000, 0.9), meio=(650, 1010, 0.95)),
    'quarto_mae': dict(cama=(650, 980, 0.95), porta=(1590, 980, 0.85), centro=(1150, 1000, 0.95)),
    'sala': dict(sofa=(840, 860, 0.9), sofa2=(1040, 860, 0.9), porta=(1800, 990, 0.9), centro=(420, 1000, 0.95)),
    'sala_manha': dict(sofa=(840, 860, 0.9), sofa2=(1040, 860, 0.9), porta=(1800, 990, 0.9), centro=(420, 1000, 0.95)),
    'cozinha': dict(a=(560, 1000, 0.95), b=(1410, 1000, 0.95), c=(960, 1000, 0.95)),
    'porta': dict(a=(500, 1010, 1.0), porta=(960, 1000, 1.0), b=(1500, 1010, 1.0)),
    'preto': dict(c=(960, 1000, 1.0)),
    'quarto_vo': dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'quarto_vo_escuro': dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'quarto_vo_manha': dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'quarto_vo_ramo': dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'cama': dict(deitado=(1250, 625, 0.85), lado=(400, 1000, 0.9)),
    'cama_escuro': dict(deitado=(1250, 625, 0.85), lado=(400, 1000, 0.9)),
    'quintal': dict(a=(560, 1010, 0.95), b=(1420, 1010, 0.95), portao=(960, 830, 0.8)),
    'quintal_manha': dict(a=(560, 1010, 0.95), b=(1420, 1010, 0.95), portao=(960, 830, 0.8)),
    'cortina': dict(lado=(330, 1010, 1.0), centro=(960, 1010, 1.0), dir=(1640, 1010, 0.95)),
}
