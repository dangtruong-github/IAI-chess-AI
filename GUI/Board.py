import pygame
import chess

import Square
import Pieces

class board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.selected_piece = None
        self.turn = 'w'

        self.board = None
        self.draw_board = None

    def convert_board(self): #type(board) == chess.Board()
        pgn = self.board.epd()
        foo = []  #Final board
        pieces = pgn.split(" ", 1)[0]
        rows = pieces.split("/")
        for row in rows:
            foo2 = []  #This is the row I make
            for thing in row:
                if thing.isdigit():
                    for i in range(0, int(thing)):
                        foo2.append('.')
                else:
                    foo2.append(thing)
            foo.append(foo2)
        return foo

    def create(self):
        self.square_width = self.width // 8
        self.square_height = self.height // 8

        self.board = chess.Board()
        self.draw_board = self.convert_board()
        
        # [
		# 	['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
		# 	['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
		# 	['','','','','','','',''],
		# 	['','','','','','','',''],
		# 	['','','','','','','',''],
		# 	['','','','','','','',''],
		# 	['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
		# 	['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
		# ]

        #generate array of squares
        self.squares = [[[] for i in range(8)] for j in range(8)]

        for y in range(8):
            for x in range(8):
                self.squares[x][y] = Square.square(x, y, self.square_width, self.square_height)

                color = 'b'
                if self.draw_board[x][y].isupper():
                    color = 'w'
                match self.draw_board[x][y].lower():
                    case 'b':
                        self.squares[x][y].piece = Pieces.bishop(x, y, color, self.square_width, self.square_height)
                        continue
                    case 'k':
                        self.squares[x][y].piece = Pieces.king(x, y, color, self.square_width, self.square_height)
                        continue
                    case 'n':
                        self.squares[x][y].piece = Pieces.knight(x, y, color, self.square_width, self.square_height)
                        continue
                    case 'p':
                        self.squares[x][y].piece = Pieces.pawn(x, y, color, self.square_width, self.square_height)
                        continue
                    case 'q':
                        self.squares[x][y].piece = Pieces.queen(x, y, color, self.square_width, self.square_height)
                        continue
                    case 'r':
                        self.squares[x][y].piece = Pieces.rook(x, y, color, self.square_width, self.square_height)
                        continue
                    case '.':
                        continue

    def player_click(self, mx, my):
        y = mx // self.square_width
        x = my // self.square_height
        print("work ", x, y, self.selected_piece)

        if self.selected_piece is None:
            if self.squares[x][y].piece is not None:
                if self.squares[x][y].piece.color == self.turn:
                    self.squares[x][y].is_selected = True
                    self.selected_piece = self.squares[x][y].piece
        else:
            prev_square = self.selected_piece.pos
            move = chess.Move
            s = chr(prev_square[1] + 97) + str(8 - prev_square[0]) + chr(y + 97) + str(8 - x)
            # undo selected square by click again
            if x == prev_square[0] and y == prev_square[1]:
                self.selected_piece = None
                self.squares[prev_square[0]][prev_square[1]].is_selected = False
            elif not self.board.is_legal(chess.Move.from_uci(s)):
                self.selected_piece = None
                self.squares[prev_square[0]][prev_square[1]].is_selected = False
            else:
                self.board.push_uci(s)
                self.squares[x][y].piece = self.selected_piece
                self.squares[prev_square[0]][prev_square[1]].piece = None

                #reset and change turn
                self.selected_piece = None
                self.squares[prev_square[0]][prev_square[1]].is_selected = False
                self.turn = 'w' if self.turn == 'b' else 'b'

    def draw(self, screen):
        for y in range(8):
            for x in range(8):
                self.squares[x][y].draw(screen)
        