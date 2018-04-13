from GameObject import Game
import numpy as np

from keras import backend as K
import keras
#from keras.models import Sequential
import keras.layers as L
import keras.regularizers as R
import keras.models as M
from Loss import get_loss_bet

import matplotlib.pyplot as plt

#--------------------------
#  HELPER METHODS
#--------------------------

# To track the loss for each batch during training of a model
class batch_loss_history(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

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
    
    plt.show()
    
def plot_action_performance():
    plt.figure(3)
    bins = range(14);
    # Histogram of tricks
    plt.subplot(211)
    plt.hist([Tricks[i][0] for i in range(-train_interval/2,0)], bins, alpha=0.5, label='1')
    plt.hist([Tricks[i][2] for i in range(-train_interval/2,0)], bins, alpha=0.5, label='3')
    plt.legend(loc='upper right')
    plt.title('Tricks for Team 1')
    
    plt.subplot(212)
    plt.hist([Tricks[i][1] for i in range(-train_interval/2,0)], bins, alpha=0.5, label='2')
    plt.hist([Tricks[i][3] for i in range(-train_interval/2,0)], bins, alpha=0.5, label='4')
    plt.legend(loc='upper right')
    plt.title('Tricks for Team 2')
    
    print np.mean(np.array(Tricks)[-train_interval/2:-1],0)
    
    plt.show()


#--------------------------
#  INITIALIZATION
#--------------------------
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
strategies = [4,2,4,2]
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
xl = L.LeakyReLU()(input_layer)
x = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xl)
x = L.BatchNormalization(axis=1)(x)
x = L.LeakyReLU()(x)
x = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(x)
x = L.BatchNormalization(axis=1)(x)
x = L.Add()([x, xl])
x = L.LeakyReLU()(x)
x = L.Conv2D(2, (1,4), activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xl)
x = L.BatchNormalization(axis=1)(x)
x = L.LeakyReLU()(x)
x = L.Flatten()(x)
#x = L.Dense(13,activation = 'sigmoid', use_bias = False)(x)
output_layer = L.Dense(1, activation='linear', use_bias = False)(x)

bet_model = M.Model(inputs=input_layer, outputs=output_layer)
#bet_model.summary()

# Compile the model
bet_model.compile(loss=get_loss_bet(), optimizer=sgd, metrics=['mean_absolute_error',get_loss_bet()])


# Initialize the playing NN
input_order = L.Input(shape = (4,13,1))
input_players = L.Input(shape = (4,13,1))
input_bets = L.Input(shape = (4,))
input_tricks = L.Input(shape = (4,))
input_action = L.Input(shape = (52,))
# For the history of the order of played cards
xo = L.LeakyReLU()(input_order)
xo = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xo)
xo = L.BatchNormalization(axis=1)(xo)
# For the history of which player played each card
xp = L.LeakyReLU()(input_players)
xp = L.Conv2D(1, 1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(xp)
xp = L.BatchNormalization(axis=1)(xp)

acnn = L.Add()([xo, xp])
acnn = L.Flatten()(acnn)

# For the bets
xb = L.LeakyReLU()(input_bets)
# For the tricks
xt = L.LeakyReLU()(input_tricks)

xa = L.LeakyReLU()(input_action)

a = L.Concatenate(axis=1)([acnn, xb, xt, xa])
a = L.LeakyReLU()(a)
output_a = L.Dense(1, activation='linear', use_bias=False, kernel_regularizer=R.l2(reg))(a)

action_model = M.Model(inputs=[input_order, input_players, input_bets, input_tricks, input_action], outputs=output_a)
#action_model.summary()

action_model.compile(loss='mean_squared_error', optimizer=sgd, metrics=['mean_absolute_error'])

#--------------------------
#  PLAY AND TRAIN
#--------------------------
x_train = []
y_train = []

x_train_RL = []
y_train_RL = []

# Play the game for num_tests rounds
for t in range(1,num_tests+1):
    # Count 10,000's of rounds
    #if i % 10000 == 1:
    print t
        
    game = Game(n, strategies, bet_strategies, n, [action_model for i in range(4)], [bet_model for i in range(4)])
    scores = game.playGame()
    
    score_team1 = scores[0] + scores[2]
    score_team2 = scores[1] + scores[3]
    
    total_team1 += score_team1
    total_team2 += score_team2
    
    if score_team2 < score_team1:
        wins_team1 += 1
    elif score_team2 > score_team1:
        wins_team2 += 1
    else:
        ties += 1
    
    # Get the initial hands of each player
    init_hands = [game.initialHands[p] for p in range(4)]
    
    # Save the data from the game
    Hands.append(game.initialHands)
    History.append(game.h)
    Bets.append(game.bets)
    Scores.append(scores)
    Tricks.append(game.tricks)
    
    # SAVE DATA FOR TRAINING
    for p in [0]:
        # Save the hands as training data for the betting NN
        init_hands[p].sort()
        x_train.append( init_hands[p].get_cards_as_matrix() )
        y_train.append(game.tricks[p])
    
        # Save the game state as training data for the playing NN
        for rd in range(n):
            state = game.action_state(p,rd)
            x_train_RL.append([state[0], state[1], state[2], state[3], game.h[rd][p].as_action(n)])
            my_team_score = int(game.T[rd]==p or game.T[rd]==((p+2)%4))
            discounted_reward = gamma**(n - 1 - rd)*(scores[p] + scores[(p+2)%4])
            y_train_RL.append(discounted_reward + my_team_score)
    
    # Train the betting NN
    if t % train_interval == 0:
        print 'Training betting...'
        hist = batch_loss_history()
        bet_model.fit(np.array(x_train), np.array(y_train), batch_size=batchsize, epochs = num_epochs, verbose=0, callbacks=[hist])
        
        # --- Record the performance ---
        training_range = range(int(t/train_interval - 1)*train_interval,int(t/train_interval)*train_interval)
        # 1. Average loss across all batches
        Bet_Model_History.append( np.mean(hist.losses) )
        # 2. Average score when using the previous strategy
        Average_Scores.append([sum([Scores[i][p] for i in training_range])/train_interval for p in range(4)])
    
        # Plot the betting NN's performance
        plot_bet_performance()
        
        print 'Done.'
    
        x_train = []
        y_train = []
        
    # Train the playing NN
    elif (t + train_offset) % train_interval == 0:
        print 'Training strategies...'
        action_model.fit(x_train_RL, np.array(y_train_RL), batch_size=batchsize, epochs = num_epochs, verbose=0)
        
        plot_action_performance()
        
        print 'Done.'
        
        x_train_RL = []
        y_train_RL = []

Total_Scores = [sum([Scores[i][p] for i in range(num_tests)]) for p in range(4)]
