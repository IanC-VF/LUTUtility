# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 10:18:47 2021

@author: ian
"""


import pandas as pd
import numpy as np
import glob2
import datetime
from LUTConv import Convert_LUT_to_vflpc
curday=datetime.datetime.today()
DataDir='C:/Users/iancl/Documents/RawCalibrationData/'
infoname='CalibrationInfo.csv'
csvpath='C:/Users/iancl/Documents/LUTcsvFiles/'
binpath='C:/Users/iancl/Documents/LUTbinfiles/'
Coeffpath='C:/Users/iancl/Documents/CurveCoefficients/'
para=pd.read_csv(DataDir+infoname,header=0)
textnumbers=para.values[:,0]
RackNumbers=para.values[:,1]
LaserNumbers=para.values[:,2]
CFHeader=[ 'a', 'b', 'c']  
PowerLevelsdf=para['Power Levels (in decimal percent of total power)']
#PowerLevels.apply(pd.to_numeric, errors='coerce')
PulseTimedf=para['Pulse time (secs)']
PulseTime=PulseTimedf[0]
MaxPowerdf=para['Max Power (W)']
MaxPower=MaxPowerdf[0]
CalIDdf=para['ID']
CalID=int(CalIDdf[0])
upperthresholddf=para['Upper Limit (%)']
upperthreshold=upperthresholddf[0]
PulseEnergy=PulseTime*MaxPower
PowerLevels=PowerLevelsdf.dropna().values
RacksUsed=np.unique(RackNumbers)
datalength=len(PowerLevels)
rows, cols, mats =(21,3,8)
powerperct=np.linspace(0,1,256)
CFMatrix=np.asarray([[[0 for i in range(cols)] for j in range(rows)]for z in range(mats)], dtype=float)
for i in range(rows):
    for z in range(mats):
        CFMatrix[z][i][1]=1

for laser in glob2.glob('C:/Users/iancl/Documents/RawCalibrationData/955521_*.txt'):
    #print(laser)
    txtnum=int(laser[-6:-4])
    RackNum=int(RackNumbers[txtnum-1])
    LaserNum=int(LaserNumbers[txtnum-1])
    
    
    laserrawdata=pddata=pd.read_csv(laser, sep='\t', header = None, skiprows=36,usecols=[1]).values
    fitpointsY=[]
    for d in range(1,(datalength+1)):
        powerraw=[laserrawdata[d*10-10][0],laserrawdata[d*10-9][0],laserrawdata[d*10-8][0],laserrawdata[d*10-7][0],laserrawdata[d*10-6][0],laserrawdata[d*10-5][0],laserrawdata[d*10-4][0],laserrawdata[d*10-3][0],laserrawdata[d*10-2][0],laserrawdata[d*10-1][0]]
        #print(powerraw)
        laseravg=(np.mean(powerraw)/PulseEnergy)        
        fitpointsY.append(laseravg)
    ce=np.polyfit(fitpointsY,PowerLevels,2)
    CFMatrix[RackNum-1][LaserNum-1][0]=float(ce[0])
    CFMatrix[RackNum-1][LaserNum-1][1]=float(ce[1])
    CFMatrix[RackNum-1][LaserNum-1][2]=float(ce[2])
    
for R in RacksUsed:
    Matrix=CFMatrix[int(R)-1]
    folder='ID'+str(CalID).zfill(5)+'/'
    CCname='CurveCoefficients_Rack'+str(int(R))+'.csv'
    finalpath=Coeffpath+folder+CCname
    #print(finalpath)
    R0=pd.DataFrame(Matrix,columns = CFHeader)
    R0.to_csv(finalpath, header = True, index = False)
    for i in range(0,21):
        ce=Matrix[i][:]
        adjpower=ce[0]*powerperct*powerperct+ce[1]*powerperct+ce[2]
        scaledpower=np.round(adjpower*65535,0) #scale all values to 0-65535 scale for VFLCR
        scaledpower[scaledpower>(65535*upperthreshold)]=np.round(65535*upperthreshold,0)
        final=scaledpower.reshape((-1,1)).astype(int)
        Lnum=str(i+1).zfill(2)
        RackFolder='R'+str(int(R)).zfill(2)+'/'
        csvsavename='R'+str(int(R)).zfill(2)+'L'+Lnum+'_'+'ID'+str(CalID).zfill(5)+'_'+str(curday.day).zfill(2)+str(curday.month).zfill(2)+str(curday.year)+'.csv'
        pd.DataFrame(final).to_csv(csvpath+RackFolder+csvsavename, index=False, header=None)

Convert_LUT_to_vflpc(csvpath,binpath,CalID)       
        
    




