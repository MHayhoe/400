import numpy as np
import csv
from GameObject import Game
import numpy as np
import pandas as pd
import datetime as dt
import copy
num_batches = 1000
batch_size = 1000
Bets = []
Tricks = []
strategies = [2,2,2,2]
nameString = './Data/greedy_v_greedy_bet_data.csv'
x_size = 26
y_size = 1

for batch in range(num_batches):
    dataarray = np.zeros((4*batch_size, x_size+y_size))
    for t in range(batch_size):
        #print progress
        if t%batch_size/10==1:
            print '{}0 percent of batch complete: batch size is {} and we are on batch {} of {}'.format(t,batch_size, batch, num_batches)
        #generate a new game
        game = Game(13, strategies)
        scores = game.playGame()
        for p in range(4):
            #scount tricks taken and get suits and card vals
            tricks = sum(game.T[t] == p for t in range(13))
            hand = game.initialHands[p]
            vals = [0 for i in range(13)]
            suits = [0 for i in range(13)]
            for c in range(13):
                card = hand.cards[c]
                vals[c] = card.value
                suits[c] = card.suit
            #add x and y data to array
            x_obs = vals + suits
            y_obs = tricks
            dataarray[4*t+p,0:x_size] = x_obs
            dataarray[4*t+p, x_size:x_size+y_size] = y_obs
    #now ready to append current array
    with open(nameString, "a") as output:
        np.savetxt(output, dataarray,delimiter=',')

