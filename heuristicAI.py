# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 00:13 2018

@author: Hadi
"""
from Hand import Hand
from Deck import Deck
from Card import Card

import random as rnd
def heuristicChoice(p,valid_cards, card_played_by,cards_this_round,suit_trumped_by,bet_deficits,cards_played_by):
    #determine position of player
    pos = determine_position(p,cards_this_round)
    #get partner player index
    partner = (p+2)%4
    leadsuit = valid_cards[0].lead
    trumpsuit = valid_cards[0].trump
    #split valid cards into lead suit, trump cards, and throwaways
    lead_cards = [card for card in valid_cards if card.suit==leadsuit]
    trump_cards = [card for card in valid_cards if card.suit==trumpsuit]
    throwaway_cards = [card for card in valid_cards if card.suit != Card.lead and card.suit != Card.trump]
    cur_max = current_max_card(cards_this_round)
    current_winner = currently_winning_player(cur_max, cards_this_round)
    chosen_card = choose_card(p,pos,cur_max, valid_cards, current_winner, lead_cards,trump_cards, throwaway_cards,partner,bet_deficits,suit_trumped_by,cards_played_by)
    if chosen_card is None:
        print 'warning: chosen card was none'
        return rnd.randint(0,len(valid_cards)-1)
    print chosen_card
    print [str(card) for card in valid_cards]
    chosen_card_valid_idx = None
    for i in range(0,len(valid_cards)-1):
        if chosen_card==valid_cards[i]:
            chosen_card_valid_idx=i
    print chosen_card_valid_idx
    if chosen_card_valid_idx is None:
        print 'warning: chosen card index was none'
        print chosen_card_valid_idx
        print chosen_card
        print valid_cards
        return rnd.randint(0,len(valid_cards)-1)

    return chosen_card_valid_idx
def current_max_card(cards_this_round):
    non_null_cards = [card for card in cards_this_round.values() if card is not None]
    if len(non_null_cards)>0:
        return max(non_null_cards)
    else:
        return None
def currently_winning_player(cur_max, cards_this_round):

    for i in range(4):
        if cards_this_round[i]==cur_max:
            return i
    else:
        return None
def choose_card(p,pos,cur_max,valid_cards,winner, suitc,trumpc, throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by):
    if pos ==1:
        choice = move_first(p,cur_max, valid_cards,winner,suitc,trumpc, throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by)
    if pos ==2:
        choice = move_second(p,cur_max,valid_cards,winner,suitc,trumpc, throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by)
    if pos == 3:
        choice = move_third(p,cur_max, valid_cards,winner,suitc, trumpc, throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by)
    else:
        choice = move_fourth(p,cur_max,valid_cards,winner, suitc,trumpc, throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by)
    return choice
def move_first(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by):
    #choice = choose_random(valid_cards)
    choice = move_not_last(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by)
    return choice

def move_second(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by):
    #choice = choose_random
    choice = move_not_last(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by)
    return choice
def move_third(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by):
    #choice = choose_random(valid_cards)
    choice = move_not_last(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by)
    return choice
def move_fourth(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by):
    choice = move_last(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by)
    return choice
def move_not_last(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by):
    #find smallest card that wins, if it exists
    winnable = min_winnable(cur_max, suitc, trumpc)
    losable = min_throwable(suitc, throwc, trumpc)
    if winnable is not None:
        winnable_safe = determine_safe(cards_played_by,winnable,prtner_idx,suit_trumped_by)
    else:
        winnable_safe = 'N/A'
    #if partner is not winning, try to win if possible, or throw lowest card
    if winner!=prtner_idx:
        if winnable is not None:
            print 'winnable: ' + str(winnable)
            print 'safe?: ' + str(winnable_safe)
            if winnable_safe == True:
                return winnable
            else:
                return losable
        else:
            print 'Winnable: ' + str(winnable)
            print 'losable: ' + str(losable)
            return losable
    #if partner is winning, try to win if partners deficit is less than own
    else:
        if bet_deficits[prtner_idx]<bet_deficits[p] and winnable is not None:
            print 'take from partner - sorry! :' + str(winnable)
            return winnable
        else:
            print 'give to partner : ' + str(losable)
            return losable
def move_last(p,cur_max,valid_cards,winner, suitc,trumpc,throwc,prtner_idx,bet_deficits,suit_trumped_by,cards_played_by):
    #find smallest card that wins, if it exists
    winnable = min_winnable(cur_max, suitc, trumpc)
    losable = min_throwable(suitc, throwc, trumpc)
    #if partner is not winning, try to win if possible, or throw lowest card
    if winner!=prtner_idx:
        if winnable is not None:
            print 'winnable: ' + str(winnable)
            print 'safe?: ' + 'moving last - always safe'
            return winnable
        else:
            print 'Winnable: ' + str(winnable)
            print 'losable: ' + str(losable)
            return losable
    #if partner is winning, try to win if partners deficit is less than own
    else:
        if bet_deficits[prtner_idx]<bet_deficits[p] and winnable is not None:
            print 'take from partner - sorry! :' + str(winnable)
            return winnable
        else:
            print 'give to partner : ' + str(losable)
            return losable
def determine_position(p,cards_this_round):
    return 4-sum([cards_this_round[i]==None for i in range(4)])
def max_lead_suit(valid_cards):
    return max([card for card in valid_cards if card.suit==card.lead ])
def min_lead_suit(valid_cards):
    return min([card for card in valid_cards if card.suit==card.lead ])
def min_lead_suit_gt_card(valid_cards,other_card):
    winning_cards = [card for card in valid_cards if card.suit==card.lead and card > other_card ]
    if len(winning_cards)>0:
        return min(winning_cards)
    else:
        return None
def min_throwable(suitc,throwc,trumpc):
    if len(suitc)>0:
        return min(suitc)
    if len(throwc)>0:
        return min(throwc)
    else:
        return min(trumpc)
def min_winnable(max_card,suitc,trumpc):
    if len(suitc)>0:
        return min(suitc)
    if len(trumpc)>0:
            return min(trumpc)
    else:
        return None
def suit_broken(cards_played,suit):
    for card in Deck().cards:
        if card.suit==suit:
            if cards_played[str(card)] is not None:
                return True
    return False
def choose_random(valid_cards):
    return valid_cards[rnd.randint(0,len(valid_cards)-1)]
def determine_safe(cards_played,card_considered,partner,suit_trumped_by):
    higher_cards = card_considered.get_higher_cards()
    trumpers = suit_trumped_by[card_considered.suit]
    #check if suit broken by opponents
    if len(trumpers.symmetric_difference([partner]))>0:
        return False
    #if not broken, check whether higher cards of the same suit have not yet been played
    else:
        higher_of_suit = [card for card in higher_cards if card.suit==card_considered.suit and cards_played[str(card)] is None]
        if len(higher_of_suit)>0:
            return False
    return True
