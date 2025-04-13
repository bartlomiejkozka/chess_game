from enum import Enum
import random as rd


class ChessColor(Enum):
    WHITE = 1
    BLACK = 2


class ChessDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3


from King import King
from Queen import Queen
from Knight import Knight
from Rook import Rook
from Bishop import Bishop
from Pawn import Pawn


class Move:
    src: tuple[int, int]
    dst: tuple[int, int]
    def __init__(self, src: tuple[int, int], dst: tuple[int, int]) -> None:
        self.src = src
        self.dst = dst


class Board:
    def __init__(self):
        self.dimension = (8,8)
        self.board = [[None for _ in range(self.dimension[1])] for _ in range(self.dimension[0])]

        if rd.randint(0,1) == 0:
            self.upColor = ChessColor.WHITE
            self.downColor = ChessColor.BLACK
        else:
            self.upColor = ChessColor.BLACK
            self.downColor = ChessColor.WHITE

        self.fillBoard()

        self.whiteStrikedList = []
        self.blackStrikedList = []
        self.whitePoints = 0
        self.blackPoints = 0

        self.colorMove = ChessColor.WHITE

        self.prevStart = None
        self.prevStop = None
        self.prevColor = None


# ===================SHORT FUNCTIONS=======================
    def __getitem__(self, key):
        return self.board[key[0]][key[1]]

    def __setitem__(self, tuplePos, chessMan):
        self.board[tuplePos[0]][tuplePos[1]] = chessMan

    def getColorMove(self):
        return self.colorMove

    def setBoardCell(self, tuplePos, chessMan, color, board=None):
        if board is None: man = chessMan(color)
        else: man = chessMan(color, board)
        self[tuplePos] = man

    def isEmptyCell(self, tuplePos):
        return self[tuplePos] == None

    def isStrike(self, stop, color):
        return self[stop] != None and self[stop].color != color

    def isCollision(self, stop, color):
        return self[stop] != None and self[stop].color == color

    def matchPoints(self, strikedName):
        match strikedName:
            case 'Pawn':   return 1
            case 'Knight': return 3
            case 'Bishop': return 3
            case 'Rook':   return 5
            case 'Queen':  return 9

    def addSriked(self, stop):
        name = type(self[stop]).__name__
        if self[stop].color is ChessColor.WHITE:
            self.blackStrikedList.append(name)
            self.blackPoints += self.matchPoints(name)
        elif self[stop].color is ChessColor.BLACK:
            self.whiteStrikedList.append(name)
            self.whitePoints += self.matchPoints(name)

    def deleteStirked(self, colorMove):
        if colorMove == ChessColor.WHITE: self.whiteStrikedList.pop()
        else: self.blackStrikedList.pop()

    def getkingPosition(self, color):
        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if isinstance(self[(row,col)], King) and self[(row,col)].color == color:
                    return (row, col)

    def changeColor(self):
        self.prevColor = self.colorMove
        if self.colorMove == ChessColor.WHITE: self.colorMove = ChessColor.BLACK
        elif self.colorMove == ChessColor.BLACK: self.colorMove = ChessColor.WHITE

    # FUNKCJA PRZELICZAJCA RUCH (np. 11 ---> B1)
    def moveRecalculation(self, cooridante):
            match cooridante[0].upper:
                case 'A': return 0
                case 'B': return 1
                case 'C': return 2
                case 'D': return 3
                case 'E': return 4
                case 'F': return 5
                case 'G': return 6
                case 'I': return 7
                case _ : raise Exception("You put a wrong letter in chess coordinate!")


# ======================LONG FUNCTIONS======================
    def fillBoard(self):
        color = None
        for row in range(self.dimension[0]):
            if row > 1 and row < 6:
                continue
            elif row <= 1:
                color = self.upColor
            elif row >= 6:
                color = self.downColor

            for col in range(self.dimension[1]):
                if row == 0 or row == 7:
                    if col == 0 or col == 7:
                        self[(row, col)] = Rook(color)
                    elif col == 1 or col == 6:
                        self[(row, col)] = Knight(color)
                    elif col == 2 or col == 5:
                        self[(row, col)] = Bishop(color)
                    elif col == 3:
                        self[(row, col)] = Queen(color)
                    elif col == 4:
                        self[(row, col)] = King(color)
                elif row == 1 or row == 6:
                    self.setBoardCell((row, col), Pawn, color, self)

