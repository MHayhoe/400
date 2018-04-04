# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 09:49:50 2018

@author: Victor
"""

import csv
import numpy as np

xdata = []
ydata = []

typeString = 'sorted'

with open('Data/greedy_v_greedy_bet_data_' + typeString + '.csv','r') as file:
    rdr = csv.reader(file, delimiter =',')
    for row in rdr:
        xdata.append([float(i) for i in row[0:-1]])
        ydata.append(float(row[-1]))

test_lim = int(np.round(len(xdata)*0.8))
np.save('Data/Greedy_v_Greedy_bet_' + typeString + '_x_train.npy',xdata[0:test_lim])
np.save('Data/Greedy_v_Greedy_bet_' + typeString + '_y_train.npy',ydata[0:test_lim])
np.save('Data/Greedy_v_Greedy_bet_' + typeString + '_x_test.npy',xdata[test_lim:-1])
np.save('Data/Greedy_v_Greedy_bet_' + typeString + '_y_test.npy',ydata[test_lim:-1])


with open('Data/heuristic_v_heuristic_bet_data_' + typeString + '.csv','r') as file:
    rdr = csv.reader(file, delimiter =',')
    for row in rdr:
        xdata.append([float(i) for i in row[0:-1]])
        ydata.append(float(row[-1]))

np.save('Data/Heuristic_v_Heuristic_bet_data_' + typeString + '_x_train.npy',xdata[0:test_lim])
np.save('Data/Heuristic_v_Heuristic_bet_data_' + typeString + '_y_train.npy',ydata[0:test_lim])
np.save('Data/Heuristic_v_Heuristic_bet_data_' + typeString + '_x_test.npy',xdata[test_lim:-1])
np.save('Data/Heuristic_v_Heuristic_bet_data_' + typeString + '_y_test.npy',ydata[test_lim:-1])
