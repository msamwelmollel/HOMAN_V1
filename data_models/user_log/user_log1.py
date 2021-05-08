# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 18:56:18 2019

@author: 2427060M
"""
import numpy as np
import os
import sys
import random
from keras.utils import to_categorical
sys.path.append('C:/Users/2427060M/Dropbox/PHD - MANDELA/Paper to write/paper 3/mobile-data/mobile_data')
from data_models.base_data_model import BaseDataModel
from data_models.deep_q import DeepNeuralNetowk


EXPLORATION_TEST = 0.002



class DDQNDataModel(BaseDataModel):
    def __init__(self,input_shape,action_space,model_path):
        BaseDataModel.__init__(self,input_shape, action_space)
        self.model_path = model_path
        self.ddqn = DeepNeuralNetowk(self.input_shape, action_space).model
        if os.path.isfile(self.model_path):
            self.ddqn.load_weights(self.model_path)
            
    def _save_model(self):
        self.ddqn.save_weights(self.model_path)
        
        

class DDQNSolver(DDQNDataModel):

    def __init__(self,input_shape, action_space, intensity, min_SNR, delay_cost, user):
        testing_model_path = './data_models/models/model_save_intensity_'+str(intensity)+'_min_sinr_'+str(min_SNR)+'_delay_cost_'+str(delay_cost)+'_user_'+str(user)+'_.h5'
        if os.path.isfile(testing_model_path):
            DDQNDataModel.__init__(self, input_shape,action_space,testing_model_path)

        

    def move(self, state):
        state= (np.squeeze(state, axis=0))
        if np.random.rand() < EXPLORATION_TEST:
            return random.randrange(self.action_space)
        q_values = self.ddqn.predict(np.expand_dims(np.asarray(state).astype(np.float64), axis=0), batch_size=1)
        return np.argmax(q_values[0])
        

def print_data(SNR,user,intensity,position,state,delay_cost,action_space,INPUT_SHAPE,min_SNR,total_step):

    move_solver = DDQNSolver(INPUT_SHAPE, action_space, intensity,min_SNR,delay_cost,user)
    action= np.argmax(SNR[0,:])
    LOCATIONXY = 1000

    antennas = intensity
    a=[]
    current_state=np.reshape(np.append(SNR[0,:], to_categorical(action, num_classes=SNR.shape[1])),[1, INPUT_SHAPE])
    state=current_state
    for i in range(LOCATIONXY):
        if state[:, action] >= min_SNR:
            action = action
        elif ((state[:, action] < min_SNR) and (state[:, action]==np.max(state[:,0:action_space]))):
            action =  action
        else: 
            action = int(move_solver.move(state))
        
        
        state_next=np.reshape(np.append(SNR[i+1,:], to_categorical(action, num_classes=SNR.shape[1])),[1,INPUT_SHAPE])
#
        state = state_next
#
        SNR_print=SNR[i,0:int(antennas)].tolist()
        a.extend([action+1,position[i,0],position[i,1]])
        a.extend(SNR_print)

    a=np.reshape(a, (LOCATIONXY,(int(antennas)+3)))
          
    #a=np.reshape(a, (LOCATIONXY,(int(antennas)+3)))
    np.savetxt("./data_models/user_log/intensity_"+str(intensity)+"_user_"+str(user)+"_position_delay_"+str(delay_cost)+"_SNR_"+str(min_SNR)+".csv", a, delimiter=",",fmt='%10.5f',header= "")    
#    
    
