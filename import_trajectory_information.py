# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:41:02 2019

@author: 2427060M
"""

import pandas as pd
import numpy as np

def process_sinr(intensity,antennas, user):
    SNR=[]
    antenna = [i+1 for i in range(antennas)]

    for ant in antenna:
        path = path = "C:\\Users\\2427060M\\Dropbox\\PHD - MANDELA\\Paper to write\\paper 3\\data\\antenna\\"+str(intensity)+"lambda\\Antenna_"+str(ant)+"_User_"+str(user)+".csv"
        df =pd.read_csv(path,delim_whitespace=True, header=None)
        sn=df[[9]].values.tolist()
        SNR.extend(sn)
        
    position=df[[1,2]]
    position = np.reshape(position.values.tolist(),(position.shape[0],2))
    SNR=np.reshape(SNR,(len(antenna),position.shape[0])).T
    max_snr = (np.amax(np.asarray(SNR)))
    SNR2 = np.absolute(SNR - max_snr)
    return SNR, SNR2, position


