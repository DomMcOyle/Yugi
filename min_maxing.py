#from aima.games import alphabeta_search
import constants
import numpy as np


class tablut_move:
    def __init__(self):
        self.lut = np.array(constants.alph) #lookuptable

    def from_num_to_notation(self, num_move):
        #move converter, from couple of integers in range [0,8] to standard notation (string)
        chosen_column = self.lut[num_move[0]]
        chosen_row = num_move[1] + 1
        to_return = chosen_column + str(chosen_row)
        return to_return

    def from_notation_to_num(self, notation_move):
        #move converter, from standard notation to couple of integers in range [0,8]
        notation_move_to_use = list(notation_move)
        chosen_column = np.where(self.lut == notation_move_to_use[0])[0][0]
        chosen_row = int(notation_move_to_use[1]) - 1
        to_return = (chosen_column, chosen_row)
        return to_return


class tablut_state:
    def __init__(self, player, board):
        self.current_player = player
        self.current_board = board
        self.initial = np.array(constants.initial_state)

    def get_current_player(self):
        return self.current_player

    def set_current_player(self, player):
        self.current_player = player

    def get_current_board(self):
        return self.current_board

    def get_initial_board(self):
        return self.initial

    def negate_current_player(self):
        if self.current_player == constants.w_player:
            return constants.b_player
        else:
            return constants.w_player

    def __str__(self):
        return str((self.current_player, self.current_board))



class tablut_game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""
    def __free_box__(self, state, pos):
        if state.get_current_board()[pos[0], pos[1]] != constants.free_box:
            return False
        else:
            return True

    def __free_box_king__(self, state, pos):
        #print(state.get_current_board()[pos[0], pos[1]])
        if (state.get_current_board()[pos[0], pos[1]] == constants.free_box
                or state.get_current_board()[pos[0], pos[1]] == constants.tower):
            return True
        else:
            return False

    def actions(self, state):
        """
        given a state, returns all the possible moves for the pawns belonging to the current player
        :param state:
        :return:
            a list of moves, each move is a couple (starting_position, ending_position)
        """
        pos = np.where(state.get_current_board() == state.get_current_player())
        pos_rows = pos[0]
        pos_cols = pos[1]
        move_dict = {}
        for j in range(0, pos_rows.shape[0]):
            row = pos_rows[j]
            col = pos_cols[j]
            couple_list = []

            for i in range(0, 9):
                if self.__free_box__(state, (row, i)) and (row, i) not in couple_list:
                    couple_list.extend([(row, i)])

                if self.__free_box__(state, (i, col)) and (i, col) not in couple_list:
                    couple_list.extend([(i, col)])

            move_dict.update({(row, col): couple_list})
        # if it's the white's turn, consider the king
        if state.get_current_player() == constants.w_player:
            king_pos = np.where(state.get_current_board() == constants.king)
            king_pos_rows = king_pos[0]
            king_pos_cols = king_pos[1]
            for j in range(0, king_pos_rows.shape[0]):
                row = king_pos_rows[j]
                col = king_pos_cols[j]
                couple_list = []
                for i in range(0, 9):
                    if self.__free_box_king__(state, (row, i)) and (row, i) not in couple_list:
                        couple_list.extend([(row, i)])
                    if self.__free_box_king__(state, (i, col)) and (i, col) not in couple_list:
                        couple_list.extend([(i, col)])
            move_dict.update({(row, col): couple_list})
        to_return = []
        for pawn_pos in move_dict.keys():
            for dest_pos in move_dict.get(pawn_pos):
                to_return.append(np.array([pawn_pos, dest_pos]))
        return np.array(to_return)

    def result(self, state, move): #chiedere che cosa implementare
        """Return the state that results from making a move from a state."""
        result_board = state.get_current_board()
        if result_board[move[0][0], move[0][1]] != constants.king:
            result_board[move[1][0], move[1][1]] = state.get_current_player()
            result_board[move[0][0], move[0][1]] = constants.free_box
        else:
            result_board[move[1][0], move[1][1]] = constants.king
            if np.all(move[0] == constants.tower_position):
                result_board[move[0][0], move[0][1]] = constants.tower
            else:
                result_board[move[0][0], move[0][1]] = constants.free_box
        #handle captures
        try:
            if result_board[move[1][0]+1, move[1][1]] == state.negate_current_player():
                if (result_board[move[1][0] + 2, move[1][1]] == state.get_current_player()
                        or (state.get_current_player() == constants.w_player
                            and (result_board[move[1][0] + 2, move[1][1]] == constants.king))):
                    result_board[move[1][0] + 1, move[1][1]] = constants.free_box
        except:
           pass
        try:
            if result_board[move[1][0] - 1, move[1][1]] == state.negate_current_player():
                if (result_board[move[1][0] - 2, move[1][1]] == state.get_current_player()
                        or (state.get_current_player() == constants.w_player
                            and (result_board[move[1][0] - 2, move[1][1]] == constants.king))):
                    result_board[move[1][0] - 1, move[1][1]] = constants.free_box
        except:
           pass
        try:
            if result_board[move[1][0], move[1][1] + 1] == state.negate_current_player():
                if (result_board[move[1][0], move[1][1] + 2] == state.get_current_player()
                        or (state.get_current_player() == constants.w_player
                            and (result_board[move[1][0], move[1][1] + 2] == constants.king))):
                    result_board[move[1][0], move[1][1] + 1] = constants.free_box
        except:
           pass
        try:
            if result_board[move[1][0], move[1][1] - 1] == state.negate_current_player():
                if (result_board[move[1][0], move[1][1] - 2] == state.get_current_player()
                        or (state.get_current_player() == constants.w_player
                            and (result_board[move[1][0], move[1][1] - 2] == constants.king))):
                    result_board[move[1][0], move[1][1] - 1] = constants.free_box
        except:
           pass
        return result_board


    def utility(self, state, player): #euristica (da fare)
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state): #distinzione fra bianchi e neri (da fare)
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.get_current_player()

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        while True:
            for player in players:
                move = player(self, state)
                state = self.result(state, move)
                if self.terminal_test(state):
                    self.display(state)
                    return self.utility(state, self.to_move(self.initial))


def alphabeta_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action



gm = tablut_game()
cs = tablut_state(constants.b_player, np.array(constants.king_check_state))
move = np.array([[4, 2], [5, 2]])
print(gm.result(cs, move))