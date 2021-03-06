from keras import models
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import to_categorical
import keras
from keras import backend as K
import numpy as np

typeString = 'sorted'
nameString = './Data/Greedy_v_Greedy_bet_'+typeString
modelString = 'Greedy_v_Greedy_bet_'+ typeString
x_train = np.load(nameString + '_x_train.npy')
y_train = np.load(nameString + '_y_train.npy' )
x_test = np.load(nameString + '_x_test.npy')
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

model = Sequential()
#add initial layer
model.add(Dense(13, input_dim=26, activation='relu'))
model.add(Dense(13, activation='relu'))
#model.add(Dropout(.5))
model.add(Dense(1, activation='relu'))
#model.summary()

sgd = keras.optimizers.SGD(lr=.01,clipnorm=10.)
opt = keras.optimizers.RMSprop(lr=.01,clipnorm=10.)

model.compile(loss=get_loss_bet(),
              optimizer=sgd,
              metrics=['mean_absolute_error',get_loss_bet()])
batchsize = 128
epoches = 20
history = model.fit(x_train, y_train,
                    batch_size=batchsize,
                    epochs = epoches,
                    verbose=1,
                    validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, batch_size = batchsize)

pred = model.predict(x_test)

mae = [0 for i in range(len(pred))]

for i in range(len(pred)):
    mae[i] = np.abs(np.round(pred[i]) - y_test[i])

model.save('./Models/'+modelString+'.h5')