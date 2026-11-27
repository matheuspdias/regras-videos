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


# ---------------------------------------------------------------- noite 06: a porta da frente vista de fora
def bg_mm_varanda(ctx, t, manha=False, jaqueta=True):
    """varanda da frente, vista de fora: porta fechada com olho mágico, luz amarela fraca em cima, capacho,
    janela com grade à esquerda e o gancho da jaqueta reserva do pai à direita"""
    mm_room(ctx, fy=900)
    for k in range(9):                                           # lajotas
        ctx.move_to(k * 240 - 80, 900); ctx.line_to(k * 300 - 360, H)
    ctx.set_source_rgba(LINE[0], LINE[1], LINE[2], 0.25); ctx.set_line_width(3); ctx.stroke()
    lr(ctx, 790, 240, 340, 660, fill='#0E0E10', lw=6)          # porta
    for yy in (330, 560):
        lr(ctx, 830, yy, 260, 190, fill='#131316', lw=3)
    ctx.arc(1080, 600, 13, 0, TAU); ctx.set_source_rgba(*LINE); ctx.fill()
    ctx.arc(960, 300, 10, 0, TAU); ctx.set_source_rgba(0.75, 0.75, 0.8, 1); ctx.fill()   # olho mágico
    lr(ctx, 330, 330, 300, 330, fill='#0F1218')                 # janela da sala
    ctx.set_source_rgba(*LINE); ctx.set_line_width(4)
    for k in range(1, 6):
        ctx.move_to(330 + k * 50, 330); ctx.line_to(330 + k * 50, 660)
    ctx.move_to(330, 495); ctx.line_to(630, 495); ctx.stroke()
    ctx.save(); ctx.translate(960, 935); ctx.scale(1, 0.28)    # capacho
    ctx.rectangle(-190, -60, 380, 120); ctx.restore()
    setc(ctx, '#2A2622' if not manha else '#1C1A18'); ctx.fill()
    if manha:                                                  # capacho molhado
        ctx.save(); ctx.translate(960, 935); ctx.scale(1, 0.22); ctx.arc(0, 0, 150, 0, TAU); ctx.restore()
        ctx.set_source_rgba(0.5, 0.6, 0.75, 0.18); ctx.fill()
    ctx.arc(1340, 380, 10, 0, TAU); ctx.set_source_rgba(*LINE); ctx.fill()   # gancho
    if jaqueta:
        ctx.move_to(1340, 385); ctx.line_to(1270, 440); ctx.line_to(1250, 640); ctx.line_to(1430, 640); ctx.line_to(1410, 440)
        ctx.close_path(); setc(ctx, '#2C2C31'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
        ctx.move_to(1340, 400); ctx.line_to(1340, 640); ctx.stroke()
    lr(ctx, 930, 150, 60, 34, fill='#2A2A2E', r=8)              # luminária
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.12); ctx.fill()
    else:
        fl = 0.85 + 0.15 * math.sin(t * 9) * math.sin(t * 2.3)
        ctx.arc(960, 194, 16, 0, TAU); ctx.set_source_rgba(1, 0.85, 0.5, 0.95 * fl); ctx.fill()
        amber(ctx, 960, 260, 520, 0.22 * fl, t)


def bg_mm_porta_manha(ctx, t):
    bg_mm_porta(ctx, t)
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.12); ctx.fill()


def fita_olho(ctx, t):
    """fita crepe em X tapando o olho mágico (cenário porta)"""
    for a in (0.5, -0.5):
        ctx.save(); ctx.translate(960, 300); ctx.rotate(a)
        ctx.rectangle(-60, -13, 120, 26); setc(ctx, '#CFC6AE'); ctx.fill_preserve()
        ctx.set_source_rgba(0.3, 0.28, 0.24, 1); ctx.set_line_width(2); ctx.stroke(); ctx.restore()


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
    lr(ctx, 1270, 330, 110, 100, fill='#0A0A0C')                              # janela da vizinha da frente
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


# ---------------------------------------------------------------- banheiro (noite 04)
def vapor(ctx, x, y, w, t, a=0.12, n=6):
    """fiapos de vapor subindo"""
    for k in range(n):
        ph = (t * 0.25 + k / n) % 1.0
        xx = x + (k + 0.5) * w / n + 30 * math.sin(t * 0.8 + k * 1.7)
        yy = y - ph * 260
        rr_ = 40 + ph * 70
        g = cairo.RadialGradient(xx, yy, 2, xx, yy, rr_)
        g.add_color_stop_rgba(0, 0.85, 0.87, 0.9, a * (1 - ph)); g.add_color_stop_rgba(1, 0.85, 0.87, 0.9, 0)
        ctx.rectangle(xx - rr_, yy - rr_, 2 * rr_, 2 * rr_); ctx.set_source(g); ctx.fill()


def bg_mm_corredor_banho(ctx, t, agua=False, manha=False):
    """corredor: porta da irmã (esq., entreaberta), banheiro no meio com luz por baixo e vapor, seu quarto (dir.)"""
    mm_room(ctx, fy=820)
    door(ctx, 240, 280, 240, 540, open_frac=0.25)
    door(ctx, 820, 280, 240, 540, light=not manha, t=t)
    door(ctx, 1400, 280, 240, 540, open_frac=0.3)
    # plaquinha da porta do banheiro
    lr(ctx, 905, 360, 70, 44, fill=DARK3, r=8)
    ctx.set_source_rgba(*LINE); ctx.set_line_width(3)
    ctx.arc(940, 382, 9, 0, TAU); ctx.stroke()
    for x in (630, 1210):
        ctx.arc(x, 380, 18, 0, TAU); ctx.set_source_rgba(1, 0.75, 0.35, 0.8 if not manha else 0.25); ctx.fill()
        if not manha:
            amber(ctx, x, 380, 110, 0.45, t)
    if agua:
        # poça saindo por baixo da porta do banheiro, refletindo a luz
        ctx.move_to(800, 822)
        ctx.curve_to(760, 900, 640, 960, 700, 1040); ctx.curve_to(820, 1090, 1100, 1090, 1220, 1030)
        ctx.curve_to(1290, 970, 1150, 900, 1080, 822); ctx.close_path()
        g = cairo.LinearGradient(0, 822, 0, 1080)
        g.add_color_stop_rgba(0, 1, 0.78, 0.4, 0.45); g.add_color_stop_rgba(1, 0.6, 0.65, 0.75, 0.18)
        ctx.set_source(g); ctx.fill_preserve()
        ctx.set_source_rgba(0.8, 0.82, 0.86, 0.5); ctx.set_line_width(3); ctx.stroke()
        for k in range(3):
            rr_ = 30 + ((t * 40 + k * 50) % 150)
            ctx.save(); ctx.translate(950, 960); ctx.scale(1, 0.25); ctx.arc(0, 0, rr_, 0, TAU); ctx.restore()
            ctx.set_source_rgba(0.9, 0.9, 0.95, 0.25 * (1 - rr_ / 180)); ctx.set_line_width(3); ctx.stroke()
    if not manha:
        vapor(ctx, 830, 830, 220, t, a=0.14)
    else:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.12); ctx.fill()


