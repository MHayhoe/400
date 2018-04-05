from GameObject import Game
import numpy as np

from keras import backend as K
import keras
from keras.models import Sequential
from keras.layers import Dense

num_tests = 10
n = 13;

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
strategies = [2,2,2,2]

# For saving the game state after each game
Hands = []
History = []
Bets = []
Scores = []
Tricks = []

# For tracking performance of the NN throguh training
Bet_Model_History = []

# Returns our custom loss function
def get_loss_bet():
    return loss_bet

# Our custom loss function: if we make our bet (y_true >= y_pred), the loss
# is the amount we could have gotten if we'd bet y_true, i.e., it's
# y_true - y_pred. If we didn't make our bet, then our loss is what we
# could have gotten minus what we lost, i.e., y_true + y_pred
# (since -1*(-bet) = bet)
def loss_bet(y_true, y_pred):
    return K.mean(y_true + K.sign(y_pred - y_true) * y_pred)

# Initialize the betting NN model
bet_model = Sequential()
bet_model.add(Dense(13, input_dim=26, activation='relu'))
bet_model.add(Dense(13, activation='relu'))
bet_model.add(Dense(1, activation='relu'))

# Initialize the NN optimizer and other parameters
sgd = keras.optimizers.SGD(lr=.01,clipnorm=10.)
batchsize = 128
epoches = 100

# Compile the model
bet_model.compile(loss=get_loss_bet(), optimizer=sgd, metrics=['mean_absolute_error',get_loss_bet()])


#--------------------------
#  PLAY AND TRAIN
#--------------------------
# Play the game for num_tests rounds
for i in range(num_tests):
    # Count 10,000's of rounds
    if i % 10000 == 1:
        print(i)
        
    game = Game(n, strategies, )
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
    x_train = []
    
    # Save the hands as training data for the betting NN
    for p in range(4):
        init_hands[p].sort()
        vals = [init_hands[p].cards[i].value for i in range(n)]
        suits = [init_hands[p].cards[i].suit for i in range(n)]
        x_train.append(vals + suits)
    
    # Count the number of tricks each player won
    tricks = [sum(game.T[t] == p for t in range(n)) for p in range(4)]
    
    # Train the betting NN
    hist = bet_model.fit(np.array(x_train), tricks, batch_size=1, epochs = epoches, verbose=1)
    
    # Record the performance
    Bet_Model_History.append(hist)

    Hands.append(game.initialHands)
    History.append(game.h)
    Bets.append(game.bets)
    Scores.append(scores)
    Tricks.append(tricks)

