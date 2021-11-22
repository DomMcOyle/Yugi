import train_utils as tu
import pandas as pd
import numpy as np

from keras.layers import Conv2D, MaxPooling2D, Input, Dropout, Flatten, Dense
from keras.models import Model
from keras.optimizers.adam_v2 import Adam
from keras import callbacks


def build_network(input_shape):
    input_layer = Input(input_shape)
    hidden = Conv2D(filters=16 ,kernel_size=(2,2),strides=(1,1), activation='relu')(input_layer)
    hidden = MaxPooling2D()(hidden)
    hidden = Conv2D(filters=8,kernel_size=(2,2),strides=(1,1), activation='relu')(hidden)
    hidden = MaxPooling2D()(hidden)
    f_hidden = Flatten()(hidden)
    f_hidden = Dense(64, activation='relu')(f_hidden)
    f_hidden = Dense(32, activation='relu')(f_hidden)
    output = Dense(2, activation='sigmoid')(f_hidden)
    return Model(input_layer, output)


ds = tu.load_dataset("..\\dataset\\parsed_dataset.csv")
ds = ds.drop('turn_number', axis=1)
ds = ds.drop('color_player', axis=1)
input_shape = (9,9)
learning_rate = 0.001
arrayset = ds.to_numpy()
train_set = tu.convert_boardstate(arrayset[:, 0], input_shape)
label_list = tu.get_labels(arrayset)
model = build_network(input_shape)
ada = Adam(lr=learning_rate)
model.compile(loss='mse', optimizer=ada)

