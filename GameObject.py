import random as rnd
from copy import deepcopy
import numpy as np

from Hand import Hand
from Deck import Deck
from Card import Card
from AIPlayer import AIPlayer


class Game:
    # Constructor to build a new Game object
    def __init__(self, num_rounds, strategy_vector, bet_vector, n=13, AIs=[None,None,None,None],action_model_objects=[None, None, None, None], bet_model_objects = [None, None, None, None],genetic_parameter_list=[None,None,None,None]):
        # type: (object, object, object) -> object
        self.num_rounds = num_rounds;
        self.player_strategy = strategy_vector;
        self.bet_strategy = bet_vector;
        self.n = n;
        self.aiplayers = [AIs[i] if AIs[i] is not None else
                          AIPlayer(self.player_strategy[i], self.bet_strategy[i], 'matrix', bet_model_objects[i], action_model_objects[i], genetic_parameter_list[i])
                          for i in range(4)]

        # For tracking the state for the playing NN
        self.state = {'order': np.zeros((1,52)),'players': np.zeros((1,52))};
        
        self.play_order = [[] for i in range(num_rounds)]

        # There's a human player, so we want to print
        if 0 in strategy_vector:
            self.verbose = True;
        else:
            self.verbose = False;


    # ----- METHODS -----
    # To print a string, only if we want to be verbose
    def printVerbose(self, s):
        if self.verbose:
            print s
            
    # For verifying human input
    def isInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    # To handle human input for player p
    def humanInput(self, p):
        # Show them their hand
        self.H[p].sort()
        print 'Player ' + str(p + 1) + '\'s Hand: ' + str(self.H[p])
        # Save and display the list of valid cards
        valid_cards = self.H[p].validCards();
        print 'VALID cards: ' + Card.printListIndices( valid_cards )

        # Ask for input
        card_index = input('Pick index of VALID card to play: ')

        # Check if the chosen index was valid
        while not( self.isInt(card_index) ) or card_index < 0 or card_index >= len(valid_cards):
           # Ask for input
           card_index = input('Invalid. Pick again (from VALID): ')

        return self.H[p].play( self.H[p].validToRealIndex( int(card_index) ) )
    
    # To handle human bet for player p
    def humanBet(self, p):
        # Show them their hand
        self.H[p].sort()
        print 'Player ' + str(p + 1) + '\'s Hand: ' + str(self.H[p])
        bet = input('Bet tricks to take: ')
        
        while not(bet>=2):
            #Ask for new bet
            bet = input('The minimum bet is 2. Bet: ')
            
        return bet
    
    # Update the running dictionary of the state
    def update_state(self, p, t):
        c = self.h[t][p];
        self.state['order'][0,c.suit*self.n + c.value-2] = np.max(self.state['order']) + 1;
        self.state['players'][0,c.suit*self.n + c.value-2] = p + 1;
        
    # Returns the state for the playing NN, used during the play of a game
    def get_state(self, p, t):
        state = self.state
        
        state['hand'] = self.H[p].get_cards_binary(self.n)
        state['lead'] = np.array(self.leads[t])
        
        # Change the state to be relative to this player
        for i in range(self.n*4):
            state['players'][0,i] = (self.state['players'][0,i] - (p + 1)) % 4 + 1
        state['tricks'] = np.reshape(self.tricks[p:] + self.tricks[:p],(1,4));
        state['bets'] = np.reshape(self.bets[p:] + self.bets[:p],(1,4));
                
        return state
    
    # Returns the state in a form that's expected by the playing NN (builds
    # from scratch; should only be used externally to save training data)
    def action_state(self, player, current_round):
        count = 1;
        state = {}
        state['order'] = np.zeros((1,52));
        state['players'] = np.zeros((1,52));
        
        # Loop through previous rounds
        for t in range(current_round):
            for p in self.play_order[t]:
                c = self.h[t][p];
                if c is not None:
                    state['order'][0,c.suit*self.n + c.value-2] = count;
                    count = count + 1;
                    state['players'][0,c.suit*self.n + c.value-2] = p + 1;
        
        # Loop through current round, up to and including 'player'
        for p in self.play_order[current_round]:
            c = self.h[current_round][p];
            state['order'][0,c.suit*self.n + c.value-2] = count;
            count = count + 1;
            state['players'][0,c.suit*self.n + c.value-2] = p + 1;
            if p == player:
                break
            
        # Find tricks up until now
        tricks = [sum([self.T[t] == p for t in range(current_round+1)]) for p in range(4)]
        
        # Change the state to be relative to this player
        for i in range(self.n*4):
            state['players'][0,i] = (state['players'][0,i] - (player + 1)) % 4 + 1
        state['tricks'] = np.reshape(tricks[player:] + tricks[:player],(1,4));
        state['bets'] = np.reshape(self.bets[player:] + self.bets[:player],(1,4));  
        
        state['hand'] = self.H_history[current_round][player].get_cards_binary(self.n)
        state['lead'] = np.array(self.leads[current_round])
        
        return state
    
    # To handle AI input for player p     
    def aiInput(self, p, current_round, strategy, valid_cards):
        if strategy == 3: # Simple heuristic
            state = [self.play_order[current_round].index(p),self.card_played_by,self.cards_this_round,self.suit_trumped_by,self.bet_deficits]
        elif strategy == 4: # Playing NN
            state = self.get_state(p, current_round)
        elif strategy == 5: #playing genetic
            state = self.get_state(p, current_round)
        else: # Don't need the state, e.g. random, greedy
            state = []
        # Check if we care about the current winning card (to determine who wins a trick)
        if (np.max(self.state['order'])) % 4 > 0: # some cards have been played this trick
        #if (np.max(self.state['order']) + 1) % 4 == 0: # 3 cards have been played this trick
            current_winner = np.max([cc for cc in self.h[current_round] if cc is not None])
        else:
            current_winner = None

        chosen_action = self.aiplayers[p].get_action(self.n, p, state, valid_cards, current_winner)
        return self.H[p].play(self.H[p].validToRealIndex( chosen_action ));

    #To handle AI bets for player p
    def aiBet(self, p, strategy=1):
        return self.aiplayers[p].get_bet(self.H[p])

    # Find the winning player from a trick
    def winner(self, cards):
        srtd = sorted(cards,reverse=True)
        return cards.index(srtd[0])


    # ----- BETTING ROUND -----
    def bettingRound(self):
        for p in range(4):
            if self.player_strategy[p] == 0: #ask for human bet
                self.bets[p] = self.humanBet(p)
            else:
                self.bets[p] = self.aiBet(p, self.player_strategy[p])
            
            self.printVerbose('Player ' + str(p+1) + ' bet '  +str(self.bets[p]))


    # ----- PLAYING ROUNDS -----
    def initializeRound(self, n=13):
        # Make a new deck with n cards of each suit, and shuffle it.
        deck = Deck(n);
        deck.shuffle();

        # Deal n cards to each player
        self.H = [Hand(deck.deal(n)) for i in range(4)];
        # Make a separate list to save the initial hands
        self.initialHands = deepcopy(self.H);
        if self.verbose:
            for h in self.H:
                h.sort()
                print h
        self.H_history = [[[] for i in range(4)] for t in range(self.num_rounds)]
        self.h = [[None for i in range(4)] for t in range(self.num_rounds)]
        self.T = [-1 for i in range(self.num_rounds)]
        self.tricks = [0 for i in range(4)]
        self.leads = [-1 for i in range(self.num_rounds)]
        
        # Initialize the bets to zero
        self.bets = [0 for i in range(4)];

    def playRound(self,n=13):
        # Initialize the round
        self.initializeRound(n);
        
        # Get the bets
        self.bettingRound();
        self.initialbets = self.bets;
        
        # Initialize some state-dependent metrics to pass to AI
        self.card_played_by = {card.__str__():None for card in Deck().cards}
        self.suit_trumped_by = {i:set() for i in range(4)}
        self.bet_deficits = list(self.bets)
        
        # Go through the rounds
        for t in range(0, self.num_rounds):
            # No lead suit yet
            Card.lead = -1;
            self.cards_this_round = {i: None for i in range(4)}
            
            # Save the current hands for history
            self.H_history[t] = deepcopy(self.H)
            
            order = range(4);
            
            # Permute player order
            if t > 0: # The previous winner should go first, then continue in order
                self.play_order[t] = order[self.T[t-1]:] + order[:self.T[t-1]]
            else:   # Randomly choose who goes first
                first_player = rnd.randint(0,3);
                self.play_order[t] = order[first_player:] + order[:first_player]
            
            # Loop through players
            for p in self.play_order[t]:
                print str(p+1) + ': ' + str(self.bets[p]) + ' bet, ' + str(self.tricks[p]) + ' won'
                if self.player_strategy[p] == 0: # Ask for human input
                    self.h[t][p] = self.humanInput(p);
                else:                   # Ask for AI input with strategy in player_strategy[p]
                    self.h[t][p] = self.aiInput(p, t, self.player_strategy[p], self.H[p].validCards());
                # Set the lead suit, if it hasn't been yet
                if Card.lead == -1:
                    Card.lead = self.h[t][p].suit;
                    self.leads[t] = Card.lead;

                # Update the state for the playing NN
                self.update_state(p, t);

                # Display what was played
                self.printVerbose(str(p + 1) + ':  ' + str(self.h[t][p]))
                self.printVerbose('')
                
                # Update
                self.cards_this_round[p] = self.h[t][p]
                #update the card_played_by dict
                self.card_played_by[str(self.h[t][p])]=p
                if Card.lead != -1 and Card.lead != Card.trump:
                    if self.h[t][p].suit == Card.trump:
                        self.suit_trumped_by[Card.lead].add(p)
                        
               

            # Find the winning player from the cards played this round
            self.T[t] = self.winner(self.h[t]);
            self.tricks[self.T[t]] = self.tricks[self.T[t]] + 1;
            self.printVerbose('Player ' + str(self.T[t] + 1) + ' won the trick.')
            self.bet_deficits[self.T[t]] -= 1;

    def getFinalScores(self, bets, T):
        scores = [0,0,0,0];
        for p in range(4):
            tricks_p = sum(T[t] ==p for t in range(13))
            bet_p = bets[p]
            chg_score = (2*(tricks_p>= bet_p)-1)*bet_p
            self.printVerbose('Player ' + str(p) + ' bet ' +str(bet_p) + ' and won ' +str(tricks_p) + ' for a total of ' + str(chg_score))
            scores[p]=chg_score
        return scores
    
    # Play the game. Call this method to run the game externally.
    def playGame(self):
        self.playRound()
        return(self.getFinalScores(self.bets, self.T))
        
    def getTricks(self):
        return self.tricks