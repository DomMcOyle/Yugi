# from aima.games import alphabeta_search
import constants
import numpy as np
from keras.models import load_model


class tablut_move:
    def __init__(self):
        self.lut = np.array(constants.ALPH)  # lookuptable

    def from_num_to_notation(self, num_move):
        # move converter, from couple of integers in range [0,8] to standard notation (string)
        chosen_column = self.lut[num_move[0]]
        chosen_row = num_move[1] + 1
        to_return = chosen_column + str(chosen_row)
        return to_return

    def from_notation_to_num(self, notation_move):
        # move converter, from standard notation to couple of integers in range [0,8]
        notation_move_to_use = list(notation_move)
        chosen_column = np.where(self.lut == notation_move_to_use[0])[0][0]
        chosen_row = int(notation_move_to_use[1]) - 1
        to_return = (chosen_column, chosen_row)
        return to_return

    @staticmethod
    def to_json_dict(from_, to, turn, convert=True):
        to_send = dict()
        if convert:
            move = tablut_move()
            to_send[constants.JSON_FROM] = move.from_num_to_notation(from_)
            to_send[constants.JSON_TO] = move.from_num_to_notation(to)
        else:
            to_send[constants.JSON_FROM] = from_
            to_send[constants.JSON_TO] = to
        if turn == constants.W_PLAYER:
            to_send[constants.JSON_TURN] = constants.JSON_WPLAYER
        else:
            to_send[constants.JSON_TURN] = constants.JSON_BPLAYER
        return to_send


class tablut_state:
    def __init__(self, player, board):
        self.current_player = player
        self.current_board = board
        self.initial = np.array(constants.INITIAL_STATE)

    def get_current_player(self):
        return self.current_player

    def set_current_player(self, player):
        self.current_player = player

    def get_current_board(self):
        return self.current_board

    def get_initial_board(self):
        return self.initial

    def negate_current_player(self):
        if self.current_player == constants.W_PLAYER:
            return constants.B_PLAYER
        else:
            return constants.W_PLAYER

    def render(self):
        print("Turn: " + str(self.current_player))
        i = 1
        print("  a  b  c  d  e  f  g  h  i")
        for row in self.current_board:
            temp = str(row)
            print(str(i) + " " + (temp.replace("[", "").replace("]", "").replace(",", " ").replace("'", "")))
            i = i + 1


    def __str__(self):
        return str((self.current_player, self.current_board))

    @staticmethod
    def from_json_dict_state(json_dict):
        player = json_dict[constants.JSON_TURN]
        if player == constants.JSON_BPLAYER:
            player = constants.B_PLAYER
        elif player == constants.JSON_WPLAYER:
            player = constants.W_PLAYER
        elif player == constants.JSON_BWIN:
            player = constants.B_WIN
        elif player == constants.JSON_WWIN:
            player = constants.W_WIN
        elif player == constants.JSON_DRAW:
            player = constants.DRAW
        board = json_dict[constants.JSON_BOARD]
        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                board[r][c] = constants.JSON_LOOKUP[board[r][c]]

        return tablut_state(player, board)


