import pytest
from chess.Board import Board
from enum import Enum

# Excpected parameters values of different starting positions
# See https://www.chessprogramming.org/Perft_Results
# For current needs only depth level: 1,2
class InitialPosition(Enum):
    FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    NODES = {1: 20, 2: 400}
    CAPUTERS = {1: 0, 2: 0}
    E_P = {1: 0, 2: 0}
    CASTLES = {1: 0, 2: 0}
    PROMOTIONS = {1: 0, 2: 0}
    CHECKS = {1: 0, 2: 0}
    CHECKMATES = {1: 0, 2: 0}
class Position2(Enum):
    FEN = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1"
    NODES = {1: 48, 2: 2039}
    CAPUTERS = {1: 8, 2: 351}
    E_P = {1: 0, 2: 1}
    CASTLES = {1: 2, 2: 91}
    PROMOTIONS = {1: 0, 2: 0}
    CHECKS = {1: 0, 2: 3}
    CHECKMATES = {1: 0, 2: 0}
class Position3(Enum):
    FEN = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
    NODES = {1: 14, 2: 191}
    CAPUTERS = {1: 1, 2: 14}
    E_P = {1: 0, 2: 0}
    CASTLES = {1: 0, 2: 0}
    PROMOTIONS = {1: 0, 2: 0}
    CHECKS = {1: 2, 2: 10}
    CHECKMATES = {1: 0, 2: 0}


def playMoves(depth, board):
    if depth == 0: 
        return 1
    
    moves = board.legal_moves()
    numPositions = 0

    for move in moves:
        board.move(move.src, move.dst)

        numPositions += playMoves(depth - 1, board)

        board.undoMove()

    return numPositions


class TestChessMoves:
    def test_initial_position(self):
        board = Board(fen_notation=InitialPosition.FEN.value)
        assert playMoves(1, board) == InitialPosition.NODES.value[1]
        assert playMoves(2, board) == InitialPosition.NODES.value[2]
        assert board.parameters["captures"] == InitialPosition.CAPUTERS.value[1]
        assert board.parameters["E.p"] == InitialPosition.E_P.value[1]
        assert board.parameters["castles"] == InitialPosition.CASTLES.value[1]
        # assert board.parameters["promotions"] == InitialPosition.PROMOTIONS.value[1]
        assert board.parameters["checks"] == InitialPosition.CHECKS.value[1]
        assert board.parameters["checkmates"] == InitialPosition.CHECKMATES.value[1]

    def test_position_2(self):
        board = Board(fen_notation=Position2.FEN.value)
        assert playMoves(1, board) == Position2.NODES.value[1]
        assert playMoves(2, board) == Position2.NODES.value[2]
        assert board.parameters["captures"] == Position2.CAPUTERS.value[1]
        assert board.parameters["E.p"] == Position2.E_P.value[1]
        assert board.parameters["castles"] == Position2.CASTLES.value[1]
        # assert board.parameters["promotions"] == Position2.PROMOTIONS.value[1]
        assert board.parameters["checks"] == Position2.CHECKS.value[1]
        assert board.parameters["checkmates"] == Position2.CHECKMATES.value[1]

    def test_position_3(self):
        board = Board(fen_notation=Position3.FEN.value)
        assert playMoves(1, board) == Position3.NODES.value[1]
        assert playMoves(2, board) == Position3.NODES.value[2]
        assert board.parameters["captures"] == Position3.CAPUTERS.value[1]
        assert board.parameters["E.p"] == Position3.E_P.value[1]
        assert board.parameters["castles"] == Position3.CASTLES.value[1]
        # assert board.parameters["promotions"] == Position3.PROMOTIONS.value[1]
        assert board.parameters["checks"] == Position3.CHECKS.value[1]
        assert board.parameters["checkmates"] == Position3.CHECKMATES.value[1]