from Board import ChessDirection

class Pawn:
    def __init__(self, color, board):
        self.color = color
        self.isFlier = False
        self.directions = [ChessDirection.VERTICAL]
        self.unmoved = True
        self.board = board


    # return list which contains tuples of appropriate moves
    def validMove(self, start, dim):
        moves = []
        if start[0] == 1 and self.unmoved is True:
            moves.extend([(start[0] + 1, start[1]), (start[0] + 2, start[1])])
            if start[1] + 1 < dim[0]:
                moves.append((start[0] + 1, start[1] + 1))
            if start[1] - 1 >= 0:
                moves.append((start[0] + 1, start[1] - 1))
        elif start[0] == 6 and self.unmoved is True:
            moves.extend([(start[0] - 1, start[1]), (start[0] - 2, start[1])])
            if start[1] + 1 < dim[0]:
                moves.append((start[0] - 1, start[1] + 1))
            if start[1] - 1 >= 0:
                moves.append((start[0] - 1, start[1] - 1))
        elif self.color == self.board.upColor and start[0]+1 < dim[0]:
            moves.append((start[0] + 1, start[1]))
            if start[1] + 1 < dim[0]:
                moves.append((start[0] + 1, start[1] + 1))
            if start[1] - 1 >= 0:
                moves.append((start[0] + 1, start[1] - 1))
        elif self.color == self.board.downColor and start[0]-1 >= 0:
            moves.append((start[0] - 1, start[1]))
            if start[1] + 1 < dim[0]:
                moves.append((start[0] - 1, start[1] + 1))
            if start[1] - 1 >= 0:
                moves.append((start[0] - 1, start[1] - 1))

        return moves