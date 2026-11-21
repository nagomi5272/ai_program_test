# tiny-chess-01 entry

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