def bg_mm_banheiro(ctx, t, manha=False):
    """banheiro por dentro: azulejo, espelho embaçado e pia (esq.), vaso, vitrô no alto, box de vidro (dir.; o vidro vai no fg)"""
    ctx.rectangle(0, 0, W, H); setc(ctx, '#161618'); ctx.fill()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.13); ctx.set_line_width(2)
    for x in range(0, W, 80):
        ctx.move_to(x, 0); ctx.line_to(x, 840)
    for y in range(0, 840, 80):
        ctx.move_to(0, y); ctx.line_to(W, y)
    ctx.stroke()
    ctx.rectangle(0, 840, W, H - 840); setc(ctx, DARK3); ctx.fill()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.18); ctx.set_line_width(2)
    for x in range(-400, W + 400, 140):
        ctx.move_to(x, 840); ctx.line_to(x + (x - 960) * 0.35, H)
    ctx.stroke()
    ctx.set_source_rgba(*LINE); ctx.set_line_width(5); ctx.move_to(0, 840); ctx.line_to(W, 840); ctx.stroke()
    # vitrô basculante
    lr(ctx, 1180, 90, 320, 130, fill='#0F1218' if not manha else '#5A6470')
    ctx.set_source_rgba(*LINE); ctx.set_line_width(3)
    for k in range(1, 4):
        ctx.move_to(1180, 90 + k * 32); ctx.line_to(1500, 90 + k * 32)
    ctx.stroke()
    # espelho e pia
    lr(ctx, 220, 240, 320, 320, fill='#1E2126', r=10)
    ctx.rectangle(232, 252, 296, 296); ctx.set_source_rgba(0.8, 0.82, 0.86, 0.10); ctx.fill()
    lr(ctx, 190, 590, 380, 70, r=14)
    lr(ctx, 330, 660, 100, 180, fill=DARK3)
    lr(ctx, 368, 560, 24, 34, fill='#3A3A40', r=4)
    # vaso
    lr(ctx, 720, 560, 150, 180, fill=DARK2, r=12)
    ctx.save(); ctx.translate(800, 760); ctx.scale(1, 0.45); ctx.arc(0, 0, 105, 0, TAU); ctx.restore()
    setc(ctx, DARK2); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    lr(ctx, 745, 780, 110, 60, fill=DARK2)
    # cabide com toalha (vazio: a toalha ficou no quarto)
    lr(ctx, 600, 320, 80, 14, fill='#3A3A40', r=6)
    # box: fundo, chuveiro e ralo
    lr(ctx, 1060, 200, 760, 660, fill='#121214')
    ctx.set_source_rgba(*LINE); ctx.set_line_width(6)
    ctx.move_to(1440, 200); ctx.line_to(1440, 250); ctx.line_to(1400, 270); ctx.stroke()
    ctx.save(); ctx.translate(1380, 280); ctx.rotate(0.4); ctx.scale(1, 0.4); ctx.arc(0, 0, 50, 0, TAU); ctx.restore()
    setc(ctx, '#3A3A40'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    lr(ctx, 1640, 500, 60, 60, fill='#2A2A2E', r=30)                              # registro
    ctx.save(); ctx.translate(1430, 850); ctx.scale(1, 0.3); ctx.arc(0, 0, 40, 0, TAU); ctx.restore()
    setc(ctx, '#050506'); ctx.fill()
    # lâmpada acesa
    ctx.arc(960, 40, 22, 0, TAU); ctx.set_source_rgba(1, 0.8, 0.45, 0.95 if not manha else 0.2); ctx.fill()
    if not manha:
        amber(ctx, 960, 60, 520, 0.22, t)
    else:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.12); ctx.fill()


def fg_mm_banheiro(ctx, t, manha=False):
    """vidro do box embaçado por cima de quem está dentro"""
    ctx.rectangle(1080, 210, 720, 640)
    ctx.set_source_rgba(0.72, 0.75, 0.8, 0.16 if manha else 0.24); ctx.fill()
    if not manha:
        vapor(ctx, 1090, 760, 700, t, a=0.16, n=7)
    ctx.set_source_rgba(0.78, 0.78, 0.82, 1); ctx.set_line_width(7)
    ctx.rectangle(1070, 200, 740, 660); ctx.stroke()
    ctx.move_to(1440, 200); ctx.line_to(1440, 860); ctx.set_line_width(5); ctx.stroke()
    # gotas escorrendo no vidro
    ctx.set_source_rgba(0.9, 0.92, 0.96, 0.35); ctx.set_line_width(3)
    for k, x in enumerate((1130, 1250, 1520, 1700)):
        y0 = 260 + k * 90
        ctx.move_to(x, y0); ctx.line_to(x + 4, y0 + 120 + 40 * math.sin(t + k)); ctx.stroke()


def bg_mm_banheiro_porta(ctx, t):
    """close na porta do banheiro, vista do corredor: luz por baixo, vapor saindo pela fresta, fechadura"""
    mm_room(ctx, fy=800)
    door(ctx, 640, 40, 640, 760, light=True, t=t)
    lr(ctx, 1180, 430, 50, 70, fill='#2A2A2E', r=8)
    ctx.arc(1205, 410, 16, 0, TAU); ctx.set_source_rgba(*LINE); ctx.fill()
    lr(ctx, 870, 200, 180, 110, fill=DARK3, r=12)
    ctx.set_source_rgba(*LINE); ctx.set_line_width(4)
    ctx.arc(960, 255, 24, 0, TAU); ctx.stroke()
    for x in (330, 1590):                                                    # arandelas do corredor
        lr(ctx, x - 30, 300, 60, 40, fill=DARK3, r=10)
        ctx.arc(x, 330, 14, 0, TAU); ctx.set_source_rgba(1, 0.75, 0.35, 0.8); ctx.fill()
        amber(ctx, x, 330, 160, 0.4, t)
    lr(ctx, 760, 830, 400, 60, fill='#202024', r=20)                        # tapetinho
    vapor(ctx, 660, 830, 600, t, a=0.26, n=7)
    vapor(ctx, 660, 100, 600, t + 3, a=0.12, n=5)


def bg_mm_cama_duda(ctx, t):
    """quarto da irmã: cama grande, janela com lua, varal de luzinhas e pôsteres"""
    mm_room(ctx, wall_c='#141417', fy=880)
    moon_window(ctx, 880, 110, 280, 240)
    for k, (x, y, w, h) in enumerate(((1300, 150, 150, 200), (1490, 190, 170, 130), (300, 170, 160, 210))):
        lr(ctx, x, y, w, h, fill='#1E1E22', r=4)
        ctx.set_source_rgba(0.6, 0.6, 0.64, 0.3); ctx.set_line_width(3)
        ctx.arc(x + w / 2, y + h * 0.45, min(w, h) * 0.22, 0, TAU); ctx.stroke()
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.6); ctx.set_line_width(2)
    ctx.move_to(240, 70); ctx.curve_to(700, 150, 1300, 150, 1780, 70); ctx.stroke()
    for k in range(14):
        u = k / 13
        x = 240 + u * 1540
        y = 70 + 4 * u * (1 - u) * 80 + 8
        ctx.arc(x, y, 7, 0, TAU); ctx.set_source_rgba(1, 0.8, 0.45, 0.85); ctx.fill()
        amber(ctx, x, y, 40, 0.25, t)
    big_bed(ctx)



def guarda_roupa(ctx, x, y, w=380, h=560, t=0, espelho_luz=0.10):
    """guarda-roupa antigo da vó: duas portas, a da direita com espelho oval, paninho de crochê em cima"""
    lr(ctx, x, y, w, h, fill='#1A1714', r=6)
    lr(ctx, x + 12, y + 14, w / 2 - 18, h - 70, fill='#16130F', r=4)
    lr(ctx, x + w / 2 + 6, y + 14, w / 2 - 18, h - 70, fill='#16130F', r=4)
    for k in (-1, 1):
        ctx.arc(x + w / 2 + k * 20, y + h * 0.5, 7, 0, TAU); ctx.set_source_rgba(*LINE); ctx.fill()
    # espelho oval na porta direita
    ex, ey = x + w * 0.75, y + h * 0.42
    ctx.save(); ctx.translate(ex, ey); ctx.scale(1, 1.9); ctx.arc(0, 0, w * 0.17, 0, TAU); ctx.restore()
    g = cairo.LinearGradient(ex - 60, ey - 160, ex + 60, ey + 160)
    g.add_color_stop_rgba(0, 0.55, 0.6, 0.7, 0.10 + espelho_luz); g.add_color_stop_rgba(1, 0.05, 0.06, 0.08, 1)
    ctx.set_source(g); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    ctx.set_source_rgba(0.85, 0.88, 0.95, 0.25); ctx.set_line_width(3)
    ctx.move_to(ex - 30, ey - 90); ctx.line_to(ex - 10, ey - 120); ctx.stroke()
    # gavetão e pés
    lr(ctx, x + 12, y + h - 48, w - 24, 36, fill=DARK3, r=4)
    lr(ctx, x + 10, y + h, 24, 20); lr(ctx, x + w - 34, y + h, 24, 20)
    # paninho de crochê e uma foto da vó em cima
    ctx.move_to(x + 40, y); 
    for k in range(9):
        ctx.arc(x + 60 + k * 32, y + 4, 14, 0, math.pi)
    ctx.set_source_rgba(0.85, 0.84, 0.8, 0.55); ctx.set_line_width(3); ctx.stroke()
    lr(ctx, x + w * 0.55, y - 92, 70, 88, fill='#22201C', r=4)
    ctx.arc(x + w * 0.55 + 35, y - 58, 16, 0, TAU); ctx.set_source_rgba(0.6, 0.6, 0.64, 0.5); ctx.fill()
    ctx.arc(x + w * 0.55 + 35, y - 72, 9, 0, TAU); ctx.fill()


