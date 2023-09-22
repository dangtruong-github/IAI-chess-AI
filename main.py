import pygame

from GUI import board

pygame.init()

window_size = (600, 600)

screen = pygame.display.set_mode(window_size)

main_board = board(window_size[0], window_size[1])
main_board.create()

def draw(screen):
    screen.fill('white')
    main_board.draw(screen)

    pygame.display.update()

while True:
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                main_board.player_click(mx, my)
    draw(screen)