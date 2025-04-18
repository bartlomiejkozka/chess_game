import string
import Render
import time

import Board as b
from Board import ChessColor
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Pawn import Pawn


def printChessSymbol(cell):
    match cell:
        case None: return '.'
        case _ if isinstance(cell, King) and cell.color == ChessColor.WHITE: return '\u265A'
        case _ if isinstance(cell, Queen) and cell.color == ChessColor.WHITE: return '\u265B'
        case _ if isinstance(cell, Rook) and cell.color == ChessColor.WHITE: return '\u265C'
        case _ if isinstance(cell, Knight) and cell.color == ChessColor.WHITE: return '\u265E'
        case _ if isinstance(cell, Bishop) and cell.color == ChessColor.WHITE: return '\u265D'
        case _ if isinstance(cell, Pawn) and cell.color == ChessColor.WHITE: return '\u265F'

        case _ if isinstance(cell, King) and cell.color == ChessColor.BLACK: return '\u2654'
        case _ if isinstance(cell, Queen) and cell.color == ChessColor.BLACK: return '\u2655'
        case _ if isinstance(cell, Rook) and cell.color == ChessColor.BLACK: return '\u2656'
        case _ if isinstance(cell, Knight) and cell.color == ChessColor.BLACK: return '\u2658'
        case _ if isinstance(cell, Bishop) and cell.color == ChessColor.BLACK: return '\u2657'
        case _ if isinstance(cell, Pawn) and cell.color == ChessColor.BLACK: return '\u2659'

def printChessBoard(board):
    for row,n in zip(board, range(8)):
        print(n, end=' ')
        for cell in row:
            print(printChessSymbol(cell), end=" ")
        print()

def play(board, boardList):
    printChessBoard(boardList)

    while True:
        print()
        print(f'{board.getColorMove()} TURN:')
        start = input("Enter move from (with whitespace between): ")
        stop = input("Enter move toward (with whitespace between): ")
        start = tuple(int(x) for x in start.split(" "))
        stop = tuple(int(x) for x in stop.split(" "))
        if not board.move(start, stop): print("Enter the right move!")
        printChessBoard(boardList)


def playFirstPossibleMoves(depth, board, renderer=None, delay=0.5):
    if depth == 0: 
        return 1
    
    moves = board.legal_moves()
    for move in moves:
        print([move.src, move.dst], end=";")
    numPosittions = 0

    for move in moves:
        print(move.src, move.dst)
        print(board.colorMove)

        res = board.move(move.src, move.dst)
        print(res)

        renderer.render2(board)
        time.sleep(delay)

        numPosittions += playFirstPossibleMoves(depth-1, board, renderer, delay)
        board.undoMove()


    return numPosittions


def main():
    Board1 = b.Board()
    # play(Board1, Board1.board)
    game = Render.Render(720 + 100, Board1)
    # game.render(Board1)
    numPositions = playFirstPossibleMoves(2, Board1, game, 0.01)
    print(f"Num positions: {numPositions}")


if __name__ == "__main__":
    main()