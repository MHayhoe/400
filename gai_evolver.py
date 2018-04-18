from GameObject import Game
import numpy as np
import datetime as dt
import os
import copy
num_tests = 1
import keras
from keras import backend as K

# Let's test heuristic vs random
total_score_even = 0
total_score_odd = 0
wins_even  = 0
wins_odd = 0
total_tricks_even = 0
total_tricks_odd = 0
ties = 0
strategies = [5,5,5,5]

#uncomment this block to switch to all greedy
#strategies = [2,2,2,2]

# For saving the game state after each game
Hands = []
History = []
Bets = []
Scores = []
Tricks = []
datatype='matrix'

model_vector = ['genetic', 'genetic', 'genetic', 'genetic']
genetic_parameter_lists
genetic_parameters ={}
genetic_parameters['bet_params'] = np.random.rand(52)
genetic_parameters['state_params'] = {}
genetic_parameters['prob_param']=1
genetic_parameters['action_params'] = {}
genetic_parameters['urgency_param'] = .5
genetic_param_list = [genetic_parameters for i in range(4)]
