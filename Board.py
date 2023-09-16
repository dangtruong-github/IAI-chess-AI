import pygame
import chess
import Square

class board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.selected_piece = None
        self.turn = 'w'

        self.board = None

    def create(self):
        self.square_width = self.width // 8
        self.square_height = self.height // 8

        self.board = chess.Board()

        #generate array of squares
        self.squares = []
        for y in range(8):
            for x in range(8):
                self.squares.append(Square.square(x, y, self.square_width, self.square_height))
        

    def draw(self, screen):
        for square in self.squares:
            square.draw(screen)