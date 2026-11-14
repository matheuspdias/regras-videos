"""Foto de perfil (800x800) e banner (2560x1440) do canal Manual da Madrugada."""
import cairo
from .chars import draw_char, Pose
from .render import rich_text


def bg(ctx, w, h):
    ctx.rectangle(0, 0, w, h); ctx.set_source_rgba(0.03, 0.03, 0.035, 1); ctx.fill()
    g = cairo.RadialGradient(w / 2, h / 2, 0, w / 2, h / 2, max(w, h) * 0.6)
    g.add_color_stop_rgba(0, 0.12, 0.12, 0.14, 1); g.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 1)
    ctx.rectangle(0, 0, w, h); ctx.set_source(g); ctx.fill()


def door(ctx, dx, dy, dw, dh, lw, cid_scale, cx_off):
    """porta entreaberta com a criatura espiando"""
    ctx.rectangle(dx, dy, dw, dh); ctx.set_source_rgba(0.0, 0.0, 0.0, 1); ctx.fill()
    ctx.save(); ctx.rectangle(dx, dy, dw, dh); ctx.clip()
    draw_char(ctx, 'coisa', dx + cx_off, dy + dh + 10 * cid_scale, cid_scale,
              Pose(mouth='grin', facing=-1, arms='down'))
    ctx.restore()
    hinge = dx + dw * 0.42
    ctx.rectangle(hinge, dy, dx + dw - hinge, dh); ctx.set_source_rgba(0.14, 0.14, 0.16, 1); ctx.fill()
    ctx.set_source_rgba(0.85, 0.85, 0.88, 1); ctx.set_line_width(lw)
    ctx.rectangle(dx, dy, dw, dh); ctx.stroke()
    ctx.move_to(hinge, dy); ctx.line_to(hinge, dy + dh); ctx.stroke()
    ctx.arc(dx + dw - dw * 0.12, dy + dh * 0.55, lw * 0.9, 0, 6.3); ctx.fill()


def avatar(out):
    S = 800
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S, S); ctx = cairo.Context(surf)
    bg(ctx, S, S)
    door(ctx, 190, 70, 420, 820, 12, 1.15, 125)
    surf.write_to_png(out)


def banner(out):
    Wb, Hb = 2560, 1440
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, Wb, Hb); ctx = cairo.Context(surf)
    bg(ctx, Wb, Hb)
    cx, cy = Wb / 2, Hb / 2           # área segura: 1546x423 (y 508..931)
    floor = cy + 205
    ctx.set_source_rgba(0.75, 0.75, 0.78, 1); ctx.set_line_width(5)
    ctx.move_to(0, floor); ctx.line_to(Wb, floor); ctx.stroke()
    # luminárias do corredor
    for x in (cx - 1150, cx + 1150):
        g = cairo.RadialGradient(x, cy - 120, 0, x, cy - 120, 110)
        g.add_color_stop_rgba(0, 1, 0.72, 0.3, 0.55); g.add_color_stop_rgba(1, 1, 0.6, 0.2, 0)
        ctx.arc(x, cy - 120, 110, 0, 6.3); ctx.set_source(g); ctx.fill()
        ctx.arc(x, cy - 120, 16, 0, 6.3); ctx.set_source_rgba(1, 0.75, 0.35, 1); ctx.fill()
    # protagonista com medo (esq.) e criatura na porta (dir.)
    draw_char(ctx, 'voce', cx - 880, floor + 8, 0.62,
              Pose(eyes='wide', mouth='o', arms='face', sweat=True, facing=1))
    door(ctx, cx + 700, cy - 230, 230, 435, 6, 0.6, 70)
    ctx.select_font_face('Poppins', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    rich_text(ctx, 'MANUAL DA **MADRUGADA**', cx - 30, cy - 10, 96)
    ctx.set_font_size(40); ctx.set_source_rgba(0.82, 0.82, 0.85, 1)
    for msg, y in (('regras para sobreviver até o amanhecer', cy + 70),):
        e = ctx.text_extents(msg); ctx.move_to(cx - 30 - e.x_advance / 2, y); ctx.show_text(msg)
    tag = 'UMA NOITE NOVA TODO DIA'
    ctx.set_font_size(30); e = ctx.text_extents(tag)
    from .chars import rrect
    rrect(ctx, cx - 30 - e.x_advance / 2 - 30, cy + 105, e.x_advance + 60, 54, 27)
    ctx.set_source_rgba(0.9, 0.15, 0.17, 1); ctx.fill()
    ctx.move_to(cx - 30 - e.x_advance / 2, cy + 143); ctx.set_source_rgba(1, 1, 1, 1); ctx.show_text(tag)
    surf.write_to_png(out)


if __name__ == '__main__':
    avatar('build/brand_avatar.png')
    banner('build/brand_banner.png')