#===================================

    def isObsctacleBetween(self, start, stop, directionsList):  # start, stop --> tuples

        def diagonalMove(start, stop): # return True if obstacle exist
            if stop[0] > start[0]:  # south direction
                if stop[1] > start[1]:  # south-east direction
                    return not all([self.isEmptyCell((row, col)) for row, col in
                                zip(range(start[0] + 1, stop[0]), range(start[1] + 1, stop[1]))])
                elif stop[1] < start[1]:  # south-west direction
                    return not all([self.isEmptyCell((row, col)) for row, col in
                                zip(range(start[0] + 1, stop[0]), range(start[1] - 1, stop[1], -1))])
            elif stop[0] < start[0]:  # north direction
                if stop[1] > start[1]:  # north-east direction
                    return not all([self.isEmptyCell((row, col)) for row, col in
                                zip(range(start[0] - 1, stop[0], -1), range(start[1] + 1, stop[1]))])
                elif stop[1] < start[1]:  # north-west direction
                    return not all([self.isEmptyCell((row, col)) for row, col in
                                zip(range(start[0] - 1, stop[0], -1), range(start[1] - 1, stop[1], -1))])
            else:
                raise Exception("IsObstacleBetween error: diagonalMove function\n")

        def horizontalMove(start, stop):
            if start[1] < stop[1]:
                return not all([self.isEmptyCell((start[0], x)) for x in range(start[1]+1, stop[1])])
            elif start[1] > stop[1]:
                return not all([self.isEmptyCell((start[0], x)) for x in range(start[1] - 1, stop[1], -1)])

        def verticalMove(start, stop):
            if start[0] < stop[0] and isinstance(self[start], Pawn):
                return not all([self.isEmptyCell((x, start[1])) for x in range(start[0]+1, stop[0]+1)])
            elif start[0] > stop[0] and isinstance(self[start], Pawn):
                return not all([self.isEmptyCell((x, start[1])) for x in range(start[0]-1, stop[0]-1, -1)])
            elif start[0] < stop[0]:
                return not all([self.isEmptyCell((x, start[1])) for x in range(start[0]+1, stop[0])])
            elif start[0] > stop[0]:
                return not all([self.isEmptyCell((x, start[1])) for x in range(start[0]-1, stop[0], -1)])


        for dir in directionsList:
            match dir:
                case ChessDirection.VERTICAL:
                    if start[1] == stop[1]:
                        return verticalMove(start, stop)
                    else:
                        continue

                case ChessDirection.HORIZONTAL:
                    if start[0] == stop[0]:
                        return horizontalMove(start, stop)
                    else:
                        continue

                case ChessDirection.DIAGONAL:
                    if start[0] != stop[0] and start[1] != stop[1]:
                        return diagonalMove(start, stop)
                    else:
                        continue
        return False

#===================================

    def move(self, start, stop):
        prevChessManStart = self[start]
        prevChessManStop = self[stop]
        isStriked = False
        isMoved = False

        if start == stop: 
            print('ERR1')
            return False

        # ChessMan color check
        if self[start].color != self.colorMove:
            print('ERR2')
            return False

        # Check if castling is
        if self.castling(start, stop):
            self.changeColor()
            self.prevPositionStart = [start, prevChessManStart]
            self.prevPositionStop = [stop, prevChessManStop]
            return True

        # Check is the move appropriate in general
        if not (stop in self[start].validMove(start, self.dimension)):
            # (self[start].validMove(start, self.dimension))
            # print(self.upColor)
            print('ERR3')
            print(stop, start)
            print(self[start].unmoved)
            print(self[start].validMove(start, self.dimension))
            return False

        # Check if is the obstacle on the way
        if self[start].isFlier is False and not isinstance(self[start], King):
            if self.isObsctacleBetween(start, stop, self[start].directions):
                print('ERR4')
                return False

        # Check if is friend ChessMan on the stop cell
        if self.isCollision(stop, self[start].color):
            print('ERR5')
            return False

        # Check if the pawn has moved diagonal (want to strike)
        if isinstance(self[start], Pawn) and stop[1] != start[1]:
            if self[stop] is None:
                print('ERR6')
                return False

        # Check if is strike
        if self.isStrike(stop, self[start].color):
            isStriked = True
            self.addSriked(stop)

        if isinstance(self[start], Rook) or isinstance(self[start], King) or isinstance(self[start], Pawn):
            isMoved = True
            self[start].unmoved = False

        # Check the check
        if self.isCheck(self.getkingPosition(self.colorMove))[0]:
            tmp = self[stop]
            tmp1 = self[start]
            self[stop] = self[start]
            self[start] = None
            if self.isCheck(self.getkingPosition(self.colorMove))[0]:
                self[stop] = tmp
                self[start] = tmp1
                if isStriked: self.deleteStirked(self.colorMove)
                if isMoved: self[start].unmoved = True
                print('ERR7')
                return False

            # print(self.whiteStrikedList, self.whitePoints)
            # print(self.blackStrikedList, self.blackPoints)
            self.changeColor()
            self.prevPositionStart = [start, prevChessManStart]
            self.prevPositionStop = [stop, prevChessManStop]
            return True

        tmp = self[stop]
        tmp1 = self[start]
        self[stop] = self[start]
        self[start] = None
        if self.isCheck(self.getkingPosition(self.colorMove))[0]:
            print("This move cause the CHECK!!!")
            self[start] = tmp1
            self[stop] = tmp
            if isStriked: self.deleteStirked(self.colorMove)
            if isMoved: self[start].unmoved = True
            print('ERR8')
            return False

        # print(self.whiteStrikedList, self.whitePoints)
        # print(self.blackStrikedList, self.blackPoints)
        self.changeColor()

        if self.isCheck(self.getkingPosition(self.colorMove))[0]:
            if self.isCheckMate(self.getkingPosition(self.colorMove)):
                raise Exception("GAME OVER!!!!!!!!!!!!!!!!!")
        
        self.prevPositionStart = [start, prevChessManStart]
        self.prevPositionStop = [stop, prevChessManStop]
        return True


    def undoMove(self):
        if self.prevPositionStart is None:
            print("There is no previous move!")
            return

        self[self.prevPositionStart[0]] = self.prevPositionStart[1]
        self[self.prevPositionStop[0]] = self.prevPositionStop[1]
        self.colorMove = self.prevColor
        if isinstance(self[self.prevPositionStart[0]], Pawn) or isinstance(self[self.prevPositionStart[0]], Rook) or isinstance(self[self.prevPositionStart[0]], King):
            self[self.prevPositionStart[0]].unmoved = True
        
        

