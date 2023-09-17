import pygame

class square:
    def __init__(self, x, y, width, height):
        self.pos = [x, y] #position relative to the board (reversed)
        self.width = width
        self.height = height

        self.loc = (x * width, y * height) #position relative to the screen (pixel)

        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        self.draw_color = (241, 211, 170) if self.color == 'light' else (180, 126, 82)
        self.selected_color = (150, 255, 100) if self.color == 'light' else (50, 220, 0)

        self.rect = pygame.Rect(self.loc[1], self.loc[0], self.width, self.height)

        self.is_selected = False
        self.piece = None

    def pos_on_board(self):
        column = "abcdefgh"
        return column[self.loc[0]] + str(self.loc[1]+1)

    def draw(self, screen):
        if self.is_selected:
            pygame.draw.rect(screen, self.selected_color, self.rect)
        else:
            pygame.draw.rect(screen, self.draw_color, self.rect)

        if self.piece != None:
            #print("here pos:", self.piece.pos)
            centering_rect = self.piece.image.get_rect()
            centering_rect.center = self.rect.center
            screen.blit(self.piece.image, centering_rect.topleft)