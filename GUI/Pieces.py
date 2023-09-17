import pygame

class pieces:
    def __init__(self, x, y, color, image, square_width, square_height):
        self.pos = [x, y]
        self.color = color
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (square_width-25, square_height-25))

class bishop(pieces):
    def __init__(self, x, y, color, square_width, square_height):
        super().__init__(x, y, color, 'GUI\imgs\{0}_bishop.png'.format(color), square_width, square_height)

class king(pieces):
    def __init__(self, x, y, color, square_width, square_height):
        super().__init__(x, y, color, 'GUI\imgs\{0}_king.png'.format(color), square_width, square_height)

class knight(pieces):
    def __init__(self, x, y, color, square_width, square_height):
        super().__init__(x, y, color, 'GUI\imgs\{0}_knight.png'.format(color), square_width, square_height)

class pawn(pieces):
    def __init__(self, x, y, color, square_width, square_height):
        super().__init__(x, y, color, 'GUI\imgs\{0}_pawn.png'.format(color), square_width, square_height)

class queen(pieces):
    def __init__(self, x, y, color, square_width, square_height):
        super().__init__(x, y, color, 'GUI\imgs\{0}_queen.png'.format(color), square_width, square_height)

class rook(pieces):
    def __init__(self, x, y, color, square_width, square_height):
        super().__init__(x, y, color, 'GUI\imgs\{0}_rook.png'.format(color), square_width, square_height)