#===================================

    # ROSZADA
    def castling(self, start, stop):
        if isinstance(self[start], King) and isinstance(self[stop], Rook):
            # up-left rokade
            if start == (0, 4) and stop == (0, 2) and self[(0,4)].unmoved is True and \
                    self[(0,0)].unmoved is True and all([self.isEmptyCell((0, x)) for x in range(1, 3+1)]) \
                    and not self.isCheck((0, 2)) and not self.isCheck((0, 3)):
                self[(0,2)] = self[(0,4)]
                self[(0,4)] = None
                self[(0,3)] = self[(0,0)]
                self[(0,0)] = None
                return True
            # up-right rokade
            elif start == (0, 4) and stop == (0, 6) and self[(0,4)].unmoved is True and \
                    self[(0,7)].unmoved is True and all([self.isEmptyCell((0, x)) for x in range(5, 6+1)]) \
                    and not self.isCheck((0, 6)) and not self.isCheck((0, 5)):
                self[(0,6)] = self[(0,4)]
                self[(0,4)] = None
                self[(0,5)] = self[(0,7)]
                self[(0,7)] = None
                return True
            # down-left
            elif start == (7, 4) and stop == (7, 2) and self[(7,4)].unmoved is True and \
                    self[(7,0)].unmoved is True and all([self.isEmptyCell((7, x)) for x in range(1, 3+1)]) \
                    and not self.isCheck((7, 2)) and not self.isCheck((7, 3)):
                self[(7,2)] = self[(7,4)]
                self[(7,4)] = None
                self[(7,3)] = self[(7,0)]
                self[(7,0)] = None
                return True
            # down-right
            elif start == (7, 4) and stop == (7, 6) and self[(7,4)].unmoved is True and \
                    self[(7,7)].unmoved is True and all([self.isEmptyCell((7, x)) for x in range(5, 6+1)]) \
                    and not self.isCheck((7, 6)) and not self.isCheck((7, 5)):
                self[(7,6)] = self[(7,4)]
                self[(7,4)] = None
                self[(7,5)] = self[(7,7)]
                self[(7,7)] = None
                return True

        return False

# ===================================

    # SZACH
    def isCheck(self, kingPos):
        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if self[(row,col)] != None and self[(row,col)].color != self.colorMove:
                    # for Knight
                    if self[(row,col)].isFlier is True:
                        if kingPos in self[(row,col)].validMove((row, col), self.dimension):
                            return [True, (row, col)]
                    # for Pawn
                    elif isinstance(self[(row,col)], Pawn):
                        if self.upColor != self.colorMove:
                            if (row + 1, col + 1) == kingPos:
                                return [True, (row, col)]
                            elif (row + 1, col - 1) == kingPos:
                                return [True, (row, col)]
                        elif self.downColor != self.colorMove:
                            if (row - 1, col + 1) == kingPos:
                                return [True, (row, col)]
                            elif (row - 1, col - 1) == kingPos:
                                return [True, (row, col)]
                    # for the rest
                    elif kingPos in self[(row,col)].validMove((row, col), self.dimension):
                        if isinstance(self[(row,col)], King) or not self.isObsctacleBetween((row, col), kingPos, self[(row,col)].directions):
                            return [True, (row, col)]     # Check
        return [False, (0, 0)]
    

    def isCheckAfterMove(self, start, stop):
        res = False
        tmp = self[stop]
        tmp1 = self[start]
        self[stop] = self[start]
        self[start] = None
        if self.isCheck(self.getkingPosition(self.colorMove))[0]:
            res = True
        self[start] = tmp1
        self[stop] = tmp
        return res

