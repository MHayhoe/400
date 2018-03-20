#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 15:44:48 2018

@author: Mikhail
"""
import random as rnd
from Deck import Deck
# Variables
num_rounds = 13;

# Strategy for each player:
# 0:    human
# 1:    random - play a valid card at random
# 2:    highest - play the highest valid card
player_strategy = [0, 2, 1, 1];

# Make a new deck, and shuffle it.
deck = Deck();
deck.shuffle();

# Deal 13 cards to each player
H = [Hand(deck.deal(13)) for i in range(4)];
h = [[0 for i in range(4)] for t in range(num_rounds)]
T = [-1 for i in range(num_rounds)]


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

# To handle AI decisions for player p
def aiInput(p, strategy=1):
    if strategy == 2: # Heuristic: pick the highest playable card every time
        # Sort the hand, so when we pick a valid card it will be the biggest valid card
        H[p].sort()
        return H[p].play( H[p].validToRealIndex(0) );
    else: # Random choice
        # Pick a valid card at random
        ind = rnd.randint( 0, len(H[p].validCards()) - 1 )
        return H[p].play( H[p].validToRealIndex(ind) )

# Find the winning player from a trick
def winner(cards):
    srtd = sorted(cards,reverse=True)
    return cards.index(srtd[0])


# ----- BETTING ROUND -----
# To be done

# ----- PLAYING ROUNDS -----
def initializeRound(n=13):
    # Make a new deck with n cards of each suit, and shuffle it.
    deck = Deck(n);
    deck.shuffle();
    
    # Deal 13 cards to each player
    H = [Hand(deck.deal(13)) for i in range(4)];
    h = [[0 for i in range(4)] for t in range(num_rounds)]
    T = [-1 for i in range(num_rounds)]

def playRound(n=13):
    initializeRound(n);
    
    for t in range(0, num_rounds):
        # No lead suit yet
        Card.lead = -1;
        
        # Loop through players
        for p in range(4):
            if t > 0: # The previous winner should go first, then continue in order
                p = (p + T[t-1]) % 4;
            
            if player_strategy[p] == 0: # Ask for human input
                h[t][p] = humanInput(p);
            else:                   # Ask for AI input with strategy in player_strategy[p]
                h[t][p] = aiInput(p, player_strategy[p]);
            
            # Set the lead suit, if it hasn't been yet
            if Card.lead == -1:
                Card.lead = h[t][p].suit;
                
            # Display what was played
            print str(p + 1) + ':  ' + str(h[t][p])
            print ''
        
        # Find the winning player from the cards played this round
        T[t] = winner(h[t]);
        print 'Player ' + str(T[t] + 1) + ' won the trick.'
        
    
    