from os import walk
import pandas as pd
import numpy as np

convert_dict = {"O": "0", "T": "0", "W": "2", "B": "1", "K": "3"}

"""
    Script used to create a dataset from all the logs of previous years games of tablut challenge
"""


def parse_dataset(path_to_games, save_path="./"):
    df = pd.DataFrame(
        columns=["current_state", "color_player", "turn_number", "match_result_white", "match_result_black"])
    filenames = next(walk(path_to_games), (None, None, []))[2]
    row_ds = 0

    for filename in filenames:
        n_turn = 1
        color_player = 0

        f = open(path_to_games + "\\" + filename, "r")
        lines = f.readlines()

        match_result = (0, 0)
        for back_index in range(len(lines) - 1, 0, -1):
            if "vince" in lines[back_index]:
                match_result = (1, 0) if "Bianco" in lines[back_index] else (0, 1)
                break
            if "pareggio" in lines[back_index]:
                break

        for line_index in range(0, len(lines)):
            if "Stato:" in lines[line_index]:
                current_state = "".join(lines[line_index + 1:line_index + 10]).replace("\n", "")
                if current_state[-1] == "-":
                    current_state = lines[line_index][
                                    lines[line_index].rfind(":") + 2:lines[line_index].rfind(":") + 11] + current_state[
                                                                                                          :-1]
                current_state = "".join(map(str, [convert_dict[value] for value in current_state]))
                df.loc[row_ds] = [current_state, color_player, n_turn, match_result[0], match_result[1]]

                #prepare for flipping - flip both axis
                current_statea = np.array(list(current_state))
                current_stater = current_statea.reshape(9,9)
                current_stater = np.flip(current_stater)
                origin_flip = "".join(current_stater.ravel())

                row_ds += 1
                df.loc[row_ds] = [origin_flip, color_player, n_turn, match_result[0], match_result[1]]

                #flip only one axis
                current_stater0 = np.flip(current_stater, axis=0)
                flip_0 = "".join(current_stater0.ravel())

                row_ds += 1
                df.loc[row_ds] = [flip_0, color_player, n_turn, match_result[0], match_result[1]]

                #flip the other axis
                current_stater1 = np.flip(current_stater, axis=1)
                flip_1 = "".join(current_stater1.ravel())

                row_ds += 1
                df.loc[row_ds] = [flip_1, color_player, n_turn, match_result[0], match_result[1]]

                n_turn += 1
                color_player = abs(color_player - 1)
                row_ds += 1

    df.to_csv(save_path + "parsed_dataset_v3.csv", index=False, mode="w+")

parse_dataset("C:\\Users\\Neo Dom-Z Mk. II\\Desktop\\games")