def bg_mm_corredor_vo(ctx, t, manha=False):
    """corredor: seu quarto (esq.), quarto do Bento (meio, entreaberto), guarda-roupa da vó no fim (dir.)"""
    mm_room(ctx, fy=820)
    door(ctx, 240, 280, 240, 540)
    door(ctx, 820, 280, 240, 540, open_frac=0.22)
    guarda_roupa(ctx, 1380, 260, t=t)
    for x in (630, 1210):
        ctx.arc(x, 380, 18, 0, TAU); ctx.set_source_rgba(1, 0.75, 0.35, 0.8 if not manha else 0.25); ctx.fill()
        if not manha:
            amber(ctx, x, 380, 110, 0.4, t)
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.12); ctx.fill()


def bg_mm_quarto_bento(ctx, t):
    """quarto do irmão: cama baixa, estrelinhas que brilham no escuro no teto, luz de tomada, janela"""
    mm_room(ctx, wall_c='#131418')
    moon_window(ctx, 1420, 170, 280, 260)
    door(ctx, 760, 260, 230, 540, open_frac=0.2)
    rnd = random.Random(5)
    for k in range(16):
        x, y = rnd.uniform(120, 1800), rnd.uniform(40, 150)
        star(ctx, x, y, rnd.uniform(9, 15), '#C9E6B8')
    bed(ctx, 140, 800, 560, made=False)
    lr(ctx, 1150, 690, 210, 110, fill=DARK3, r=8)                     # baú de brinquedos
    ctx.arc(1255, 690, 22, math.pi, 0); ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.stroke()
    ctx.arc(1080, 720, 12, 0, TAU); ctx.set_source_rgba(1, 0.75, 0.35, 0.9); ctx.fill()   # luz de tomada
    amber(ctx, 1080, 720, 170, 0.35, t)


# ---------------------------------------------------------------- casa da vó no interior (noite 07)
def chinelo(ctx, x, y, s=1.0, virado=False):
    """par de chinelos de dedo no chão (y = chão)"""
    for k, dx in enumerate((-34, 34)):
        ctx.save(); ctx.translate(x + dx * s, y - 8 * s); ctx.rotate(0.12 * (k * 2 - 1)); ctx.scale(s, s * 0.42)
        rrect(ctx, -26, -70, 52, 140, 26)
        setc(ctx, '#3A3A40' if virado else '#2C2C32'); ctx.fill_preserve()
        ctx.set_source_rgba(*LINE); ctx.set_line_width(4 / s); ctx.stroke()
        if not virado:
            ctx.set_source_rgba(0.75, 0.75, 0.8, 1); ctx.set_line_width(7 / s)
            ctx.move_to(0, -40); ctx.line_to(-20, 10); ctx.move_to(0, -40); ctx.line_to(20, 10); ctx.stroke()
        ctx.restore()


