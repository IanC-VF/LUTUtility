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
#local directories used
Coeffpath='C:/Users/iancl/Documents/CurveCoefficients/'
#name='CurveCoefficients_Rack6.csv'
csvpath='C:/Users/iancl/Documents/LUTcsvFiles/'
binpath='C:/Users/iancl/Documents/LUTbinfiles/'
os.chdir(Coeffpath)
#this line will be replaced with pulling the ID off the the B&R eventually
Calibration_ID=6
folder='ID'+str(Calibration_ID).zfill(5)+'/'
upperthreshold=.6
for csv in glob2.glob('C:/Users/iancl/Documents/CurveCoefficients/'+folder+'CurveCoefficients_Rack*.csv'): #collect all coefficient files
    data=pd.read_csv(csv,header = None, skiprows=1)
    data=data.values #pull out data for each one
    powerperct=np.linspace(0,1,256) #create a linearly distributed array of 256 values between 0 and 1 (power percentages)
    Rack=csv[-5]#rack number from the name of the coefficient file
   # threshold=0.9#max percentage power in LUT desired (ceiling on power output)
    dirname='Rack'+Rack
    curday=datetime.datetime.today()
    lasernum=0
    for l in range(0,21):#pull the coefficients out of the file in groups of three
        lasernum=lasernum+1
        a = data[l][0]
        b = data[l][1]
        c = data[l][2]
        lcoeff=[a,b,c]
        adjpower=lcoeff[0]*powerperct*powerperct+lcoeff[1]*powerperct+lcoeff[2] #quadratic function to put the power percentages through
        #adjpower[0:39]=np.zeros(39)# this zeroes out all values from 0 to 0.15 so no power is sent too low
    
        # for i in powerperct:# this loop finds the point where the output should be saturated after based on the threshold defined above
        #     if i >= threshold:
        #         threshindex=np.where(powerperct==i)[0][0]
        #         threshvalue=adjpower[threshindex]
        #         #print(threshvalue)
        #         break
        # fillsize=np.size(adjpower[threshindex:])
        # adjpower[threshindex:]=(np.ones(fillsize)*threshvalue)#changes all values past the threshold to be the threshold value
        scaledpower=np.round(adjpower*65535,0) #scale all values to 0-65535 scale for VFLCR
        scaledpower[scaledpower>(65535*upperthreshold)]=np.round(65535*upperthreshold,0)
        final=scaledpower.reshape((-1,1)).astype(int)#reshape array for export purposes
        #name and save .csv
        Lnum=str(lasernum).zfill(2)
        RackFolder='R0'+Rack+'/'
        savename='R0'+Rack+'L'+Lnum+'_'+'ID'+str(Calibration_ID).zfill(5)+'_'+str(curday.day).zfill(2)+str(curday.month).zfill(2)+str(curday.year)+'.csv'
        pd.DataFrame(final).to_csv(csvpath+RackFolder+savename, index=False, header=None)

Convert_LUT_to_vflpc(csvpath,binpath,Calibration_ID)
    
    
    



