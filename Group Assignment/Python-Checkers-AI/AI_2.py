from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255, 255, 255)

class AI:
    def __init__ (self):
        self.totalnodes = 0

    def explored_node(self):
        return self.totalnodes

    def minimax(self, position, depth, alpha, beta, max_player, turn, game):
        self.totalnodes+=1
        if depth == 0 or position.winner() != None:
            return self.evalState(position, turn), position
        
        if max_player:
            maxEval = float('-inf')
            best_move = None
            for move in self.get_all_moves(position, turn, game):
                evaluation = self.minimax(move, depth-1, alpha, beta, False, turn, game)[0]
                maxEval = max(maxEval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
                if maxEval == evaluation:
                    best_move = move
            
            return maxEval, best_move
        else:
            minEval = float('inf')
            best_move = None
            for move in self.get_all_moves(position, turn, game):
                evaluation = self.minimax(move, depth-1, alpha, beta, True, turn, game)[0]
                minEval = min(minEval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
                if minEval == evaluation:
                    best_move = move
            
            return minEval, best_move


    def evalState(self, move, turn):
        score = 0
        board = move.board
        c_x = -1
        for x in board:
            c_y = -1
            c_x += 1
            for y in x:
                c_y += 1
                if (y == turn and c_x == 0):
                    score += 4
                elif (y == turn and c_x == 7):
                    score += 4
                elif (y == turn):
                    score += 2
                elif (y != turn and y != 0):
                    score -= 3
        return score

    def simulate_move(self, piece, move, board, game, skip):
        board.move(piece, move[0], move[1])
        if skip:
            board.remove(skip)

        return board


    def get_all_moves(self, board, color, game):
        moves = []

        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                # self.draw_moves(game, board, piece)
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, game, skip)
                moves.append(new_board)
        
        return moves


    def draw_moves(self, game, board, piece):
        valid_moves = board.get_valid_moves(piece)
        board.draw(game.win)
        pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
        game.draw_valid_moves(valid_moves.keys())
        pygame.display.update()
        #pygame.time.delay(100)

  