class tablut_game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def __free_box__(self, state, pos):
        if state.get_current_board()[pos[0], pos[1]] != constants.FREE_BOX:
            return False
        else:
            return True

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
        if state.get_current_player() == constants.W_PLAYER:
            king_pos = np.where(state.get_current_board() == constants.KING)
            pos_rows = np.append(pos[0], (king_pos[0]))
            pos_cols = np.append(pos[1], (king_pos[1]))

        move_dict = {}
        for i in range(0, pos_rows.shape[0]):
            couple_list = []
            down_flag = True
            left_flag = True
            up_flag = True
            right_flag = True
            for j in range(1, 9):
                row_to_check_down = pos_rows[i] + j
                col_to_check_left = pos_cols[i] + j
                row_to_check_up = pos_rows[i] - j
                col_to_check_right = pos_cols[i] - j
                if row_to_check_down < 9 and down_flag:
                    if self.__free_box__(state, (row_to_check_down, pos_cols[i])):
                        couple_list.extend([(row_to_check_down, pos_cols[i])])
                    else:
                        down_flag = False
                if col_to_check_left < 9 and left_flag:
                    if self.__free_box__(state, (pos_rows[i], col_to_check_left)):
                        couple_list.extend([(pos_rows[i], col_to_check_left)])
                    else:
                        left_flag = False
                if row_to_check_up >= 0 and up_flag:
                    if self.__free_box__(state, (row_to_check_up, pos_cols[i])):
                        couple_list.extend([(row_to_check_up, pos_cols[i])])
                    else:
                        up_flag = False
                if col_to_check_right >= 0 and right_flag:
                    if self.__free_box__(state, (pos_rows[i], col_to_check_right)):
                        couple_list.extend([(pos_rows[i], col_to_check_right)])
                    else:
                        right_flag = False
                move_dict.update({(pos_rows[i], pos_cols[i]): couple_list})
        fields = constants.CAMP_POSITION
        to_return = []
        for pawn_pos in move_dict.keys():
            for dest_pos in move_dict.get(pawn_pos):
                if pawn_pos in fields or (dest_pos not in fields and dest_pos != constants.TOWER_POSITION):
                    to_return.append(np.array([pawn_pos, dest_pos]))
        return np.array(to_return)

    def result(self, state, move):  # controllare molto bene
        """Return the state that results from making a move from a state."""
        result_board = state.get_current_board()
        if result_board[move[0][0], move[0][1]] != constants.KING:
            result_board[move[1][0], move[1][1]] = state.get_current_player()
            result_board[move[0][0], move[0][1]] = constants.FREE_BOX
        else:
            result_board[move[1][0], move[1][1]] = constants.KING
            if np.all(move[0] == constants.TOWER_POSITION):
                result_board[move[0][0], move[0][1]] = constants.TOWER
            else:
                result_board[move[0][0], move[0][1]] = constants.FREE_BOX

        # handle captures add capture with camps (the next box can be a camp, the tower or an allied pawn, or king
        # in case of the white player)
        try:
            if result_board[move[1][0] + 1, move[1][1]] == state.negate_current_player():
                if (result_board[move[1][0] + 2, move[1][1]] == state.get_current_player()
                        or (move[1][0] + 2, move[1][1]) in constants.CAMP_POSITION
                        or (move[1][0] + 2, move[1][1]) == constants.TOWER_POSITION
                        or (state.get_current_player() == constants.W_PLAYER
                            and (result_board[move[1][0] + 2, move[1][1]] == constants.KING))):
                    result_board[move[1][0] + 1, move[1][1]] = constants.FREE_BOX
        except:
            pass
        try:
            if result_board[move[1][0] - 1, move[1][1]] == state.negate_current_player():
                if (result_board[move[1][0] - 2, move[1][1]] == state.get_current_player()
                        or (move[1][0] - 2, move[1][1]) in constants.CAMP_POSITION
                        or (move[1][0] - 2, move[1][1]) == constants.TOWER_POSITION
                        or (state.get_current_player() == constants.W_PLAYER
                            and (result_board[move[1][0] - 2, move[1][1]] == constants.KING))):
                    result_board[move[1][0] - 1, move[1][1]] = constants.FREE_BOX
        except:
            pass
        try:
            if result_board[move[1][0], move[1][1] + 1] == state.negate_current_player():
                if (result_board[move[1][0], move[1][1] + 2] == state.get_current_player()
                        or (move[1][0], move[1][1] + 2) in constants.CAMP_POSITION
                        or (move[1][0], move[1][1] + 2) == constants.TOWER_POSITION
                        or (state.get_current_player() == constants.W_PLAYER
                            and (result_board[move[1][0], move[1][1] + 2] == constants.KING))):
                    result_board[move[1][0], move[1][1] + 1] = constants.FREE_BOX
        except:
            pass
        try:
            if result_board[move[1][0], move[1][1] - 1] == state.negate_current_player():
                if (result_board[move[1][0], move[1][1] - 2] == state.get_current_player()
                        or (move[1][0], move[1][1] - 2) in constants.CAMP_POSITION
                        or (move[1][0], move[1][1] - 2) == constants.TOWER_POSITION
                        or (state.get_current_player() == constants.W_PLAYER

                            and (result_board[move[1][0], move[1][1] - 2] == constants.KING))):
                    result_board[move[1][0], move[1][1] - 1] = constants.FREE_BOX
        except:
            pass
        state_to_return = tablut_state(state.negate_current_player(), result_board)
        return state_to_return

    def utility(self, state, player):  # euristica (da fare)
        """Return the value of this final state to player."""
        # dimensione in più: reshape(1, 9, 9, 1) conversione da stringa a numero. Guardare branch neural
        file_path = "Test1//"
        pre_trained = load_model(file_path)
        #print(type(state.get_current_board()))
        new_mat = np.vectorize(constants.CONVERT_DICT.get)(state.get_current_board())
        #print(type(new_mat))
        to_predict = np.reshape(new_mat, (1, 9, 9, 1))/3

        prediction = pre_trained.predict(to_predict)
        #print(prediction)
        to_return = 0
        prediction = np.reshape(prediction, 2)
        if abs(prediction[0] - prediction[1]) > 0.1:
            max_val = max(prediction)
            if player == constants.W_PLAYER and np.where(prediction == max_val)[0][0] == 0:
                to_return = prediction[0]
            elif player == constants.W_PLAYER and np.where(prediction == max_val)[0][0] == 1:
                to_return = -prediction[1]
            elif player == constants.B_PLAYER and np.where(prediction == max_val)[0][0] == 1:
                to_return = prediction[1]
            elif player == constants.B_PLAYER and np.where(prediction == max_val)[0][0] == 0:
                to_return = -prediction[0]
        return to_return

    def __king_adjacent_to_tower__(self, state):
        king_pos = np.where(state.get_current_board() == constants.KING)
        king_pos_rows = king_pos[0]
        king_pos_cols = king_pos[1]
        if (king_pos_rows, king_pos_cols) in constants.ADJACENT_TO_TOWER_POSITION:
            return True
        return False

    def __king_surrounded_num__(self, state):
        king_pos = np.where(state.get_current_board() == constants.KING)
        king_pos_rows = king_pos[0]
        king_pos_cols = king_pos[1]
        to_return = 0
        try:
            if state.get_current_board()[king_pos_rows + 1, king_pos_cols] == constants.B_PLAYER:
                to_return += 1
        except:
            pass
        try:
            if state.get_current_board()[king_pos_rows - 1, king_pos_cols] == constants.B_PLAYER:
                to_return += 1
        except:
            pass
        try:
            if state.get_current_board()[king_pos_rows, king_pos_cols + 1] == constants.B_PLAYER:
                to_return += 1
        except:
            pass
        try:
            if state.get_current_board()[king_pos_rows, king_pos_cols - 1] == constants.B_PLAYER:
                to_return += 1
        except:
            pass
        return to_return

    def terminal_test(self, state):  # distinzione fra bianchi e neri (da fare)
        """Return True if this is a final state for the game."""
        king_pos = np.where(state.get_current_board() == constants.KING)
        king_pos_rows = king_pos[0]
        king_pos_cols = king_pos[1]
        # white wins, the king has escaped

        if (king_pos_rows, king_pos_cols) in constants.ESCAPE_POSITION:
            return True
        else:
            if ((king_pos_rows, king_pos_cols) == constants.TOWER_POSITION
                    and self.__king_surrounded_num__(state) == 4):
                return True  # black wins by capturing the king in the tower
            else:
                if self.__king_adjacent_to_tower__(state) and self.__king_surrounded_num__(state) == 3:
                    return True # black wins by capturing the king adjacent to the tower and surrounded by
                                # 3 pawns
                elif not self.__king_adjacent_to_tower__(state) and self.__king_surrounded_num__(state) == 2:
                    return True # black wins by capturing the king as a normal pawn
        return False

        # return not self.actions(state)

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


def alphabeta_search(state, game, d=2, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""
    player = game.to_move(state)

    def max_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            print("max: " + str(eval_fn(state)))
            print(state.get_current_board())
            return eval_fn(state)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if cutoff_test(state, depth):
            print("min: " + str(eval_fn(state)))
            print(state.get_current_board())
            return eval_fn(state)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
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


""" test result
gm = tablut_game()
cs = tablut_state(constants.B_PLAYER, np.array(constants.KING_CHECK_STATE))
move = np.array([[6, 5], [6, 4]])
print(gm.result(cs, move))"""

""" test alphabeta"""
gm = tablut_game()
cs = tablut_state(constants.B_PLAYER, np.array(constants.KING_CHECK_STATE))
print(alphabeta_search(cs, gm))




""" test actions
gm = tablut_game()
cs = tablut_state(constants.W_PLAYER, np.array(constants.KING_CHECK_STATE))
print(gm.actions(cs))"""

""" test utility 
gm = tablut_game()
cs = tablut_state(constants.B_PLAYER, np.array(constants.KING_CHECK_STATE))
print(gm.utility(cs, cs.get_current_player()))
"""