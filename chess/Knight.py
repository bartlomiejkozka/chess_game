class Knight:
    def __init__(self, color):
        self.color = color
        self.isFlier = True


    def validMove(self, start, dim):
        moves = []
        # two cells forward first
        for rows in [-2, 2]:
            if 0 <= start[0] + rows < dim[0]:
                if 0 <= start[1] + 1 < dim[0]:
                    moves.append((start[0] + rows, start[1] + 1))
                if 0 <= start[1] - 1 < dim[0]:
                    moves.append((start[0] + rows, start[1] - 1))
        for cols in [-2, 2]:
            if 0 <= start[1] + cols < dim[0]:
                if 0 <= start[0] + 1 < dim[0]:
                    moves.append((start[0] + 1, start[1] + cols))
                if 0 <= start[0] - 1 < dim[0]:
                    moves.append((start[0] - 1, start[1] + cols))
        return moves
    