#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 15:44:48 2018

@author: Mikhail
"""
from Hand import Hand
from Deck import Deck
from Card import Card
from heuristicAI import heuristicChoice
class Game:
    def __init__(self, num_rounds,strategy_vector):
        self.num_rounds = num_rounds;
        self.player_strategy=strategy_vector;

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
    H = [Hand(deck.deal(13)) for i in range(4)];
    h = [[0 for i in range(4)] for t in range(num_rounds)]
    T = [-1 for i in range(num_rounds)]
    bets = [0 for i in range(4)]

    # ----- METHODS -----
    # For verifying human input
    def isInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    # To handle human input for player p
    def humanInput(p):
        # Show them their hand
        H[p].sort()
        print 'Player ' + str(p + 1) + '\'s Hand: ' + str(H[p])
        # Save and display the list of valid cards
        valid_cards = H[p].validCards();
        print 'VALID cards: ' + Card.printListIndices( valid_cards ),

        # Ask for input
        card_index = input('Pick index of VALID card to play: ')

        # Check if the chosen index was valid
        while not( isInt(card_index) ) or card_index < 0 or card_index >= len(valid_cards):
           # Ask for input
           card_index = input('Invalid. Pick again (from VALID): ')

        return H[p].play( H[p].validToRealIndex( int(card_index) ) )
    # To handle human bet for player p
    def humanBet(p):
        # Show them their hand
        H[p].sort()
        print 'Player ' + str(p + 1) + '\'s Hand: ' + str(H[p])
        bet = input('Bet tricks to take:')
        while not(bet>1):
            #ask for new bet
            bet = input('The minimum bet is 2.')
        return bet
    # To handle AI decisions for player p
    def aiInput(p, strategy,valid_cards, card_played_by,cards_this_round,suit_trumped_by,bet_deficits,cards_played_by):
        if strategy == 3: #simple heuristic
            valid_idx= heuristicChoice(p,valid_cards,card_played_by,cards_this_round,suit_trumped_by,bet_deficits,cards_played_by)
            return H[p].play(H[p].validToRealIndex(valid_idx))
        if strategy == 2: # Myopic Greedy: pick the highest playable card every time
            # Sort the hand, so when we pick a valid card it will be the biggest valid card
            H[p].sort()
            return H[p].play( H[p].validToRealIndex(0) );
        else: # Random choice
            # Pick a valid card at random
            ind = rnd.randint( 0, len(H[p].validCards()) - 1 )
            return H[p].play( H[p].validToRealIndex(ind) )
    #To handle AI bets for player p
    def aiBet(p, strategy=1):
        if strategy==3:
            bet = rnd.randint(2,5)
            return bet
        if strategy==2:
            bet = rnd.randint(2,5)
            return bet
        if strategy==1:#random player
            bet = rnd.randint(2,5)
            return bet

    # Find the winning player from a trick
    def winner(cards):
        srtd = sorted(cards,reverse=True)
        return cards.index(srtd[0])


    # ----- BETTING ROUND -----
    # To be done
    def bettingRound():
        for p in range(4):
            if player_strategy[p] ==0: #ask for human bet
                bets[p] = humanBet(p)
            else:
                bets[p] = aiBet(p,player_strategy[p])
            print 'Player ' + str(p) + ' bet '  +str(bets[p])


    # ----- PLAYING ROUNDS -----
    def initializeRound(n=13):
        # Make a new deck with n cards of each suit, and shuffle it.
        deck = Deck(n);
        deck.shuffle();

        # Deal 13 cards to each player
        H = [Hand(deck.deal(n)) for i in range(4)];
        h = [[0 for i in range(4)] for t in range(num_rounds)]
        T = [-1 for i in range(num_rounds)]

    def playRound(self,n=13):
        self.initializeRound(n);
        self.bettingRound()
        initialbets = bets
        card_played_by = {card.__str__():None for card in Deck().cards}
        suit_trumped_by = {i:set() for i in range(4)}
        bet_deficits = list(bets)
        for t in range(0, num_rounds):
            # No lead suit yet
            Card.lead = -1;
            cards_this_round = {i: None for i in range(4)}
            # Loop through players
            for p in range(4):
                if t > 0: # The previous winner should go first, then continue in order
                    p = (p + T[t-1]) % 4;

                if player_strategy[p] == 0: # Ask for human input
                    h[t][p] = self.humanInput(p);
                else:                   # Ask for AI input with strategy in player_strategy[p]
                    h[t][p] = self.aiInput(p, player_strategy[p],H[p].validCards(),card_played_by,cards_this_round,suit_trumped_by,bet_deficits,card_played_by);

                # Set the lead suit, if it hasn't been yet
                if Card.lead == -1:
                    Card.lead = h[t][p].suit;

                # Display what was played
                print str(p + 1) + ':  ' + str(h[t][p])
                print ''
                #update
                cards_this_round[p] = h[t][p]
                #update the card_played_by dict
                card_played_by[str(h[t][p])]=p
                if Card.lead in [1,2,4]:
                    if h[t][p].suit == 3:
                        suit_trumped_by[Card.lead].add(p)

            # Find the winning player from the cards played this round
            T[t] = winner(h[t]);
            print 'Player ' + str(T[t] + 1) + ' won the trick.'
            bet_deficits[T[t]] -= 1

    def getFinalScores(bets,T):
        scores = [0,0,0,0];
        for p in range(4):
            tricks_p = sum(T[t] ==p for t in range(13))
            bet_p = bets[p]
            print bets[p]
            chg_score = (2*(tricks_p>= bet_p)-1)*bet_p
            print 'Player ' + str(p) + ' bet ' +str(bet_p) + ' and won ' +str(tricks_p) + ' for a total of ' + str(chg_score)
            scores[p]=chg_score
        return scores
    def playGame(self):
        self.playRound()
        print(bets)
        return(getFinalScores(bets,T))