# ===================================

    # SZACH MAT
    def isCheckMate(self, kingPos):
        for position in self[kingPos].validMove(kingPos, self.dimension):
            if self.isCollision(position, self[kingPos].color):
                continue
            elif not self.isCheck(position)[0]:
                return False
        # sprawdzenie czy nie da sie zasłonic lub zbić
        killerPos = self.isCheck(kingPos)[1]
        polesBetween = []

        if kingPos[0] > killerPos[0]:  # south direction
            if kingPos[1] > killerPos[1]:  # south-east direction
                polesBetween = [(row, col) for row, col in
                                zip(range(killerPos[0], kingPos[0]), range(killerPos[1], kingPos[1]))]
            elif kingPos[1] < killerPos[1]:  # south-west direction
                polesBetween = [(row, col) for row, col in
                                zip(range(killerPos[0], kingPos[0]), range(killerPos[1], kingPos[1], -1))]
        elif kingPos[0] < killerPos[0]:  # north direction
            if kingPos[1] > killerPos[1]:  # north-east direction
                polesBetween = [(row, col) for row, col in
                                zip(range(killerPos[0], kingPos[0], -1), range(killerPos[1], kingPos[1]))]
            elif kingPos[1] < killerPos[1]:  # north-west direction
                polesBetween = [(row, col) for row, col in
                                zip(range(killerPos[0], kingPos[0], -1), range(killerPos[1], kingPos[1], -1))]
        elif kingPos[0] == killerPos[0]:    # horizontal
            if kingPos[1] < killerPos[1]:
                polesBetween = [(kingPos[0], col) for col in range(killerPos[1], kingPos[1], -1)]
            elif kingPos[1] > killerPos[1]:
                polesBetween = [(kingPos[0], col) for col in range(killerPos[1], kingPos[1])]
        elif kingPos[1] == killerPos[1]:    # vertical
            if kingPos[0] < killerPos[0]:
                polesBetween = [(row, kingPos[1]) for row in range(killerPos[0], kingPos[0], -1)]
            elif kingPos[0] > killerPos[0]:
                polesBetween = [(row, kingPos[1]) for row in range(killerPos[0], kingPos[0])]

        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if self[(row, col)] is not None and self[(row, col)].color == self.colorMove and not isinstance(self[(row,col)], King):
                    for item in self[(row,col)].validMove((row, col), self.dimension):
                        if (isinstance(self[(row,col)], Pawn) and item[1] == col and item == killerPos) or (isinstance(self[(row,col)], Pawn) and item[1] != col and item in polesBetween):
                            continue
                        elif item in polesBetween:
                            if not self.isObsctacleBetween((row,col), item, self[(row,col)].directions):
                                return False

        return True

# ===================================
# Returns a list of tuples with all possible legal moves
    def legal_moves(self) -> list[tuple[int, int]]:
        moves: list[Move] = []
        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if self[(row, col)] is not None and self[(row, col)].color == self.colorMove:
                    for item in self[(row, col)].validMove((row, col), self.dimension):
                        # (self[(row,col)], (row,col), item)
                        if self.isCheckAfterMove((row, col), item):
                            continue           
                        # KING CASTLING
                        if self.castling((row, col), item):
                                    moves.append(Move((row, col), item))
                        # PAWN STRIKE
                        elif isinstance(self[(row,col)], Pawn) and item[1] != col and self[item] != None and self[item].color != self.colorMove:
                                moves.append(Move((row, col), item))
                        # OBSTACLE BETWEEN and IS STRIKED CHESSMAN A FREIND
                        elif self[(row,col)].isFlier is False and not isinstance(self[(row,col)], King) and not isinstance(self[(row,col)], Pawn):
                            if not self.isObsctacleBetween((row,col), item, self[(row,col)].directions) and not self.isCollision(item, self[(row,col)].color):
                                moves.append(Move((row, col), item))
                        elif isinstance(self[(row,col)], Pawn) and item[1] == col and not self.isCollision(item, self[(row,col)].color):
                            moves.append(Move((row, col), item))
                        else:
                            if not self.isCollision(item, self[(row,col)].color) and not isinstance(self[(row,col)], Pawn):
                                moves.append(Move((row, col), item))
        return moves

