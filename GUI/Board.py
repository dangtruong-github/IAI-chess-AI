import pygame
import chess
import os

unicode_to_algebraic = {
    '♚': 'K', '♛': 'Q', '♜': 'R', '♝': 'B', '♞': 'N', '♟': 'P',
    '♔': 'k', '♕': 'q', '♖': 'r', '♗': 'b', '♘': 'n', '♙': 'p'
}

promotion_code = ['q', 'r', 'b', 'n']
promotion_list = ['queen', 'rook', 'bishop', 'knight']

class board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.square_height = height // 8
        self.square_width = width // 8
        self.selected_piece = None
        self.promotion = None

        self.board = chess.Board() 
        self.draw_board = self.convert_board()
        
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
                        foo2.append(['.', 0])
                else:
                    foo2.append([thing, 0])
            foo.append(foo2)
        return foo

    def player_click(self, mx, my, screen):
        y = mx // self.square_width
        x = my // self.square_height
        updated = False

        # handle promotion
        if self.promotion is not None and y >= 8 and y <= 10 and x < 4:
            move = self.promotion + promotion_code[x]
            print(move)
            self.board.push_uci(move)
            updated = True
            self.promotion = None
            self.selected_piece = None
            self.update(0)
            return
    
        pos = chr(y + ord('a')) + chr((7 - x) + ord('1'))
        piece = self.board.piece_at(chess.parse_square(pos))
        print("work ", x, y, self.selected_piece, pos, piece)

        if self.selected_piece is None:
            if piece is not None:
                print(piece.unicode_symbol())
                team = chess.WHITE if unicode_to_algebraic[piece.unicode_symbol()].isupper() else chess.BLACK
                print("team", unicode_to_algebraic[piece.unicode_symbol()], team, self.board.turn)
                if self.board.turn != team:
                    self.selected_piece = [x, y]
                    self.draw_board[7-x][y] = [unicode_to_algebraic[piece.unicode_symbol()], 1]
                    
                    updated = True
        else:
            # promotion
            piece = self.board.piece_at(chess.parse_square(chr(self.selected_piece[1] + ord('a')) + chr(7 - self.selected_piece[0] + ord('1'))))   
            move = chr(self.selected_piece[1] + ord('a')) + chr(7 - self.selected_piece[0] + ord('1')) + pos
            print(move)      

            if unicode_to_algebraic[piece.unicode_symbol()].lower() == 'p' and ((move[1] == '7' and move[3] == '8') or (move[1] == '2' and move[3] == '1')):
                self.promotion = move
                self.draw_promotion(screen)
            else:
                self.promotion = None
                self.draw_board[7-self.selected_piece[0]][self.selected_piece[1]][1] = 0
                print(self.selected_piece)

                # undo selected square by click again
                if x == self.selected_piece[0] and y == self.selected_piece[1]:
                    self.selected_piece = None
                # block illegal moves
                elif not self.board.is_legal(chess.Move.from_uci(move)):
                    
                    self.selected_piece = None
                else:
                    self.selected_piece = None
                    self.board.push_uci(move)
                self.draw(screen)
            updated = True
    
        if updated:
            self.update()
            #self.print_draw_board()

    def move(self, move):
        if self.board.is_legal(move):    
            self.board.push_uci(move)
            self.update(0)
            return True
        return False

    def update(self, mode = 1):
        for x in range(8):
            for y in range(8):
                pos = chr(y + ord('a')) + chr((7 - x) + ord('1'))
                piece = self.board.piece_at(chess.parse_square(pos)) 
                updated = self.draw_board[x][y][1] if mode == 1 else 0
                self.draw_board[x][y] = [piece if piece is not None else ".", updated]

    def draw(self, screen):
        self.update()
        for x in range(8):
            for y in range(8):
                # 0, 0 = a, 8; 0, 1 = b, 8 --> x 

                loc = (x * (self.square_width), y * (self.square_height)) #position relative to the screen (pixel)

                color = 'light' if (x + y) % 2 == 1 else 'dark'
                pos = chr(y + ord('a')) + chr((7 - x) + ord('1'))
                
                piece = self.board.piece_at(chess.parse_square(pos))
        
                draw_color = (241, 211, 170) if color == 'light' else (180, 126, 82)
                selected_color = (150, 255, 100) if color == 'light' else (50, 220, 0)

                rect = pygame.Rect(loc[1], loc[0], self.square_width, self.square_height)

                pygame.draw.rect(screen, selected_color if self.draw_board[7-x][y][1] == 1 else draw_color, rect)

                if piece is not None:
                    #print("here pos:", self.piece.pos)
                    piece_code = unicode_to_algebraic[piece.unicode_symbol()]
                    piece_str = None
                    match piece_code.lower():
                        case 'r':
                            piece_str = "rook" 
                        case 'n':
                            piece_str = "knight"
                        case 'b':
                            piece_str = "bishop"
                        case 'q':
                            piece_str = "queen"
                        case 'k':
                            piece_str = "king"
                        case 'p':
                            piece_str = "pawn"
                    
                    team_code = 'w' if piece_code.islower() else 'b'
                    
                    img_path = 'imgs/{0}_{1}.png'.format(team_code, piece_str)
                        
                    base_path = os.path.dirname(__file__)
                    dude_path = os.path.join(base_path, img_path)
                    image = pygame.image.load(dude_path)
                    image = pygame.transform.scale(image, ((self.square_width)-25, (self.square_height)-25))

                    centering_rect = image.get_rect()
                    centering_rect.center = rect.center
                    screen.blit(image, centering_rect.topleft)
        if self.promotion is not None:
            self.draw_promotion(screen)

    def draw_promotion(self, screen):
        print("drawing promotion")
        team = 'w' if self.board.turn == chess.WHITE else 'b'

        for i in range(4):
            loc = self.square_height * i
            color = 'light' if i % 2 == 1 else 'dark'
            #pos = chr(y + ord('a')) + chr((7 - x) + ord('1'))
            
            #piece = self.board.piece_at(chess.parse_square(pos))

            draw_color = (241, 211, 170) if color == 'light' else (180, 126, 82)

            rect = pygame.Rect(600 + 20, loc, self.square_width, self.square_height)

            pygame.draw.rect(screen, draw_color, rect)
            print("drawing")
    
            img_path = 'imgs/{0}_{1}.png'.format(team, promotion_list[i])
                
            base_path = os.path.dirname(__file__)
            dude_path = os.path.join(base_path, img_path)
            image = pygame.image.load(dude_path)
            image = pygame.transform.scale(image, ((self.square_width)-25, (self.square_height)-25))

            centering_rect = image.get_rect()
            centering_rect.center = rect.center
            screen.blit(image, centering_rect.topleft)
            

    def print_draw_board(self):
        for x in range(8):
            for y in range(8):
                print(self.draw_board[x][y][0], end=" ")
            print()
        for x in range(8):
            for y in range(8):
                print(self.draw_board[x][y][1], end=" ")
            print()