# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 09:49:50 2018

@author: Victor
"""

import csv
import numpy as np
def split_bet_data(strategy_var, organization_var):
    xdata = []
    ydata = []
    typeString = organization_var
    #typeString = 'sorted'
    #typeString = 'binary'
    #typeString = 'standard'
    #typeString = 'interleave'
    #typeString = 'interleave_sorted'
    strategyString = strategy_var
    #strategyString = 'Heuristic_v_Greedy'
    #strategyString = 'Heuristic_v_Heuristic'
    #strategyString = 'Greedy_v_Greedy'
    #strategyString = 'Greedy_v_Heuristic'
    modelString = strategyString + '_bet_data_' + typeString
    nameString = './Data/' + strategyString + '_bet_data_' + typeString
    with open(nameString + '.csv','r') as file:
        rdr = csv.reader(file, delimiter =',')
        for row in rdr:
            x_obs = [float(i) for i in row[0:-1]]
            if organization_var=='matrix':
                x_obs = np.reshape(x_obs, (4, 13, 1))
            xdata.append(x_obs)
            ydata.append(float(row[-1]))

    test_lim = int(np.round(len(xdata)*0.8))
    np.save(nameString + '_x_train.npy',xdata[0:test_lim])
    np.save(nameString + '_y_train.npy',ydata[0:test_lim])
    np.save(nameString + '_x_test.npy',xdata[test_lim:-1])
    np.save(nameString + '_y_test.npy',ydata[test_lim:-1])

