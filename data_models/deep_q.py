# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 13:43:21 2019

@author: 2427060M
"""

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
#from keras.utils import to_categorical

class DeepNeuralNetowk:
    
    def __init__(self, observation_space, action_space):
        self.model = Sequential()
        self.model.add(Dense(128, input_shape = (observation_space, ), activation = "relu"))
        self.model.add(Dense(64, activation = "relu"))
        self.model.add(Dense(128, activation = "relu" ))
        self.model.add(Dense(64, activation = "relu"))
        self.model.add(Dense(action_space, activation = "linear"))
        self.model.compile(loss = "mse", optimizer = Adam(lr = 0.001))
        self.model.summary()
        
        
        
        
        
        
        
        
        