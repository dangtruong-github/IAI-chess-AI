import pygame
import chess

from GUI import board

pygame.init()

window_size = (800, 600)
board_size = (600, 600)

screen = pygame.display.set_mode(window_size)

main_board = board(board_size[0], board_size[1])
main_board.print_draw_board()

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
                main_board.player_click(mx, my, screen)
    draw(screen)
    if main_board.board.is_game_over():
        if main_board.board.is_checkmate():
            if main_board.board.turn == chess.WHITE:
                print("Black wins by checkmate!")
            else:
                print("White wins by checkmate!")
        elif main_board.board.is_stalemate():
            print("Stalemate!")
        elif main_board.board.is_insufficient_material():
            print("Insufficient material for checkmate.")
        elif main_board.board.is_seventyfive_moves():
            print("Draw due to 75-move rule.")
        elif main_board.board.is_fivefold_repetition():
            print("Draw due to fivefold repetition.")
        else:
            print("Game over for some other reason.")
        break
