from GameObject import Game
import numpy as np
import datetime as dt
import os
import copy
num_tests = 100
import keras
from keras import backend as K

# Let's test heuristic vs random
total_score_even = 0
total_score_odd = 0
wins_even  = 0
wins_odd = 0
ties = 0
strategies = [3,2,3,2]

#uncomment this block to switch to all greedy
#strategies = [2,2,2,2]

# For saving the game state after each game
Hands = []
History = []
Bets = []
Scores = []
Tricks = []
datatype='sorted'
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

model_vector = ['model', 'model', 'model', 'model']
betting_model_objects = [None, None, None, None]
for p in range(4):
    if model_vector[p] == 'model':
        if strategies[p] == 3:
            #print os.getcwd()
            #betting_model_objects[p] = keras.models.load_model('Models/Heuristic_v_Heuristic_bet_data_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})
            betting_model_objects[p] = keras.models.load_model('Models/Heuristic_v_Greedy_bet_data_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})

        elif strategies[p] == 2:
            betting_model_objects[p] = keras.models.load_model('Models/Greedy_v_Heuristic_bet_data_'+datatype+'.h5', custom_objects={'get_loss_bet':get_loss_bet, 'loss_bet':loss_bet})
print betting_model_objects
#games = [Game(13, strategies) for i in range(num_tests)]
for i in range(num_tests):
    #print i
    #if i% 10000 ==1:
     #   print i
    game = Game(13, strategies, model_vector, betting_model_objects=betting_model_objects)
    #game = games[i]
    scores = game.playGame()
    print game.initialbets
    #print(scores)
    odd_score = scores[1]+scores[3]
    even_score = scores[0]+scores[2]
    
    total_score_even += even_score
    total_score_odd += odd_score
    
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

print 'Even won ' + str(wins_even*1.0/num_tests*100) + '% of games with a score of ' + str(total_score_even)
print 'Odd won ' + str(wins_odd*1.0/num_tests*100) + '% of games with a score of ' + str(total_score_odd)
print 'There were ' + str(ties*1.0/num_tests*100) + '% of games tied'


# it is probably better to just convert to data here...

# num_rounds = len(hands)
# x_data = [np.array([]) for t in range(num_rounds*4)]
# y_data = [-1 for t in range(num_rounds*4)]
# for t in range(num_rounds):
#     if t=
#     for p in range(4):
#         vals = [0 for i in range(13)]
#         suits = [0 for i in range(13)]
#         for c in range(13):
#             card = hands[t][p].cards[c]
#             vals[c] = card.value
#             suits[c] = card.suit
#         x_obs = vals + suits
#         y_obs = tricks[t][p]
#         x_data[4*t+p] = x_obs
#         y_data[4*t+p] = y_obs
#
# x_train = x_data[0:(int(num_rounds*.8))]
# y_train = y_data[0:(int(num_rounds*.8))]
# x_test = x_data[-(int(num_rounds*.8)+1):]
# y_test = y_data[-(int(num_rounds*.8)+1):]
#
# nameString = 'tf_ve/Data/Greedy_v_Greedy_bet'
# np.save(nameString + '_x_train', x_train )
# np.save(nameString + '_y_train', y_train )
# np.save(nameString + '_x_test', x_test)
# np.save(nameString + '_y_test', y_test)
#
