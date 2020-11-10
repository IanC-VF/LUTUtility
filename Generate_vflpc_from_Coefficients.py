# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 08:50:53 2020

@author: ian
"""


import pandas as pd
import numpy as np
import os
import datetime
import glob2
from LUTConv import Convert_LUT_to_vflpc
Coeffpath='C:/Users/iancl/Documents/CurveCoefficients/'
name='CurveCoefficients_Rack6.csv'
csvpath='C:/Users/iancl/Documents/LUTcsvFiles/'
binpath='C:/Users/iancl/Documents/LUTbinFiles/'
os.chdir(Coeffpath)
for csv in glob2.glob('C:/Users/iancl/Documents/CurveCoefficients/CurveCoefficients_Rack*.csv'):
    data=pd.read_csv(csv,header = None, skiprows=7, usecols=[3])
    data=data.values
    powerperct=np.linspace(0,1,256)
    Rack=csv[-5]
    upperthreshold=0.5
    lowerthreshold=0.15
    dirname='Rack'+Rack
    curday=datetime.datetime.today()
    lasernum=0
    for l in range(0,57,3):
        lasernum=lasernum+1
        a = data[l]
        b = data[l+1]
        c = data[l+2]
        lcoeff=[a[0],b[0],c[0]]
        adjpower=lcoeff[0]*powerperct*powerperct+lcoeff[1]*powerperct+lcoeff[2]
        
        lowercheck=False
        uppercheck=False
        for i in powerperct:
            if i >= lowerthreshold and lowercheck == False:
                zeroindex= np.where(powerperct==i)[0][0]
                lowercheck=True
            if i >= upperthreshold and uppercheck == False:
                threshindex=np.where(powerperct==i)[0][0]
                threshvalue=adjpower[threshindex]
                #print(threshvalue)
                uppercheck = True
                break
        fillsize=np.size(adjpower[threshindex:])
        adjpower[threshindex:]=(np.ones(fillsize)*threshvalue)
        adjpower[0:zeroindex]=np.zeros(zeroindex)
        scaledpower=np.round(adjpower*65535,0)
        final=scaledpower.reshape((-1,1)).astype(int)
        Lnum=str(lasernum).zfill(2)
        RackFolder='R0'+Rack+'/'
        savename='R0'+Rack+'L'+Lnum+'_'+str(curday.day).zfill(2)+str(curday.month).zfill(2)+str(curday.year)+'.csv'
        pd.DataFrame(final).to_csv(csvpath+RackFolder+savename, index=False, header=None)
    os.chdir(Coeffpath)
Convert_LUT_to_vflpc(csvpath,binpath)
    
    
    



