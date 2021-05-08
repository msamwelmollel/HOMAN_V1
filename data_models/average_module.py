# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 17:55:45 2019

@author: 2427060M
"""

import numpy as np
import pandas as pd
import os
import sys

if os.path.exists('C:/Users/msamw/Dropbox/PHD - MANDELA/Paper to write/paper4/conference/conference'): 
    sys.path.append('C:/Users/msamw/Dropbox/PHD - MANDELA/Paper to write/paper4/conference/conference') # new pc
    my_path= 'C:\\Users\\msamw\\Dropbox'
else:
    sys.path.append('C:/Users/2427060M/Dropbox/PHD - MANDELA/Paper to write/paper4/conference/conference') # desktop
    my_path= 'C:\\Users\\2427060M\\Dropbox'


def average_data(j, intensity, delay_cost):
    SNR1 = [i+1 for i in range(1,30)]
    if j < 52:
        return
    intensity = [intensity]
    active_snr = []
    for intensity in intensity:
        inte_array = []
        
        for SNR in SNR1:
            y = []
            active_user= 0
            for user in range(1,12):
                path = "PHD - MANDELA\\Paper to write\\Paper 3\\mobile-data\\mobile_data\\data_models\\user_log\\handover_report_intensity_"+str(intensity)+"_user_"+str(user)+"_delay_cost_"+str(delay_cost)+".csv"
                path = os.path.join(my_path, path)
                if os.path.exists(path):
                    df = pd.read_csv(path,sep=',',header=None)
                    #print(df)
                    df.columns = ['a','b','c','d','e','f','g','h'] 
                    #print(df[1:2])
                    if df.empty != True:
                        data = df.loc[(df['b']==SNR) & (df['a']==intensity)]
                        if data.empty != True:
                            y =list(np.append(y, data))
                            active_snr.append(SNR)
                            active_user = active_user+1

            if not (y):
                continue
            else:
                y = np.reshape(np.asarray(y),(active_user,8))
                y = np.mean(y,axis=0)
                y = (np.reshape(y,(1,8)))
                y[:,2], y[:,5] = int(y[:,2]), int(y[:,5])
                inte_array = np.append(inte_array,y)
        row_len = (len(list(set(active_snr))))
        inte_array = np.reshape(np.asarray(inte_array),(row_len,8))
        np.savetxt("C:\\Users\\2427060M\\Dropbox\\PHD - MANDELA\\Paper to write\\Paper 3\\mobile-data\\mobile_data\\data_models\\user_log\\average_handover_report_intensity_"+str(intensity)+"_delay_cost_"+str(delay_cost)+".csv", inte_array, delimiter=",",fmt='%10.5f',header= "")
        
        
#if __name__ == "__main__":
#    average_data(10,2)
a = [0.75, 1, 2, 3]
inten = [10, 48]
for i in a:
    for inte in inten: 
        average_data(63, inte, i)