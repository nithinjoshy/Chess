import sys
import math
import copy
from collections import defaultdict
from operator import itemgetter

import pygame
from pygame.locals import *

from constants import *

class Board():
    WhitePieces = []
    BlackPieces = []
    squares = defaultdict(int)
    MoveHistory = []
    Move = 0

    def CreatePiece(self, piece, color, pos):
        NewPiece = Piece(piece, pos, color)
        self.squares[pos] = NewPiece

        if color == 'white':
            self.WhitePieces.append(NewPiece)

            if piece == 'king':
                self.KingWhite = NewPiece
        else:
            self.BlackPieces.append(NewPiece)

            if piece == 'king':
                self.KingBlack = NewPiece
        
    def MovePiece(self, oldpos, newpos):
        OldPiece = self.squares[oldpos]
        NewPiece = self.squares[newpos]

        self.MoveHistory.append((OldPiece, oldpos, newpos, NewPiece, OldPiece.has_moved))

        if NewPiece != 0:
            if NewPiece.color == 'white':
                self.WhitePieces.remove(NewPiece)
            else:
                self.BlackPieces.remove(NewPiece)

        self.squares[newpos] = OldPiece
        self.squares[oldpos] = 0
        self.squares[newpos].pos = newpos
        self.squares[newpos].has_moved = True
        self.Move += 1

    def ReverseMove(self, count):
        for x in range(count):
            LastMove = self.MoveHistory.pop()

            self.squares[LastMove[2]] = LastMove[3]
            self.squares[LastMove[1]] = LastMove[0]
            self.Move -= 1
            LastMove[0].pos = LastMove[1]

            if LastMove[3] != 0:
                LastMove[3].pos = LastMove[2]

                if LastMove[3].color == 'white':
                    self.WhitePieces.append(LastMove[3])
                else:
                    self.BlackPieces.append(LastMove[3])
            
            if LastMove[4] == False:
                LastMove[0].has_moved = False
    
    def IllegalMove(self, oldpos, newpos):
        turn = self.squares[oldpos].color
        self.MovePiece(oldpos, newpos)

        if turn == 'white':
            if self.KingWhite.pos in self.FindAllMoves('black', first=False)[1]:
                self.ReverseMove(1)
                return True
        else:
            if self.KingBlack.pos in self.FindAllMoves('white', first=False)[1]:
                self.ReverseMove(1)
                return True
        
        self.ReverseMove(1)
        return False

    def FindMoves(self, pos, first=True):
        possible_moves = []
        
        if self.squares[pos] == 0:
            return possible_moves
        else:
            piece = self.squares[pos]

        if piece.type == "pawn":

            if piece.color == "white":
                PawnMove = (0, -1)
                PawnCaptureMoves = [(-1, -1), (1, -1)]

                NewLocation = AddPos(piece.pos, PawnMove)
                if self.squares[NewLocation] == 0:
                    possible_moves.append(NewLocation)
                
                for move in PawnCaptureMoves:
                    NewLocation = AddPos(piece.pos, move)
                    if self.squares[NewLocation] != 0:
                        if self.squares[NewLocation].color != piece.color:
                            possible_moves.append(NewLocation)

                if piece.has_moved == False:            
                    NewLocation = AddPos(piece.pos, (0, -2))
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)

            elif piece.color == "black":
                PawnMove = (0, 1)
                PawnCaptureMoves = [(-1, 1), (1, 1)]

                NewLocation = AddPos(piece.pos, PawnMove)
                if self.squares[NewLocation] == 0:
                    possible_moves.append(NewLocation)
                
                for move in PawnCaptureMoves:
                    NewLocation = AddPos(piece.pos, move)
                    if self.squares[NewLocation] != 0:
                        if self.squares[NewLocation].color != piece.color:
                            possible_moves.append(NewLocation)

                if piece.has_moved == False:            
                    NewLocation = AddPos(piece.pos, (0, 2))
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)

        elif piece.type == "knight":
            KnightMoves = [(-2, 1), (-2, -1), (2, 1), (2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2)]

            for move in KnightMoves:
                NewLocation = AddPos(piece.pos, move)
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0 or self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)

        elif piece.type == "bishop" or piece.type == "queen":
            for value in range(1, 8):
                NewLocation = AddPos(piece.pos, (value, value))
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)
                    elif self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
                        break
                    else:
                        break
                else:
                    break
            
            for value in range(1, 8):
                NewLocation = AddPos(piece.pos, (value, -value))
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)
                    elif self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
                        break
                    else:
                        break
                else:
                    break
            
            for value in range(1, 8):
                NewLocation = AddPos(piece.pos, (-value, -value))
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)
                    elif self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
                        break
                    else:
                        break
                else:
                    break
            
            for value in range(1, 8):
                NewLocation = AddPos(piece.pos, (-value, value))
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)
                    elif self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
                        break
                    else:
                        break
                else:
                    break

        elif piece.type == "king":
            KingMoves = [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]

            for move in KingMoves:
                NewLocation = AddPos(piece.pos, move)
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0 or self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
            
            if piece.has_moved == False:
                RookLocation = AddPos(piece.pos, (3, 0))
                if self.squares[RookLocation] != 0 and self.squares[RookLocation].type == 'rook' and self.squares[RookLocation].color == piece.color:
                    if self.squares[RookLocation].has_moved == False:
                        MoveLocs = [(1, 0), (2, 0)]
                        possible = True
                        for move in MoveLocs:
                            NewLocation = AddPos(piece.pos, move)
                            if self.squares[NewLocation] != 0 or self.IllegalMove(piece.pos, NewLocation):
                                possible = False
                        if possible:
                            possible_moves.append(AddPos(piece.pos, (2, 0)))
                            # CURRENTLY CAN CASTLE WHILE IN CHECK
                
        if piece.type == "rook" or piece.type == "queen":
            for value in range(1, 8):
                NewLocation = AddPos(piece.pos, (value, 0))
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)
                    elif self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
                        break
                    else:
                        break
                else:
                    break
            
            for value in range(1, 8):
                NewLocation = AddPos(piece.pos, (-value, 0))
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)
                    elif self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
                        break
                    else:
                        break
                else:
                    break
            
            for value in range(1, 8):
                NewLocation = AddPos(piece.pos, (0, value))
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)
                    elif self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
                        break
                    else:
                        break
                else:
                    break
            
            for value in range(1, 8):
                NewLocation = AddPos(piece.pos, (0, -value))
                if NewLocation[0] < 8 and NewLocation[0] > -1 and NewLocation[1] < 8 and NewLocation[1] > -1:
                    if self.squares[NewLocation] == 0:
                        possible_moves.append(NewLocation)
                    elif self.squares[NewLocation].color != piece.color:
                        possible_moves.append(NewLocation)
                        break
                    else:
                        break
                else:
                    break

        if first == True:
            IllegalMoves = []
            for move in possible_moves:
                if self.IllegalMove(piece.pos, move):
                    IllegalMoves.append(move)
            
            for move in IllegalMoves:
                possible_moves.remove(move)

        return possible_moves

    def FindAllMoves(self, color, first=True):
        pieces = []
        moves = []

        if color == 'white':
            for piece in self.WhitePieces:
                for move in self.FindMoves(piece.pos, first):
                    pieces.append((piece, piece.pos))
                    moves.append(move)
        else:
            for piece in self.BlackPieces:
                for move in self.FindMoves(piece.pos, first):
                    pieces.append((piece, piece.pos))
                    moves.append(move)

        return (pieces, moves)
    
    def EvaluatePosition(self):
        value = 0

        for piece in self.WhitePieces:
            if piece.type == 'king':
                value -= KING
                value -= KING_POSITIONS[piece.pos[1]][piece.pos[0]]
            elif piece.type == 'queen':
                value -= QUEEN
                value -= QUEEN_POSITIONS[piece.pos[1]][piece.pos[0]]
            elif piece.type == 'rook':
                value -= ROOK
                value -= ROOK_POSITIONS[piece.pos[1]][piece.pos[0]]
            elif piece.type == 'bishop':
                value -= BISHOP
                value -= BISHOP_POSITIONS[piece.pos[1]][piece.pos[0]]
            elif piece.type == 'knight':
                value -= KNIGHT
                value -= KNIGHT_POSITIONS[piece.pos[1]][piece.pos[0]]
            elif piece.type == 'pawn':
                value -= PAWN
                value -= PAWN_POSITIONS[piece.pos[1]][piece.pos[0]]
        
        for piece in self.BlackPieces:
            if piece.type == 'king':
                value += KING
                value += KING_POSITIONS[7 - piece.pos[1]][piece.pos[0]]
            elif piece.type == 'queen':
                value += QUEEN
                value += QUEEN_POSITIONS[7 - piece.pos[1]][piece.pos[0]]
            elif piece.type == 'rook':
                value += ROOK
                value += ROOK_POSITIONS[7 - piece.pos[1]][piece.pos[0]]
            elif piece.type == 'bishop':
                value += BISHOP
                value += BISHOP_POSITIONS[7 - piece.pos[1]][piece.pos[0]]
            elif piece.type == 'knight':
                value += KNIGHT
                value += KNIGHT_POSITIONS[7 - piece.pos[1]][piece.pos[0]]
            elif piece.type == 'pawn':
                value += PAWN
                value += PAWN_POSITIONS[7 - piece.pos[1]][piece.pos[0]]
        
        return value
    
    def BestMove(self, depth, turn='black', history=()):
        if depth == 0:
            return (self.EvaluatePosition(), history)
        else:
            Evaluations = []
            PieceMoves = self.FindAllMoves(turn, first=True)
            if PieceMoves == ([], []):
                if turn == 'black':
                    return (-1000000, history)
                else:
                    return (1000000, history)
            for x in range(len(PieceMoves[0])):
                piece = PieceMoves[0][x][0]
                move = PieceMoves[1][x]
                NewHistory = (*history, (piece.pos, move))
                self.MovePiece(piece.pos, move)
                if turn == 'black':
                    Evaluations.append(self.BestMove(depth-1, turn='white', history=NewHistory))
                else:
                    Evaluations.append(self.BestMove(depth-1, turn='black', history=NewHistory))
                self.ReverseMove(1)
            if turn == 'black':
                return max(Evaluations, key=itemgetter(0), default=None)
            else:
                return min(Evaluations, key=itemgetter(0), default=None)


