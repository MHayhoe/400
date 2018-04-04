import numpy as np
import csv
from GameObject import Game
import numpy as np
import pandas as pd
import datetime as dt
import copy
num_batches = 24
batch_size = 1000
Bets = []
Tricks = []
#strategies = [2,2,2,2]
strategies = [3,3,3,3]
#nameString = './Data/greedy_v_greedy_bet_data.csv'
nameString = './Data/heuristic_v_heuristic.csv'
gameTypeString = 'heuristic_v_heuristic'
x_size = 26
#organization ='standard'
#set data organization
#organization = 'binary'
organization = 'sorted'
#organization = 'interleave'
#organization = 'interleave_sorted'

if organization =='binary':
    nameString = './Data/'+gameTypeString+ '_bet_data_' + organization+'.csv'
    x_size = 52
elif organization == 'interleave':
    nameString = './Data/'+gameTypeString+ '_bet_data_' + organization+'.csv'
elif organization == 'sorted':
    nameString = './Data/'+gameTypeString+ '_bet_data_' + organization+'.csv'
elif organization =='interleave_sorted':
    nameString ='./Data/'+gameTypeString+ '_bet_data_' + organization+'.csv'

y_size = 1

for batch in range(num_batches):
    dataarray = np.zeros((4*batch_size, x_size+y_size)).astype(int)
    for t in range(batch_size):
        #print progress
        if t%(batch_size/10)==1:
            print '{}0 percent of batch complete: batch size is {} and we are on batch {} of {}'.format(t,batch_size, batch, num_batches)
        #generate a new game
        game = Game(13, strategies)
        scores = game.playGame()
        for p in range(4):
            #scount tricks taken and get suits and card vals
            tricks = sum(game.T[t] == p for t in range(13))
            hand = game.initialHands[p]
            vals = np.zeros(13).astype(int)
            suits = np.zeros(13).astype(int)
            x_binary = np.zeros(52).astype(int)
            vals_sorted = np.zeros(13).astype(int)
            suits_sorted = np.zeros(13).astype(int)
            for c in range(13):
                card = hand.cards[c]
                value = card.value
                suit = card.suit
                vals[c] = value
                suits[c] =suit
                x_binary[value+4*suit] = 1
            hand.sort()
            for c in range(13):
                card = hand.cards[c]
                value = card.value
                suit = card.suit
                vals_sorted[c] = value
                suits_sorted[c] = suit
            #add x and y data to array
            #x_obs = vals + suits
            x_obs = np.concatenate([vals,suits])
            #x_sorted = vals_sorted + suits_sorted
            x_sorted = np.concatenate([vals_sorted,suits_sorted])
            x_interleave = np.array([val for pair in zip(vals,suits) for val in pair]).astype(int)
            x_interleave_sorted = np.array([val for pair in zip(vals_sorted,suits_sorted) for val in pair]).astype(int)
            if organization =='interleave sorted':
                x_obs = x_interleave_sorted
            elif organization == 'interleave':
                x_obs = x_interleave
            elif organization== 'binary':
                x_obs = x_binary.astype(int)
            elif organization=='sorted':
                x_obs = x_sorted
            y_obs = tricks
            dataarray[4*t+p,0:x_size] = x_obs
            dataarray[4*t+p, x_size:x_size+y_size] = y_obs
    #now ready to append current array
    with open(nameString, "a") as output:
        np.savetxt(output, dataarray,delimiter=',',fmt= '%i')


