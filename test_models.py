import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

from GameObject import Game
from Models import initialize_parameters, construct_bet_NN, construct_play_NN
from Loss import batch_loss_history

#--------------------------
#  HELPER METHODS
#--------------------------
# Plots the performance of the betting NN since last training
def plot_bet_performance():
    plt.figure(2)
    # Loss value
    plt.subplot(411)
    plt.plot(Bet_Model_History)
    plt.title('Average Loss')
    # Scores
    plt.subplot(412)
    plt.plot(Average_Scores)
    plt.title('Average Score')
    
    plt.subplot(413)
    bins = range(14);
    # Histogram of tricks
    plt.hist([Tricks[i][0] for i in range(-train_interval,0)], bins, alpha=0.5, label='Tricks')
    # Histogram of recent bets
    plt.hist([Bets[i][0] for i in range(-train_interval,0)], bins, alpha=0.5, label='Bets')
    plt.legend(loc='upper right')
    plt.title('Player 1\'s Bets & Tricks')
    
    plt.subplot(414)
    bins = range(-14,14)
    plt.hist([Tricks[i][0] - Bets[i][0] for i in range(-1000,0)], bins)
    plt.title('Player 1\'s Trick - Bet')
    
    plt.tight_layout()
    plt.show()
  
# Plots the performance of the playing NN since last training
def plot_action_performance():
    plt.figure(3)
    bins = range(14);
    # Histogram of tricks
    plt.hist([Tricks[i][0] + Tricks[i][2] for i in range(-train_interval/2,0)], bins, alpha=0.5, label='Team 1')
    plt.hist([Tricks[i][1] + Tricks[i][3] for i in range(-train_interval/2,0)], bins, alpha=0.5, label='Team 2')
    #plt.hist([Tricks[i][3] for i in range(-train_interval/2,0)], bins, alpha=0.5, label='4')
    plt.legend(loc='upper right')
    plt.title('Tricks for each team')
    
    print np.mean(np.array(Tricks)[-train_interval/2:-1],0)
    
    plt.show()
 
# Returns a state dictionary from the game after applying the action that was
    # taken by player p in round rd.
def update_state(p, rd):
    # Get the game state
    state = game.action_state(p,rd)
    # Get the action taken
    a = game.h[rd][p]
    # Update the state based on action taken
    state['order'][0,a.suit*n + a.value - 2] = max(state['order'][0]) + 1
    state['players'][0,a.suit*n + a.value - 2] = p + 1
    state['hand'][0,a.suit*n + a.value - 2] = 0
    
    # If this would be the first play, update lead suit
    if state['lead'] == -1:
        state['lead'] = a.suit + 1
    
    return state


#-------------------------------
#  INITIALIZATION OF VARIABLES  
#-------------------------------
 # Number of rounds of play to run
num_tests = 100000          

# Interval at which to train
train_interval = num_tests/100;
# Offset of training for betting and playing
train_offset = train_interval/2;

# For tracking scores in the games
total_team1 = 0
total_team2 = 0
wins_team1 = 0.0
wins_team2 = 0.0
ties = 0.0

# Number of cards to give to each player, and number of tricks in each round
n = 13;

# Discount factor for the reward
gamma = 0.9

# Strategies that each player should use to play
strategies = [4,3,4,3]
bet_strategies = ['model','heuristic','model','heuristic']

# For saving the game state after each game
Hands = []
History = []
Bets = []
Scores = []
Tricks = []

# For tracking performance of the NN throughout training
Bet_Model_History = []
Play_Model_History = []
Average_Scores = []

# Save the current time
tempTime = dt.datetime.now().time();
timeString = str(dt.datetime.now().date()) + '-' + str(tempTime.hour) + '-' + str(tempTime.minute) + '-' + str(tempTime.second);


#----------------------------------
#  INITIALIZATION OF NEURAL NETS  
#----------------------------------
# Initialize the parameters
[sgd, opt, batchsize, num_epochs, reg] = initialize_parameters()
    
