#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:46:41 2018

@author: Mikhail
"""
from GameObject import Game

# Number of full games to play
num_games = 100
wins_team1 = 0
wins_team2 = 0

for g in range(num_games):
    Total_Scores = [0 for p in range(4)]
    
    while True:
        game = Game(n, strategies, bet_strategies, n, [action_model for i in range(4)], [bet_model for i in range(4)])
        scores = game.playGame()
    
        for p in range(4):
            Total_Scores[p] += scores[p]
                        
        if (Total_Scores[0] >= 41 and Total_Scores[2] >= 0) or (Total_Scores[0] >= 0 and Total_Scores[2] >= 41):
               wins_team1 += 1
               print 'Team 1 won'
               break
        if (Total_Scores[1] >= 41 and Total_Scores[3] >= 0) or (Total_Scores[1] >= 0 and Total_Scores[3] >= 41):
               wins_team2 += 1
               print 'Team 2 won'
               break
           
    print Total_Scores
