import pygame
import Board

window_size = (800, 800)

screen = pygame.display.set_mode(window_size)

board = Board.board(window_size[0], window_size[1])
board.create()

def draw(screen):
    screen.fill('white')
    board.draw(screen)

    pygame.display.update()

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            break
    draw(screen)