def maquina_costura(ctx, x, y):
    """máquina de costura de pedal (y = chão)"""
    lr(ctx, x, y - 300, 300, 26, fill=DARK3, r=4)                     # tampo
    ctx.set_source_rgba(*LINE); ctx.set_line_width(5)
    for xx in (x + 30, x + 270):                                       # pés de ferro em X
        ctx.move_to(xx - 20, y - 274); ctx.line_to(xx + 20, y); ctx.move_to(xx + 20, y - 274); ctx.line_to(xx - 20, y)
    ctx.stroke()
    ctx.arc(x + 150, y - 120, 60, 0, TAU); ctx.stroke()                # volante
    lr(ctx, x + 90, y - 34, 120, 20, fill=DARK3, r=4)                   # pedal
    # a máquina em cima
    ctx.move_to(x + 60, y - 300); ctx.line_to(x + 60, y - 400); ctx.curve_to(x + 70, y - 430, x + 220, y - 430, x + 230, y - 400)
    ctx.line_to(x + 230, y - 350); ctx.line_to(x + 200, y - 350); ctx.line_to(x + 200, y - 300); ctx.close_path()
    setc(ctx, '#1E1E22'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    ctx.arc(x + 90, y - 380, 14, 0, TAU); ctx.stroke()


def fuxico(ctx, x, y, w, h):
    """colcha de fuxico dobrada: florzinhas redondas de retalho"""
    lr(ctx, x, y, w, h, fill='#2A2724', r=10)
    ctx.save(); ctx.rectangle(x, y, w, h); ctx.clip()
    for i in range(int(w / 34) + 1):
        for j in range(int(h / 34) + 1):
            ctx.arc(x + 17 + i * 34, y + 17 + j * 34, 13, 0, TAU)
            ctx.set_source_rgba(0.6, 0.6, 0.64, 0.30 + 0.12 * ((i + j) % 2)); ctx.set_line_width(3); ctx.stroke()
    ctx.restore()


def cama_ferro(ctx, x, y, w):
    """cama de ferro alta, com grade na cabeceira e nos pés"""
    ctx.set_source_rgba(*LINE); ctx.set_line_width(6)
    for xx, top in ((x, y - 190), (x + w, y - 120)):
        ctx.move_to(xx, y + 120); ctx.line_to(xx, top); ctx.stroke()
    ctx.move_to(x, y - 190); ctx.curve_to(x + 30, y - 220, x + 60, y - 220, x + 90, y - 190); ctx.line_to(x + 90, y - 30); ctx.stroke()
    for k in range(1, 4):
        ctx.move_to(x + k * 22, y - 195); ctx.line_to(x + k * 22, y - 30); ctx.stroke()
    ctx.move_to(x + w, y - 120); ctx.curve_to(x + w - 30, y - 150, x + w - 60, y - 150, x + w - 90, y - 120); ctx.line_to(x + w - 90, y - 30); ctx.stroke()
    for k in range(1, 4):
        ctx.move_to(x + w - k * 22, y - 125); ctx.line_to(x + w - k * 22, y - 30); ctx.stroke()
    lr(ctx, x + 6, y - 30, w - 12, 80, r=10)                           # colchão
    lr(ctx, x + 100, y - 66, 170, 46, fill='#2A2A2E', r=20)            # travesseiro
    ctx.move_to(x + 290, y - 36); ctx.curve_to(x + 380, y - 70, x + 470, y - 20, x + w - 100, y - 44)
    ctx.line_to(x + w - 100, y + 40); ctx.line_to(x + 290, y + 40); ctx.close_path()
    setc(ctx, '#26262A'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    fuxico(ctx, x + w - 210, y - 60, 110, 40)
    ctx.set_source_rgba(*LINE); ctx.set_line_width(6)
    for xx in (x + 20, x + w - 20):                                   # pés compridos (dá pra ver debaixo da cama)
        ctx.move_to(xx, y + 50); ctx.line_to(xx, y + 130); ctx.stroke()


def bg_mm_quarto_costura(ctx, t, manha=False, chinelo_=True):
    """seu quarto na casa da vó: cama de ferro alta, máquina de costura de pedal, chinelo no chão, porta e janela padrão"""
    mm_room(ctx, wall_c='#151413', fy=800)
    wood_window(ctx, 220, 160, 300, 280)
    door(ctx, 760, 260, 230, 540)
    maquina_costura(ctx, 1010, 800)
    cama_ferro(ctx, 1340, 790, 540)
    if chinelo_:
        chinelo(ctx, 1260, 905, 0.9)
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.13); ctx.fill()


def filtro_barro(ctx, x, y):
    lr(ctx, x - 60, y, 120, 20, fill=DARK3, r=4)
    for yy, ww in ((y - 150, 110), (y - 290, 100)):
        ctx.save(); ctx.translate(x, yy + 70); ctx.scale(1, 1.25); ctx.arc(0, 0, ww / 2 + 6, 0, TAU); ctx.restore()
        setc(ctx, '#2A2420'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    lr(ctx, x - 6, y - 70, 30, 12, fill=DARK3)


def fogao_lenha(ctx, x, y):
    lr(ctx, x, y - 260, 420, 260, fill='#1E1B18', r=6)
    lr(ctx, x - 10, y - 280, 440, 24, fill=DARK3, r=4)
    for k in range(2):
        ctx.arc(x + 110 + k * 180, y - 268, 40, math.pi, 0); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    lr(ctx, x + 40, y - 190, 120, 90, fill='#0B0A09', r=6)             # boca do fogo, apagada
    lr(ctx, x + 340, y - 900, 60, 640, fill='#1A1816')                 # chaminé


def bg_mm_cozinha_vo(ctx, t, aberta=False, manha=False):
    """cozinha da vó: fogão a lenha (esq.), filtro de barro, porta dos fundos de madeira (dir.) e a vassoura atrás dela"""
    mm_room(ctx, wall_c='#151413', fy=820)
    fogao_lenha(ctx, 120, 820)
    filtro_barro(ctx, 760, 620)
    lr(ctx, 640, 620, 240, 200, fill=DARK3)                           # mesinha do filtro
    wood_window(ctx, 860, 200, 220, 200, open_=False)
    # porta dos fundos (rect 1300,260,300,560)
    if aberta:
        lr(ctx, 1300, 260, 300, 560, fill='#07080A')
        g = cairo.LinearGradient(1300, 260, 1300, 820)
        g.add_color_stop_rgba(0, 0.5, 0.55, 0.7, 0.10); g.add_color_stop_rgba(1, 0.5, 0.55, 0.7, 0.02)
        ctx.rectangle(1300, 260, 300, 560); ctx.set_source(g); ctx.fill()
        ctx.move_to(1600, 260); ctx.line_to(1700, 230); ctx.line_to(1700, 850); ctx.line_to(1600, 820); ctx.close_path()
        setc(ctx, '#1E1A17'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    else:
        lr(ctx, 1300, 260, 300, 560, fill='#1E1A17')
        ctx.set_source_rgba(*LINE); ctx.set_line_width(3)
        ctx.move_to(1300, 540); ctx.line_to(1600, 540); ctx.stroke()      # porta de duas folhas (cima/baixo)
        lr(ctx, 1560, 520, 50, 14, fill=DARK3)                            # tramela
        if not manha:                                                     # a vassoura da vó encostada
            ctx.set_source_rgba(0.6, 0.55, 0.48, 1); ctx.set_line_width(9)
            ctx.move_to(1690, 380); ctx.line_to(1660, 760); ctx.stroke()
            ctx.move_to(1640, 750); ctx.line_to(1680, 750); ctx.line_to(1700, 820); ctx.line_to(1610, 820); ctx.close_path()
            setc(ctx, '#7A6E5C'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.stroke()
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.13); ctx.fill()


def bg_mm_terreiro(ctx, t, manha=False, chinelo_=False):
    """terreiro de terra batida atrás da casa: varal, pé de manga, a parede da casa com a porta da cozinha (esq.)"""
    ctx.rectangle(0, 0, W, H); setc(ctx, '#101217' if not manha else '#2A3140'); ctx.fill()
    if not manha:
        ctx.arc(1500, 170, 36, 0, TAU); ctx.set_source_rgba(0.85, 0.86, 0.9, 0.9); ctx.fill()
    ctx.rectangle(0, 860, W, H - 860); setc(ctx, '#1E1B18' if not manha else '#3A352E'); ctx.fill()
    ctx.set_source_rgba(*LINE); ctx.set_line_width(5); ctx.move_to(0, 860); ctx.line_to(W, 860); ctx.stroke()
    # parede da casa e porta da cozinha
    lr(ctx, -10, 140, 560, 720, fill='#18171A')
    lr(ctx, 160, 320, 260, 540, fill='#1E1A17')
    ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.move_to(160, 590); ctx.line_to(420, 590); ctx.stroke()
    lr(ctx, 130, 860, 320, 24, fill=DARK3)                              # degrau
    # pé de manga
    ctx.set_source_rgba(*LINE); ctx.set_line_width(26); ctx.move_to(1540, 860); ctx.curve_to(1530, 700, 1560, 600, 1520, 480); ctx.stroke()
    setc(ctx, '#0E100E' if not manha else '#1E2620')
    for cx_, cy_, r_ in ((1520, 380, 220), (1380, 430, 160), (1680, 420, 170), (1530, 260, 150)):
        ctx.arc(cx_, cy_, r_, 0, TAU); ctx.fill()
    for cx_, cy_, r_ in ((1520, 380, 220), (1380, 430, 160), (1680, 420, 170), (1530, 260, 150)):
        ctx.arc(cx_, cy_, r_, 0, TAU); ctx.set_source_rgba(0.6, 0.6, 0.64, 0.25); ctx.set_line_width(3); ctx.stroke()
    # varal
    ctx.set_source_rgba(*LINE); ctx.set_line_width(5)
    ctx.move_to(700, 860); ctx.line_to(700, 420); ctx.move_to(1250, 860); ctx.line_to(1250, 420); ctx.stroke()
    ctx.set_line_width(2); ctx.move_to(700, 440); ctx.curve_to(900, 480, 1050, 480, 1250, 440); ctx.stroke()
    for x0, w0 in ((760, 110), (1000, 90)):
        lr(ctx, x0, 466, w0, 120, fill='#26262A' if not manha else '#4A4A52', lw=3)
    # pé de arruda no vaso
    lr(ctx, 1240, 900, 70, 60, fill='#2A2420')
    ctx.set_source_rgba(0.55, 0.62, 0.55, 1); ctx.set_line_width(4)
    for a in (-0.4, 0, 0.35):
        ctx.move_to(1275, 900); ctx.line_to(1275 + math.sin(a) * 70, 900 - math.cos(a) * 70); ctx.stroke()
    if chinelo_:
        chinelo(ctx, 1120, 960, 0.9, virado=True)
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.08); ctx.fill()


# ---------------------------------------------------------------- noite 08: a cozinha do café
def xicara(ctx, x, y, s=1.0, t=0, quente=True, vazia=False):
    """xícara branca no pires (y = apoio); quente solta um fio de vapor"""
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.save(); ctx.scale(1, 0.28); ctx.arc(0, -8, 58, 0, TAU); ctx.restore()
    setc(ctx, '#BDBDC2'); ctx.fill_preserve(); ctx.set_source_rgba(*OUT); ctx.set_line_width(4); ctx.stroke()
    ctx.move_to(-36, -60); ctx.line_to(36, -60); ctx.curve_to(34, -18, 24, -10, 0, -10); ctx.curve_to(-24, -10, -34, -18, -36, -60); ctx.close_path()
    setc(ctx, '#E2E2E4'); ctx.fill_preserve(); ctx.set_source_rgba(*OUT); ctx.set_line_width(4); ctx.stroke()
    ctx.arc(42, -40, 13, -1.5, 1.5); ctx.set_source_rgba(*OUT); ctx.set_line_width(5); ctx.stroke()
    ctx.save(); ctx.scale(1, 0.22); ctx.arc(0, -60 / 0.22, 34, 0, TAU); ctx.restore()
    setc(ctx, '#1A0F08' if not vazia else '#D0D0D4'); ctx.fill()
    ctx.restore()
    if quente:
        vapor(ctx, x - 40 * s, y - 70 * s, 80 * s, t, a=0.16, n=2)


def chaleira(ctx, x, y):
    """chaleira de alumínio em cima da boca do fogão (y = apoio)"""
    ctx.move_to(x - 70, y); ctx.curve_to(x - 80, y - 90, x + 80, y - 90, x + 70, y); ctx.close_path()
    setc(ctx, '#3A3A40'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    ctx.arc(x, y - 72, 44, math.pi * 1.1, math.pi * 1.9); ctx.set_line_width(6); ctx.stroke()
    ctx.move_to(x + 60, y - 30); ctx.line_to(x + 120, y - 70); ctx.set_line_width(10); ctx.stroke()


def coador(ctx, x, y):
    """suporte de madeira com o coador de pano, em cima do balcão (y = apoio)"""
    ctx.set_source_rgba(*LINE); ctx.set_line_width(7)
    ctx.move_to(x - 70, y); ctx.line_to(x - 70, y - 200); ctx.move_to(x + 70, y); ctx.line_to(x + 70, y - 200)
    ctx.move_to(x - 90, y - 200); ctx.line_to(x + 90, y - 200); ctx.stroke()
    ctx.move_to(x - 50, y - 200); ctx.curve_to(x - 40, y - 110, x + 40, y - 110, x + 50, y - 200); ctx.close_path()
    setc(ctx, '#5A4A3A'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.stroke()
    lr(ctx, x - 44, y - 90, 88, 90, fill='#2E2E33', r=10)               # bule embaixo


def bg_mm_cozinha_cafe(ctx, t, luz=True, quente=True, xicaras=2, manha=False, escorredor=False):
    """cozinha da casa (noite 08): balcão com pia e escorredor (esq.), lâmpada pendurada, mesa com toalha xadrez e as
    xícaras, coador de pano e fogão de quatro bocas com a chaleira (dir.), porta dos fundos fechada"""
    mm_room(ctx, wall_c='#151413' if not manha else '#2A2D33', floor_c=DARK3 if not manha else '#34363C', fy=820)
    for k in range(0, 1920, 64):                                         # azulejo meia-parede
        ctx.move_to(k, 560); ctx.line_to(k, 820)
    for k in range(560, 820, 64):
        ctx.move_to(0, k); ctx.line_to(1920, k)
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.10); ctx.set_line_width(2); ctx.stroke()
    lr(ctx, 80, 190, 560, 190)                                           # armário alto
    ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.move_to(360, 190); ctx.line_to(360, 380); ctx.stroke()
    moon_window(ctx, 700, 200, 240, 200) if not manha else lr(ctx, 700, 200, 240, 200, fill='#8A98AE')
    lr(ctx, 80, 600, 680, 220)                                           # balcão com pia
    for k in range(3):
        lr(ctx, 100 + k * 220, 630, 200, 170, fill=DARK3)
    lr(ctx, 70, 586, 700, 20, fill='#2E2E33')
    ctx.set_source_rgba(*LINE); ctx.set_line_width(6)                    # torneira
    ctx.move_to(300, 586); ctx.line_to(300, 520); ctx.line_to(350, 520); ctx.line_to(350, 545); ctx.stroke()
    lr(ctx, 480, 520, 200, 66, fill='#1E1E22', r=6)                     # escorredor
    for k in range(4):
        ctx.move_to(495 + k * 50, 586); ctx.line_to(495 + k * 50, 520)
    ctx.set_source_rgba(*LINE); ctx.set_line_width(2); ctx.stroke()
    if escorredor:                                                       # a xícara a mais, de boca pra baixo, ainda morna
        ctx.move_to(540, 580); ctx.line_to(620, 580); ctx.curve_to(616, 540, 600, 528, 580, 528); ctx.curve_to(560, 528, 544, 540, 540, 580); ctx.close_path()
        setc(ctx, '#E2E2E4'); ctx.fill_preserve(); ctx.set_source_rgba(*OUT); ctx.set_line_width(4); ctx.stroke()
        vapor(ctx, 540, 560, 80, t, a=0.14, n=2)
    coador(ctx, 1290, 600)
    lr(ctx, 1180, 600, 220, 220)                                         # balcãozinho do coador
    lr(ctx, 1460, 560, 300, 260, fill='#1C1C1F')                         # fogão
    lr(ctx, 1450, 540, 320, 24, fill='#2E2E33')
    for k in range(4):
        ctx.arc(1505 + k * 70, 690, 14, 0, TAU); ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.stroke()
    lr(ctx, 1490, 600, 240, 60, fill='#0E0E10', r=6)                     # vidro do forno
    chaleira(ctx, 1560, 540)
    lr(ctx, 1800, 260, 120, 560, fill='#1E1A17')                         # porta dos fundos (borda)
    # mesa com toalha xadrez
    lr(ctx, 780, 690, 380, 24, fill='#2A2A2E')
    ctx.move_to(770, 700); ctx.line_to(1170, 700); ctx.line_to(1190, 800); ctx.line_to(750, 800); ctx.close_path()
    setc(ctx, '#2C2626'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    ctx.save(); ctx.move_to(770, 700); ctx.line_to(1170, 700); ctx.line_to(1190, 800); ctx.line_to(750, 800); ctx.close_path(); ctx.clip()
    for k in range(750, 1200, 40):
        ctx.rectangle(k, 700, 20, 100)
    ctx.set_source_rgba(0.6, 0.6, 0.64, 0.12); ctx.fill()
    ctx.restore()
    ctx.set_source_rgba(*LINE); ctx.set_line_width(8)
    for xx in (790, 1150):
        ctx.move_to(xx, 800); ctx.line_to(xx, 930); ctx.stroke()
    lr(ctx, 1080, 560, 56, 130, fill='#3A3A40', r=12)                    # garrafa térmica
    lr(ctx, 1090, 545, 36, 20, fill='#2E2E33', r=4)
    pos = [(860, 702), (980, 702), (920, 702), (1040, 702)][:xicaras]
    for k, (xx, yy) in enumerate(sorted(pos)):
        xicara(ctx, xx, yy, 0.85, t + k * 0.7, quente=quente)
    # lâmpada pendurada
    ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.move_to(960, 0); ctx.line_to(960, 150); ctx.stroke()
    ctx.move_to(920, 150); ctx.line_to(1000, 150); ctx.line_to(1030, 190); ctx.line_to(890, 190); ctx.close_path()
    setc(ctx, '#2E2E33'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.stroke()
    if luz and not manha:
        flick = 1.0 if quente else 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 19) * math.sin(t * 5.1))
        ctx.arc(960, 198, 16, 0, TAU); ctx.set_source_rgba(1, 0.85, 0.5, flick); ctx.fill()
        g = cairo.RadialGradient(960, 260, 20, 960, 420, 900)
        g.add_color_stop_rgba(0, 1, 0.72, 0.32, 0.30 * flick); g.add_color_stop_rgba(1, 1, 0.72, 0.32, 0)
        ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.10); ctx.fill()


def bg_mm_corredor_cafe(ctx, t, xicara_=False, fria=False, mancha=False):
    """corredor de casa à noite: a sua porta (esq.), o quarto da mãe (meio) e, no fundo à direita, a porta da cozinha
    aberta com a luz acesa e o vapor saindo (rect da cozinha 1400,280,240,540)"""
    mm_room(ctx, fy=820)
    door(ctx, 240, 280, 240, 540, light=False)
    door(ctx, 820, 280, 240, 540)
    k = 1.0 if not fria else 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * 19) * math.sin(t * 5.1))
    g = cairo.LinearGradient(1400, 280, 1400, 820)
    g.add_color_stop_rgba(0, 1, 0.72, 0.32, 0.55 * k); g.add_color_stop_rgba(1, 1, 0.65, 0.3, 0.35 * k)
    ctx.rectangle(1400, 280, 240, 540); ctx.set_source(g); ctx.fill()
    ctx.set_source_rgba(0.08, 0.07, 0.07, 1)                             # mesa lá dentro, em contraluz
    ctx.rectangle(1440, 650, 200, 20); ctx.fill(); ctx.rectangle(1460, 670, 12, 150); ctx.fill()
    ctx.rectangle(1400, 280, 240, 540); ctx.set_source_rgba(*LINE); ctx.set_line_width(5); ctx.stroke()
    ctx.move_to(1400, 820); ctx.line_to(1640, 820); ctx.line_to(1820, 1080); ctx.line_to(1180, 1080); ctx.close_path()
    g2 = cairo.LinearGradient(0, 820, 0, 1080)
    g2.add_color_stop_rgba(0, 1, 0.72, 0.32, 0.22 * k); g2.add_color_stop_rgba(1, 1, 0.72, 0.32, 0)
    ctx.set_source(g2); ctx.fill()
    if not fria:
        vapor(ctx, 1400, 420, 240, t, a=0.10, n=4)
    for x in (630, 1210):
        ctx.arc(x, 380, 18, 0, TAU); ctx.set_source_rgba(0.5, 0.5, 0.52, 0.6); ctx.fill()
    if xicara_:
        xicara(ctx, 380, 900, 0.9, t, quente=not fria)
    if mancha:                                                           # a rodinha de café seco no piso
        ctx.save(); ctx.translate(380, 895); ctx.scale(1, 0.3); ctx.arc(0, 0, 50, 0, TAU); ctx.restore()
        ctx.set_source_rgba(0.35, 0.22, 0.12, 0.8); ctx.set_line_width(6); ctx.stroke()


