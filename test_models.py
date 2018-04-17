import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

import keras
import keras.layers as L
import keras.regularizers as R
import keras.models as M

from GameObject import Game
from Loss import get_loss_bet, batch_loss_history

#--------------------------
#  HELPER METHODS
#--------------------------
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
num_tests = 10000           

# Interval at which to train
train_interval = num_tests/10;
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
strategies = [4,4,4,4]
bet_strategies = ['model','model','model','model']

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

#----------------------------------
#  INITIALIZATION OF NEURAL NETS  
#----------------------------------
# Initialize the NN optimizer and other parameters
sgd = keras.optimizers.SGD(lr=.01,clipnorm=10.)
opt = keras.optimizers.RMSprop(lr=.01,clipnorm=1.)
batchsize = 128
num_epochs = 20
reg = 0.1

### Initialize the betting NN model
#bet_model = Sequential()
##bet_model.add(L.Dense(10, input_shape=(4,13,1)))
#bet_model.add(L.LeakyReLU(alpha=0.3, input_shape=(4,13,1)))
#bet_model.add(L.Conv2D(1, (1,3), use_bias=False, activation='linear', kernel_regularizer=R.l2(10)))
#bet_model.add(L.BatchNormalization(axis=1))
##bet_model.add(L.Dense(10))
#bet_model.add(L.LeakyReLU(alpha=0.3))
#bet_model.add(L.Conv2D(1, (1,3), use_bias=False, activation='linear', kernel_regularizer=R.l2(0.1)))
#bet_model.add(L.BatchNormalization(axis=1))
#bet_model.add(L.Flatten())
##bet_model.add(Dense(5, activation='relu'))
##bet_model.add(Dense(10, activation='relu'))
#bet_model.add(L.Dense(1, activation='relu'))
##bet_model.summary()

# Initialize the betting NN
input_layer = L.Input(shape = (4,13,1))
xinp = L.LeakyReLU()(input_layer)
x = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xinp)
x = L.BatchNormalization(axis=1)(x)
x = L.LeakyReLU()(x)
x = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(x)
x = L.BatchNormalization(axis=1)(x)
x = L.Add()([x, xinp])
x = L.LeakyReLU()(x)
x = L.Conv2D(2, (1,4), activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xinp)
x = L.BatchNormalization(axis=1)(x)
x = L.LeakyReLU()(x)
x = L.Flatten()(x)
#x = L.Dense(13,activation = 'sigmoid', use_bias = False)(x)
output_layer = L.Dense(1, activation='linear', use_bias = False)(x)

# Compile the model
bet_model = M.Model(inputs=input_layer, outputs=output_layer)
bet_model.compile(loss=get_loss_bet(), optimizer=sgd, metrics=['mean_absolute_error',get_loss_bet()])
#bet_model.summary()


# Initialize the playing NN branches
input_order = L.Input(shape = (1,n*4), name='order')
input_players = L.Input(shape = (1,n*4), name='players')
input_hand = L.Input(shape = (1,n*4), name='hand')
input_bets = L.Input(shape = (1,4), name='bets')
input_tricks = L.Input(shape = (1,4), name='tricks')
input_lead = L.Input(shape = (1,), name='lead')
#input_action = L.Input(shape = (1,52), name='action')

# Branch for the history of the order of played cards
xo = L.Reshape((4,13,1))(input_order)
xo = L.LeakyReLU()(xo)
xo = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xo)
xo = L.BatchNormalization(axis=1)(xo)
xo = L.Flatten()(xo)

# Branch for the history of which player played each card
xp = L.Reshape((4,13,1))(input_players)
xp = L.LeakyReLU()(xp)
xp = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xp)
xp = L.BatchNormalization(axis=1)(xp)
xp = L.Flatten()(xp)

# Branch for the current player's hand
xh = L.Reshape((4,13,1))(input_hand)
xh = L.LeakyReLU()(xh)
xh = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xh)
xh = L.BatchNormalization(axis=1)(xh)
xh = L.Flatten()(xh)

# Branch for the bets
xb = L.LeakyReLU()(input_bets)
xb = L.Flatten()(xb)

# Branch for the tricks
xt = L.LeakyReLU()(input_tricks)
xt = L.Flatten()(xt)

# Branch for the lead suit
xl = L.LeakyReLU()(input_lead)

# Add all NN branches together
a = L.Concatenate(axis=1)([xo, xp, xh, xb, xt, xl])
a = L.LeakyReLU()(a)
output_a = L.Dense(1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(a)

# Compile the model
action_model = M.Model(inputs=[input_order, input_players, input_hand, input_bets, input_tricks, input_lead], outputs=output_a)
action_model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['mean_absolute_error'])
#action_model.summary()


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

Total_Scores = [sum([Scores[i][p] for i in range(num_tests)]) for p in range(4)]

# Save the final models
tempTime = dt.datetime.now().time();
timeString = str(dt.datetime.now().date()) + '-' + str(tempTime.hour) + '-' + str(tempTime.minute) + '-' + str(tempTime.second);
action_model.save('./Models/action_' + t + '_' + timeString + '.h5')
bet_model.save('./Models/bet_' + t + '_' + timeString + '.h5')

