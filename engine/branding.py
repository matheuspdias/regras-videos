"""Foto de perfil (800x800) e banner (2560x1440) do canal Já Pensou?"""
import math
import cairo
from .chars import draw_char, Pose, TAU
from .scenes import text
from .render import neon_bar, heart


def bg(ctx, w, h):
    g = cairo.LinearGradient(0, 0, w, h)
    g.add_color_stop_rgb(0, 0.23, 0.05, 0.64)
    g.add_color_stop_rgb(1, 0.45, 0.04, 0.72)
    ctx.rectangle(0, 0, w, h); ctx.set_source(g); ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.06)
    for i in range(-20, 40):
        ctx.move_to(i * 120, 0); ctx.line_to(i * 120 - h, h); ctx.set_line_width(30); ctx.stroke()


def avatar(out):
    S = 800
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S, S); ctx = cairo.Context(surf)
    bg(ctx, S, S)
    # ponto de interrogação neon atrás
    text(ctx, '?', 590, 250, 210, '#FFD23F', outline='#2B0A4A', lw=16)
    draw_char(ctx, 'voce', 400, 1030, 1.4, Pose(eyes='wide', mouth='smile', arms='face', look=0.6))
    surf.write_to_png(out)


def banner(out):
    Wb, Hb = 2560, 1440
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, Wb, Hb); ctx = cairo.Context(surf)
    bg(ctx, Wb, Hb)
    # área segura: 1546x423 no centro (y 508..931)
    cx, cy = Wb / 2, Hb / 2
    text(ctx, 'JÁ PENSOU?', cx, cy + 20, 150, '#FFFFFF', outline='#2B0A4A', lw=22)
    text(ctx, 'e se você pudesse...?', cx, cy + 105, 50, '#FFD23F', outline='#2B0A4A', lw=10)
    text(ctx, 'vídeo novo todo dia', cx, cy + 170, 40, '#FFFFFF')
    draw_char(ctx, 'voce', cx - 600, cy + 300, 0.7, Pose(eyes='wide', mouth='o', arms='face', sweat=True))
    b = draw_char(ctx, 'bia', cx + 600, cy + 300, 0.68, Pose(eyes='happy', mouth='smile', blush=True, facing=-1))
    neon_bar(ctx, b['top'][0], b['top'][1] - 45, 0.85, 58)
    for k in range(9):
        heart(ctx, cx - 1100 + k * 270, cy - 360 + (k % 3) * 40, 22, (1, 0.35, 0.65, 0.5))
    surf.write_to_png(out)


if __name__ == '__main__':
    avatar('build/brand_avatar.png')
    banner('build/brand_banner.png')
