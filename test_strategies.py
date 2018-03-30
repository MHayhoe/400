from GameObject import Game
num_tests = 100

#let's test heurstic vs random
total_score_rando = 0
total_score_heuristic = 0
wins_heuristic = 0
wins_rando = 0
ties = 0

for i in range(num_tests):
    game = Game(13, [3,2,3,2])
    scores = game.playGame()
    rando_score = scores[1]+scores[3]
    heuristic_score = scores[0]+scores[2]
    
    total_score_rando += rando_score
    total_score_heuristic += heuristic_score
    
    if rando_score < heuristic_score:
        wins_heuristic += 1
    if rando_score < heuristic_score:
        wins_rando += 1
    if rando_score == heuristic_score:
        ties +=1