# Initialize the Neural Nets
bet_model = construct_bet_NN(n)
action_model = construct_play_NN(n)


#--------------------------
#  PLAY AND TRAIN
#--------------------------
# Initialize training data for NNs
x_train = []
y_train = []
x_train_RL = {'order':[], 'players':[], 'bets':[], 'tricks':[], 'hand':[], 'lead':[]}
y_train_RL = []

# Play the game for num_tests rounds
for t in range(1,num_tests+1):
    # Count 100's of rounds
    if t % 100 == 0:
        print t
    
    # Play the game
    game = Game(n, strategies, bet_strategies, n, [action_model for i in range(4)], [bet_model for i in range(4)])
    scores = game.playGame()
    
    # Save the scores for each team
    score_team1 = scores[0] + scores[2]
    score_team2 = scores[1] + scores[3]
    total_team1 += score_team1
    total_team2 += score_team2
    
    # Check who won the game
    if score_team2 < score_team1:
        wins_team1 += 1
    elif score_team2 > score_team1:
        wins_team2 += 1
    else:
        ties += 1
    
    # Get the initial hands of each player
    init_hands = [game.H_history[0][p] for p in range(4)]
    
    # Save the data from the game
    Hands.append(game.initialHands)
    History.append(game.h)
    Bets.append(game.bets)
    Scores.append(scores)
    Tricks.append(game.tricks)
    
    # Save data for training
    for p in [0]:
        # Save the hands as training data for the betting NN
        init_hands[p].sort()
        x_train.append( init_hands[p].get_cards_as_matrix() )
        y_train.append(game.tricks[p])
    
        # Save the game state as training data for the playing NN
        for rd in range(n):
            # Get and update the game state based on the action taken
            state = update_state(p, rd)
            for key in state:
                x_train_RL[key].append(state[key])
            # REWARD:
            my_team_score = int(game.T[rd]==p or game.T[rd]==((p+2)%4))
            discounted_reward = gamma**(n - 1 - rd)*(scores[p] + scores[(p+2)%4])
            #y_train_RL.append(discounted_reward + my_team_score)
            y_train_RL.append(discounted_reward + my_team_score)
    
    # Train the betting NN
    if t % train_interval == 0:
        print 'Training betting...'
        hist = batch_loss_history()
        bet_model.fit(np.asarray(x_train), np.asarray(y_train), batch_size=batchsize, epochs = num_epochs, verbose=0, callbacks=[hist])
        
        # --- Record the performance ---
        training_range = range(int(t/train_interval - 1)*train_interval,int(t/train_interval)*train_interval)
        Bet_Model_History.append( np.mean(hist.losses) ) # Average loss across all batches
        Average_Scores.append([sum([Scores[i][p] for i in training_range])/train_interval for p in range(4)]) # Average score when using the previous strategy
    
        # Plot the betting NN's performance
        plot_bet_performance()
        
        print 'Done.'
    
        x_train = []
        y_train = []
        
    # Train the playing NN
    if (t + train_offset) % train_interval == 0:
        print 'Training strategies...'
        for key in x_train_RL:
            x_train_RL[key] = np.asarray(x_train_RL[key])
        action_model.fit(x_train_RL, np.asarray(y_train_RL), batch_size=batchsize, epochs = num_epochs, verbose=0)
        
        # Plot the playing NN's performance
        plot_action_performance()
        
        print 'Done.'
        
        for key in x_train_RL:
            x_train_RL[key] = []
        y_train_RL = []
    
    # Save the models after they have been trained 10 times
    if t % train_interval*10 == 0:
        # Save the models
        action_model.save('./Models/action_' + timeString + '_' + str(t) + '.h5')
        bet_model.save('./Models/bet_' + timeString + '_' + str(t) + '.h5')

Total_Scores = [sum([Scores[i][p] for i in range(num_tests)]) for p in range(4)]

