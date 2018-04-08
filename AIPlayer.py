# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:13 2018

@author: Hadi
"""
import random as rnd
from keras import models
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import to_categorical
import keras
from keras import backend as K
import numpy as np
import heuristicAI as hai
import os

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

class AIPlayer:
    # Constructor
    def __init__(self, strategy,bettype, datatype, model_object=None):
        self.strategy = strategy;
        self.bettype = bettype
        self.datatype = datatype;
        if self.bettype == 'model': #or self.bettype=='heuristic':
            if strategy==2 or strategy == 1:
                if model_object is not None:
                    self.betmodel = model_object
                else:
                    print ('loading greedy from AI Player')
                    self.betmodel = keras.models.load_model('./Models/Greedy_v_Greedy_bet_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})
            elif strategy==3:
                if model_object is not None:
                    self.betmodel = model_object
                else:
                    #self.betmodel = keras.models.load_model('./Models/Heuristic_v_Heuristic_bet_data_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})
                    self.betmodel = keras.models.load_model('./Models/Heuristic_v_Greedy_bet_data_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})

        elif self.bettype=='heuristic':
            pass
        else:
            pass

    # ----- PRINTING METHODS -----
    # String representation
    def __str__(self):
        return str((self.strategy.name));


    # ----- Get Action -----
    def get_action(self, state,actions):
        feasible_actions=actions;
        return self.actionmodel(state,feasible_actions)

    # ----- Get Bet -----
    def get_bet(self, hand):
        #print hand
        #print self.datatype
        #print self.get_cards(hand)
        if self.bettype == 'model': #or self.bettype=='heuristic':
            model_bet = self.betmodel.predict(np.array([self.get_cards(hand)]))[0][0]
            #print model_bet
            bet = max(min(13, round(model_bet)), 2)
            #print bet
        elif self.bettype == 'heuristic':
            bet = hai.heuristicBet(hand)
        else:
            bet = rnd.randint(2, 5)
        return bet
    
    #------ Get Cards ----
    def get_cards(self,hand):
        if self.datatype=='sorted':
            return hand.get_cards_as_val_suit_sorted()
        elif self.datatype=='binary':
            return hand.get_cards_as_binary()
        elif self.datatype=='interleave':
            return hand.get_cards_as_interleave()
        elif self.datatype=='interleave_sorted':
            return hand.get_cards_as_interleave_sorted()
        elif self.datatype=='standard':
            return hand.get_cards_as_val_suit()
