# from aima.games import alphabeta_search

import constants
import numpy as np
from tensorflow.keras.models import load_model
import time
from manual_heuristics import ManualHeuristics


class tablut_move:
    def __init__(self):
        self.lut = np.array(constants.ALPH)  # lookuptable

    def from_num_to_notation(self, num_move):
        # move converter, from couple of integers in range [0,8] to standard notation (string)
        chosen_column = self.lut[num_move[1]]
        chosen_row = num_move[0] + 1
        to_return = chosen_column + str(chosen_row)
        return to_return

    def from_notation_to_num(self, notation_move):
        # move converter, from standard notation to couple of integers in range [0,8]
        notation_move_to_use = list(notation_move)
        chosen_column = np.where(self.lut == notation_move_to_use[0])[0][0]
        chosen_row = int(notation_move_to_use[1]) - 1
        to_return = (chosen_row, chosen_column)
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
        print("  a b c d e f g h i")
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

        return tablut_state(player, np.array(board))


class tablut_game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def __init__(self, neuralpath="Atem//"):
        if neuralpath is None:
            self.pre_trained = None
        else:
            self.pre_trained = load_model(neuralpath)

    def __free_box__(self, state, pos):
        if state.get_current_board()[pos[0], pos[1]] != constants.FREE_BOX:
            return False
        else:
            return True

    def __inbetween__(self, pawn_pos, dest_pos):
        if pawn_pos[0] == dest_pos[0]:
            min_val = min((pawn_pos[1], dest_pos[1]))
            return [(pawn_pos[0], min_val + i) for i in range(0, abs(pawn_pos[1] - dest_pos[1]) + 1)]
        if pawn_pos[1] == dest_pos[1]:
            min_val = min((pawn_pos[0], dest_pos[0]))
            return [(pawn_pos[1], min_val + i) for i in range(0, abs(pawn_pos[0] - dest_pos[0]) + 1)]


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
                    to_return.append([pawn_pos, dest_pos])
                if pawn_pos in fields and dest_pos in fields:
                    if pawn_pos[0] == dest_pos[0]:
                        if abs(pawn_pos[1] - dest_pos[1]) < constants.CITADEL_THRESHOLD:
                            to_return.append([pawn_pos, dest_pos])
                if pawn_pos not in fields and dest_pos not in fields:
                    for inb_elem in self.__inbetween__(pawn_pos, dest_pos):
                        if inb_elem in constants.CAMP_POSITION:
                            if [pawn_pos, dest_pos] in to_return:
                                to_return.remove([pawn_pos, dest_pos])
        return np.array(to_return)

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        result_board = state.get_current_board().copy()

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
                        or (move[1][0] + 2, move[1][1]) in constants.CAMP_POSITION_FOR_CAPTURES
                        or (move[1][0] + 2, move[1][1]) == constants.TOWER_POSITION
                        or (state.get_current_player() == constants.W_PLAYER
                            and (result_board[move[1][0] + 2, move[1][1]] == constants.KING))):
                    result_board[move[1][0] + 1, move[1][1]] = constants.FREE_BOX
        except:
            pass
        try:
            if result_board[move[1][0] - 1, move[1][1]] == state.negate_current_player():
                if (result_board[move[1][0] - 2, move[1][1]] == state.get_current_player()
                        or (move[1][0] - 2, move[1][1]) in constants.CAMP_POSITION_FOR_CAPTURES
                        or (move[1][0] - 2, move[1][1]) == constants.TOWER_POSITION
                        or (state.get_current_player() == constants.W_PLAYER
                            and (result_board[move[1][0] - 2, move[1][1]] == constants.KING))):
                    result_board[move[1][0] - 1, move[1][1]] = constants.FREE_BOX
        except:
            pass
        try:
            if result_board[move[1][0], move[1][1] + 1] == state.negate_current_player():
                if (result_board[move[1][0], move[1][1] + 2] == state.get_current_player()
                        or (move[1][0], move[1][1] + 2) in constants.CAMP_POSITION_FOR_CAPTURES
                        or (move[1][0], move[1][1] + 2) == constants.TOWER_POSITION
                        or (state.get_current_player() == constants.W_PLAYER
                            and (result_board[move[1][0], move[1][1] + 2] == constants.KING))):
                    result_board[move[1][0], move[1][1] + 1] = constants.FREE_BOX
        except:
            pass
        try:
            if result_board[move[1][0], move[1][1] - 1] == state.negate_current_player():
                if (result_board[move[1][0], move[1][1] - 2] == state.get_current_player()
                        or (move[1][0], move[1][1] - 2) in constants.CAMP_POSITION_FOR_CAPTURES
                        or (move[1][0], move[1][1] - 2) == constants.TOWER_POSITION
                        or (state.get_current_player() == constants.W_PLAYER

                            and (result_board[move[1][0], move[1][1] - 2] == constants.KING))):
                    result_board[move[1][0], move[1][1] - 1] = constants.FREE_BOX
        except:
            pass
        # king capture
        king_pos = np.where(result_board == constants.KING)
        king_pos_rows = king_pos[0]
        king_pos_cols = king_pos[1]
        result_state = tablut_state(state.negate_current_player(), result_board)
        if state.get_current_player() == constants.B_PLAYER:
            if ((king_pos_rows, king_pos_cols) == constants.TOWER_POSITION
                    and self.__king_surrounded_num__(result_state) == 4):
                result_board[king_pos_rows, king_pos_cols] = constants.TOWER # black wins by capturing the king in the tower
            else:
                if self.__king_adjacent_to_tower__(result_state) and self.__king_surrounded_num__(result_state) == 3:
                    result_board[king_pos_rows, king_pos_cols] = constants.FREE_BOX
                    # black wins by capturing the king adjacent to the tower and surrounded by
                    # 3 pawns
                elif not self.__king_adjacent_to_tower__(result_state) and self.__king_surrounded_num__(result_state) == 2 \
                        and self.__king_eaten_normal__(result_state):
                    result_board[king_pos_rows, king_pos_cols] = constants.FREE_BOX
                    # black wins by capturing the king as a normal pawn

        state_to_return = tablut_state(state.negate_current_player(), result_board)
        return state_to_return

    def utility(self, state, player, depth):
        """Return the value of this final state to player."""

        man_val = ManualHeuristics.evaluate(state, player, depth=depth)
        if abs(man_val) > constants.MAN_THRESHOLD:
            return man_val

        new_mat = np.vectorize(constants.CONVERT_DICT.get)(state.get_current_board())
        to_predict = (np.reshape(new_mat, (1, 9, 9, 1)) - 1)/2

        prediction = self.pre_trained(to_predict, training=False)
        to_return = 0
        prediction = prediction.numpy()[0][0]
        if player == constants.W_PLAYER:
            to_return = prediction
        elif player == constants.B_PLAYER:
            to_return = 1-prediction
        return (1 + to_return) * man_val

    def __king_eaten_normal__(self, state):
        king_pos = np.where(state.get_current_board() == constants.KING)
        king_pos_rows = king_pos[0]
        king_pos_cols = king_pos[1]
        board = state.get_current_board()
        try:
            return board[king_pos_rows + 1, king_pos_cols] == board[king_pos_rows - 1, king_pos_cols] == constants.B_PLAYER \
                or board[king_pos_rows, king_pos_cols + 1] == board[king_pos_rows, king_pos_cols - 1] == constants.B_PLAYER
        except IndexError:
            return False

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

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        king_pos = np.where(state.get_current_board() == constants.KING)
        king_pos_rows = king_pos[0]
        king_pos_cols = king_pos[1]
        # white wins, the king has escaped
        if king_pos_rows.shape[0] == 0 and king_pos_cols.shape[0] == 0:
            return True
        elif (king_pos_rows, king_pos_cols) in constants.ESCAPE_POSITION:
            return True
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

    def __complement_player__(self, player):
        if player == constants.W_PLAYER:
            return constants.B_PLAYER
        else:
            return constants.W_PLAYER

    def max_value(self, state, alpha, beta, depth, game, cutoff_test, eval_fn, choosing_player, start_time):

        if cutoff_test(state, depth):
            return eval_fn(state, choosing_player, depth)
        v = -np.inf
        obtained_actions = game.actions(state)
        np.random.shuffle(obtained_actions)
        for a in obtained_actions:
            if time.time() - start_time > constants.TIME_THRESHOLD:
                return max(v, self.utility(game.result(state, a), choosing_player, depth))
            v = max(v, self.min_value(game.result(state, a), alpha, beta, depth + 1, game,
                                      cutoff_test, eval_fn, choosing_player, start_time))#self.__complement_player__(choosing_player)))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth, game, cutoff_test, eval_fn, choosing_player, start_time):

        if cutoff_test(state, depth):
            return eval_fn(state, choosing_player, depth)
        v = np.inf
        obtained_actions = game.actions(state)
        np.random.shuffle(obtained_actions)
        for a in obtained_actions:
            if time.time() - start_time > constants.TIME_THRESHOLD:
                return min(v, self.utility(game.result(state, a), choosing_player, depth))

            v = min(v, self.max_value(game.result(state, a), alpha, beta, depth + 1, game,
                                      cutoff_test, eval_fn, choosing_player, start_time))#self.__complement_player__(choosing_player)))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def alphabeta_search(self, state, game, choosing_player, d=2, cutoff_test=None, eval_fn=None):
        """Search game to determine best action; use alpha-beta pruning.
        This version cuts off search and uses an evaluation function."""

        player = game.to_move(state)
        # Body of alpha_beta_cutoff_search starts here:
        # The default test cuts off at depth d or at a terminal state
        cutoff_test = (cutoff_test or (lambda state, depth: depth > d or game.terminal_test(state)))
        eval_fn = eval_fn or (lambda state, choosing_player, depth: game.utility(state, player, depth))
        best_score = -np.inf
        beta = np.inf
        best_action = None
        start_time = time.time()
        obtained_actions = game.actions(state)
        np.random.shuffle(obtained_actions)
        for a in obtained_actions:
            v = self.min_value(game.result(state, a), best_score, beta, 1, game, cutoff_test,
                               eval_fn, choosing_player, start_time)
            if v > best_score:
                best_score = v
                best_action = a
        alpha_computation_time = time.time() - start_time
        return best_action, alpha_computation_time