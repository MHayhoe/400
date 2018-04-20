from GameObject import Game
import keras
import numpy as np
import matplotlib.pyplot as plt
from Loss import loss_bet, get_loss_bet


# Number of full games to play
num_games = 100
wins_team1 = 0
wins_team2 = 0
datatype='matrix'
hvh = keras.models.load_model('Models/Heuristic_v_Heuristic_bet_data_model_' + datatype + '_model.h5',
                                                   custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

def test_game(test_type, bet_strategies, action_models, bet_models):
    if  test_type == 'nnvh':
#        strategies = [3,4,3,4]
#        bet_strategies = ['model', 'model', 'model', 'model']
#        action_models = [None, nn_action_model, None, nn_action_model]
#        bet_models = [hvh, nn_bet_model,hvh,nn_bet_model]
        strategies = [4,3,4,3]
    elif test_type == 'nnvnn':
        strategies = [4,4,4,4]

    n=13
    wins_team1 = 0
    wins_team2 = 0
    score_team1 = 0
    score_team2 = 0
    #wins_team1 = [0 for i in range(10)]
    #wins_team2 = [0 for i in range(10)]
    #frac_won_by_nn = [0 for i in range(10)]

    for g in range(num_games):
        Total_Scores = [0 for p in range(4)]

        while True:
            #game = Game(n, strategies, bet_strategies, n, [action_model for i in range(4)], [bet_model for i in range(4)])
            game = Game(n, strategies, bet_strategies, n, action_models, bet_models)
            scores = game.playGame()

            for p in range(4):
                Total_Scores[p] += scores[p]
            score_team1 = score_team1 + Total_Scores[0] + Total_Scores[2]
            score_team2 = score_team2 + Total_Scores[1] + Total_Scores[3]
            if (Total_Scores[0] >= 41 and Total_Scores[2] >= 0) or (Total_Scores[0] >= 0 and Total_Scores[2] >= 41):
                   wins_team1 += 1
                   #print 'Team 1 won'
                   break
            if (Total_Scores[1] >= 41 and Total_Scores[3] >= 0) or (Total_Scores[1] >= 0 and Total_Scores[3] >= 41):
                   wins_team2 += 1
                   #print 'Team 2 won'
                   break
            #print scores
            #print Total_Scores
        print 'game: ' + str(g)
        #print Total_Scores
    print 'Team 1 won' + str(wins_team1)
    print 'Team 2 won' + str(wins_team2)
    #frac_won_by_nn[i] = wins_team2[i]*1.0/num_games
    #print frac_won_by_nn

    #plt.figure(2)
    #plt.plot(frac_won_by_nn)
    #plt.title('NN performance vs heuristic team')
    #plt.savefig('Plots/nn.png')
    return (wins_team1, wins_team2,score_team1,score_team2)


timestr='2018-04-19-17-44-9'
timestamp = timestr
nameString='results' + timestr + '.csv'
nn_v_h_frac_win = [0. for i in range(10)]
nn2_v_young_nn_frac_win = [0. for i in range(10)]
total_score_nn = [0. for i in range(10)]
total_score_h = [0. for i in range(10)]
nn_v_young_nn_score = [0. for i in range(10)]
young_nn_score = [0. for i in range(10)]

young_nn_action = keras.models.load_model('Models/action_' + timestr + '_' + str(10000) + '.h5',
                                          custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
young_nn_bet = keras.models.load_model('Models/bet_' + timestr + '_' + str(10000) + '.h5',
                                       custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
for i in range(10):
    iterations = str((i + 1) * 10000)
    nn_action_model = keras.models.load_model('Models/action_' + timestr + '_' + str(iterations) + '.h5',
                                          custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
    nn_bet_model = keras.models.load_model('Models/bet_' + timestr + '_' + str(iterations) + '.h5',
                                       custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
    #nn v heuristic
    bet_strategies = ['model', 'model', 'model', 'model']
    action_models = [nn_action_model, None, nn_action_model, None]
    bet_models = [nn_bet_model, hvh, nn_bet_model, hvh]
    wins = test_game('nnvh',bet_strategies,action_models,bet_models)
    nn_v_h_frac_win[i] = wins[0]/num_games
    print wins
    with open(nameString, "a") as output:
        np.savetxt('Plots/' + timestamp + '_results_nnvh_'+str(i)+'.csv', np.asarray(wins),delimiter=',')

    action_models = [ nn_action_model, young_nn_action, nn_action_model, young_nn_action]
    bet_models = [nn_bet_model, young_nn_bet, nn_bet_model, young_nn_bet]
    wins = test_game('nnvnn',bet_strategies,action_models,bet_models)
    nn2_v_young_nn_frac_win[i] = wins[0]/num_games
    scores = wins[2]
    with open(nameString, "a") as output:
        np.savetxt('Plots/' + timestamp + '_results_nnvnn_'+str(i)+'.csv', np.asarray(wins),delimiter=',')

with open(nameString, "a") as output:
    np.savetxt('Plots/' + timestamp + '_results2'+'.csv', np.asarray([nn_v_h_frac_win,nn2_v_young_nn_frac_win, total_score_nn, young_nn_score, nn_v_young_nn_score ,young_nn_score]), delimiter=',', fmt='%i')


plt.figure(2)
plt.plot(nn_v_h_frac_win)
plt.title('Frac won vs heuristic')
plt.savefig('Plots/' + timestamp + '/frac_won_vs_heuristic' + '.eps', bbox_inches='tight')
plt.clf()

plt.figure(2)
plt.plot(nn2_v_young_nn_frac_win)
plt.title('Frac won vs youngest NN')
plt.savefig('Plots/' + timestamp + '/frac_won_vs_young_nn' + '.eps', bbox_inches='tight')
plt.clf()

plt.figure(2)
plt.plot(total_score_nn)
plt.title('Neural network score vs heuristic')
plt.savefig('Plots/' + timestamp + '/score_nn_v_h' + '.eps', bbox_inches='tight')
plt.clf()

plt.figure(2)
plt.plot([nn_v_young_nn_score, young_nn_score])
plt.title('Trained and Young NN scores')
plt.savefig('Plots/' + timestamp + '/score_nn_v_nn' + '.eps', bbox_inches='tight')
plt.clf()

