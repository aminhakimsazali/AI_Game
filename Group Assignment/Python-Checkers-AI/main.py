
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from AI import AI

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI_GAME - Solving Checkers with Minimax Alpha Beta Pruning')
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    AIbot = AI()
    no_moves = False
    while run:
        clock.tick(FPS)


        if game.turn == WHITE:
            value, new_board = AIbot.minimax(game.get_board(), 4, float('-inf'), float('inf'), False, WHITE, game)
            if (new_board is not None):
                game.ai_move(new_board)
            else:
                no_moves=True


        if game.winner() != None:
            print(game.winner())
            run = False
        if no_moves == True:
            if game.turn == RED:
                print("WHITE Wins!")
            else:
                print("RED Wins!")
            run = False


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print("Explored node: ", AIbot.explored_node())
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Explored node: ", AIbot.explored_node())
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()
