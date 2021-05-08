# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 18:56:18 2019

@author: 2427060M
"""
import numpy as np
from keras.utils import to_categorical

#def print_data(SNR,min_SNR,move,observation_space,action_space,intensity,position,user):
def print_data(SNR,user,move,intensity,position,state,delay_cost,action_space,INPUT_SHAPE,min_SNR,total_step):

#    delay_cost = 2
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
            action = int(move(state))
        
        
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
    
