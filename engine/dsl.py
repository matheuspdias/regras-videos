"""Helpers para escrever episódios: S (cena) e C (personagem na cena)."""


def S(bg, *cast, cam=None, fx=None):
    return dict(bg=bg, cast=list(cast), cam=cam or {}, fx=fx or [])


def C(cid, slot, bar=None, **pose):
    return (cid, slot, pose, bar)
