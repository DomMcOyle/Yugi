### CLIENT ###
w_name = "white"
b_name = "black"
w_port = 5800
b_port = 5801
### STATE ###
w_player = "W"
b_player ="B"
w_win = "WW"
b_win = "BW"
draw = "D"
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