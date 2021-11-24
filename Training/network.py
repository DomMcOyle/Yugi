import keras.models

import train_utils as tu
import pandas as pd
import numpy as np

from keras.layers import Conv2D, MaxPooling2D, Input, Dropout, Flatten, Dense
from keras.models import Model
from tensorflow.keras.optimizers import Adam
from keras import callbacks
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, max_error, mean_squared_error


def build_network(input_shape):
    input_layer = Input(input_shape)
    hidden = Conv2D(filters=16,
                    kernel_size=(2, 2),
                    strides=(1, 1),
                    activation='relu')(input_layer)
    hidden = MaxPooling2D()(hidden)
    f_hidden = Flatten()(hidden)
    f_hidden = Dropout(rate=0.2)(f_hidden)
    f_hidden = Dense(128, activation='relu')(f_hidden)
    f_hidden = Dense(64, activation='relu')(f_hidden)
    output = Dense(1, activation='sigmoid')(f_hidden)
    return Model(input_layer, output)

rs = 42
name = "Testprob3"
ds = tu.load_dataset("..\\dataset\\parsed_dataset.csv")
# remove initial states
ds = ds[ds.turn_number != 1]
#remove draws
ds = ds[ds.match_result_white != ds.match_result_black]
"""
0. undersampling delle probabilità 0 -- capiamo

1. cambio da label a probabilità
2. rimozione pareggi
3. normalizzazione del turno

"""
# drop useless columns (4now)
ds = ds.drop('turn_number', axis=1)
ds = ds.drop('color_player', axis=1)

ds = ds.groupby(ds.current_state).sum().reset_index()
ds["white_prob"] = ds["match_result_white"]/(ds["match_result_white"]+ds["match_result_black"])

ds = ds.drop('match_result_white', axis=1)
ds = ds.drop('match_result_black', axis=1)
print(ds.head())

input_shape = (9, 9)
arrayset = ds.to_numpy()

train_set = tu.convert_boardstate(arrayset[:, 0], input_shape)
# applying minmaxing
minmax = MinMaxScaler()
minmax.fit(train_set.reshape(-1, train_set.shape[-1]))
train_set = minmax.transform(train_set.reshape(-1, train_set.shape[-1])).reshape(train_set.shape)
#getting labels
#label_list = tu.get_labels(arrayset).astype('float32')
label_list = np.array(arrayset[:,1]).astype('float32')
print(label_list)


learning_rate = 0.001
bs = 32
epochs = 150
features = 1


X = train_set.reshape((train_set.shape[0], train_set.shape[1], train_set.shape[2], features))
X_train, X_test, y_train, y_test = train_test_split(X, label_list,
                                                    #stratify=label_list,
                                                    test_size=0.3, shuffle=True, random_state=rs)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,
                                                  #stratify=y_train,
                                                  test_size=0.2, shuffle=True, random_state=rs)

model = build_network(X.shape[1:])
ada = Adam(learning_rate=learning_rate)
model.compile(loss='mse', optimizer=ada)
print(model.summary())

callbacks_list = [
    callbacks.EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=10,
                            restore_best_weights=True),
]

model.fit(X_train,
          y_train,
          batch_size=bs,
          verbose=2,
          callbacks=callbacks_list,
          epochs=epochs,
          validation_data=(X_val, y_val))

prediction = model.predict(X_test)
print(mean_absolute_error(y_test, prediction))

#model = keras.models.load_model("Model\\Testprob2")
#print(label_list[0:])
#print(model.predict(X[0:]))

"""
ll = label_list[0:]
pred = model.predict(X[0:])
"""
ll = y_test
pred = model.predict(X_test)
print(max_error(ll,pred))
print(mean_absolute_error(ll,pred))
print(mean_squared_error(ll,pred))
ll = ll.reshape((len(ll),1))
print(ll)
obb = np.concatenate((ll,pred),axis=1)
print(obb)
np.savetxt("obb.txt", obb, '%.5f')


#print((X[11]*3).reshape(9,9))
#print(label_list[11])
model.save('Model\\' + name)