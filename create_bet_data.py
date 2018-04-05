import numpy as np
import csv
from GameObject import Game
import numpy as np
import pandas as pd
import datetime as dt
import copy
num_batches = 50
batch_size = 1000
Bets = []
Tricks = []
#strategy_var = 'Greedy_v_Heuristic'
#strategy_var = 'Greedy_v_Greedy'
#strategy_var = 'Heuristic_v_Heuristic'
strategy_var = 'Heuristic_v_Greedy'

#organization ='standard'
#set data organization
#organization = 'binary'
organization = 'sorted'
#organization = 'interleave'
#organization = 'interleave_sorted'

import keras
from keras import backend as K
import numpy as np
import heuristicAI as hai

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

betting_model_objects= [None,None,None,None]
players_to_learn_from = range(4)
if strategy_var=='Greedy_v_Greedy':
    nameString = './Data/Greedy_v_Greedy.csv'
    gameTypeString = 'Greedy_v_Greedy'
    strategies = [2,2,2,2]
    #doesn't matter how they are betting since we are learning. Just bet heuristic
    model_vector = ['heuristic','heuristic','heuristic','heuristic']
    #model_vector = ['model','model','model','model']
    betting_model_objects = [keras.models.load_model('./Models/Greedy_v_Greedy_bet_' + datatype + '.h5', custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet}) for i in range(4)]


elif strategy_var =='Greedy_v_Heuristic':
    nameString = './Data/Greedy_v_Heuristic.csv'
    gameTypeString = 'Greedy_v_Heuristic'
    strategies  = [2,3,2,3]
    players_to_learn_from = [0,2]
    #model_vector = ['heuristic','heuristic','heuristic','heuristic']


elif strategy_var=='Heuristic_v_Heuristic':
    nameString = './Data/Heuristic_v_Heuristic.csv'
    gameTypeString = 'Heuristic_v_Heuristic'
    strategies = [3,3,3,3]
    model_vector = ['heuristic','heuristic','heuristic','heuristic']
    #betting_model_objects = [keras.models.load_model('./Models/Heuristic_v_Heuristic_bet_' + datatype + '.h5', custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet}) for i in range(4)]

elif strategy_var=='Heuristic_v_Greedy':
    nameString = './Data/Heuristic_v_Greedy.csv'
    gameTypeString = 'Heuristic_v_Greedy'
    strategies = [3,2,3,2]
    players_to_learn_from = [0,2]
    model_vector = ['heuristic','heuristic','heuristic','heuristic']


x_size = 26

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

models = []
num_learn_from = len(players_to_learn_from)
for batch in range(num_batches):
    dataarray = np.zeros((num_learn_from*batch_size, x_size+y_size)).astype(int)
    for t in range(batch_size):
        #print progress
        if t%(batch_size/10)==1:
            print '{}0 percent of batch complete: batch size is {} and we are on batch {} of {}'.format(t,batch_size, batch, num_batches)
        #generate a new game
        game = Game(13, strategies, model_vector, betting_model_objects)
        scores = game.playGame()
        #print players_to_learn_from
        for p in players_to_learn_from:
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
            dataarray[num_learn_from*t+(p%num_learn_from),0:x_size] = x_obs
            dataarray[num_learn_from*t+(p%num_learn_from), x_size:x_size+y_size] = y_obs
    #now ready to append current array
    with open(nameString, "a") as output:
        np.savetxt(output, dataarray,delimiter=',',fmt= '%i')


