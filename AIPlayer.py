# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:13 2018

@author: Hadi
"""

class AIPlayer:
    # Constructor
    def __init__(self, strategy):
        self.strategy = strategy;

    # ----- PRINTING METHODS -----
    # String representation
    def __str__(self):
        return str((self.strategy.name));


    # ----- Get Action -----
    def get_action(self, state,feasible_actions):
        return self.strategy(state,feasible_actions)

