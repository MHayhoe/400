# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:15:52 2018

@author: Mikhail
"""
from Card import Card
class Hand:
    # cards - list of Card objects, representing what's in the hand.
    
    # Constructor; set the cards by the given list of cards, empty by default.
    def __init__(self, list=[]):
        self.cards = list;
    
    # Remove a card from the hand, if it exists
    def removeCard(self,c):
        if c in self.cards:
            self.cards.remove(c);
          
    # Play a card in our hand, based on an index i
    def play(self, i):
        # Finds the card at index i, removes it from the hand and returns it
        return self.cards.pop(i)
    
    # Takes index i of card in valid list, and returns index in cards
    def validToRealIndex(self, i):
        c = self.validCards()[i];
        return self.cards.index(c);
     
    # For sorting the cards in hand
    def sort(self):
        self.cards.sort(reverse=True);
        
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
    def print_sorted(self):
        sorted_list = []
        for i in range(4):
            suit_cards = []
            for c in range(len(self.cards)):
                if self.cards[c].suit==i:
                    suit_cards.append(self.cards[c])
            suit_cards.sort(reverse=True)
            sorted_list = sorted_list + suit_cards
        return Card.printList(sorted_list)
    #------ COUNTING METHODS -----
    def suit_count(self):
        suit_ct = {i: 0 for i in range(4)}
        for c in self.cards:
            suit_ct[c.suit] +=1
        return suit_ct
    def ace_by_suit(self):
        ace_ct = {i: 0 for i in range(4)}
        for card in self.cards:
            if card.value==14:
                ace_ct[card.suit] +=1
        return ace_ct
    def king_by_suit(self):
        king_ct = {i: 0 for i in range(4)}
        for card in self.cards:
            if card.value==13:
                king_ct[card.suit] +=1
        return king_ct
    def card_ct(self,card_val):
        val_ct = {i: 0 for i in range(4)}
        for card in self.cards:
            if card.value==card_val:
                val_ct[card.suit] +=1
        return val_ct
    def trump_ct(self):
        return sum( card.trump==card.suit for card in self.cards)
    def get_suit(self,suit):
        return [card for card in self.cards if card.suit==suit]
    def max_suit(self,suit):
        return max(self.get_suit(suit))
