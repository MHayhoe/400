#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:46:41 2018

@author: Mikhail
"""
from GameObject import Game
import keras
from keras import backend as K
import numpy as np
import matplotlib.pyplot as plt

strategies = [3,4,3,4]
# Number of full games to play
num_games = 50
wins_team1 = 0
wins_team2 = 0
datatype='matrix'
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
hvh = keras.models.load_model('Models/Heuristic_v_Heuristic_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

hvg = keras.models.load_model('Models/Heuristic_v_Greedy_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
gvh = keras.models.load_model('Models/Greedy_v_Heuristic_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
gvg = keras.models.load_model('Models/Greedy_v_Greedy_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

n=13
frac_won_by_nn = [0 for i in range(10)]
for i in range(10):
    iterations = str((i+1)*10000)
    nn_action_model =keras.models.load_model('Models/action_2018-04-17-17-58-35_'+str(iterations)+'.h5',  custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
    nn_bet_model = keras.models.load_model('Models/bet_2018-04-17-17-58-35_'+str(iterations)+'.h5', custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
    bet_strategies = ['model', 'model', 'model', 'model']
    bet_models = [hvh, nn_bet_model,hvh,nn_bet_model]
    action_models = [None, nn_action_model, None, nn_action_model]

    for g in range(num_games):
        Total_Scores = [0 for p in range(4)]

        while True:
            #game = Game(n, strategies, bet_strategies, n, [action_model for i in range(4)], [bet_model for i in range(4)])
            game = Game(n, strategies, bet_strategies, n, action_models, bet_models)
            scores = game.playGame()

            for p in range(4):
                Total_Scores[p] += scores[p]

            if (Total_Scores[0] >= 41 and Total_Scores[2] >= 0) or (Total_Scores[0] >= 0 and Total_Scores[2] >= 41):
                   wins_team1 += 1
                   #print 'Team 1 won'
                   break
            if (Total_Scores[1] >= 41 and Total_Scores[3] >= 0) or (Total_Scores[1] >= 0 and Total_Scores[3] >= 41):
                   wins_team2 += 1
                   #print 'Team 2 won'
                   break

        #print Total_Scores
    print 'Team 1 won' + str( wins_team1)
    print 'Team 2 won' + str(wins_team2)
    frac_won_by_nn[i] = wins_team2/num_games
    wins_team1 = 0
    wins_team2 = 0
print frac_won_by_nn
plt.figure(2)
plt.plot(frac_won_by_nn)
plt.title('NN performance vs heuristic team')
