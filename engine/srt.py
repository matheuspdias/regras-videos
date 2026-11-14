"""Gera legenda .srt a partir da linha do tempo do episódio (texto exato do roteiro)."""
import re
import sys
from .render import build


def fmt(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}'.replace(',1000', ',999')


def chunks(text, maxlen=84):
    """quebra em blocos de até ~2 linhas de 42 caracteres, preferindo fim de frase."""
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    out = []
    for s in sents:
        words = s.split()
        cur = ''
        for w in words:
            if len(cur) + len(w) + 1 > maxlen and cur:
                out.append(cur)
                cur = w
            else:
                cur = (cur + ' ' + w).strip()
        if cur:
            out.append(cur)
    return out


def two_lines(s, width=42):
    if len(s) <= width:
        return s
    words = s.split()
    best = None
    for i in range(1, len(words)):
        a, b = ' '.join(words[:i]), ' '.join(words[i:])
        score = max(len(a), len(b))
        if best is None or score < best[0]:
            best = (score, a, b)
    return best[1] + '\n' + best[2]


def main(ep_mod, ep_id, out):
    ep, clips, shots, total = build(ep_mod, ep_id)
    n = 1
    lines = []
    for c in clips:
        txt = re.sub(r'\[[a-z ]+\]\s*', '', c['text'])
        parts = chunks(txt)
        total_chars = sum(len(p) for p in parts)
        t = c['t0']
        dur = c['t1'] - c['t0']
        for p in parts:
            d = dur * len(p) / total_chars
            lines.append(f'{n}\n{fmt(t)} --> {fmt(t + d)}\n{two_lines(p)}\n')
            n += 1
            t += d
    open(out, 'w', encoding='utf-8').write('\n'.join(lines))
    print(out, n - 1)


if __name__ == '__main__':
    main(*sys.argv[1:4])
