import pytest
import chess

def test_first_moves(depth):
    board = chess.Board()

    starting_pos = []
    for y in range(0, 2):
        for x in range(0, 8):
            starting_pos.append((x, y))

    for sp in starting_pos:
        pass