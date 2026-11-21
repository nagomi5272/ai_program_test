import json, os, urllib.request

V = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 0, "": 0}
N = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
O = ((1,0),(-1,0),(0,1),(0,-1))
D = ((1,1),(1,-1),(-1,1),(-1,-1))
K = O + D

def post(url, body):
  req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json"}, method="POST")
  with urllib.request.urlopen(req) as r:
    return json.loads(r.read())

def parse_fen(fen):
  ps = fen.split()
  b, r = {}, 7
  for row in ps[0].split("/"):
    c = 0
    for ch in row:
      if ch.isdigit(): c += int(ch)
      else: b[(r, c)] = ch; c += 1
    r -= 1
  ep = None if len(ps) < 4 or ps[3] == "-" else (int(ps[3][1]) - 1, ord(ps[3][0]) - 97)
  return b, len(ps) < 2 or ps[1] == "w", ep

def attacked(b, sq, w):
  r, c = sq
  p, pr = ("P", r - 1) if w else ("p", r + 1)
  if b.get((pr, c - 1)) == p or b.get((pr, c + 1)) == p:
    return True
  for ds, ch in ((N, "N" if w else "n"), (K, "K" if w else "k")):
    if any(b.get((r + dr, c + dc)) == ch for dr, dc in ds):
      return True
  for ds, pcs in ((O, "RQ" if w else "rq"), (D, "BQ" if w else "bq")):
    for dr, dc in ds:
      nr, nc = r + dr, c + dc
      while 0 <= nr < 8 and 0 <= nc < 8:
        t = b.get((nr, nc))
        if t:
          if t in pcs: return True
          break
        nr += dr; nc += dc
  return False

def opp_max(b, w, ep):
  ok = "K" if w else "k"
  ksq = next((s for s, p in b.items() if p == ok), None)
  best = 0
  def chk(src, dst, p, val, epc=None):
    nonlocal best
    if val <= best: return
    tb = b.copy()
    del tb[src]
    if epc: tb.pop(epc, None)
    tb[dst] = p
    nk = dst if p == ok else ksq
    if nk is None or not attacked(tb, nk, not w): best = val
  for (r, c), p in b.items():
    if p.isupper() != w: continue
    pt = p.lower()
    if pt == "p":
      nr = r + (1 if w else -1)
      for dc in (-1, 1):
        nc = c + dc
        t = b.get((nr, nc))
        if t and t.isupper() != w: chk((r, c), (nr, nc), p, V[t.lower()])
        elif ep == (nr, nc) and b.get((r, nc)) == ("p" if w else "P"): chk((r, c), (nr, nc), p, 1, (r, nc))
    elif pt in "nk":
      for dr, dc in (N if pt == "n" else K):
        t = b.get((r + dr, c + dc))
        if t and t.isupper() != w: chk((r, c), (r + dr, c + dc), p, V[t.lower()])
    else:
      for dr, dc in (O if pt == "r" else D if pt == "b" else K):
        nr, nc = r + dr, c + dc
        while 0 <= nr < 8 and 0 <= nc < 8:
          t = b.get((nr, nc))
          if t:
            if t.isupper() != w: chk((r, c), (nr, nc), p, V[t.lower()])
            break
          nr += dr; nc += dc
    if best == 9: break
  return best

def move_key(b, w, ep, mv):
  sr, sc, dr, dc = int(mv[1]) - 1, ord(mv[0]) - 97, int(mv[3]) - 1, ord(mv[2]) - 97
  pr = mv[4:5].lower()
  nb = b.copy()
  m = nb.pop((sr, sc), "")
  t = nb.get((dr, dc), "")
  if t and m and m.isupper() != t.isupper(): cap = V[t.lower()]
  elif m.lower() == "p" and ep == (dr, dc) and sc != dc: cap = 1; nb.pop((sr, dc), None)
  else: cap = 0
  if m.lower() == "k" and abs(dc - sc) == 2:
    rf, rt = (7, 5) if dc > sc else (0, 3)
    if (sr, rf) in nb: nb[(sr, rt)] = nb.pop((sr, rf))
  nb[(dr, dc)] = (pr.upper() if m.isupper() else pr) if pr else m
  nep = ((sr + dr) // 2, sc) if m.lower() == "p" and abs(dr - sr) == 2 else None
  return (opp_max(nb, not w, nep) - cap, -V[pr], V[m.lower()] if cap else 0, mv)

def choose_move(fen, legal_moves):
  b, w, ep = parse_fen(fen)
  return min(legal_moves, key=lambda m: move_key(b, w, ep, m))

def main():
  base = os.environ["MAKEFUN_ENV_URL"].rstrip("/")
  st = post(base + "/game", {})
  while st.get("status") != "done":
    if st.get("status") != "your_move": break
    mvs = st.get("legal_moves") or []
    if not mvs: break
    st = post(base + "/move", {"game": st["game"], "move": choose_move(st["fen"], mvs)})
    if st.get("status") not in ("your_move", "done"): st = post(base + "/game", {})

if __name__ == "__main__":
  main()