class Piece():

    def __init__(self, piece, pos, color):
        self.pos = pos
        self.type = piece
        self.path = f"Pieces/{piece}_{color}.png"
        self.has_moved = False
        self.color = color

    def __str__(self):
        return f'{self.color} {self.type} at {self.pos}'
    
    def __repr__(self):
        return self.type


def DrawBoard(display, SQUARE_LENTH):
    color = "white"
    for x in range(8):
        for y in range(8):
            if color == "white":
                pygame.draw.rect(display, (255, 255, 255), (x * SQUARE_LENTH, y * SQUARE_LENTH, SQUARE_LENTH, SQUARE_LENTH))
                color = "black"
            else:
                pygame.draw.rect(display, (112, 128, 144), (x * SQUARE_LENTH, y * SQUARE_LENTH, SQUARE_LENTH, SQUARE_LENTH))
                color = "white"

        if color == "white":
            color = "black"
        else:
            color = "white"


def CreateGame():
    board = Board()

    for x in range(8):
        board.CreatePiece('pawn', 'black', (x, 1))
        board.CreatePiece('pawn', 'white', (x, 6))


    InitialPositions = [['knight', 'black', (1, 0)], ['knight', 'black', (6, 0)], ['knight', 'white', (1, 7)], ['knight', 'white', (6, 7)],
                        ['bishop', 'black', (2, 0)], ['bishop', 'black', (5, 0)], ['bishop', 'white', (2, 7)], ['bishop', 'white', (5, 7)],
                        ['rook', 'black', (0, 0)], ['rook', 'black', (7, 0)], ['rook', 'white', (0, 7)], ['rook', 'white', (7, 7)],
                        ['queen', 'black', (3, 0)], ['queen', 'white', (3, 7)],
                        ['king', 'black', (4, 0)], ['king', 'white', (4, 7)]]

    for position in InitialPositions:
        board.CreatePiece(position[0], position[1], position[2])

    return board


