from enum import Enum
import random as rd
import string


class ChessColor(Enum):
    WHITE = 1
    BLACK = 2

class ChessDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3

class Move:
    src: tuple[int, int]
    dst: tuple[int, int]
    
    def __init__(self, src: tuple[int, int], dst: tuple[int, int]) -> None:
        self.src = src
        self.dst = dst

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        return self.src == other.src and self.dst == other.dst

    def __repr__(self):
        return f"Move({self.src}, {self.dst})"
    def __str__(self):
        return f"Move({self.src}, {self.dst})"


from King import King
from Queen import Queen
from Knight import Knight
from Rook import Rook
from Bishop import Bishop
from Pawn import Pawn


class Board:
    castling: dict[ChessColor, list[tuple[int, int]]]
    """en passant
            ChessColor: color of the pawn that can be captured
            tuple[int, int]: position of the board where opponent pawn can be moved to capture ChessColor pawn
    """
    en_passant: dict[ChessColor, tuple[int, int]]
    halfmove: int
    fullmove: int
    moved_stack: list[dict[str, object]]

    def __init__(self, random_color_pos: bool = False, fen_notation: string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        self.dimension = (8,8)
        self.board = [[None for _ in range(self.dimension[1])] for _ in range(self.dimension[0])]

        if random_color_pos:
            if rd.randint(0,1) == 0:
                self.upColor = ChessColor.WHITE
                self.downColor = ChessColor.BLACK
            else:
                self.upColor = ChessColor.BLACK
                self.downColor = ChessColor.WHITE
        else:
            self.upColor = ChessColor.BLACK
            self.downColor = ChessColor.WHITE

        self.prevStart = None
        self.prevStop = None
        self.prevColor = None
        self.moved_stack = []
        self.castling = {
            ChessColor.WHITE: [],
            ChessColor.BLACK: []
        }
        self.en_passant = {
            ChessColor.WHITE: None,
            ChessColor.BLACK: None
        }
        self.halfmove = 0
        self.fullmove = 0

        self.fillBoardFEN(fen_notation)

        self.whiteStrikedList = []
        self.blackStrikedList = []
        self.whitePoints = 0
        self.blackPoints = 0

        self.colorMove = ChessColor.WHITE

# =================================================
# ===================HELPERS=======================
# =================================================
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
        if self.colorMove == ChessColor.WHITE: self.colorMove = ChessColor.BLACK
        elif self.colorMove == ChessColor.BLACK: self.colorMove = ChessColor.WHITE

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

    def enPassant(self, start, stop):
        if stop[0] == start[0] + 2:
            self.en_passant[self.colorMove] = (stop[0] + 1, stop[1])
        elif stop[0] == start[0] - 2:
            self.en_passant[self.colorMove] = (stop[0] - 1, stop[1])
        else:
            pass

    def clearEnPassant(self):
        self.en_passant[self.colorMove] = None

    def oppositeColor(self):
        if self.colorMove == ChessColor.WHITE:
            return ChessColor.BLACK
        elif self.colorMove == ChessColor.BLACK:
            return ChessColor.WHITE
        else:
            raise ValueError("Invalid color")
# =================================================
# =================================================
# =================================================

    def fillBoardFEN(self, fen : string) -> None:
        """Fill the board with pieces according to the FEN notatnion string."""
        parts = fen.split(" ")
        if len(parts) != 6:
            raise ValueError("Invalid FEN notation")
        self.colorMove = ChessColor.WHITE if parts[1] == "w" else ChessColor.BLACK
        for castling in parts[2]:
            if castling == 'K':
                self.castling[ChessColor.WHITE].append((7, 6))
            elif castling == 'Q':
                self.castling[ChessColor.WHITE].append((7, 2))
            elif castling == 'k':
                self.castling[ChessColor.BLACK].append((0, 6))
            elif castling == 'q':
                self.castling[ChessColor.BLACK].append((0, 2))
        self.en_passant[self.oppositeColor()] = self.moveRecalculation(parts[3]) if parts[3] != '-' else None
        self.halfmove = int(parts[4])
        self.fullmove = int(parts[5])

        rows = parts[0].split("/")
        for i, row in enumerate(rows):
            j = 0
            for char in row:
                if char.isdigit():
                    j += int(char)
                elif char.isalpha():
                    color = ChessColor.WHITE if char.isupper() else ChessColor.BLACK
                    piece = None
                    match char.lower():
                        case 'k': piece = King(color)
                        case 'q': piece = Queen(color)
                        case 'r': piece = Rook(color)
                        case 'n': piece = Knight(color)
                        case 'b': piece = Bishop(color)
                        case 'p': piece = Pawn(color)
                    self[(i,j)] = piece
                    j += 1

#===================================

    def move(self, start, stop) -> bool:
        if self.isCheckMate(self.getkingPosition(self.colorMove)):
            raise Exception("GAME OVER!!!!!!!!!!!!!!!!!")
        isMoved = False
        self.clearEnPassant()

        piece_moved = self[start]
        piece_captured = self[stop]

        if Move(start, stop) in self.legal_moves():
            isMoved = True
        else:
            print(self.legal_moves())
            print("Illegal move")
            return isMoved

        self.moved_stack.append({
            "src": start,
            "dst": stop,
            "piece_moved": piece_moved,
            "piece_captured": piece_captured,
            "color": self.colorMove,
            "unmoved": getattr(piece_moved, 'unmoved', None)
        })

        if self.isStrike(stop, piece_moved.color):
            self.addSriked(stop)
            self.halfmove = 0

        if isinstance(piece_moved, Pawn):
            piece_moved.unmoved = False
            self.enPassant(start, stop)
            self.halfmove = 0

        elif isinstance(piece_moved, Rook) or isinstance(piece_moved, King):
            self.castling[self.colorMove].remove(stop) if stop in self.castling[self.colorMove] else None
        else: 
            pass

        self[start] = None
        self[stop] = piece_moved
        self.halfmove += 1
        self.fullmove += 1 if self.colorMove == ChessColor.BLACK else 0
        self.changeColor()

        return isMoved

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

    def undoMove(self) -> None:
        """Undo the last move made on the board."""
        if not self.moved_stack:
            print("No moves to undo")
            return

        last_move = self.moved_stack.pop()

        self[last_move["src"]] = last_move["piece_moved"]
        self[last_move["dst"]] = last_move["piece_captured"]

        if hasattr(self[last_move["src"]], "unmoved"):
            self[last_move["src"]].unmoved = last_move["unmoved"]

        self.colorMove = last_move["color"]

#===================================

    def isCastling(self, start: tuple[int, int], stop: tuple[int, int]):
        isCastling = False
        if not isinstance(self[start], King):
            return isCastling
        
        for castling in self.castling[self.colorMove]:
            if castling[1] < start[1]:
                if all([(self.isEmptyCell(square) and self.isCheck(square)) for square in [(start[0], i) for i in range(start[1]-1, castling[1]+2, -1)]]):
                    isCastling = True
            elif castling[1] > start[1]:
                if all([(self.isEmptyCell(square) and self.isCheck(square)) for square in [(start[0], i) for i in range(start[1]+1, castling[1]+2)]]):
                    isCastling = True
            else:
                # already handled
                pass 

        return isCastling

# ===================================

    def isCheck(self, checkPos: tuple[int, int]) -> list[bool, tuple[int, int]]:
        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if self[(row,col)] != None and self[(row,col)].color != self.colorMove:
                    # KNIGHT
                    if self[(row,col)].isFlier is True:
                        if checkPos in self[(row,col)].validMove((row, col), self.dimension):
                            return [True, (row, col)]
                    # PAWN
                    elif isinstance(self[(row,col)], Pawn):
                        if Move((row,col), checkPos) in self[(row,col)].validMove((row, col), self.dimension):
                            return [True, (row, col)]
                    # REST
                    elif checkPos in self[(row,col)].validMove((row, col), self.dimension):
                        if isinstance(self[(row,col)], King) or not self.isObsctacleBetween((row, col), checkPos, self[(row,col)].directions):
                            return [True, (row, col)]
        return [False, (0, 0)]
    

    def isCheckAfterMove(self, start, stop):
        res = False
        tmpStop = self[stop]
        tmpStart = self[start]
        self[stop] = self[start]
        self[start] = None
        if self.isCheck(self.getkingPosition(self.colorMove))[0]:
            res = True
        self[start] = tmpStart
        self[stop] = tmpStop
        return res
    
# ===================================

    def isCheckMate(self, kingPos):
        if not self.isCheck(kingPos)[0]:
            return False
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
    def legal_moves(self) -> list[Move]:
        moves: list[Move] = []
        for row in range(self.dimension[0]):
            for col in range(self.dimension[1]):
                if self[(row, col)] is not None and self[(row, col)].color == self.colorMove:
                    for item in self[(row, col)].validMove((row, col), self.dimension):
                        # temp
                        if isinstance(self[(row,col)], Pawn): item = item.dst

                        # no need to check if the check is before the move
                        if self.isCheckAfterMove((row, col), item):
                            continue

                        if self.isCastling((row, col), item):
                            moves.append(Move((row, col), item))
                        # PAWN CASES
                        elif isinstance(self[(row,col)], Pawn):
                            if item[1] != col:
                                if self[item] != None and self[item].color != self.colorMove:
                                    moves.append(Move((row, col), item))
                                elif self[item] == None and item == self.en_passant[self.oppositeColor()]:
                                    moves.append(Move((row, col), item))
                            elif item[1] == col and not self.isCollision(item, self[(row,col)].color) and not self.isObsctacleBetween((row,col), item, self[(row,col)].directions):
                                moves.append(Move((row, col), item))
                        # OBSTACLE BETWEEN and IS STRIKED CHESSMAN A FREIND
                        elif not self[(row,col)].isFlier and not isinstance(self[(row,col)], King):
                            if not self.isObsctacleBetween((row,col), item, self[(row,col)].directions) and not self.isCollision(item, self[(row,col)].color):
                                moves.append(Move((row, col), item))
                        elif isinstance((row, col), King) or isinstance(self[(row,col)], Knight) and not self.isCollision(item, self[(row,col)].color):
                            moves.append(Move((row, col), item))
                        else:
                            pass
        return moves

