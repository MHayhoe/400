#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 15:44:48 2018

@author: Mikhail
"""

import input as ip

# Variables
num_rounds = 13;

# Whether each player is AI or not
ai_player = [False for i in range(4)];

# Make a new deck, and shuffle it.
deck = Deck();
deck.shuffle();

# Deal 13 cards to each player
H = [Hand(deck.deal(13)) for i in range(4)];
h = [[0 for i in range(4)] for t in range(num_rounds)]
T = [-1 for i in range(num_rounds)]

# ----- BETTING ROUND -----
# To be done

# ----- PLAYING ROUNDS -----

for t in range(0, num_rounds):
    # No lead suit yet
    Card.lead = -1;
    
    # Loop through players
    for p in range(4):
        if t > 0: # The previous winner should go first, then continue in order
            p = (p + T[t-1]) % 4;
        
        if ai_player[p] == True: # Ask for AI input
            h[t][p] = aiInput(p);
        else:                   # Ask for human input
            h[t][p] = humanInput(p);
        
        # Set the lead suit
        if Card.lead == -1:
            Card.lead = h[t][p].suit;
    
    # Find the winning player from the cards played this round
    T[t] = winner(h[t]);
    
# To handle human input for player p   
def humanInput(p):
    # Show them their hand
    print H[p]
    
    # Ask for input
    card_index = int(ip.input('Index of card to play: '))
    
    while lead != -1 and H[p].cards[card_index].suit != :
        
    return H[p].play(card_index)

# Finda the winning player from a trick
def winner(cards):
    return cards.index(max(cards))