# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:15:52 2018

@author: Mikhail
"""
class Hand:
    # cards - list of Card objects, representing what's in the hand.
    
    # Constructor; set the cards by the given list of cards, empty by default.
    def __init__(self, list=[]):
        self.cards = list;
    
    # Remove a card from the hand, if it exists
    def removeCard(self,c):
        if c in self.cards:
            self.cards.remove(c);
          
    # Play a card in our hand, based on an index
    def play(self, i):
        # Finds the card at index i, removes it from the hand and returns it
        return self.cards.pop(i)
     
    # For sorting the cards in hand
    def sort(self):
        self.cards.sort();
        
    # Returns a list of valid cards to be played, based on the lead suit. When
    # no lead suit has been established, Card.lead = -1.
    def validCards(self):
        lst = [];
        
        for c in self.cards:
            if c.suit == Card.lead:
                lst.append(c)
                
        if len(lst) > 0: # We had some cards of the lead suit
            return lst
        else: # No cards of lead suit, so all are valid
            return self.cards;
    
    # ----- PRINTING METHODS -----
    # String representation
    def __str__(self):
        return Card.printList(self.cards)