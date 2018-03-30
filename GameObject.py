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
from heuristicAI import heuristicChoice

class Game:
    def __init__(self, num_rounds,strategy_vector, n=13):
        self.num_rounds = num_rounds;
        self.player_strategy=strategy_vector;
        self.n = n;
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
    player_strategy = [3,2,2,2];
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
    
    # To handle AI decisions for player p
    def aiInput(self, p, strategy,valid_cards, card_played_by,cards_this_round,suit_trumped_by,bet_deficits,cards_played_by):
        if strategy == 3: #simple heuristic
            valid_idx= heuristicChoice(p,valid_cards,card_played_by,cards_this_round,suit_trumped_by,bet_deficits,cards_played_by)
            return self.H[p].play( self.H[p].validToRealIndex(valid_idx) )
        if strategy == 2: # Myopic Greedy: pick the highest playable card every time
            # Sort the hand, so when we pick a valid card it will be the biggest valid card
            self.H[p].sort()
            return self.H[p].play( self.H[p].validToRealIndex(0) );
        else: # Random choice
            # Pick a valid card at random
            ind = rnd.randint( 0, len(self.H[p].validCards()) - 1 )
            return self.H[p].play( self.H[p].validToRealIndex(ind) )
        
    #To handle AI bets for player p
    def aiBet(self, p, strategy=1):
        if strategy==3: # Simple heuristic
            bet = rnd.randint(2,5)
            return bet
        if strategy==2: # Myopic greedy
            bet = rnd.randint(2,5)
            return bet
        if strategy==1: # Random strategy
            bet = rnd.randint(2,5)
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
        self.h = [[0 for i in range(4)] for t in range(self.num_rounds)]
        self.T = [-1 for i in range(self.num_rounds)]
        
        # Initialize the bets to zero
        self.bets = [0 for i in range(4)];

    def playRound(self,n=13):
        # Initialize the round
        self.initializeRound(n);
        
        # Get the bets
        self.bettingRound();
        self.initialbets = self.bets;
        
        # Initialize some state-dependent metrics to pass to AI
        card_played_by = {card.__str__():None for card in Deck().cards}
        suit_trumped_by = {i:set() for i in range(4)}
        bet_deficits = list(self.bets)
        
        # Go through the rounds
        for t in range(0, self.num_rounds):
            # No lead suit yet
            Card.lead = -1;
            cards_this_round = {i: None for i in range(4)}
            # Loop through players
            for p in range(4):
                if t > 0: # The previous winner should go first, then continue in order
                    p = (p + self.T[t-1]) % 4;

                if self.player_strategy[p] == 0: # Ask for human input
                    self.h[t][p] = self.humanInput(p);
                else:                   # Ask for AI input with strategy in player_strategy[p]
                    self.h[t][p] = self.aiInput(p, self.player_strategy[p], self.H[p].validCards(),card_played_by,cards_this_round,suit_trumped_by,bet_deficits,card_played_by);

                # Set the lead suit, if it hasn't been yet
                if Card.lead == -1:
                    Card.lead = self.h[t][p].suit;

                # Display what was played
                self.printVerbose(str(p + 1) + ':  ' + str(self.h[t][p]))
                self.printVerbose('')
                
                #update
                cards_this_round[p] = self.h[t][p]
                #update the card_played_by dict
                card_played_by[str(self.h[t][p])]=p
                if Card.lead in [1,2,4]:
                    if self.h[t][p].suit == 3:
                        suit_trumped_by[Card.lead].add(p)

            # Find the winning player from the cards played this round
            self.T[t] = self.winner(self.h[t]);
            self.printVerbose('Player ' + str(self.T[t] + 1) + ' won the trick.')
            bet_deficits[ self.T[t] ] -= 1;

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