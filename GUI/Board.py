import pygame
import chess

from .Square import square
from .Pieces import bishop, rook, knight, queen, king, pawn

class board:
    def __init__(self):
        self.selected_piece = None

        self.board = chess.Board() 
        self.draw_board = None
    
    