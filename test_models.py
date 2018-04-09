from GameObject import Game
import numpy as np

from keras import backend as K
import keras
#from keras.models import Sequential
import keras.layers as L
import keras.regularizers as R
import keras.models as M

import matplotlib.pyplot as plt

# Number of rounds of play to run
num_tests = 100000           

# Number of cards to give to each player, and number of tricks in each round
n = 13;

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

#--------------------------
#  INITIALIZATION
#--------------------------
# Strategies that each player should use to play
strategies = [3,3,3,3]

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

# Returns our custom loss function
def get_loss_bet():
    return loss_bet

# Our custom loss function: if we make our bet (y_true >= y_pred), the loss
# is the amount we could have gotten if we'd bet y_true, i.e., it's
# y_true - y_pred. If we didn't make our bet, then our loss is what we
# could have gotten minus what we lost, i.e., y_true + y_pred
# (since -1*(-bet) = bet)
def loss_bet(y_true, y_pred):
    #return K.square(y_true - y_pred)
    return K.square(y_true + K.sign(y_pred - y_true) * y_pred)

# To track the loss for each batch during training of a model
class batch_loss_history(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))

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

reg = 0.1

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
bet_model.summary()

# Initialize the NN optimizer and other parameters
sgd = keras.optimizers.SGD(lr=.01,clipnorm=1000.)
opt = keras.optimizers.RMSprop(lr=.01,clipnorm=1.)
batchsize = 128
num_epochs = 20

# Compile the model
bet_model.compile(loss=get_loss_bet(), optimizer=sgd, metrics=['mean_absolute_error',get_loss_bet()])

x_train = []
y_train = []

#--------------------------
#  PLAY AND TRAIN
#--------------------------
# Play the game for num_tests rounds
for t in range(1,num_tests+1):
    # Count 10,000's of rounds
    #if i % 10000 == 1:
    #print(t)
        
    game = Game(n, strategies, ['model','heuristic','model','heuristic'], n, [bet_model for i in range(4)])
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
    
    #x_train = np.array((n*2,4))
    init_hands = [game.initialHands[p] for p in range(4)]
    
    # Count the number of tricks each player won
    tricks = [sum(game.T[t] == p for t in range(n)) for p in range(4)]
    
    # Save the data from the game
    Hands.append(game.initialHands)
    History.append(game.h)
    Bets.append(game.bets)
    Scores.append(scores)
    Tricks.append(tricks)
    
    # Save the hands as training data for the betting NN
    for p in [0]:
        init_hands[p].sort()
#        vals = [init_hands[p].cards[i].value for i in range(n)]
#        suits = [init_hands[p].cards[i].suit for i in range(n)]
#        x_train.append(vals + suits)
#        x_binary = [0 for i in range(n*4)]
#        for c in init_hands[p].cards:
#            x_binary[c.suit*4 + c.value] = 1
#        x_train.append(x_binary)
        x_train.append( init_hands[p].get_cards_as_matrix() )
        y_train.append(tricks[p])
    
    # Train the betting NN
    if t % train_interval == 0:
        print 'Training betting...'
        hist = batch_loss_history()
        bet_model.fit(np.array(x_train), np.array(y_train), batch_size=batchsize, epochs = num_epochs, verbose=0, callbacks=[hist])
        print 'Done.'
        
        # --- Record the performance ---
        training_range = range(int(t/train_interval - 1)*train_interval,int(t/train_interval)*train_interval)
        # 1. Average loss across all batches
        Bet_Model_History.append( np.mean(hist.losses) )
        # 2. Average score when using the previous strategy
        Average_Scores.append([sum([Scores[i][p] for i in training_range])/train_interval for p in range(4)])
    
        x_train = []
        y_train = []
        
        plt.figure(2)
        plt.plot(Bet_Model_History)

        plt.figure(3)
        plt.plot(Average_Scores)
        
        plt.show()
    # Train the playing NN
    elif (t + train_offset) % train_interval == 0:
        print 'Training strategies PLACEHOLDER'

Total_Scores = [sum([Scores[i][p] for i in range(num_tests)]) for p in range(4)]

#Tricks = np.array(Tricks)
#Bets = np.array(Bets)
#Scores = np.array(Scores)
#diff = [Tricks[i,0] - Bets[i,0] for i in range(num_tests)]
#plt.figure(1)
#plt.plot(diff)
#plt.plot([Scores[i,0] for i in range(num_tests)])
