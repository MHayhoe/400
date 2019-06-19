import keras

from GameObject import Game
from AIPlayer import AIPlayer
from Loss import loss_bet,get_loss_bet

# Play with 13 cards (whole deck)
n = 13

# 0 means human player, 4 means AI player
strategies = [0,4,4,4]
# 'none' for no bet model
bet_strategies = ['none','model','model','model']

# Load the NN models
timeStamp = '2019-06-13-16-5-29'
iter = 100000
bet_model = keras.models.load_model('Models/bet_' + timeStamp +'_' + str(iter) +'.h5',custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})
action_model = keras.models.load_model('Models/action_' + timeStamp +'_' + str(iter) +'.h5',custom_objects={'get_loss_bet': get_loss_bet, 'loss_bet': loss_bet})

# Create the AI objects
AIs = [None for p in range(4)]
for p in range(4):
    if strategies[p] == 4:
        AIs[p] = AIPlayer(4,'model','matrix',bet_model,action_model,None,0)
        
game = Game(n, strategies, bet_strategies, n, AIs)
#scores = game.playGame()