
class King:
    def __init__(self, color):
        self.color = color
        self.unmoved = True
        self.isFlier = False


    def validMove(self, start, dim):
        moves = []
        for row in range(-1, 1+1):
            if 0 <= start[0] + row < dim[0]:
                for col in range(-1, 1+1):
                    if row == 0 and col == 0:
                        continue
                    if 0 <= start[1] + col < dim[1]:
                        moves.append((start[0] + row, start[1] + col))
        return moves

