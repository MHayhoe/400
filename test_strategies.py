from GameObject import Game
import numpy as np
import datetime as dt

num_tests = 1000

# Let's test heuristic vs random
total_score_rando = 0
total_score_heuristic = 0
wins_heuristic = 0.0
wins_rando = 0.0
ties = 0.0
#strategies = [3,2,3,2]

#uncomment this block to switch to all greedy
strategies = [2,2,2,2]

# For saving the game state after each game
Hands = [[] for i in range(num_tests)];
History = [[] for i in range(num_tests)];
Winners = [[] for i in range(num_tests)];
Bets = [[] for i in range(num_tests)];
Scores = [[] for i in range(num_tests)];
Tricks = [[] for i in range(num_tests)];
for i in range(num_tests):
    game = Game(13, strategies)
    scores = game.playGame()
    rando_score = scores[1]+scores[3]
    heuristic_score = scores[0]+scores[2]
    
    total_score_rando += rando_score
    total_score_heuristic += heuristic_score
    
    if rando_score < heuristic_score:
        wins_heuristic += 1
    elif rando_score > heuristic_score:
        wins_rando += 1
    else:
        ties += 1
    tricks = [-1 for i in range(4)]
    for p in range(4):
        tricks[p] = sum(game.T[t] == p for t in range(13))

    Hands[i] = game.initialHands;
    History[i] = game.h;
    Winners[i] = game.T;
    Bets[i] = game.bets;
    Scores[i] = scores;
    Tricks[i] = tricks;

tempTime = dt.datetime.now().time();
#timeString = 'Data/Heuristic_v_Greedy' + str(dt.datetime.now().date()) + '-' + str(tempTime.hour) + '-' + str(tempTime.minute) + '-' + str(tempTime.second);
#timeString = 'Data/Greedy_v_Greedy' + str(dt.datetime.now().date()) + '-' + str(tempTime.hour) + '-' + str(tempTime.minute) + '-' + str(tempTime.second);
timeString = 'Data/Greedy_v_Greedy' #+ str(dt.datetime.now().date()) + '-' + str(tempTime.hour) + '-' + str(tempTime.minute) + '-' + str(tempTime.second);

np.save(timeString + '_Hands', Hands)
np.save(timeString + '_History', History)
np.save(timeString + '_Winners', Winners)
np.save(timeString + '_Bets', Bets)
np.save(timeString + '_numTests', num_tests)
np.save(timeString + '_Scores', Scores)
np.save(timeString + '_Tricks', Tricks)

#print 'Heuristic won ' + str(wins_heuristic/num_tests*100) + '% of games, tied ' + str(ties/num_tests*100) + '% of games.'