from copy import deepcopy
import pygame
import random

RED = (255, 0, 0)
WHITE = (255, 255, 255)


class BASE:
    def __init__(self):
        self.totalnodes = 0

    def explored_node(self):
        return self.totalnodes

    def random_move(self, position, turn, game):
        move_list = []
        
        # Get all possible moves
        for move in self.get_all_moves(position, turn, game):
            move_list.append(move)

        # randomly choose one move
        try:
            random_move = random.choice(move_list)
            return random_move
        except:
            return 

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