def bg_mm_quarto_cafe(ctx, t, toalha=False, manha=False):
    """o seu quarto com a luz da cozinha passando por baixo da porta e o vapor entrando pela fresta; toalha=True: a
    fresta tapada com a toalha enrolada"""
    mm_room(ctx)
    moon_window(ctx, 220, 160, 300, 280)
    door(ctx, 760, 260, 230, 540, light=not toalha and not manha, t=t)
    if not toalha and not manha:
        vapor(ctx, 760, 830, 230, t, a=0.09, n=4)
    if toalha:
        lr(ctx, 740, 776, 270, 34, fill='#4A4A52', r=16)
        ctx.set_source_rgba(0.6, 0.6, 0.64, 0.5); ctx.set_line_width(2)
        for k in range(760, 1000, 26):
            ctx.move_to(k, 780); ctx.line_to(k + 8, 806)
        ctx.stroke()
    bed(ctx, 1180, 780, 640, made=False)
    lr(ctx, 1060, 640, 100, 160, r=6)
    lr(ctx, 1085, 560, 50, 80, fill='#2C2C30')
    ctx.move_to(1070, 560); ctx.line_to(1150, 560); ctx.line_to(1130, 520); ctx.line_to(1090, 520); ctx.close_path()
    setc(ctx, '#3A3A40'); ctx.fill()
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.13); ctx.fill()


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
    'corredor_banho': (bg_mm_corredor_banho, None),
    'corredor_agua': (lambda c, t: bg_mm_corredor_banho(c, t, agua=True), None),
    'corredor_banho_manha': (lambda c, t: bg_mm_corredor_banho(c, t, manha=True), None),
    'banho': (bg_mm_banheiro, fg_mm_banheiro),
    'banho_manha': (lambda c, t: bg_mm_banheiro(c, t, manha=True), lambda c, t: fg_mm_banheiro(c, t, manha=True)),
    'banheiro_porta': (bg_mm_banheiro_porta, None),
    'cama_duda': (bg_mm_cama_duda, fg_mm_cama),
    'corredor_vo': (bg_mm_corredor_vo, None),
    'corredor_vo_manha': (lambda c, t: bg_mm_corredor_vo(c, t, manha=True), None),
    'quarto_bento': (bg_mm_quarto_bento, None),
    'varanda': (bg_mm_varanda, None),
    'varanda_manha': (lambda c, t: bg_mm_varanda(c, t, manha=True, jaqueta=False), None),
    'varanda_jaqueta': (lambda c, t: bg_mm_varanda(c, t, jaqueta=False), None),
    'porta_manha': (bg_mm_porta_manha, None),
    'porta_fita': (lambda c, t: (bg_mm_porta(c, t), fita_olho(c, t)), None),
    'quarto_costura': (bg_mm_quarto_costura, None),
    'quarto_costura_vazio': (lambda c, t: bg_mm_quarto_costura(c, t, chinelo_=False), None),
    'cozinha_vo': (bg_mm_cozinha_vo, None),
    'cozinha_vo_aberta': (lambda c, t: bg_mm_cozinha_vo(c, t, aberta=True), None),
    'cozinha_vo_manha': (lambda c, t: bg_mm_cozinha_vo(c, t, manha=True), None),
    'terreiro': (bg_mm_terreiro, None),
    'terreiro_manha': (lambda c, t: bg_mm_terreiro(c, t, manha=True), None),
    'terreiro_chinelo': (lambda c, t: bg_mm_terreiro(c, t, manha=True, chinelo_=True), None),
    'cozinha_cafe': (bg_mm_cozinha_cafe, None),
    'cozinha_fria': (lambda c, t: bg_mm_cozinha_cafe(c, t, quente=False), None),
    'cozinha_vazia': (lambda c, t: bg_mm_cozinha_cafe(c, t, luz=False, quente=False, xicaras=0), None),
    'cozinha_manha': (lambda c, t: bg_mm_cozinha_cafe(c, t, xicaras=0, manha=True), None),
    'cozinha_domingo': (lambda c, t: bg_mm_cozinha_cafe(c, t, xicaras=3, manha=True, escorredor=True), None),
    'corredor_cafe': (bg_mm_corredor_cafe, None),
    'corredor_xicara': (lambda c, t: bg_mm_corredor_cafe(c, t, xicara_=True), None),
    'corredor_frio': (lambda c, t: bg_mm_corredor_cafe(c, t, fria=True), None),
    'corredor_mancha': (lambda c, t: bg_mm_corredor_cafe(c, t, fria=True, mancha=True), None),
    'quarto_cafe': (bg_mm_quarto_cafe, None),
    'quarto_toalha': (lambda c, t: bg_mm_quarto_cafe(c, t, toalha=True), None),
    'quarto_cafe_manha': (lambda c, t: bg_mm_quarto_cafe(c, t, toalha=True, manha=True), None),
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
    'corredor_banho': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), p3=(1520, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'corredor_agua': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), p3=(1520, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'corredor_banho_manha': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), p3=(1520, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'banho': dict(porta=(680, 1020, 0.95), pia=(380, 1010, 0.95), box=(1430, 860, 0.9)),
    'banho_manha': dict(porta=(680, 1020, 0.95), pia=(380, 1010, 0.95), box=(1430, 860, 0.9)),
    'banheiro_porta': dict(esq=(380, 1040, 1.05), dir=(1540, 1040, 1.05)),
    'cama_duda': dict(deitado=(1250, 625, 0.85), lado=(400, 1000, 0.9)),
    'corredor_vo': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'corredor_vo_manha': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'quarto_bento': dict(cama=(540, 765, 0.9), porta=(875, 960, 0.95), centro=(1000, 1000, 1.0), dir=(1560, 1000, 0.95)),
    'varanda': dict(a=(520, 1010, 1.0), porta=(960, 940, 0.95), b=(1500, 1010, 1.0)),
    'varanda_manha': dict(a=(520, 1010, 1.0), porta=(960, 940, 0.95), b=(1500, 1010, 1.0)),
    'varanda_jaqueta': dict(a=(520, 1010, 1.0), porta=(960, 940, 0.95), b=(1500, 1010, 1.0)),
    'porta_manha': dict(a=(500, 1010, 1.0), porta=(960, 1000, 1.0), b=(1500, 1010, 1.0)),
    'porta_fita': dict(a=(500, 1010, 1.0), porta=(960, 1000, 1.0), b=(1500, 1010, 1.0)),
    'quarto_costura': dict(cama=(1580, 810, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'quarto_costura_vazio': dict(cama=(1580, 810, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'cozinha_vo': dict(a=(520, 1010, 0.95), b=(1100, 1010, 0.95), porta=(1450, 990, 0.95)),
    'cozinha_vo_aberta': dict(a=(520, 1010, 0.95), b=(1100, 1010, 0.95), porta=(1450, 990, 0.95)),
    'cozinha_vo_manha': dict(a=(520, 1010, 0.95), b=(1100, 1010, 0.95), porta=(1450, 990, 0.95)),
    'terreiro': dict(a=(560, 1010, 0.95), b=(960, 1010, 0.95), c=(1400, 1010, 0.95)),
    'terreiro_manha': dict(a=(560, 1010, 0.95), b=(960, 1010, 0.95), c=(1400, 1010, 0.95)),
    'terreiro_chinelo': dict(a=(560, 1010, 0.95), b=(960, 1010, 0.95), c=(1400, 1010, 0.95)),
    'cozinha_cafe': dict(a=(470, 1000, 0.95), b=(1400, 1010, 0.95), c=(960, 1010, 0.95), mesa=(660, 960, 0.85), mesa2=(1290, 960, 0.85)),
    'cozinha_fria': dict(a=(470, 1000, 0.95), b=(1400, 1010, 0.95), c=(960, 1010, 0.95), mesa=(660, 960, 0.85), mesa2=(1290, 960, 0.85)),
    'cozinha_vazia': dict(a=(470, 1000, 0.95), b=(1400, 1010, 0.95), c=(960, 1010, 0.95), mesa=(660, 960, 0.85), mesa2=(1290, 960, 0.85)),
    'cozinha_manha': dict(a=(470, 1000, 0.95), b=(1400, 1010, 0.95), c=(960, 1010, 0.95), mesa=(660, 960, 0.85), mesa2=(1290, 960, 0.85)),
    'cozinha_domingo': dict(a=(470, 1000, 0.95), b=(1400, 1010, 0.95), c=(960, 1010, 0.95), mesa=(660, 960, 0.85), mesa2=(1290, 960, 0.85)),
    'corredor_cafe': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'corredor_xicara': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'corredor_mancha': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'corredor_frio': dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95)),
    'quarto_cafe': dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'quarto_toalha': dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
    'quarto_cafe_manha': dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0)),
}


