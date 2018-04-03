from keras import models
from keras.models import Sequential
from keras.layers import Dense, Activation,Dropout
from keras.utils import to_categorical
import keras
import numpy as np

nameString = './Data/Greedy_v_Greedy_bet'
x_train = np.load(nameString + '_x_train.npy')
y_train = np.load(nameString + '_y_train.npy' )
x_test = np.load(nameString + '_x_test.npy')
y_test = np.load(nameString + '_y_test.npy')
#censor ys
y_train = [min(y_train[i],6) for i in range(len(y_train))]
y_test = [min(y_test[i],6) for i in range(len(y_test))]

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)



model = Sequential()
#add initial layer
model.add(Dense(13, input_dim=26,activation='relu'))
model.add(Dropout(.5))
model.add(Dense(7))
model.add(Activation('relu'))
model.add(Dense(4))
model.add(Activation('relu'))
model.add(Dense(7))
model.summary()

sgd = keras.optimizers.SGD()
opt = keras.optimizers.RMSprop(lr=.01,clipnorm=10.)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])
batchsize = 128
epoches = 20
history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs = epoches,
                    verbose=1,
                    validation_data=(x_test, y_test))
