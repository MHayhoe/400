# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:15:52 2018

@author: Mikhail
"""
import Card

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
        return self.cards.pop(i)
     
    # For sorting the cards in hand
    def sort(self):
        self.cards.sort();
    
    
    # ----- PRINTING METHODS -----
    # String representation
    def __str__(self):
        return Card.printList(self.cards)