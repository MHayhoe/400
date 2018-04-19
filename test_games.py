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
from Loss import loss_bet, get_loss_bet


# Number of full games to play
num_games = 100
wins_team1 = 0
wins_team2 = 0
datatype='matrix'


hvh = keras.models.load_model('Models/Heuristic_v_Heuristic_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

hvg = keras.models.load_model('Models/Heuristic_v_Greedy_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
gvh = keras.models.load_model('Models/Greedy_v_Heuristic_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
gvg = keras.models.load_model('Models/Greedy_v_Greedy_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
timestr = '2018-04-17-21-14-15'
iterations = 100000

nn_action_model = keras.models.load_model('Models/action_' + timestr + '_' + str(iterations) + '.h5',
                                          custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
nn_bet_model = keras.models.load_model('Models/bet_' + timestr + '_' + str(iterations) + '.h5',
                                       custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

#'2018-04-17-17-58-35'
def test_game(test_type):
    if test_type == 'hvg':
        strategies = [2,3,2,3]
        bet_models = [hvh, nn_bet_model,hvh,nn_bet_model]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None,None,None,None]
        num_iters =1
    elif test_type == 'hvr':
        strategies = [1,3,1,3]
        bet_models = [hvh, gvg,hvh,gvg]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None,None,None,None]
        num_iters = 1
    elif test_type == 'gvr':
        strategies = [1,2,1,2]
        bet_models = [hvh, gvg,hvh,gvg]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None,None,None,None]
        num_iters = 1
    elif test_type == 'nnvh':
        strategies = [3,4,3,4]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None, nn_action_model, None, nn_action_model]
        bet_models = [hvh, nn_bet_model,hvh,nn_bet_model]
        num_iters = 10
    elif test_type == 'nnvg':
        strategies = [2,4,2,4]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None, nn_action_model, None, nn_action_model]
        bet_models = [gvg, nn_bet_model,gvg,nn_bet_model]
        num_iters = 10
    elif test_type == 'nnvr':
        strategies = [1,4,1,4]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None, nn_action_model, None, nn_action_model]
        bet_models = [gvg, nn_bet_model,gvg,nn_bet_model]
        num_iters = 10

    n=13
    wins_team1 = [0 for i in range(10)]
    wins_team2 = [0 for i in range(10)]
    frac_won_by_nn = [0 for i in range(10)]

    for i in range(1):
        #iterations = str((i+1)*10000)

        for g in range(num_games):
            Total_Scores = [0 for p in range(4)]

            while True:
                #game = Game(n, strategies, bet_strategies, n, [action_model for i in range(4)], [bet_model for i in range(4)])
                game = Game(n, strategies, bet_strategies, n, action_models, bet_models)
                scores = game.playGame()

                for p in range(4):
                    Total_Scores[p] += scores[p]

                if (Total_Scores[0] >= 41 and Total_Scores[2] >= 0) or (Total_Scores[0] >= 0 and Total_Scores[2] >= 41):
                       wins_team1[i] += 1
                       #print 'Team 1 won'
                       break
                if (Total_Scores[1] >= 41 and Total_Scores[3] >= 0) or (Total_Scores[1] >= 0 and Total_Scores[3] >= 41):
                       wins_team2[i] += 1
                       #print 'Team 2 won'
                       break

            #print Total_Scores
        print 'Team 1 won' + str(wins_team1[i])
        print 'Team 2 won' + str(wins_team2[i])
        frac_won_by_nn[i] = wins_team2[i]*1.0/num_games
    print frac_won_by_nn
    #plt.figure(2)
    #plt.plot(frac_won_by_nn)
    #plt.title('NN performance vs heuristic team')
    #plt.savefig('Plots/nn.png')

test_game('hvg')