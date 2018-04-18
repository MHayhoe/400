#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 15:44:48 2018

@author: Mikhail
"""
import random as rnd
from copy import copy, deepcopy

from Hand import Hand
from Deck import Deck
from Card import Card
from AIPlayer import AIPlayer
from heuristicAI import heuristicChoice
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.utils import to_categorical
import keras
from keras import backend as K
import numpy as np

class Game:
    #hack - fix later! importing betmodel in game object
    def __init__(self, num_rounds, strategy_vector, bet_vector, n=13, action_model_objects=[None, None, None, None], bet_model_objects = [None, None, None, None],genetic_parameter_list=[None,None,None,None]):
        # type: (object, object, object) -> object
        self.num_rounds = num_rounds;
        self.player_strategy = strategy_vector;
        self.bet_strategy = bet_vector;
        self.n = n;
        #self.bet_models = betting_model_objects
        #self.action_models = 
        self.aiplayers = [AIPlayer(self.player_strategy[i], self.bet_strategy[i], 'matrix', bet_model_objects[i], action_model_objects[i], genetic_parameter_list[i]) for i in range(4)]

        # For tracking the state for the playing NN
        self.state = {'order': np.zeros((1,52)),'players': np.zeros((1,52))};
        
        self.play_order = [[] for i in range(num_rounds)]

        # There's a human player, so we want to print
        if 0 in strategy_vector:
            self.verbose = True;
        else:
            self.verbose = False;

    #Variables
    num_rounds = 13;

    # Strategy for each player:
    # 0:    human
    # 1:    random - play a valid card at random
    # 2:    highest - play the highest valid card
    #player_strategy = [0, 2, 1, 1];
    # Make a new deck, and shuffle it.
    deck = Deck();
    deck.shuffle();


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
        
        while not(bet>1):
            #ask for new bet
            bet = input('The minimum bet is 2. Bet: ')
            
        return bet
    
    # Returns the state in a form that's expected by the playing NN
    def update_state(self, p, t):
        c = self.h[t][p];
        self.state['order'][0,c.suit*self.n + c.value-2] = max(self.state['order']) + 1;
        self.state['players'][0,c.suit*self.n + c.value-2] = p + 1;
        
    # Returns the state for the playing NN
    def get_state(self, p, t):
        self.state['hand'] = self.H[p].get_cards_binary(self.n)
        self.state['tricks'] = np.reshape(self.tricks,(1,4));
        self.state['lead'] = self.leads[t]
        
        return self.state
    
    # Returns the state in a form that's expected by the playing NN (builds from
    # scratch; should only be used externally to save training data)
    def action_state(self, player, current_round):
        count = 1;
        self.state['order'] = np.zeros((1,52));
        self.state['players'] = np.zeros((1,52));
        
        # Loop through previous rounds
        for t in range(current_round):
            for p in self.play_order[t]:
                c = self.h[t][p];
                if c is not None:
                    self.state['order'][0,c.suit*self.n + c.value-2] = count;
                    count = count + 1;
                    self.state['players'][0,c.suit*self.n + c.value-2] = p + 1;
        
        # Loop through current round, until 'player'
        for p in self.play_order[current_round]:
            if p == player:
                break
            c = self.h[current_round][p];
            self.state['order'][0,c.suit*self.n + c.value-2] = count;
            count = count + 1;
            self.state['players'][0,c.suit*self.n + c.value-2] = p + 1;
            
        self.state['hand'] = self.H_history[current_round][p].get_cards_binary(self.n)
        self.state['tricks'] = np.reshape(self.tricks,(1,4));
        self.state['lead'] = np.array(self.leads[current_round])
        self.state['current_winner'] = np.array(max([cc for cc in self.h[t] if cc is not None]))
        
        return self.state
    
    
    # To handle AI decisions for player p
    #old def aiInput(self, p, strategy,valid_cards, card_played_by,cards_this_round,suit_trumped_by,bet_deficits,cards_played_by,position):
        #if strategy == 3: #simple heuristic
        #    valid_idx= heuristicChoice(p,valid_cards,card_played_by,cards_this_round,suit_trumped_by,bet_deficits,cards_played_by,position)
            #print self.H[p].cards[self.H[p].validToRealIndex(valid_idx) ]
        #    return self.H[p].play( self.H[p].validToRealIndex(valid_idx) )
        #if strategy == 2: # Myopic Greedy: pick the highest playable card every time
            # Sort the hand, so when we pick a valid card it will be the biggest valid card
        #    self.H[p].sort()
         #   return self.H[p].play( self.H[p].validToRealIndex(0) );
        #else: # Random choice
            # Pick a valid card at random
         #   ind = rnd.randint( 0, len(self.H[p].validCards()) - 1 )
          #  return self.H[p].play( self.H[p].validToRealIndex(ind) )
          
    def aiInput(self, p, current_round, strategy, valid_cards):
        if strategy == 3: # Simple heuristic
            state = [self.play_order[current_round].index(p),self.card_played_by,self.cards_this_round,self.suit_trumped_by,self.bet_deficits]
        elif strategy == 4: # Playing NN
            state = self.get_state(p, current_round)#self.action_state(p, current_round)
        elif strategy == 5: #playing genetic
            state = self.get_state(p, current_round)#self.action_state(p, current_round)
        else: # Don't need the state, e.g. random, greedy
            state = []
        return self.H[p].play(self.H[p].validToRealIndex( self.aiplayers[p].get_action(self.n, p, state, valid_cards) ));


    #To handle AI bets for player p
    def aiBet(self, p, strategy=1):
        return self.aiplayers[p].get_bet(self.H[p])
       

    def heuristicBet(self, p):
        bet = min(sum(self.H[p].ace_by_suit().values()) + sum(self.H[p].king_by_suit().values()) + round(self.H[p].trump_ct()/4), 13)
        return bet

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
            
            self.printVerbose('Player ' + str(p) + ' bet '  +str(self.bets[p]))


    # ----- PLAYING ROUNDS -----
    def initializeRound(self, n=13):
        # Make a new deck with n cards of each suit, and shuffle it.
        deck = Deck(n);
        deck.shuffle();

        # Deal n cards to each player
        self.H = [Hand(deck.deal(n)) for i in range(4)];
        # Make a separate list to save the initial hands
        self.initialHands = deepcopy(self.H);
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
        
        # Save the bets in the state
        self.state['bets'] = np.reshape(self.bets,(1,4));
        
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
                if self.player_strategy[p] == 0: # Ask for human input
                    self.h[t][p] = self.humanInput(p);
                else:                   # Ask for AI input with strategy in player_strategy[p]
                    #old: self.h[t][p] = self.aiInput(p, self.player_strategy[p], self.H[p].validCards(),card_played_by,cards_this_round,suit_trumped_by,bet_deficits,card_played_by,position+1);
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
                
                #update
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
            #print bet_deficits[self.T[t]];
            self.bet_deficits[self.T[t]] -= 1;

    def getFinalScores(self, bets, T):
        scores = [0,0,0,0];
        for p in range(4):
            tricks_p = sum(T[t] ==p for t in range(13))
            bet_p = bets[p]
            self.printVerbose(bets[p])
            chg_score = (2*(tricks_p>= bet_p)-1)*bet_p
            self.printVerbose('Player ' + str(p) + ' bet ' +str(bet_p) + ' and won ' +str(tricks_p) + ' for a total of ' + str(chg_score))
            scores[p]=chg_score
        return scores
    
    # Play the game. Call this method to run the game externally.
    def playGame(self):
        self.playRound()
        self.printVerbose(self.bets)
        return(self.getFinalScores(self.bets, self.T))
        
    def getTricks(self):
        return self.tricks
#        tricks = [-1,-1,-1,-1]
#        for p in range(4):
#            tricks_p = sum(self.T[t] ==p for t in range(13))
#            tricks[p] = tricks_p
#        return tricks