# ---------------------------------------------------------------- a irmã que pede pra dormir no seu quarto (noite 09)
def trinco(ctx, x, y, fechado=True):
    """trinco de porta (ferrolho) visto de frente; x,y = canto esquerdo da chapa"""
    lr(ctx, x, y, 70, 26, fill='#3A3A40', r=4)
    lr(ctx, x + (34 if fechado else 6), y + 6, 46, 14, fill='#8A8A90', r=4)
    ctx.arc(x + 20, y + 13, 7, 0, TAU); ctx.set_source_rgba(*LINE); ctx.fill()


def estrelinhas(ctx, x, y, w, h, n=9, seed=9, a=0.85):
    rnd = random.Random(seed)
    for k in range(n):
        star(ctx, x + rnd.uniform(0, w), y + rnd.uniform(0, h), rnd.uniform(9, 15), '#C9E6B8')


def luz_estrela(ctx, x, y, t, a=0.4):
    """luzinha de tomada em forma de estrela, com o brilho em volta"""
    amber(ctx, x, y, 190, a, t)
    star(ctx, x, y, 22, '#FFD27A')


def bg_mm_quarto_trinco(ctx, t, manha=False, aberta=False):
    """o seu quarto: a porta com trinco (fechado), a cama encostada na parede do quarto da Larinha (estrelinhas que
    ela colou na cabeceira), a janela; aberta=True: a porta destrancada e entreaberta com a luz da manhã"""
    mm_room(ctx)
    moon_window(ctx, 220, 160, 300, 280)
    if aberta:
        door(ctx, 760, 260, 230, 540, open_frac=0.45)
        g = cairo.LinearGradient(760, 0, 990, 0)
        g.add_color_stop_rgba(0, 0.75, 0.8, 0.9, 0.0); g.add_color_stop_rgba(1, 0.75, 0.8, 0.9, 0.18)
        ctx.rectangle(760 + 230 * 0.55, 260, 230 * 0.45, 540); ctx.set_source(g); ctx.fill()
    else:
        door(ctx, 760, 260, 230, 540)
        trinco(ctx, 900, 470, fechado=True)
    bed(ctx, 1180, 780, 640, made=False)
    estrelinhas(ctx, 1200, 440, 560, 150, n=10, seed=4)
    lr(ctx, 1060, 640, 100, 160, r=6)
    lr(ctx, 1085, 560, 50, 80, fill='#2C2C30')
    ctx.move_to(1070, 560); ctx.line_to(1150, 560); ctx.line_to(1130, 520); ctx.line_to(1090, 520); ctx.close_path()
    setc(ctx, '#3A3A40'); ctx.fill()
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.13); ctx.fill()


