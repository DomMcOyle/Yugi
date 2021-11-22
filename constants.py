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
free_box = "O"
initial_state = [list("OOOBBBOOO"),
                 list("OOOOBOOOO"),
                 list("OOOOWOOOO"),
                 list("BOOOWOOOB"),
                 list("BBWWKWWBB"),
                 list("BOOOWOOOB"),
                 list("OOOOWOOOO"),
                 list("OOOOBOOOO"),
                 list("OOOBBBOOO")]
king_check_state = [list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOBOTOOOO"),
                     list("OOOWBOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO")]
alph = list("abcdefghi")
king = "K"
tower = "T"
tower_position = [4,4]
JSON_LOOKUP = {'EMPTY': free_box, 'KING': king, 'WHITE':W_PLAYER, 'BLACK': B_PLAYER, 'THRONE':tower }

