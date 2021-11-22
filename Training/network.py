import train_utils as tu
import pandas as pd
import numpy as np

from keras.layers import Conv2D, MaxPooling2D, Input, Dropout, Flatten, Dense
from keras.models import Model
from tensorflow.keras.optimizers import Adam
from keras import callbacks


def build_network(input_shape):
    input_layer = Input(input_shape)
    hidden = Conv2D(filters=16,
                    kernel_size=(2, 2),
                    strides=(1, 1),
                    activation='relu')(input_layer)
    hidden = MaxPooling2D()(hidden)
    f_hidden = Flatten()(hidden)
    f_hidden = Dropout(rate=0.3)(f_hidden)
    f_hidden = Dense(128, activation='relu')(f_hidden)
    f_hidden = Dense(64, activation='relu')(f_hidden)
    output = Dense(2, activation='sigmoid')(f_hidden)
    return Model(input_layer, output)


ds = tu.load_dataset("..\\dataset\\parsed_dataset.csv")
# remove initial states
ds = ds[ds.turn_number != 1]

# drop useless columns (4now)
d2 = ds[ds.current_state == ds.current_state[4]]
print(d2.iloc[0])
print(d2.shape)
print(d2)
ds = ds.drop('turn_number', axis=1)
ds = ds.drop('color_player', axis=1)

input_shape = (9, 9)
arrayset = ds.to_numpy()
train_set = tu.convert_boardstate(arrayset[:, 0], input_shape)

label_list = tu.get_labels(arrayset)

learning_rate = 0.001
features = 1
X = train_set.reshape((train_set.shape[0], train_set.shape[1], train_set.shape[2], features))


model = build_network(X.shape[1:])
ada = Adam(learning_rate=learning_rate)
model.compile(loss='mse', optimizer=ada)
print(model.summary())
print(label_list.astype('float32'))

model.fit(X,label_list.astype('float32'), batch_size=64, epochs=50)
print(label_list[13:16])
print(model.predict(X[13:16]))
print(label_list[0:13])
print(model.predict(X[0:13]))