def bg_mm_corredor_irma(ctx, t, luz=True, manha=False):
    """corredor: a sua porta (esq., 240), a porta da Larinha (meio, 820) com a plaquinha e o brilho da luzinha de estrela
    por baixo, e o quarto dos pais no fundo (dir., 1400), fechado, com o barulho do ventilador"""
    mm_room(ctx, fy=820)
    door(ctx, 240, 280, 240, 540)
    door(ctx, 820, 280, 240, 540)
    door(ctx, 1400, 280, 240, 540)
    lr(ctx, 855, 355, 170, 56, fill='#1E1E22', r=10)                     # plaquinha da porta da Larinha
    star(ctx, 878, 383, 11, '#C9E6B8'); star(ctx, 1002, 383, 11, '#C9E6B8')
    text(ctx, 'LARA', 940, 395, 26, col='#9A9AA0')
    if luz:
        g = cairo.LinearGradient(0, 812, 0, 880)
        g.add_color_stop_rgba(0, 1, 0.8, 0.45, 0.4); g.add_color_stop_rgba(1, 1, 0.8, 0.45, 0)
        ctx.rectangle(800, 814, 280, 66); ctx.set_source(g); ctx.fill()
    for x in (630, 1210):
        ctx.arc(x, 380, 18, 0, TAU); ctx.set_source_rgba(0.5, 0.5, 0.52, 0.6); ctx.fill()
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.14); ctx.fill()


