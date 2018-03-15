# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:45:12 2018

@author: Mikhail
"""
import Card
import random as rnd

class Deck:
    # Constructor; make all possible cards in the deck.
    def __init__(self):
        self.cards = [];
        
        # Add all cards to the deck
        for s in range(1,5):
            for v in range(1,14):
                self.cards.append(Card(v, s))
    
    # Shuffles the deck          
    def shuffle(self):
        rnd.shuffle(self.cards);
    
    # Deal n cards, default 1.
    def deal(self, n=1):
        dealt = self.cards[0:n];
        del self.cards[0:n]
        return dealt;
    
    
    # ----- PRINTING METHODS -----
    # String representation
    def __str__(self):
        return Card.printList(self.cards)