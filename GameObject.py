#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 15:44:48 2018

@author: Mikhail
"""
import random as rnd
from copy import deepcopy

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
    def __init__(self, num_rounds, strategy_vector, bet_vector, n=13, action_model_objects=[None, None, None, None], bet_model_objects = [None, None, None, None]):
        # type: (object, object, object) -> object
        self.num_rounds = num_rounds;
        self.player_strategy = strategy_vector;
        self.bet_strategy = bet_vector;
        self.n = n;
        #self.bet_models = betting_model_objects
        #self.action_models = 
        self.aiplayers = [AIPlayer(self.player_strategy[i], self.bet_strategy[i], 'sorted', bet_model_objects[i], action_model_objects[i]) for i in range(4)]

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

    # Deal 13 cards to each player
    # H = [Hand(deck.deal(13)) for i in range(4)];
    # initialHands = deepcopy(H);
    # h = [[0 for i in range(4)] for t in range(num_rounds)]
    # T = [-1 for i in range(num_rounds)]
    # bets = [0 for i in range(4)]

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
    def action_state(self, p, t):
        state = [0 for i in range(self.n*4)]
        for c in self.h[t]:
            if c is not None:
                state[(c.value - 1) + self.n*c.suit - 1] = self.card_played_by[str(c)] + 1
        
        permute_bets = self.bets[p:] + self.bets[:p]
        permute_tricks = self.tricks[p:] + self.tricks[:p]
        [state.append(b) for b in permute_bets]
        [state.append(b) for b in permute_tricks]
        
        return state
    
    # To handle AI decisions for player p
    def aiInput(self, p, current_round, strategy, valid_cards):
        if strategy == 3: # Simple heuristic
            state = [self.card_played_by,self.cards_this_round,self.suit_trumped_by,self.bet_deficits]
        elif strategy == 4: # Playing NN
            state = self.action_state(p, current_round)
        else: # Don't need the state, e.g. random, greedy
            state = []
            
        return self.H[p].play(self.H[p].validToRealIndex( self.aiplayers[p].get_action(self.n, p, state, valid_cards) ));

        
    #To handle AI bets for player p
    def aiBet(self, p, strategy=1):
        #print 'ai ' + str(p) +  ' is goign to bet ' +  str(self.aiplayers[p].get_bet(self.H[p]))
        return self.aiplayers[p].get_bet(self.H[p])
        # if strategy==3: # Simple heuristic
        #     bet = self.heuristicBet(p)
        #     return bet
        # if strategy==2: # Myopic greedy
        #     #bet = rnd.randint(2,5)
        #     bet = players[p].get_bet(H[p])
        #     return bet
        # if strategy==1: # Random strategy
        #     bet = rnd.randint(2,5)
        #     return bet
    #Betting Method 1
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
        # Make a separate object to save the initial hands
        self.initialHands = deepcopy(self.H);
        self.h = [[None for i in range(4)] for t in range(self.num_rounds)]
        self.T = [-1 for i in range(self.num_rounds)]
        self.tricks = [0 for i in range(4)]
        
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
            
            order = range(4);
            
            # Permute player order
            if t > 0: # The previous winner should go first, then continue in order
                order = order[self.T[t-1]:] + order[:self.T[t-1]]
            else:   # Randomly choose who goes first
                first_player = rnd.randint(0,3);
                order = order[first_player:] + order[:first_player]
            
            # Loop through players
            for p in order:
                if self.player_strategy[p] == 0: # Ask for human input
                    self.h[t][p] = self.humanInput(p);
                else:                   # Ask for AI input with strategy in player_strategy[p]
                    self.h[t][p] = self.aiInput(p, t, self.player_strategy[p], self.H[p].validCards());

                # Set the lead suit, if it hasn't been yet
                if Card.lead == -1:
                    Card.lead = self.h[t][p].suit;

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
    def playGame(self):
        self.playRound()
        self.printVerbose(self.bets)
        return(self.getFinalScores(self.bets, self.T))
    def getTricks(self):
        tricks = [-1,-1,-1,-1]
        for p in range(4):
            tricks_p = sum(self.T[t] ==p for t in range(13))
            tricks[p] = tricks_p
        return tricks