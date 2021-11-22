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
                     list("OBKBOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOTOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO"),
                     list("OOOOOOOOO")]
alph = list("abcdefghi")
king = "K"
tower = "T"
tower_position = (4, 4)
camp_position = [(0, 3), (0, 4), (0, 5), (1, 5),
                 (3, 0), (4, 0), (5, 0), (4, 1),
                 (4, 7), (3, 8), (4, 8), (5, 8),
                 (7, 4), (8, 3), (8, 4), (8, 5)]

escape_positions = [(0, 1), (0, 2), (1, 0), (2, 0),
                    (0, 6), (0, 7), (1, 8), (2, 8),
                    (6, 0), (7, 0), (8, 1), (8, 2),
                    (8, 6), (8, 7), (6, 8), (7, 8)]

adjacent_to_tower_positions = [(4, 3), (3, 4), (5, 4), (4, 5)]

