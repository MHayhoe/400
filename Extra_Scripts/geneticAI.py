# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:13 2018

@author: Hadi
"""
from Hand import Hand
from Deck import Deck
from Card import Card
import numpy as np
from pprint import pprint


import random as rnd


def geneticBet(hand,bet_params):
    cards = hand.get_cards_matrix_order().flatten()
    return max(min(13, round(np.dot(bet_params,cards))), 2)

def geneticChoice(n,p,state, valid_cards, genetic_params,potential_states):
    value_summands = {}
    num_actions = len(valid_cards)

    for key in genetic_params['action_params'].keys():
        value_summands[key] = [potential_states[key][i] * genetic_params['action_params'][key] for i in range(num_actions)]
    values = [0 for i in range(num_actions)]
    for key in value_summands.keys():
        for i in range(num_actions):
            values = values + value_summands[key][i]
    sum_exp_val = sum([np.exp(value) for value in values])
    weights = [(np.exp(value)/sum_exp_val) for value in values]
    ind = np.random.choice(range(len(valid_cards)), p=weights)
    return ind
def play_for_self(valid_cards,state,bet_params):
    return

def play_for_team(valid_cards,state,bet_params):
    return
def calc_value(state, genetic_params):
    state_params = genetic_params['state_params']
    prob_param = genetic_params['prob_param']

    value = 0
    for key in state_params.keys():
        value += prob_param*np.dot(state_params[key],state[key])
    return value
def calc_urgency(state,genetic_params):
    pass