def AddPos(pos1, pos2):
        newpos = (pos1[0] + pos2[0], pos1[1] + pos2[1])
        return newpos

def SubPos(pos1, pos2):
    return (pos1[0] - pos2[0], pos1[1] - pos2[1])


pygame.init()

SQUARE_LENTH = 80
display = pygame.display.set_mode((8 * SQUARE_LENTH, 8 * SQUARE_LENTH))
pygame.display.set_caption('Chess')

board = CreateGame()
turn = 'white'
ClickedSquare = 0
ClickedPiece: Piece
ClickedMoves = []

done = False
while not done:
    if turn == 'black':
        OptimalMove = board.BestMove(2)
        if OptimalMove != None:
            board.MovePiece(OptimalMove[1][0][0], OptimalMove[1][0][1])
            turn = 'white'

    DrawBoard(display, SQUARE_LENTH)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            ClickedSquare = (math.floor(pygame.mouse.get_pos()[0]/SQUARE_LENTH), math.floor(pygame.mouse.get_pos()[1]/SQUARE_LENTH))
            if ClickedMoves != []:
                if ClickedSquare in ClickedMoves:
                    board.MovePiece(ClickedPiece.pos, ClickedSquare)

                    ClickedSquare = 0
                    ClickedPiece = 0
                    ClickedMoves = []

                    if turn == 'white':
                        turn = 'black'
                    else:
                        turn = 'white'
                    
                    if board.FindAllMoves(turn) == ([], []):
                        restart = False
                        while not restart:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    restart = True
                                    done = True
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == K_r:
                                        restart = True
                                        board = CreateGame()
                                    elif event.key == K_q:
                                        restart = True
                                        done = True

                elif board.squares[ClickedSquare] != 0 and board.squares[ClickedSquare].color == turn:
                    ClickedPiece = board.squares[ClickedSquare]
                    ClickedMoves = board.FindMoves(ClickedSquare)

                else:
                    ClickedSquare = 0
                    ClickedPiece = 0
                    ClickedMoves = []

            else:
                if board.squares[ClickedSquare] != 0 and board.squares[ClickedSquare].color == turn:
                    ClickedPiece = board.squares[ClickedSquare]
                    ClickedMoves = board.FindMoves(ClickedSquare)

    for move in ClickedMoves:
        pos = (move[0] * SQUARE_LENTH, move[1] * SQUARE_LENTH, SQUARE_LENTH, SQUARE_LENTH)
        pygame.draw.rect(display, (100, 149, 237), pos)

    for key in board.squares.keys():
        if board.squares[key] != 0:
            piece = board.squares[key]
            pos = (piece.pos[0] * SQUARE_LENTH, piece.pos[1] * SQUARE_LENTH)
            display.blit(pygame.image.load(piece.path), pos)

    pygame.display.flip()

pygame.quit()
sys.exit()
