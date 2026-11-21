import json, os, sys, urllib.error, urllib.request

ENV_URL = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
V = {"p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 20000}
CTR = {"d4": 25, "e4": 25, "d5": 25, "e5": 25, "c3": 12, "f3": 12, "c6": 12, "f6": 12, "c4": 15, "f4": 15, "c5": 15, "f5": 15}
DIRS = {"n":[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],"b":[(-1,-1),(-1,1),(1,-1),(1,1)],"r":[(-1,0),(1,0),(0,-1),(0,1)],"q":[(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)],"k":[(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]}

def post(path, body):
    req = urllib.request.Request(ENV_URL + path, data=json.dumps(body).encode(), headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        sys.exit(f"{path}: HTTP {e.code} {e.read().decode(errors='replace')}")

def parse(fen):
    b = {}
    for i, row in enumerate(fen.split()[0].split("/")):
        f = 0
        for c in row:
            if c.isdigit(): f += int(c)
            else: b["abcdefgh"[f] + str(8 - i)] = c; f += 1
    return b

def attacked(b, sq, by_white):
    fc, rk = ord(sq[0]) - 97, int(sq[1])
    pd = -1 if by_white else 1
    for df in (-1, 1):
        p = b.get(chr(97 + fc + df) + str(rk + pd))
        if p == ("P" if by_white else "p"): return True
    for pt, ds in DIRS.items():
        slide = pt in "brq"
        for df, dr in ds:
            nf, nr = fc + df, rk + dr
            while 0 <= nf < 8 and 1 <= nr <= 8:
                t = b.get(chr(97 + nf) + str(nr))
                if t:
                    if t.isupper() == by_white and t.lower() == pt: return True
                    break
                if not slide: break
                nf += df; nr += dr
    return False

def eval_board(b, white):
    sc = 0
    for sq, p in b.items():
        v = V[p.lower()] + CTR.get(sq, 0)
        if p.lower() == "p":
            r = int(sq[1])
            v += (r - 2) * 8 if p == "P" else (7 - r) * 8
        sc += v if p.isupper() == white else -v
    return sc

def choose(fen, legal):
    white = fen.split()[1] == "w"
    b = parse(fen)
    best_m, best_s = legal[0], -10**9
    for m in legal:
        nb = dict(b)
        p = nb.pop(m[:2])
        victim = nb.get(m[2:4])
        if victim is None and p.lower() == "p" and m[0] != m[2]:
            nb.pop(m[2] + m[1], None)
        nb[m[2:4]] = (m[4].upper() if white else m[4].lower()) if len(m) == 5 else p
        if p.lower() == "k" and abs(ord(m[0]) - ord(m[2])) == 2:
            rk = m[1]
            if m[2] == "g": nb["f" + rk] = nb.pop("h" + rk)
            else: nb["d" + rk] = nb.pop("a" + rk)
        sc = eval_board(nb, white)
        if attacked(nb, m[2:4], not white):
            sc -= int(V[nb[m[2:4]].lower()] * 0.75)
        if sc > best_s:
            best_s, best_m = sc, m
    return best_m

while True:
    g = post("/game", {})
    if g["status"] == "done": break
    while g["status"] == "your_move":
        g = post("/move", {"game": g["game"], "move": choose(g["fen"], g["legal_moves"])})
