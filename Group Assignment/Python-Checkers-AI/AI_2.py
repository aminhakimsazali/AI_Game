from copy import deepcopy
from mcts import mcts

RED = (255,0,0)
WHITE = (255, 255, 255)

class AI:

    def play(self, board, turn, game):
        action = None
        mc = mcts(timeLimit=1500)
        try:
            action = mc.search(initialState=boardState(board, turn, 0))
        except:
            return None
        move = action.move
        skip = action.skip
        temp_piece = board.get_piece(action.piece.row, action.piece.col)
        new_board = self.simulate_move(temp_piece, move, board, game, skip)
        return new_board

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
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, game, skip)
                moves.append(self.gameState(new_board, color, game))
        return moves


class boardState():
    def __init__(self, board, color, depth):
        self.board = board
        self.color = color
        self.validActions = self.getActions()
        self.depth = depth

    def getActions(self):
        moves = []
        for piece in self.board.get_all_pieces(self.color):
            valid_moves = self.board.get_valid_moves(piece)
            for valid_move in valid_moves.items():
                move = valid_move[0]
                skip = valid_move[1]
                a = action(move, skip, piece)

                moves.append(a)
        return moves

    def getPossibleActions(self):
        return self.validActions

    def takeAction(self, action):
        move = action.move
        skip = action.skip

        temp_board = deepcopy(self.board)
        temp_piece = temp_board.get_piece(action.piece.row, action.piece.col)

        new_board = self.simulate_move(temp_piece, move, temp_board, skip)

        new_state = boardState(new_board, self.color, self.depth+1)
        return new_state

    def isTerminal(self):
        if (self.board.winner() != None):
            return True
        if(len(self.validActions) <= 0):
            return True
        if(self.depth>=100):
            return True
        return False

    def getReward(self):
        score = 0
        my_piece_count = 0
        my_king_count = 0
        enemy_king_count = 0
        enemy_piece_count = 0

        board = self.board.board
        turn = self.color

        if (self.color == RED):
            my_king_count = self.board.red_kings
            enemy_king_count = self.board.white_kings
            my_piece_count = self.board.red_left
            enemy_piece_count = self.board.white_left
        else:
            my_king_count = self.board.white_kings
            enemy_king_count = self.board.red_kings
            my_piece_count = self.board.white_left
            enemy_piece_count = self.board.red_left

        return my_piece_count-(enemy_piece_count*2)+(my_king_count*3)-(enemy_king_count*4)

    def simulate_move(self, piece, move, board, skip):
        board.move(piece, move[0], move[1])
        best_board = None
        best_score = None
        if skip:
            board.remove(skip)
        if (self.color == WHITE):
            actions = self.getActions2(board, RED)
            if (len(actions) == 0):
                return board
            possible_states = []
            for a in actions:
                possible_states.append(self.takeAction2(board, a))
            for x in possible_states:
                score = self.evalState(x, RED)
                if (best_score is None):
                    best_score = score
                    best_board = x
                elif (score >= best_score):
                    best_score = score
                    best_board = x
            return best_board
        else:
            actions = self.getActions2(board, WHITE)
            if (len(actions) == 0):
                return board
            possible_states = []
            for a in actions:
                possible_states.append(self.takeAction2(board, a))
            for x in possible_states:
                score = self.evalState(x, WHITE)
                if (best_score is None):
                    best_score = score
                    best_board = x
                elif (score >= best_score):
                    best_score = score
                    best_board = x
            return best_board
        return board

    def simulate_move2(self, piece, move, board, skip):
        board.move(piece, move[0], move[1])
        if skip:
            board.remove(skip)
        return board

    def evalState(self, move, turn):
        score = 0
        board = move.board
        c_x = -1

        for x in board:
            c_y = -1
            c_x += 1
            for y in x:
                c_y += 1
                if (y == turn):
                    score += 2
                elif (y != turn and y != 0):
                    score -= 5
        return score

    def getActions2(self, board, color):
        moves = []
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for valid_move in valid_moves.items():
                move = valid_move[0]
                skip = valid_move[1]
                a = action(move, skip, piece)
                moves.append(a)
        return moves

    def takeAction2(self, board, action):
        move = action.move
        skip = action.skip
        temp_board = deepcopy(board)
        temp_piece = temp_board.get_piece(action.piece.row, action.piece.col)
        new_board = self.simulate_move2(temp_piece, move, temp_board, skip)
        return new_board


class action():
    def __init__(self, move, skip, piece):
        self.skip = skip
        self.move = move
        self.piece = piece

    def __hash__(self):
        s = ""
        if(len(self.skip)==0):
            s = str(0)
        else:
            for x in self.skip:
                s += str(x.color[0]) + str(x.color[1]) + str(x.color[2])
        h = int(str(self.move[0]) + str(self.move[1]) + str(self.piece.row) + str(self.piece.col) + s)
        return h