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
