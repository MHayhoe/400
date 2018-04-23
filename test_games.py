import keras
import numpy as np
import os

from GameObject import Game
from Loss import loss_bet, get_loss_bet


# Number of full games to play
num_games = 10
wins_team1 = 0
wins_team2 = 0
datatype='matrix'

# Create the betting NNs for heuristic and greedy
hvh = keras.models.load_model('Models/Heuristic_v_Heuristic_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

hvg = keras.models.load_model('Models/Heuristic_v_Greedy_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
gvh = keras.models.load_model('Models/Greedy_v_Heuristic_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
gvg = keras.models.load_model('Models/Greedy_v_Greedy_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

# To specify which playing NN to load
timestr = '2018-04-20-14-30-55'
iterations = 40000

nn_action_model = keras.models.load_model('Models/action_' + timestr + '_' + str(iterations) + '.h5',
                                          custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
nn_bet_model = keras.models.load_model('Models/bet_' + timestr + '_' + str(iterations) + '.h5',
                                       custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

def test_game(test_type):
    if test_type == 'hvg':
        strategies = [2,3,2,3]
        bet_models = [hvh, nn_bet_model,hvh,nn_bet_model]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None,None,None,None]
        num_iters =1
        
    elif test_type == 'hvr':
        strategies = [1,3,1,3]
        bet_models = [gvg, hvh,gvg,hvh]
        bet_strategies = ['none', 'model', 'none', 'model']
        action_models = [None,None,None,None]
        num_iters = 1
        
    elif test_type == 'gvr':
        strategies = [1,2,1,2]
        bet_models = [gvg, gvh,gvh,gvg]
        bet_strategies = ['none', 'heuristic', 'none', 'heuristic']
        action_models = [None,None,None,None]
        num_iters = 1
        
    elif test_type == 'nnvh':
        strategies = [4,3,4,3]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [nn_action_model, None, nn_action_model, None]
        bet_models = [nn_bet_model, hvh, nn_bet_model, hvh]
        num_iters = 1

    elif test_type == 'hvnn':
        strategies = [3, 4, 3, 4]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None, nn_action_model,None,  nn_action_model]
        bet_models = [hvh, nn_bet_model, hvh, nn_bet_model]
        num_iters = 1

    elif test_type == 'gvnn':
        strategies = [2,4,2,4]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [None, nn_action_model, None, nn_action_model]
        bet_models = [gvg, nn_bet_model,gvg,nn_bet_model]
        num_iters = 1
    elif test_type == 'nnvg':
        strategies = [4,2,4,2]
        bet_strategies = ['model', 'model', 'model', 'model']
        action_models = [ nn_action_model, None, nn_action_model,None]
        bet_models = [ nn_bet_model,gvg,nn_bet_model,gvg]
        num_iters = 1

    elif test_type == 'nnvr':
        strategies = [1,4,1,4]
        bet_strategies = ['none', 'model', 'none', 'model']
        action_models = [None, nn_action_model, None, nn_action_model]
        bet_models = [gvg, nn_bet_model,gvg,nn_bet_model]
        num_iters = 1

    n=13
    wins_team1 = [0 for i in range(num_iters)]
    wins_team2 = [0 for i in range(num_iters)]
    score_team1 = [0 for i in range(num_iters)]
    score_team2 = [0 for i in range(num_iters)]

    num_iters = 4


    for i in range(1):
        for g in range(num_games):
            Total_Scores = [0 for p in range(4)]

            while True:
                game = Game(n, strategies, bet_strategies, n, [None, None, None, None], action_models, bet_models)
                scores = game.playGame()

                for p in range(4):
                    Total_Scores[p] += scores[p]
                score_team1[i] = score_team1[i] + Total_Scores[0] + Total_Scores[2]
                score_team2[i] = score_team2[i] + Total_Scores[1] + Total_Scores[3]
                if (Total_Scores[0] >= 41 and Total_Scores[2] >= 0) or (Total_Scores[0] >= 0 and Total_Scores[2] >= 41):
                       wins_team1[i] += 1
                       break
                if (Total_Scores[1] >= 41 and Total_Scores[3] >= 0) or (Total_Scores[1] >= 0 and Total_Scores[3] >= 41):
                       wins_team2[i] += 1
                       break
        print 'Team 1 won' + str(wins_team1[i])
        print 'Team 2 won' + str(wins_team2[i])

    return (wins_team1, wins_team2)

# Make a Results directory for this time if not there already
if not os.path.exists('Results/'):
    os.mkdir('Results/')
if not os.path.exists('Results/' +timestr+'/'):
    os.mkdir('Results/' +timestr+'/')

nameString='Results/'+timestr + '/results.csv'

# Run through the given test types and save the results
for testtype in ['hvg', 'hvr', 'gvr', 'nnvh','hvnn', 'nnvg','gvnn', 'nnvr']:
    print testtype
    wins = test_game(testtype)
    print wins
    with open(nameString, "a") as output:
        np.savetxt(output, wins, delimiter=',', fmt='%i')
