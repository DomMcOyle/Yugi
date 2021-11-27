import keras.models
import sys

import constants
import train_utils as tu
import numpy as np

from keras.layers import Conv2D, MaxPooling2D, Input, Dropout, Flatten, Dense
from keras.models import Model
from tensorflow.keras.optimizers import Adam
from keras import callbacks
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, max_error, mean_squared_error

from hyperas.distributions import uniform, choice
from hyperas import optim
from hyperopt import STATUS_OK, Trials, tpe, STATUS_FAIL


def data():
    # IMPORTANT!!! -> initialize module variables before using
    train_set = tu.TRAIN_SET
    train_labels = tu.TRAIN_LABEL
    test_set = tu.TEST_SET
    test_labels = tu.TEST_LABEL
    return train_set, train_labels, test_set, test_labels


def trial_network(train_set, train_labels, test_set, test_labels):
    # choosing the hyperparameters to be used
    dropout_rate = {{uniform(0, 0.2)}}
    lr = {{uniform(0.0001, 0.01)}}

    # Building the net
    input_shape = train_set.shape[1:]
    model = build_network(input_shape=input_shape, dr=dropout_rate)
    ada = Adam(learning_rate=lr)
    model.compile(loss='mse', optimizer=ada)
    print(model.summary())

    # setting an EarlyStopping callback, in order to stop training if the validation loss doesn't get better
    callbacks_list = [
        callbacks.EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=10,
                                restore_best_weights=True),
    ]

    # Generating the validation set
    print(train_set.shape)
    print(train_labels.shape)
    x_train, x_val, y_train, y_val = train_test_split(train_set, train_labels, test_size=0.2)

    # fitting the model
    try:
        h = model.fit(x_train, y_train,
                      batch_size={{choice(tu.BS)}},
                      epochs=300,
                      verbose=2,
                      callbacks=callbacks_list,
                      validation_data=(x_val, y_val))
    except:
        print("Error in training")
        return {'status': STATUS_FAIL}

    # the score returned is the best epoch one
    best_epoch_idx = np.nanargmin(h.history['val_loss'])
    loss = h.history['loss'][best_epoch_idx]
    score = h.history['val_loss'][best_epoch_idx]

    # making prediction on the test set
    prediction = model.predict(test_set)
    print(len(test_labels))
    print(len(prediction.shape))
    mae = mean_absolute_error(test_labels, prediction)
    maxe = max_error(test_labels, prediction)
    mse = mean_squared_error(test_labels, prediction)

    print('Last best Score: ', str(tu.BEST_SCORE))

    # Saving the reference to the best model
    if score < tu.BEST_SCORE:
        tu.BEST_SCORE = score
        tu.BEST_MODEL = model

    return {'loss': score, 'status': STATUS_OK, 'n_epochs': len(h.history['loss']),
            'model': tu.BEST_MODEL, 'train_loss': loss, 'mae': mae, 'maxe': maxe, 'mse': mse}


def build_network(input_shape, dr):
    input_layer = Input(input_shape)
    hidden = Conv2D(filters=32,
                    kernel_size=(2, 2),
                    strides=(1, 1),
                    activation='relu')(input_layer)
    hidden = MaxPooling2D()(hidden)
    f_hidden = Flatten()(hidden)
    f_hidden = Dropout(rate=dr)(f_hidden)
    f_hidden = Dense(128, activation='relu')(f_hidden)
    f_hidden = Dense(64, activation='relu')(f_hidden)
    output = Dense(1, activation='sigmoid')(f_hidden)
    return Model(input_layer, output)


