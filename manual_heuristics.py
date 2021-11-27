from heuristics import Heuristics
import constants
import numpy as np


TOTAL_PAWN_B = 16
TOTAL_PAWN_W = 8

ESCAPE_BLOCK_POSITION = [(1, 2), (2, 1), (1, 6), (2, 7),
                         (6, 1), (7, 2), (6, 7), (7, 6)]

BLACK_FRONT_LINE = [(1, 4), (4, 1), (4, 7), (7, 4)]

neighborhood_coord = [(1, 0), (0, 1), (-1, 0), (0, -1)]

"""
    Support function that takes a board, two points a and b,
    and checks if the path in board between a and b is free (only 'O' in the path)
    
    If the flag check_destination is True, this function checks if the b point is free too
"""


def free_path(board, a, b, check_destination=False):
    if a[0] == b[0]:
        row_fixed = a[0]
        path = board[row_fixed][min(a[1], b[1]) + 1:max(a[1], b[1])]
        return all(c == constants.FREE_BOX for c in path) and (
                not check_destination or board[b[0]][b[1]] == constants.FREE_BOX)
    elif a[1] == b[1]:
        column_fixed = a[1]
        path = [c[column_fixed] for c in board[min(a[0], b[0]) + 1:max(a[0], b[0])]]
        return all(c == constants.FREE_BOX for c in path) and (
                not check_destination or board[b[0]][b[1]] == constants.FREE_BOX)
    return False


"""
    Support function that calculate the manhattan distance between two points a and b
"""


def manhattan_distance(a, b):
    return sum(abs(val1 - val2) for val1, val2 in zip(a, b))


"""
    Concrete class for a manual heuristic
"""


class ManualHeuristics(Heuristics):
    """
        Given a game state with the current board and the current player color
        returns an evaluation of the state, with constant weights
    """

    @staticmethod
    def evaluate(game_state, choosing_player, depth):
        w_lost_pieces = 30
        w_eaten_pieces = 20
        w_king_surround = 100

        w_king_escaped = 10000
        w_king_eaten = 10000

        # BLACK WEIGHTS
        w_king_escape = -100
        w_blocked_escape = 20
        w_front_line = 15

        # WHITE WEIGHTS
        w_escape_distance = 100
        w_free_escapes = 200
        w_king_protection = 10

        current_player = game_state.get_current_player()
        board = game_state.get_current_board()

        # Calculate remain pieces for the two players (we'll need both of them for later use!)
        remain_pieces_w = np.count_nonzero(board == constants.W_PLAYER)
        remain_pieces_b = np.count_nonzero(board == constants.B_PLAYER)

        # Calculate how many pieces has the king in the neighborhood
        coord_king = np.where(board == constants.KING)
        try:
            coord_king = (coord_king[0][0], coord_king[1][0])
        except IndexError:
            final_heuristics = (w_king_eaten - depth) if current_player == constants.W_PLAYER else (-w_king_eaten + depth)
            return final_heuristics if choosing_player != current_player else -final_heuristics

        if coord_king in constants.ESCAPE_POSITION:
            final_heuristics = (w_king_escaped - depth) if current_player == constants.B_PLAYER else (- w_king_escaped + depth)
            return final_heuristics if choosing_player != current_player else -final_heuristics

        # Generate king's neighborhood list of coordinates
        neighborhood_king = [(coord_king[0] + neighbor[0], coord_king[1] + neighbor[1]) for neighbor in
                             neighborhood_coord]
        neighborhood_king = list(filter(lambda x: (0 <= x[0] <= 8 and 0 <= x[1] <= 8), neighborhood_king))

        # Calculate how many black pawns/tower/camps there are in the king's neighborhood
        king_surround = sum(
            (board[x] in [constants.B_PLAYER, constants.TOWER]) or (x in constants.CAMP_POSITION) for x in
            neighborhood_king)

        # Heuristics for the black player
        if current_player == constants.W_PLAYER:
            lost_pieces = TOTAL_PAWN_B - remain_pieces_b
            eaten_pieces = TOTAL_PAWN_W - remain_pieces_w

            # Check if the king can escape
            king_escape = sum(
                free_path(board, coord_king, escape_coord, True) for escape_coord in constants.ESCAPE_POSITION)

            # Check how many black pieces block the king's escapes
            blocked_escape = sum(
                board[escape_block] == constants.B_PLAYER for escape_block in ESCAPE_BLOCK_POSITION)

            # Check if moved black pieces on front line camps
            front_line_moved = sum(
                board[front_line_coord] == constants.B_PLAYER for front_line_coord in BLACK_FRONT_LINE)

            player_heuristics = (king_escape * w_king_escape) + (blocked_escape * w_blocked_escape) \
                                + (front_line_moved * w_front_line)
        # Heuristics for the white player
        else:
            lost_pieces = TOTAL_PAWN_W - remain_pieces_w
            eaten_pieces = TOTAL_PAWN_B - remain_pieces_b

            # Calculate the manhattan distance between the king and all escape positions
            min_escape_distance = min([manhattan_distance(coord_king, escape_coord) for escape_coord in
                                       constants.ESCAPE_POSITION])

            # Check how many escapes are free (the white can win next turn)
            free_escapes = len([escape_coord for escape_coord in constants.ESCAPE_POSITION if
                                free_path(board, coord_king, escape_coord, True)])

            # Count how many white pieces are around the king
            king_protection = sum(board[x] == constants.W_PLAYER for x in neighborhood_king)

            player_heuristics = (w_escape_distance / min_escape_distance) + (free_escapes * w_free_escapes) \
                                + (king_protection * w_king_protection)

        fixed_heuristics = (100 + eaten_pieces * w_eaten_pieces) - (50 + lost_pieces * w_lost_pieces)
        swap_heuristics = (king_surround * w_king_surround)

        final_heuristics = fixed_heuristics + player_heuristics + \
               (-swap_heuristics if current_player == constants.W_PLAYER else swap_heuristics)

        return final_heuristics if choosing_player != current_player else -final_heuristics


"""
t = tablut_state(constants.W_PLAYER, np.array(constants.INITIAL_STATE))
ManualHeuristics.evaluate(t)
"""
