from chess.Board import ChessDirection

class Bishop:
    def __init__(self, color):
        self.color = color
        self.isFlier = False
        self.directions = [ChessDirection.DIAGONAL]

    def validMove(self, start, dim):
        moves = []
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