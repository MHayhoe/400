from keras import models
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import keras.layers as L
from keras.utils import to_categorical
import keras
from keras import backend as K
import numpy as np
import keras.regularizers as R
import keras.models as M

def train_bet_model(strategy_var, org_var,batch_size_var, epoch_var):
    typeString= org_var
    strategyString = strategy_var
    card_dim  = 26
    if org_var == 'binary' or org_var=='matrix':
        card_dim = 52
    #typeString = 'sorted'
    #typeString = 'binary'
    #typeString = 'standard'
    #typeString = 'interleave'
    #typeString = 'interleave_sorted'

    #strategyString = 'Heuristic_v_Greedy'
    #strategyString = 'Heuristic_v_Heuristic'
    #strategyString = 'Greedy_v_Greedy'
    #strategyString = 'Greedy_v_Heuristic'
    modelString = strategyString + '_bet_data_model_' + typeString
    nameString = './Data/' + strategyString + '_bet_data_' + typeString
    print(nameString)
    x_train = np.load(nameString + '_x_train.npy')
    #x_train = np.reshape(x_train,(len(x_train),card_dim,1))
    y_train = np.load(nameString + '_y_train.npy' )
    x_test = np.load(nameString + '_x_test.npy')
    #x_test = np.reshape(x_test,(len(x_test),card_dim,1))
    y_test = np.load(nameString + '_y_test.npy')

    #censor ys
    #y_train = [min(y_train[i],6) for i in range(len(y_train))]
    #y_test = [min(y_test[i],6) for i in range(len(y_test))]

    #y_train = to_categorical(y_train)
    #y_test = to_categorical(y_test)

    def loss_bet(y_true, y_pred):
        return K.mean(y_true + K.sign(y_pred - y_true) * y_pred)

    # Returns our custom loss function
    def get_loss_bet():
        # Our custom loss function: if we make our bet (y_true >= y_pred), the loss
        # is the amount we could have gotten if we'd bet y_true, i.e., it's
        # y_true - y_pred. If we didn't make our bet, then our loss is what we
        # could have gotten minus what we lost, i.e., y_true + y_pred
        # (since -1*(-bet) = bet)
        return loss_bet

    #model = Sequential()
    #add initial layer
    reg = 0.1

    if org_var == 'binary':
        input_layer = L.Input(shape=(card_dim,1))
        xl = L.LeakyReLU()(input_layer)

        print input_layer
        print xl
        x = L.Conv1D(13, 1, activation='linear',padding='valid', use_bias=False, kernel_regularizer=R.l2(reg))(xl)
        #x = L.Dense(13, activation='relu')(x)
        output_layer = L.Dense(1, activation='linear', use_bias=False)(x)


        # xl = L.LeakyReLU()(input_layer)
        # x = L.Conv1D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xl)
        # x = L.BatchNormalization(axis=1)(x)
        # x = L.LeakyReLU()(x)
        # x = L.Conv1D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(x)
        # x = L.BatchNormalization(axis=1)(x)
        # x = L.Add()([x, xl])
        # x = L.LeakyReLU()(x)
        # x = L.Conv1D(5, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xl)
        # x = L.BatchNormalization(axis=1)(x)
        # x = L.LeakyReLU()(x)
        # x = L.Flatten()(x)
        output_layer = L.Dense(1, activation='linear', use_bias=False)(x)

        # model.add(Dense(13, input_dim=card_dim, activation='relu'))
        # model.add(Dense(13, activation='relu'))
        # #model.add(Dropout(.5))
        # model.add(Dense(1, activation='relu'))
        # #model.summary()
    elif org_var =='matrix':
        input_layer = L.Input(shape=(4, 13, 1))
        xl = L.LeakyReLU()(input_layer)
        x = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xl)
        x = L.BatchNormalization(axis=1)(x)
        x = L.LeakyReLU()(x)
        x = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(x)
        x = L.BatchNormalization(axis=1)(x)
        x = L.Add()([x, xl])
        x = L.LeakyReLU()(x)
        x = L.Conv2D(5, (1, 4), activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xl)
        x = L.BatchNormalization(axis=1)(x)
        x = L.LeakyReLU()(x)
        x = L.Flatten()(x)
        output_layer = L.Dense(1, activation='linear', use_bias=False)(x)

        bet_model = M.Model(inputs=input_layer, outputs=output_layer)
        bet_model.summary()

    sgd = keras.optimizers.SGD(lr=.01,clipnorm=10.)
    opt = keras.optimizers.RMSprop(lr=.01,clipnorm=10.)

    bet_model = M.Model(inputs=input_layer, outputs=output_layer)
    bet_model.summary()

    bet_model.compile(loss=get_loss_bet(),
                  optimizer=sgd,
                  metrics=['mean_absolute_error',get_loss_bet()])
    batchsize = batch_size_var
    epoches = epoch_var

    bet_model.compile(loss=get_loss_bet(), optimizer=sgd, metrics=['mean_absolute_error', get_loss_bet()])

    history = bet_model.fit(x_train, y_train,
                        batch_size=batchsize,
                        epochs = epoches,
                        verbose=1,
                        validation_data=(x_test, y_test))
    score = bet_model.evaluate(x_test, y_test, batch_size = batchsize)

    pred = bet_model.predict(x_test)

    mae = [0 for i in range(len(pred))]

    for i in range(len(pred)):
        mae[i] = np.abs(np.round(pred[i]) - y_test[i])

    bet_model.save('./Models/'+modelString+'_model'+'.h5')
    print pred