import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from AI import AI
from AI_2 import AI as AI2
import time
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AI Checkers ')


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
    AIbot2 = AI2()
    start_side = [WHITE,RED]
    no_moves = False
    start = time.time()
    p1_wins = 0
    p2_wins = 0
    draw_count = 0
    rounds = 10
    curr_round = 0
    timeout = 6000
    agent1_name ="Minimax with A-B Pruning"
    agent2_name ="Monte Carlo Tree Search"
    outoftime = False
    while run:
        current_time = time.time()

        if(current_time-start >= timeout):
            outoftime = True

        clock.tick(FPS)
        if game.turn == start_side[0]:
            value, new_board = AIbot.minimax(game.get_board(), 4, float('-inf'), float('inf'), True,  start_side[0], game)
            if (new_board is not None):
                game.ai_move(new_board)
            else:
                no_moves=True

        elif game.turn == start_side[1]:
            new_board = AIbot2.play(game.get_board(), start_side[1], game)
            if (new_board is not None):
                game.ai_move(new_board)
            else:
                no_moves=True
        board = game.get_board()
        if((board.red_left == 1 and board.white_left == 1 and board.white_kings == 1 and board.red_kings == 1) or outoftime):
            start = time.time()
            outoftime = False
            print("Draw Game")
            draw_count+=1
            swapSide(start_side)
            game.reset()

        if game.winner() != None:
            if(game.winner() == RED):
                if(start_side[0]==RED):
                    p1_wins+=1
                    print("RED Wins! (Agent 1 - " + agent1_name + " )")
                else:
                    p2_wins+=1
                    print("RED Wins! (Agent 2 - " + agent2_name + " )")

            else:
                if(start_side[0]==WHITE):
                    p1_wins+=1
                    print("WHITE Wins! (Agent 1 - " + agent1_name + " )")
                else:
                    p2_wins+=1
                    print("WHITE Wins! (Agent 2 - " + agent2_name + " )")
            curr_round += 1
            if (curr_round >= rounds):
                run = False
            else:
                swapSide(start_side)
                game.reset()


        if no_moves == True:
            if game.turn == RED:
                if(start_side[0]==RED):
                    p2_wins+=1
                    print("WHITE Wins! (Agent 2 - " + agent2_name + " )")
                else:
                    p1_wins+=1
                    print("WHITE Wins! (Agent 1 - " + agent1_name + " )")
            else:
                if(start_side[0]==WHITE):
                    p2_wins += 1
                    print("RED Wins! (Agent 2 - " + agent2_name + " )")
                else:
                    p1_wins += 1
                    print("RED Wins! (Agent 1 - " + agent1_name + " )")
            curr_round += 1
            if (curr_round >= rounds):
                run = False
            else:
                game.reset()
                swapSide(start_side)
                no_moves = False

        game.update()


    print("Agent 1 Win count: " + str(p1_wins))
    print("Agent 2 Win count: " + str(p2_wins))
    print("Draw count: " + str(draw_count))
    pygame.quit()

def swapSide(sides):
    temp = sides[0]
    sides[0] = sides[1]
    sides[1] = temp

main()