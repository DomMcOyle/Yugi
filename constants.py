### CLIENT ###
NUM_CMD_ARG = 1
W_NAME = "white"
B_NAME = "black"
W_PORT = 5800
B_PORT = 5801
### STATE ###
W_PLAYER = "W"
B_PLAYER ="B"
W_WIN = "WW"
B_WIN = "BW"
DRAW = "D"
JSON_BOARD = "board"
JSON_TURN = 'turn'
JSON_WPLAYER = "WHITE"
JSON_BPLAYER = "BLACK"
JSON_FROM = "from"
JSON_TO = "to"
JSON_BWIN = "BLACKWIN"
JSON_WWIN = "WHITEWIN"
JSON_DRAW = "DRAW"

### MIN MAXING ###
FREE_BOX = "O"
INITIAL_STATE = [list("OOOBBBOOO"),
                 list("OOOOBOOOO"),
                 list("OOOOWOOOO"),
                 list("BOOOWOOOB"),
                 list("BBWWKWWBB"),
                 list("BOOOWOOOB"),
                 list("OOOOWOOOO"),
                 list("OOOOBOOOO"),
                 list("OOOBBBOOO")]
KING_CHECK_STATE = [list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOKBOOOOO"),
                     list("OBOOOOOOO"),
                     list("OOOOTOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO")]
ALPH = list("abcdefghi")
KING = "K"
TOWER = "T"

TOWER_POSITION = (4, 4)
CAMP_POSITION = [(0, 3), (0, 4), (0, 5), (1, 5),
                 (3, 0), (4, 0), (5, 0), (4, 1),
                 (4, 7), (3, 8), (4, 8), (5, 8),
                 (7, 4), (8, 3), (8, 4), (8, 5)]

ESCAPE_POSITION = [(0, 1), (0, 2), (1, 0), (2, 0),
                    (0, 6), (0, 7), (1, 8), (2, 8),
                    (6, 0), (7, 0), (8, 1), (8, 2),
                    (8, 6), (8, 7), (6, 8), (7, 8)]

ADJACENT_TO_TOWER_POSITION = [(4, 3), (3, 4), (5, 4), (4, 5)]

JSON_LOOKUP = {'EMPTY': FREE_BOX, 'KING': KING, 'WHITE': W_PLAYER, 'BLACK': B_PLAYER, 'THRONE': TOWER}

