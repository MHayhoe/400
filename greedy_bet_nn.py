from keras import models
from keras.models import Sequential
from keras.layers import Dense, Activation

import numpy as np
# bets = np.load('./Data/Greedy_v_Greedy2018-04-02-15-35-2_Bets.npy')
# scores = np.load('./Data/Greedy_v_Greedy2018-04-02-15-35-2_Scores.npy')
# hands = np.load('./Data/Greedy_v_Greedy2018-04-02-15-35-2_Hands.npy')

bets = np.load('./Data/Greedy_v_Greedy_Bets.npy')
scores = np.load('./Data/Greedy_v_Greedy_Scores.npy')
hands = np.load('./Data/Greedy_v_Greedy_Hands.npy')
tricks = np.load('./Data/Greedy_v_Greedy_Tricks.npy')

num_rounds = len(hands)
x_data = [np.array([]) for t in range(num_rounds*4)]
y_data = [-1 for t in range(num_rounds*4)]
for t in range(num_rounds):
    for p in range(4):
        vals = [0 for i in range(13)]
        suits = [0 for i in range(13)]
        for c in range(13):
            card = hands[t][p].cards[c]
            vals[c] = card.value
            suits[c] = card.suit
        x_obs = vals + suits
        y_obs = tricks[t][p]
        x_data[4*t+p] = x_obs
        y_data[4*t+p] = y_obs

x_train = x_data[0:(int(num_rounds*.8))]
y_train = y_data[0:(int(num_rounds*.8))]
x_test = x_data[-(int(num_rounds*.8)+1)]
y_test = y_data[-(int(num_rounds*.8)+1)]



model = Sequential([
    Dense(32, input_shape=(26,)),
    Activation('relu'),
    Dense(10),
    Activation('softmax'),
])
