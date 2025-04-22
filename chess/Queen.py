from chess.common import ChessDirection

class Queen:
    def __init__(self, color):
        self.color = color
        self.isFlier = False
        self.directions = [ChessDirection.VERTICAL, ChessDirection.HORIZONTAL, ChessDirection.DIAGONAL]


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

        # north-east direction
        for x in range(1, dim[0] - 1):
            if (0 <= start[0] - x < dim[0]) and (0 <= start[1] + x < dim[1]):
                moves.append((start[0] - x, start[1] + x))
        # south-west direction
        for x in range(1, dim[0] - 1):
            if (0 <= start[0] + x < dim[0]) and (0 <= start[1] - x < dim[0]):
                moves.append((start[0] + x, start[1] - x))
        # north-west direction
        for x in range(1, dim[0] - 1):
            if (0 <= start[0] - x < dim[0]) and (0 <= start[1] - x < dim[0]):
                moves.append((start[0] - x, start[1] - x))
        # south-east direction
        for x in range(1, dim[0] - 1):
            if (0 <= start[0] + x < dim[0]) and (0 <= start[1] + x < dim[0]):
                moves.append((start[0] + x, start[1] + x))

        return moves

