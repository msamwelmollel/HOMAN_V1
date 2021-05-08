# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:28:02 2019

@author: 2427060M
"""
import numpy as np
import pandas as pd
from statistics import mean
import os
#%%
#(model_run,delay_cost,intensity,antennas,user)
def handover_performance(SNR,delay_cost,intensity,user):
    snr_rl = 0
    snr_n = 0
    k=0
    for snr in range(SNR,SNR+1):
        path = "C:\\Users\\2427060M\\Dropbox\\PHD - MANDELA\\Paper to write\\Paper 3\\mobile-data\\mobile_data\\data_models\\user_log\\intensity_"+str(intensity)+"_user_"+str(user)+"_position_delay_"+str(delay_cost)+"_SNR_"+str(SNR)+".csv"
        #df =pd.read_csv(path,delim_whitespace=True, header=None)
        if os.path.isfile(path)==False:
            return 0,0,0,0,0,0,0,0
            
        df =pd.read_csv(path,sep=',', header=None)
        sn=np.asarray(df.iloc[:,3:df.shape[1]])
        ser_bs_station_rl=np.asarray(df.iloc[:,0])
        ser_bs_rl=ser_bs_station_rl[0]
        basestation = df.shape[1] - 3 
        
        ser_bs_rl=np.argmax(sn[0,:])+1
        hd_rl=0
        for i in range(df.shape[0]):
            if ser_bs_rl != ser_bs_station_rl[i]:
                ser_bs_rl = int(ser_bs_station_rl[i])
                hd_rl = hd_rl + 1
            else:
                ser_bs_rl = int(ser_bs_station_rl[i])
            snr_rl = snr_rl  + sn[i,ser_bs_rl-1]
        mean_snr_rl = snr_rl/df.shape[0]
        AT_rl = 500*np.log10(1+(10**(mean_snr_rl/10)))*(1-(hd_rl*delay_cost)/df.shape[0])
        
        hd_n = 0
        ser_bs_n = np.argmax(sn[0,:])
        for i in range(df.shape[0]):
            if sn[i, ser_bs_n] < snr and sn[i, ser_bs_n] != np.max(sn[i,0:sn.shape[1]]):
                ser_bs_n = np.argmax(sn[i,0:sn.shape[1]])
                hd_n = hd_n +1
            snr_n = snr_n  + sn[i,ser_bs_n]
            k=k+1
        mean_snr_n = snr_n/df.shape[0]
        AT_n = 500*np.log10(1+(10**(mean_snr_n/10)))*(1-(hd_n*delay_cost)/df.shape[0])
        
        return basestation,snr,hd_rl, mean_snr_rl,AT_rl, hd_n, mean_snr_n, AT_n
def handover(delay_cost,intensity, user):
    snr=[]
    for i in range(40):
        if os.path.exists("C:\\Users\\2427060M\\Dropbox\\PHD - MANDELA\\Paper to write\\Paper 3\\mobile-data\\mobile_data\\data_models\\user_log\\intensity_"+str(intensity)+"_user_"+str(user)+"_position_delay_"+str(delay_cost)+"_SNR_"+str(i)+".csv"):
            snr = np.append(snr,i)

    snr = list(map(int, snr))
    a=[]
    #for i in range(snr):
    for i in snr:
        a.extend(handover_performance(int(i), delay_cost, intensity, user))
    np.savetxt("C:\\Users\\2427060M\\Dropbox\\PHD - MANDELA\\Paper to write\\Paper 3\\mobile-data\\mobile_data\\data_models\\user_log\\handover_report_intensity_"+str(intensity)+"_user_"+str(user)+"_delay_cost_"+str(delay_cost)+".csv", np.reshape(np.asarray(a).T,(len(snr),8)), delimiter=",",fmt='%10.5f',header= "")

    
    
