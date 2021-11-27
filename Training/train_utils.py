import pandas as pd
import numpy as np

# variables for hyperparameter optimization
TRAIN_SET = []
TRAIN_LABEL = []
TEST_SET = []
TEST_LABEL = []
BEST_MODEL = None
BEST_SCORE = np.inf
BS = []


def load_dataset(filename, separator=",", _numpy=False):
    df = pd.read_csv(filename, sep=separator)
    if _numpy:
        return df.to_numpy()
    else:
        return df


def convert_boardstate(statearray, board_shape):
    x = []
    for state in statearray:
        temp = list(map(int, list(state)))
        x.append(np.array(temp).reshape(board_shape))
    return np.asarray(x)


def get_labels(arrayset):
    return np.array([arrayset[:, 1], arrayset[:, 2]]).transpose()



