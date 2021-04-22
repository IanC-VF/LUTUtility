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
#get date for file names and list file directories and name of info file
curday=datetime.datetime.today()
DataDir='C:/LUTDataGeneration/RAWDATA/'
infoname='CalibrationInfo.csv'
csvpath='C:/LUTDataGeneration/CSV/'
binpath='C:/LUTDataGeneration/BIN/'
Coeffpath='C:/LUTDataGeneration/COEFFICIENTS/'
#grab parameters from the info file
para=pd.read_csv(DataDir+infoname,header=0) #grab parameters as a data frame
textnumbers=para.values[:,0] #three columns needed to match data files to lasers and racks
RackNumbers=para.values[:,1]
LaserNumbers=para.values[:,2]
CFHeader=[ 'a', 'b', 'c']  #headers for coefficient file
#get pulse time and max power
SensorIDdf=para['Sensor Number']
SensorIDstr= str(int(SensorIDdf[0]))
PowerLevelsdf=para['Power Levels (in decimal percent of total power)']
PulseTimedf=para['Pulse time on (s)']
PulseTime=PulseTimedf[0]
MaxPowerdf=para['Max Power (W)']
MaxPower=MaxPowerdf[0]
CalIDdf=para['Calibration ID to be generated']# ID of 
CalID=int(CalIDdf[0])
upperthresholddf=para['Power-modified-limit (in decimal percent of total power)']
upperthreshold=upperthresholddf[0]
calledthresholddf=para['Power-called-limit (in decimal percent of total power)']
calledthreshold=int(np.round(calledthresholddf[0]*255,0))
print(f'Row index for Power Called Cutoff: {calledthreshold}')
PulseEnergy=PulseTime*MaxPower
PowerLevels=PowerLevelsdf.dropna().values
RacksUsed=np.unique(RackNumbers)
datalength=len(PowerLevels)
rows, cols, mats =(21,3,8)
powerperct=np.linspace(0,1,256)
lineardata=np.round(powerperct*65535,0)
lineardata[lineardata>(65535*upperthreshold)]=np.round(65535*upperthreshold,0)
CFMatrix=np.asarray([[[0 for i in range(cols)] for j in range(rows)]for z in range(mats)], dtype=float)
calledlimitflag=0
filesfound = len(glob2.glob(DataDir+SensorIDstr+'_*.txt'))
fileError=0
filesNeeded = len(textnumbers)
if filesfound != filesNeeded:
    print(DataDir+SensorIDstr+'_*.txt')
    print(f'Mismatch between CalibrationInfo.csv Rows: {filesNeeded} and files found in /RAWDATA: {filesfound}')
    fileError = 1
for i in range(rows):
    for z in range(mats):
        CFMatrix[z][i][1]=1

for laser in glob2.glob(DataDir+SensorIDstr+'_*.txt'):
    #print(laser)
    if len(laser)==42:
        txtnum=int(laser[-6:-4])
    else:
        txtnum=int(laser[-7:-4])
    #print(txtnum)
    txtid=np.where(textnumbers==txtnum)[0][0]
    #print(txtid)
    RackNum=int(RackNumbers[txtid])
    LaserNum=int(LaserNumbers[txtid])
    
    
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
    finalpath=Coeffpath+CCname
    #print(finalpath)
    R0=pd.DataFrame(Matrix,columns = CFHeader)
    R0.to_csv(finalpath, header = True, index = False)
    for i in range(0,21):
        calledlimitflag=0
        calledlimitrow=0
        ce=Matrix[i][:]
        adjpower=ce[0]*powerperct*powerperct+ce[1]*powerperct+ce[2]
        scaledpower=np.round(adjpower*65535,0) #scale all values to 0-65535 scale for VFLCR
        scaledpower[scaledpower>(65535*upperthreshold)]=np.round(65535*upperthreshold,0)
        for y in range(0,255):
            if scaledpower[y]==np.round(65535*upperthreshold,0):
               #print(f'Laser {i+1} on Rack {int(R)} row call: {y}')
                calledlimitrow=y
                break
        if calledlimitrow == 0:
            calledlimitrow = 300
        final=scaledpower.reshape((-1,1)).astype(int)
        
        Lnum=str(i+1).zfill(2)
        RackFolder='R'+str(int(R)).zfill(2)+'/'
        csvsavename='R'+str(int(R)).zfill(2)+'L'+Lnum+'_'+'ID'+str(CalID).zfill(5)+'_'+str(curday.day).zfill(2)+str(curday.month).zfill(2)+str(curday.year)+'.csv'
        if calledlimitrow>calledthreshold and fileError == 0:
            pd.DataFrame(final).to_csv(csvpath+RackFolder+csvsavename, index=False, header=None)
        elif fileError == 1:
            pass
        else:
            print(f'Laser {i+1} on Rack {int(R)} failed the Called Limit Check, {calledlimitrow} < {calledthreshold}\n')
            final=lineardata.reshape((-1,1)).astype(int)
            pd.DataFrame(final).to_csv(csvpath+RackFolder+csvsavename, index=False, header=None)
Convert_LUT_to_vflpc(csvpath,binpath,CalID)       
        
    




