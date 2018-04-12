#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:29:52 2018

@author: Mikhail
"""
from keras import backend as K

# Returns our custom loss function
def get_loss_bet():
    return loss_bet

# Our custom loss function: if we make our bet (y_true >= y_pred), the loss
# is the amount we could have gotten if we'd bet y_true, i.e., it's
# y_true - y_pred. If we didn't make our bet, then our loss is what we
# could have gotten minus what we lost, i.e., y_true + y_pred
# (since -1*(-bet) = bet)
def loss_bet(y_true, y_pred):
    #return K.square(y_true - y_pred)
    return K.square(y_true + K.sign(y_pred - y_true) * y_pred)