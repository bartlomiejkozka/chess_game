import string
import time

import render.Render as Render
from chess.Board import Board


def printMoves(moves, board):
    for move in moves:
        print(f"{board.FromNumber(move.src)}{board.FromNumber(move.dst)}", end=", ")
    print()


def playFirstPossibleMoves(depth, board, renderer=None, delay=0.5):
    if depth == 0: 
        return 1
    
    moves = board.legal_moves()
    numPositions = 0

    for move in moves:
        board.move(move.src, move.dst)

        if depth == 2:
            # Dla każdego ruchu białych — liczymy liczbę odpowiedzi czarnych
            childPositions = playFirstPossibleMoves(depth - 1, board, renderer, delay)
            print(f"{board.FromNumber(move.src)}{board.FromNumber(move.dst)}: {childPositions}")
            numPositions += childPositions
        else:
            numPositions += playFirstPossibleMoves(depth - 1, board, renderer, delay)

        board.undoMove()

    return numPositions


def main():
    Board1 = Board(fen_notation="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # play(Board1, Board1.board)
    # game = Render.Render(720 + 100, Board1)
    # game.render(Board1)
    numPositions = playFirstPossibleMoves(2, Board1, delay=0.01)
    print(f"Num positions: {numPositions}")
    print(Board1.parameters["nodes"])


if __name__ == "__main__":
    main()