def hyperparam_search(train_set, train_labels, test_set, test_labels, name):
    # trials object used to record the results of each iteration
    trials = Trials()

    # initializing the variables used by data() in order to pass the datasets to the optimization function
    tu.TRAIN_SET = train_set
    tu.TRAIN_LABEL = train_labels
    tu.TEST_SET = test_set
    tu.TEST_LABEL = test_labels

    tu.BS = [32, 64, 128, 256, 512]
    # optimization function
    print("Info: BEGINNING SEARCH...")
    best_run, best_model = optim.minimize(model=trial_network,
                                          data=data,
                                          functions=[trial_network, build_network],
                                          algo=tpe.suggest,
                                          max_evals=30,
                                          trials=trials
                                          )
    print("Info: SAVING RESULTS...")

    # Opening a new file and writing the column names
    output = open( constants.MODEL_STAT_PATH + name + "_stats.csv", "w")
    output.write("Trials")
    output.write("\ntrial_id, epochs, score, loss, learning_rate, batch_size, dropout_1," +
                 "mean_absolute_error, mean_squared_error, max_error")
    i = 0
    for trial in trials.trials:
        if trial['result']['status'] == STATUS_FAIL:
            # printing stats from a failed iteration
            output.write("\n%s, -, -, -, -, -, %f, %d, %f, FAIL" % (
                trial['tid'],
                trial['misc']['vals']['lr'][0],
                tu.BS[trial['misc']['vals']['batch_size'][0]],
                trial['misc']['vals']['dropout_rate'][0]
            ))
        else:
            # printing stats from a succeeded iteration
            output.write(
                "\n%s, %d, %f, %f, %f, %d, %f, %f, %f, %f"
                % (trial['tid'],
                   trial['result']['n_epochs'],
                   abs(trial['result']['loss']),
                   trial['result']['train_loss'],
                   trial['misc']['vals']['lr'][0],
                   tu.BS[trial['misc']['vals']['batch_size'][0]],
                   trial['misc']['vals']['dropout_rate'][0],
                   trial['result']['mae'],
                   trial['result']['mse'],
                   trial['result']['maxe']
                   ))
            i = i + 1

    # writing the parameters for the best model
    output.write("\nBest model\n")
    output.write(str(best_run))
    output.close()

    print("Info: SAVING MODEL...")
    print(best_run)
    tu.BEST_MODEL.save(constants.MODEL_PATH + name)

# ------------------ BEGIN PREPROCESSING SCRIPT -------------------------


if __name__ == "__main__":
    if sys.argv[1].lower() == 'test':
        training = False
    elif sys.argv[1].lower() == 'train':
        training = True
    else:
        print("Missing first argument (train/test)")
        sys.exit(-1)

    if len(sys.argv) > 2:
        name = sys.argv[2]
    else:
        print("Missing second argument (model name)")
        sys.exit(-1)

    name = "Atem"
    ds = tu.load_dataset("..\\dataset\\parsed_dataset_v3.csv")
    # remove initial states
    ds = ds[ds.turn_number != 1]
    # remove draws
    ds = ds[ds.match_result_white != ds.match_result_black]

    # drop useless columns (4now)
    ds = ds.drop('turn_number', axis=1)
    ds = ds.drop('color_player', axis=1)

    ds = ds.groupby(ds.current_state).sum().reset_index()
    ds["white_prob"] = ds["match_result_white"] / (ds["match_result_white"] + ds["match_result_black"])

    ds = ds.drop('match_result_white', axis=1)
    ds = ds.drop('match_result_black', axis=1)

    input_shape = (9, 9)
    arrayset = ds.to_numpy()

    train_set = tu.convert_boardstate(arrayset[:, 0], input_shape)
    print(train_set.shape)
    """
    # applying minmaxing !!!WARNING, ALL COLUMNS MUST HAVE AT LEAST ONE VALUE BETWEEN 0 and 3
    minmax = MinMaxScaler(feature_range=(-0.5,1))
    minmax.fit(train_set.reshape(-1, train_set.shape[-1]))
    train_set = minmax.transform(train_set.reshape(-1, train_set.shape[-1])).reshape(train_set.shape)
    """
    # all the values are brought in the range (-0.5, 1)
    train_set = train_set-1
    train_set = train_set/2
    # ----------------- DATASET PREPARATION AND LEARNING ---------------------

    label_list = np.array(arrayset[:, 1]).astype('float32')

    features = 1

    X = train_set.reshape((train_set.shape[0], train_set.shape[1], train_set.shape[2], features))

    if training:
        X_train, X_test, y_train, y_test = train_test_split(X, label_list, test_size=0.3, shuffle=True)

        hyperparam_search(X_train, y_train, X_test, y_test, name)
    else:
        final = keras.models.load_model(constants.MODEL_PATH+name)
        y = final.predict(X)

        print(mean_absolute_error(label_list, y))
        print(mean_squared_error(label_list, y))
        print(max_error(label_list, y))
