from GameObject import Game
import numpy as np

num_tests = 1000

# Let's test heuristic vs random
total_team1 = 0
total_team2 = 0
wins_team1 = 0.0
wins_team2 = 0.0
ties = 0.0

# Strategies that each player should use to play
strategies = [2,2,2,2]

# For saving the game state after each game
Hands = []
History = []
Bets = []
Scores = []
Tricks = []

# Play the game for num_tests rounds
for i in range(num_tests):
    # Count 10,000's of rounds
    if i % 10000 == 1:
        print(i)
        
    game = Game(13, strategies)
    scores = game.playGame()
    
    score_team1 = scores[0] + scores[2]
    score_team2 = scores[1] + scores[3]
    
    total_team1 += score_team1
    total_team2 += score_team2
    
    if score_team2 < score_team1:
        wins_team1 += 1
    elif score_team2 > score_team1:
        wins_team2 += 1
    else:
        ties += 1
    
    # Count the number of tricks each player won
    tricks = [sum(game.T[t] == p for t in range(13)) for p in range(4)]

    Hands.append(game.initialHands)
    History.append(game.h)
    Bets.append(game.bets)
    Scores.append(scores)
    Tricks.append(tricks)

