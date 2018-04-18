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
genetic_parameters ={}
genetic_parameters['bet_params'] = np.random.rand(52)
genetic_parameters['state_params'] = {}
genetic_parameters['prob_param']=1
genetic_parameters['action_params'] = {}
genetic_parameters['urgency_param'] = .5
genetic_param_list = [genetic_parameters for i in range(4)]


#games = [Game(13, strategies) for i in range(num_tests)]
for i in range(num_tests):
    #print i
    #if i% 10000 ==1:
     #   print i
    game = Game(13, strategies, model_vector, genetic_parameter_list=genetic_param_list)
    #game = games[i]
    scores = game.playGame()
    tricks = game.getTricks()
    #print game.initialbets
    #print tricks
    #print scores
    #print(scores)
    odd_score = scores[1]+scores[3]
    even_score = scores[0]+scores[2]
    odd_tricks = tricks[1] + tricks[3]
    even_tricks = tricks[0] + tricks[2]
    total_score_even += even_score
    total_score_odd += odd_score
    total_tricks_even += even_tricks
    total_tricks_odd += odd_tricks

    if even_score < odd_score:
        wins_odd += 1
    elif even_score > odd_score:
        wins_even += 1
    else:
        ties += 1
    tricks = [-1 for i in range(4)]
    for p in range(4):
        tricks[p] = sum(game.T[t] == p for t in range(13))

    #print Hands[i]
    #print game.initialHands
    Hands.append(game.initialHands)
    #print Hands[i]
    #print Hands
    History.append(game.h)
    Bets.append(game.bets)
    print Bets
    #Scores[i] = scores;
    Scores.append(scores)
    #print (Scores[i])
    Tricks.append(tricks)
    #print Hands[i]
    #print Bets[i]
    #print Hands


#print Hands
#print Bets
# tempTime = dt.datetime.now().time();
# #timeString = 'Data/Heuristic_v_Greedy' + str(dt.datetime.now().date()) + '-' + str(tempTime.hour) + '-' + str(tempTime.minute) + '-' + str(tempTime.second);
# #timeString = 'Data/Greedy_v_Greedy' + str(dt.datetime.now().date()) + '-' + str(tempTime.hour) + '-' + str(tempTime.minute) + '-' + str(tempTime.second);
# timeString = 'Data/Greedy_v_Greedy' #+ str(dt.datetime.now().date()) + '-' + str(tempTime.hour) + '-' + str(tempTime.minute) + '-' + str(tempTime.second);
#
# np.save(timeString + '_Hands', Hands)
# np.save(timeString + '_History', History)
# #np.save(timeString + '_Winners', Winners)
# np.save(timeString + '_Bets', Bets)
# np.save(timeString + '_numTests', num_tests)
# np.save(timeString + '_Scores', Scores)
# np.save(timeString + '_Tricks', Tricks)

print 'Even won ' + str(wins_even*1.0/num_tests*100) + '% of games with a score of ' + str(total_score_even) + ' and raw tricks of ' + str(total_tricks_even)
print 'Odd won ' + str(wins_odd*1.0/num_tests*100) + '% of games with a score of ' + str(total_score_odd) + ' and raw tricks of ' + str(total_tricks_odd)
print 'There were ' + str(ties*1.0/num_tests*100) + '% of games tied'


