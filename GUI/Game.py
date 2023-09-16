import pygame

import Board

pygame.init()

window_size = (600, 600)

screen = pygame.display.set_mode(window_size)

board = Board.board(window_size[0], window_size[1])
board.create()

def draw(screen):
    screen.fill('white')
    board.draw(screen)

    pygame.display.update()

while True:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                board.player_click(mx, my)
    draw(screen)