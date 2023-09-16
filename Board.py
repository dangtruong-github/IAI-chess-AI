import pygame
import Square

class board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.selected_piece = None
        self.turn = 'white'

        self.board = None

    def create(self):
        self.square_width = self.width // 8
        self.square_height = self.height // 8

        self.board = [
			['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
			['b ', 'b ', 'b ', 'b ', 'b ', 'b ', 'b ', 'b '],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['','','','','','','',''],
			['w ', 'w ', 'w ', 'w ', 'w ', 'w ', 'w ', 'w '],
			['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
		]

        #generate array of squares
        self.squares = []
        for y in range(8):
            for x in range(8):
                self.squares.append(Square.square(x, y, self.square_width, self.square_height))
        

    def draw(self, screen):
        for square in self.squares:
            square.draw(screen)