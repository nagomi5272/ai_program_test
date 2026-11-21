# ai_program_test

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/nagomi5272/ai_program_test/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/nagomi5272/ai_program_test/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in a single `main.py` (at most 4,096 bytes, Python 3.13,
standard library only), built for the make.fun bounty "tiny-chess-01".

It plays through the tournament environment over HTTP: it asks the env
for the game in play, reads the FEN and the list of legal moves, and
answers one move at a time until the env reports the game is done.

Move choice is a one-ply net-gain search: for each legal move it scores
the value of the piece it captures minus the value of the best capture
the opponent can answer with, and plays the highest score. Ties break
by promotion value, then by the cheaper moving piece, then by UCI
order. The engine never reads a clock and uses no randomness, so the
same position always gets the same move.

Piece values: pawn 1, knight 3, bishop 3, rook 5, queen 9.
En passant captures are handled.

License: MIT (see LICENSE).

## Run it

```sh
MAKEFUN_ENV_URL=<env-url> python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
