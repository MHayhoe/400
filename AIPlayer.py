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
from Loss import get_loss_bet, loss_bet
import os

class AIPlayer:
    # Constructor
    def __init__(self, strategy, bettype, datatype, bet_object=None, action_object=None):
        self.strategy = strategy;
        self.bettype = bettype
        self.datatype = datatype;
        self.eps = 0.05
        
        if self.bettype == 'model': #or self.bettype=='heuristic':
            if strategy==2 or strategy == 1:
                if bet_object is not None:
                    self.betmodel = bet_object
                else:
                    print ('loading greedy from AI Player')
                    self.betmodel = keras.models.load_model('./Models/Greedy_v_Greedy_bet_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})
            elif strategy==3 or strategy==4:
                if bet_object is not None:
                    self.betmodel = bet_object
                else:
                    #self.betmodel = keras.models.load_model('./Models/Heuristic_v_Heuristic_bet_data_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})
                    self.betmodel = keras.models.load_model('./Models/Heuristic_v_Greedy_bet_data_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})
        
        if self.strategy == 4:
            self.action_model = action_object
        
        elif self.bettype=='heuristic':
            pass
        else:
            pass

    # ----- PRINTING METHODS -----
    # String representation
    def __str__(self):
        return str((self.strategy.name));


    # ----- Get Action -----
    # Returns the index of the selected action, from the list of Cards 'actions'
    def get_action(self, n, p, state, actions):
        if self.strategy == 4: # Playing NN
            values = []
            for a in actions:
                data = [state[0], state[1], state[2], state[3], a.as_action(n)]
                values.append(self.action_model.predict(data))
            # Take random action w.p. eps
            if rnd.random() > self.eps:
                ind = np.argmax(values)
            else:
                ind = rnd.randint( 0, len(actions) - 1 )
        elif self.strategy == 3: # Simple heuristic
            ind = hai.heuristicChoice(p,actions,state[0],state[1],state[2],state[3])
        elif self.strategy == 2: # Myopic Greedy: pick the highest playable card every time
            ind = np.argmax(actions)
        else: # Random choice
            # Pick a valid card at random
            ind = rnd.randint( 0, len(actions) - 1 )
        return ind

    # ----- Get Bet -----
    def get_bet(self, hand):
        #print hand
        #print self.datatype
        #print self.get_cards(hand)
        if self.bettype == 'model': #or self.bettype=='heuristic':
            model_bet = self.betmodel.predict(np.array([self.get_cards(hand)]))[0][0]
            #model_bet = self.betmodel.predict(np.reshape(hand.get_cards_as_matrix(),(1,4,13,1)))[0][0]
            #print model_bet
            bet = max(min(13, round(model_bet)), 2)
            #print bet
        elif self.bettype == 'heuristic':
            bet = hai.heuristicBet(hand)
        else:
            bet = rnd.randint(2, 13)
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
