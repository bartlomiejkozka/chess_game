import Board
import pygame
import string

from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Pawn import Pawn
from Board import ChessColor


class Render:

    def __init__(self, dim, board):
        pygame.init()
        pygame.font.init()
        self.size = (dim-100, dim)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.fieldSize = (self.size[0] / board.dimension[0], (self.size[1]-100) / board.dimension[1])


    def drawChessBoard(self, board):
        font = pygame.font.SysFont('Comic Sans MS', 15, bold=True)

        for rowN in range(board.dimension[0]):
            for colN in range(board.dimension[1]):
                if rowN % 2 == 0:
                    if colN % 2 == 0: pygame.draw.rect(self.screen, (149, 245, 175),
                                                       (self.fieldSize[1]*colN, self.fieldSize[0]*rowN + 50,
                                                        self.fieldSize[1], self.fieldSize[0]))
                    else: pygame.draw.rect(self.screen, (245, 243, 203),
                                                       (self.fieldSize[1]*colN, self.fieldSize[0]*rowN + 50,
                                                        self.fieldSize[1], self.fieldSize[0]))
                else:
                    if colN % 2 == 0: pygame.draw.rect(self.screen, (245, 243, 203),
                                                       (self.fieldSize[1]*colN, self.fieldSize[0]*rowN + 50,
                                                        self.fieldSize[1], self.fieldSize[0]))
                    else: pygame.draw.rect(self.screen, (149, 245, 175),
                                                       (self.fieldSize[1]*colN, self.fieldSize[0]*rowN + 50,
                                                        self.fieldSize[1], self.fieldSize[0]))

        for row in range(board.dimension[0]):
            textSurface = font.render(str(row+1), False, (0, 0, 0))
            self.screen.blit(textSurface, (0, self.fieldSize[0] * row + 50))

        for col, char in zip(range(board.dimension[1]), string.ascii_lowercase[:8]):
            textSurface = font.render(char, False, (0, 0, 0))
            self.screen.blit(textSurface, (self.fieldSize[1] * col + 5, self.fieldSize[0] * board.dimension[0] - 20 + 50))


    def matchChessPieces(self, cell):
        match cell:
            case _ if isinstance(cell, King) and cell.color == ChessColor.WHITE: return "images/Chess_klt60.png"
            case _ if isinstance(cell, Queen) and cell.color == ChessColor.WHITE: return "images/Chess_qlt60.png"
            case _ if isinstance(cell, Rook) and cell.color == ChessColor.WHITE: return "images/Chess_rlt60.png"
            case _ if isinstance(cell, Knight) and cell.color == ChessColor.WHITE: return "images/Chess_nlt60.png"
            case _ if isinstance(cell, Bishop) and cell.color == ChessColor.WHITE: return "images/Chess_blt60.png"
            case _ if isinstance(cell, Pawn) and cell.color == ChessColor.WHITE: return "images/Chess_plt60.png"

            case _ if isinstance(cell, King) and cell.color == ChessColor.BLACK: return "images/Chess_kdt60.png"
            case _ if isinstance(cell, Queen) and cell.color == ChessColor.BLACK: return "images/Chess_qdt60.png"
            case _ if isinstance(cell, Rook) and cell.color == ChessColor.BLACK: return "images/Chess_rdt60.png"
            case _ if isinstance(cell, Knight) and cell.color == ChessColor.BLACK: return "images/Chess_ndt60.png"
            case _ if isinstance(cell, Bishop) and cell.color == ChessColor.BLACK: return "images/Chess_bdt60.png"
            case _ if isinstance(cell, Pawn) and cell.color == ChessColor.BLACK: return "images/Chess_pdt60.png"


    def matchChessPiecesWhite(self, piece):
        match piece:
            case 'King':   return "images/Chess_klt60.png"
            case 'Queen':  return "images/Chess_qlt60.png"
            case 'Rook':   return "images/Chess_rlt60.png"
            case 'Knight': return "images/Chess_nlt60.png"
            case 'Bishop': return "images/Chess_blt60.png"
            case 'Pawn':   return "images/Chess_plt60.png"

    def matchChessPiecesBlack(self, piece):
        match piece:
            case 'King':   return "images/Chess_kdt60.png"
            case 'Queen':  return "images/Chess_qdt60.png"
            case 'Rook':   return "images/Chess_rdt60.png"
            case 'Knight': return "images/Chess_ndt60.png"
            case 'Bishop': return "images/Chess_bdt60.png"
            case 'Pawn':   return "images/Chess_pdt60.png"


    def drawChessPieces(self, board, without):
        for row, rowN in zip(board.board, range(board.dimension[0])):
            for cell, colN in zip(row, range(board.dimension[1])):
                if cell is None: continue
                elif without is not None and cell == board[without]: continue
                else:
                    image = pygame.image.load(self.matchChessPieces(cell))
                    self.screen.blit(image, (self.fieldSize[1]*colN + 14, self.fieldSize[1]*rowN + 14 + 50))


    def ChessPieceMove(self, startPos, endPos=None):
        start = (int((startPos[1]-50) // self.fieldSize[0]), int(startPos[0] // self.fieldSize[1]))
        if endPos is not None: stop = (int((endPos[1]-50) // self.fieldSize[0]), int(endPos[0] // self.fieldSize[1]))
        else: stop = None
        return [start, stop]


    def createSurfaceToMove(self, cell):
        return pygame.image.load(self.matchChessPieces(cell))


    def drawPoints(self, board):
        font = pygame.font.SysFont('Comic Sans MS', 20, bold=True)

        if board.upColor == ChessColor.BLACK:
            score1txt = font.render('Score:', False, (0, 0, 0))
            score1 = font.render(str(board.blackPoints), False, (0, 0, 0))
            self.screen.blit(score1txt, (10, 10))
            self.screen.blit(score1, (80, 10))

            score2txt = font.render('Score:', False, (255, 255, 255))
            score2 = font.render(str(board.whitePoints), False, (255, 255, 255))
            self.screen.blit(score2txt, (10, self.size[1]-42))
            self.screen.blit(score2, (80, self.size[1]-42))
        else:
            score1txt = font.render('Score:', False, (255, 255, 255))
            score1 = font.render(str(board.whitePoints), False, (255, 255, 255))
            self.screen.blit(score1txt, (10, 10))
            self.screen.blit(score1, (80, 10))

            score2txt = font.render('Score:', False, (0, 0, 0))
            score2 = font.render(str(board.blackPoints), False, (0, 0, 0))
            self.screen.blit(score2txt, (10, self.size[1] - 42))
            self.screen.blit(score2, (80, self.size[1] - 42))


    def drawScoredPieces(self, board):
        if board.upColor == ChessColor.BLACK:
            x = 0
            y = 0
            for piece in board.blackStrikedList:
                image = pygame.image.load(self.matchChessPiecesWhite(piece))
                image = pygame.transform.scale(image, (25,25))
                self.screen.blit(image, (120 + x, 14))
                x += 20
            for piece in board.whiteStrikedList:
                image = pygame.image.load(self.matchChessPiecesBlack(piece))
                image = pygame.transform.scale(image, (25, 25))
                self.screen.blit(image, (120 + y, self.size[1] - 38))
                y += 20
        else:
            x = 0
            y = 0
            for piece in board.whiteStrikedList:
                image = pygame.image.load(self.matchChessPiecesBlack(piece))
                image = pygame.transform.scale(image, (25,25))
                self.screen.blit(image, (120 + x, 14))
                x += 20
            for piece in board.blackStrikedList:
                image = pygame.image.load(self.matchChessPiecesWhite(piece))
                image = pygame.transform.scale(image, (25, 25))
                self.screen.blit(image, (120 + y, self.size[1] - 38))
                y += 20



    def render(self, board):
        movedPiece = None
        running = True
        moving = False
        rect = None
        img = None
        startPos = None

        while running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    startPos = event.pos
                    moving = True
                    movedPiece = self.ChessPieceMove(startPos)[0]
                    if board[movedPiece] is not None:
                        img = pygame.image.load(self.matchChessPieces(board[movedPiece]))
                        rect = img.get_rect(center=event.pos)

                elif event.type == pygame.MOUSEBUTTONUP and moving is True:
                    endPos = event.pos
                    moving = False
                    movedPiece = None
                    if board[self.ChessPieceMove(startPos)[0]] is not None:
                        try:
                            board.move(self.ChessPieceMove(startPos, endPos)[0], self.ChessPieceMove(startPos, endPos)[1])
                        except Exception as e:
                            print(f"Caught exception: {e}")
                            running = False
                    img = None

                elif event.type == pygame.MOUSEMOTION and moving is True:
                    if rect:
                        rect.move_ip(event.rel)

            self.screen.fill((100,100,100))
            self.drawPoints(board)
            self.drawScoredPieces(board)
            self.drawChessBoard(board)
            self.drawChessPieces(board, movedPiece)
            if moving and img and rect:
                self.screen.blit(img, rect)

            pygame.display.flip()
            self.clock.tick(60)