def bg_mm_quarto_lara(ctx, t, vazio=False, manha=False):
    """quarto da Larinha: cama baixa à esquerda, a luzinha de estrela na tomada, ursinho, desenhos colados na parede;
    vazio=True: a cama desarrumada e vazia, a luzinha apagada"""
    mm_room(ctx, wall_c='#131418')
    moon_window(ctx, 1420, 170, 280, 260)
    door(ctx, 760, 260, 230, 540, open_frac=0.2)
    for k, (x, y) in enumerate(((180, 300), (380, 260), (1110, 330))):  # desenhos colados na parede
        lr(ctx, x, y, 150, 110, fill='#1C1C20', r=3)
        ctx.set_source_rgba(0.6, 0.6, 0.64, 0.7); ctx.set_line_width(3)
        ctx.arc(x + 45, y + 40, 18, 0, TAU); ctx.stroke()
        ctx.move_to(x + 20, y + 95); ctx.line_to(x + 75, y + 60); ctx.line_to(x + 130, y + 95); ctx.stroke()
    bed(ctx, 140, 800, 560, made=vazio)
    if not vazio:
        luz_estrela(ctx, 1080, 720, t)
    else:
        star(ctx, 1080, 720, 22, '#4A4A50')
    lr(ctx, 1150, 690, 210, 110, fill=DARK3, r=8)                         # baú de brinquedos
    ctx.arc(1300, 650, 40, 0, TAU); setc(ctx, '#3A3A40'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.stroke()   # ursinho
    for dx in (-28, 28):
        ctx.arc(1300 + dx, 614, 14, 0, TAU); setc(ctx, '#3A3A40'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.stroke()
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.14); ctx.fill()


BG.update({
    'quarto_trinco': (bg_mm_quarto_trinco, None),
    'quarto_trinco_manha': (lambda c, t: bg_mm_quarto_trinco(c, t, manha=True, aberta=True), None),
    'quarto_trinco_alvorada': (lambda c, t: bg_mm_quarto_trinco(c, t, manha=True), None),
    'corredor_irma': (bg_mm_corredor_irma, None),
    'corredor_irma_escuro': (lambda c, t: bg_mm_corredor_irma(c, t, luz=False), None),
    'corredor_irma_manha': (lambda c, t: bg_mm_corredor_irma(c, t, manha=True), None),
    'quarto_lara': (bg_mm_quarto_lara, None),
    'quarto_lara_vazio': (lambda c, t: bg_mm_quarto_lara(c, t, vazio=True), None),
})
_Q = dict(cama=(1420, 830, 0.95), porta=(875, 960, 0.95), centro=(560, 1000, 1.0))
_C = dict(p1=(360, 1000, 0.9), p2=(940, 1000, 0.9), p3=(1520, 1000, 0.9), meio=(650, 1010, 0.95), dir=(1250, 1010, 0.95))
_L = dict(cama=(540, 765, 0.9), porta=(875, 960, 0.95), centro=(1000, 1000, 1.0), dir=(1560, 1000, 0.95))
SLOTS.update({'quarto_trinco': dict(_Q), 'quarto_trinco_manha': dict(_Q), 'quarto_trinco_alvorada': dict(_Q), 'corredor_irma': dict(_C),
              'corredor_irma_escuro': dict(_C), 'corredor_irma_manha': dict(_C), 'quarto_lara': dict(_L),
              'quarto_lara_vazio': dict(_L)})


# ---------------------------------------------------------------- o tio que ninguém convidou (noite 10)
def lencol_sofa(ctx, x, y, w, dobrado=False):
    """lençol e travesseiro arrumados no sofá (cama de visita); dobrado=True: lençol dobrado em cima do braço"""
    if dobrado:
        lr(ctx, x + w - 190, y - 52, 160, 46, fill='#3A3A40', r=8)
        lr(ctx, x + w - 180, y - 92, 140, 40, fill='#34343A', r=8)
        return
    ctx.move_to(x + 30, y - 10); ctx.curve_to(x + w * 0.4, y - 40, x + w * 0.7, y - 4, x + w - 20, y - 18)
    ctx.line_to(x + w - 10, y + 60); ctx.line_to(x + 20, y + 60); ctx.close_path()
    setc(ctx, '#3C3C42'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    lr(ctx, x + 40, y - 70, 170, 56, fill='#46464C', r=24)


def abajur(ctx, x, y, t, aceso=True):
    lr(ctx, x - 70, y, 140, 190, r=6)                                        # mesinha
    lr(ctx, x - 12, y - 90, 24, 90, fill='#2C2C30')
    ctx.move_to(x - 55, y - 90); ctx.line_to(x + 55, y - 90); ctx.line_to(x + 35, y - 160); ctx.line_to(x - 35, y - 160); ctx.close_path()
    setc(ctx, '#5A4A36' if aceso else '#3A3A40'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(3); ctx.stroke()
    if aceso:
        amber(ctx, x, y - 110, 420, 0.32, t)


def bg_mm_sala_tio(ctx, t, luz=True, manha=False, vazio=False):
    """sala da noite 10: à esquerda, o vão escuro do corredor (de onde se vê quem entra em que porta); no meio, o sofá
    arrumado com lençol e travesseiro de visita; o abajur aceso na mesinha; a porta de entrada à direita.
    vazio=True: o lençol dobrado em cima do braço do sofá (de manhã)"""
    mm_room(ctx)
    lr(ctx, 70, 200, 360, 600, fill='#060607')                              # vão do corredor
    ctx.set_source_rgba(*LINE); ctx.set_line_width(3)
    ctx.move_to(70, 800); ctx.line_to(200, 620); ctx.line_to(300, 620); ctx.line_to(430, 800); ctx.stroke()
    lr(ctx, 205, 380, 90, 240, fill='#0C0C0E')                               # porta lá no fundo do corredor
    moon_window(ctx, 540, 170, 240, 220)
    lr(ctx, 1640, 260, 200, 540, fill='#0E0E10')                             # porta de entrada
    ctx.arc(1810, 540, 9, 0, TAU); ctx.set_source_rgba(*LINE); ctx.fill()
    lr(ctx, 780, 600, 640, 140, r=30)                                        # sofá
    lr(ctx, 780, 520, 640, 110, r=30)
    lr(ctx, 740, 560, 70, 190, r=22); lr(ctx, 1390, 560, 70, 190, r=22)      # braços
    lencol_sofa(ctx, 820, 620, 560, dobrado=vazio)
    abajur(ctx, 1550, 610, t, aceso=luz and not manha)
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.13); ctx.fill()


def bg_mm_corredor_tio(ctx, t, luz=True, manha=False):
    """corredor da noite 10: banheiro (esq., 240), o SEU quarto (meio, 820) e o quarto dos pais (fundo, 1400), três
    portas iguais; a luz do abajur da sala chega fraca pela esquerda"""
    mm_room(ctx, fy=820)
    for x in (240, 820, 1400):
        door(ctx, x, 280, 240, 540)
    for x in (630, 1210):
        ctx.arc(x, 380, 18, 0, TAU); ctx.set_source_rgba(0.5, 0.5, 0.52, 0.6); ctx.fill()
    if luz:
        g = cairo.LinearGradient(0, 0, 900, 0)
        g.add_color_stop_rgba(0, 1, 0.72, 0.3, 0.22); g.add_color_stop_rgba(1, 1, 0.72, 0.3, 0)
        ctx.rectangle(0, 0, 900, H); ctx.set_source(g); ctx.fill()
    if manha:
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.55, 0.62, 0.75, 0.14); ctx.fill()


def caixas(ctx, x, y, seed=3):
    rnd = random.Random(seed)
    for k, (dx, dy, w, h) in enumerate(((0, 0, 220, 150), (230, 0, 180, 150), (30, -130, 180, 130), (240, -110, 150, 110), (90, -240, 160, 110))):
        lr(ctx, x + dx, y - h + dy, w, h, fill=rnd.choice(('#2A2824', '#262420', '#2E2B26')), r=3)
        ctx.set_source_rgba(0.6, 0.6, 0.64, 0.5); ctx.set_line_width(3)
        ctx.move_to(x + dx + w / 2, y - h + dy); ctx.line_to(x + dx + w / 2, y + dy - h * 0.55); ctx.stroke()


def bg_mm_quartinho(ctx, t, arrumado=True):
    """quartinho dos fundos (de despejo): caixas empilhadas, ventilador velho, lâmpada pelada; arrumado=True: a cama de
    armar montada, com lençol esticado e o chinelo do lado — ninguém da casa arrumou"""
    mm_room(ctx, wall_c='#121212')
    door(ctx, 760, 260, 230, 540, open_frac=0.25)
    caixas(ctx, 120, 800)
    lr(ctx, 1640, 520, 30, 280, fill='#2C2C30')                              # ventilador velho
    ctx.arc(1655, 470, 70, 0, TAU); setc(ctx, '#1E1E22'); ctx.fill_preserve(); ctx.set_source_rgba(*LINE); ctx.set_line_width(4); ctx.stroke()
    ctx.set_source_rgba(*LINE); ctx.set_line_width(3)
    ctx.move_to(1180, 0); ctx.line_to(1180, 120); ctx.stroke()              # fio da lâmpada
    ctx.arc(1180, 140, 20, 0, TAU); ctx.set_source_rgba(1, 0.8, 0.45, 0.9 if arrumado else 0.3); ctx.fill()
    if arrumado:
        amber(ctx, 1180, 140, 520, 0.3, t, flick=True)
        lr(ctx, 1080, 740, 520, 60, fill='#3A3A40', r=10)                     # cama de armar com lençol
        lr(ctx, 1100, 700, 150, 44, fill='#46464C', r=18)
        for x in (1100, 1560):
            ctx.set_source_rgba(*LINE); ctx.set_line_width(5)
            ctx.move_to(x, 800); ctx.line_to(x + 30, 860); ctx.stroke()
        chinelo(ctx, 1400, 900, 0.9)
        from .chars import draw_prop
        draw_prop(ctx, 'mala', 1660, 780, -1)                                  # a mala vermelha, vazia
    else:
        lr(ctx, 1100, 520, 60, 280, fill='#2A2A2E', r=6)                      # cama de armar fechada, encostada


BG.update({
    'sala_tio': (bg_mm_sala_tio, None),
    'sala_tio_escuro': (lambda c, t: bg_mm_sala_tio(c, t, luz=False), None),
    'sala_tio_manha': (lambda c, t: bg_mm_sala_tio(c, t, manha=True, vazio=True), None),
    'corredor_tio': (bg_mm_corredor_tio, None),
    'corredor_tio_escuro': (lambda c, t: bg_mm_corredor_tio(c, t, luz=False), None),
    'corredor_tio_manha': (lambda c, t: bg_mm_corredor_tio(c, t, manha=True), None),
    'quartinho': (bg_mm_quartinho, None),
    'quarto_manha': (lambda c, t: (bg_mm_quarto(c, t), c.rectangle(0, 0, W, H), c.set_source_rgba(0.55, 0.62, 0.75, 0.13), c.fill()), None),
    'quartinho_caixas': (lambda c, t: bg_mm_quartinho(c, t, arrumado=False), None),
})
_ST = dict(visita=(1100, 860, 0.72), sofa=(1100, 860, 0.9), corredor=(250, 990, 0.85), centro=(560, 1000, 0.95), porta=(1740, 990, 0.9))
_QT = dict(cama=(1330, 790, 0.9), porta=(875, 960, 0.95), centro=(560, 1000, 1.0))
SLOTS.update({'sala_tio': dict(_ST), 'sala_tio_escuro': dict(_ST), 'sala_tio_manha': dict(_ST),
              'corredor_tio': dict(_C), 'corredor_tio_escuro': dict(_C), 'corredor_tio_manha': dict(_C),
              'quartinho': dict(_QT), 'quarto_manha': dict(_Q), 'quartinho_caixas': dict(_QT)})
