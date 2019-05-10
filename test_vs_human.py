import numpy as np
import random as rnd
import datetime as dt
import matplotlib.pyplot as plt
import keras
import os

from GameObject import Game
from AIPlayer import AIPlayer
from Models import initialize_parameters, construct_bet_NN, construct_play_NN
from Loss import batch_loss_history
from Loss import loss_bet,get_loss_bet

# Play with 13 cards (whole deck)
n = 13

# 0 means human player, 4 means AI player
strategies = [0,4,4,4]
# 'none' for no bet model
bet_strategies = ['none','model','model','model']

# Load the NN models
timeStamp = '2019-05-08-14-24-2'
iter = 10000
bet_model = keras.models.load_model('Models/bet_' + timeStamp +'_' + str(iter) +'.h5',custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
action_model = keras.models.load_model('Models/action_' + timeStamp +'_' + str(iter) +'.h5',custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

# Create the AI objects
AIs = [None for p in range(4)]
for p in range(4):
    if strategies[p] == 4:
        AIs[p] = AIPlayer(4,'model','matrix',bet_model,action_model,None,0)
        
game = Game(n, strategies, bet_strategies, n, AIs)
#scores = game.playGame()