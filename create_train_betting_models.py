import create_bet_data
import import_bet_data
import all_bet_nn

num_batches = 50
batch_size = 1000
for strategy_var in [ 'Greedy_v_Heuristic', 'Greedy_v_Greedy', 'Heuristic_v_Heuristic', 'Heuristic_v_Greedy']:
    for org_var in ['matrix']:
    #for org_var in ['sorted', 'binary']:

        #create_bet_data.create_bet_data(num_batches, batch_size, strategy_var, org_var)
        #import_bet_data.split_bet_data(strategy_var, org_var)
        all_bet_nn.train_bet_model(strategy_var,org_var,128,100)


