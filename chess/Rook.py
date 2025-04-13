from Board import ChessDirection

class Rook:
    def __init__(self, color):
        self.color = color
        self.isFlier = False
        self.directions = [ChessDirection.VERTICAL, ChessDirection.HORIZONTAL]
        self.unmoved = True


    def validMove(self, start, dim):
        moves = []
        for rows in range((dim[0] - start[0]) - dim[0], dim[0] - start[0]):
            if rows == 0:
                continue
            moves.append((start[0] + rows, start[1]))
        for cols in range((dim[1] - start[1]) - dim[1], dim[1] - start[1]):
            if cols == 0:
                continue
            moves.append((start[0], start[1] + cols))

        return moves