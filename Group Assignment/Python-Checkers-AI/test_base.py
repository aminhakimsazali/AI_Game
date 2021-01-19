import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from AI import AI
from AI_2 import AI as AI2
from base_model import BASE 
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
    Basebot = BASE()
    start_side = [WHITE,RED]
    no_moves = False
    timeout = 6000
    start = time.time()
    p1_wins = 0
    p2_wins = 0
    draw_count = 0
    rounds = 10
    curr_round = 0
    outoftime = False

    agent1_name ="Minimax with A-B Pruning"
    agent2_name ="Random Move"

    start_time = time.time()
    while run:
        current_time = time.time()

        if (current_time - start >= timeout):
            outoftime = True

        clock.tick(FPS)
        if game.turn == start_side[0]:
            value, new_board = AIbot.minimax(game.get_board(), 4, float('-inf'), float('inf'), True,  start_side[0], game)
            if (new_board is not None):
                game.ai_move(new_board)
            else:
                no_moves=True

        elif game.turn == start_side[1]:
            new_board = Basebot.random_move(game.get_board(), start_side[1], game)
            if (new_board is not None):
                game.ai_move(new_board)
            else:
                no_moves=True
        board = game.get_board()
        if ((board.red_left == 1 and board.white_left == 1 and board.white_kings == 1 and board.red_kings == 1) or outoftime):
            start = time.time()
            outoftime = False
            print("Draw Game")
            draw_count += 1
            swapSide(start_side)
            start_time = time.time()
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
                start_time = time.time()
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
                start_time = time.time()
                game.reset()
                swapSide(start_side)
                no_moves = False
        
        # print(time.time()-start_time)
        elapsed_time = int(time.time()-start_time)

        if elapsed_time > 100:

            print("Time out")
            # calculate each score for each agent
            agent1_piece_count = 0
            agent1_king_count = 0
            agent2_king_count = 0
            agent2_piece_count = 0

            board = game.get_board()
            

            if (start_side[0] == RED):
                color_1 = "RED"
                color_2 = "WHITE"
                agent1_king_count = board.red_kings
                agent1_piece_count = board.red_left

                agent2_king_count = board.white_kings
                agent2_piece_count = board.white_left
            else:
                color_1 = "WHITE"
                color_2 = "RED"
                agent1_piece_count = board.white_left
                agent1_king_count =  board.white_kings
                agent2_piece_count = board.red_left
                agent2_king_count =  board.red_kings
            
            agent1_score = agent1_piece_count + agent1_king_count*2
            agent2_score = agent2_piece_count + agent2_king_count*2
            

            if agent1_score > agent2_score:
                 print("{} Wins! (Agent 1 - ".format(color_1) + agent1_name + " )")
                 p1_wins+=1
            elif agent2_score > agent1_score:
                p2_wins += 1
                print("{} Wins! (Agent 2 - ".format(color_2) + agent2_name + " )")
            else:
                print("Draw Game")
                draw_count+=1            

            curr_round += 1
            if (curr_round >= rounds):
                run = False
            else:
                start_time = time.time()
                game.reset()
                swapSide(start_side)
                no_moves = False

            



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


    print("Agent 1 Win count: " + str(p1_wins))
    print("Agent 2 Win count: " + str(p2_wins))
    print("Draw count: " + str(draw_count))
    pygame.quit()

def swapSide(sides):
    temp = sides[0]
    sides[0] = sides[1]
    sides[1] = temp

main()