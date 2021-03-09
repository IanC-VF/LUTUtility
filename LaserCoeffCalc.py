# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 13:47:22 2021

@author: ian
"""


import csv 
import pandas as pd
import glob2
import numpy as np

pulseEnergy=0.005*300
calibration=6
powerLevels=[0.2, 0.278433, 0.356867, 0.4353,0.5137]
#print(powerLevels)
folder='ID'+str(calibration).zfill(5)
writePath='C:/Users/iancl/Documents/CurveCoefficients/'+folder+'/'
NumLasers=len(glob2.glob('C:/Users/iancl/Documents/RawCalibrationData/'+folder+'/955521_*.txt'))
rows, cols = (NumLasers,3) 
coefficientlist= [[0 for i in range(cols)] for j in range(rows)] 
for laser in glob2.glob('C:/Users/iancl/Documents/RawCalibrationData/'+folder+'/955521_*.txt'):
    print(laser)
    laserrawdata=pddata=pd.read_csv(laser, sep='\t', header = None, skiprows=36,usecols=[1]).values
    fitpointsY=[]
    for d in range(1,6):
        powerraw=[laserrawdata[d*10-10][0],laserrawdata[d*10-9][0],laserrawdata[d*10-8][0],laserrawdata[d*10-7][0],laserrawdata[d*10-6][0],laserrawdata[d*10-5][0],laserrawdata[d*10-4][0],laserrawdata[d*10-3][0],laserrawdata[d*10-2][0],laserrawdata[d*10-1][0]]
        #print(powerraw)
        laseravg=(np.mean(powerraw)/pulseEnergy)        
        fitpointsY.append(laseravg)
    ce=np.polyfit(fitpointsY,powerLevels,2)
    Lnum=int(laser[-6:-4])
    print(f'Laser:{Lnum} Coeff: {ce}')
    coefficientlist[(Lnum-1)][0]=ce[0]
    coefficientlist[(Lnum-1)][1]=ce[1]
    coefficientlist[(Lnum-1)][2]=ce[2]
nplist=np.array(coefficientlist)

Lnumcol=[i for i in range(1,(NumLasers+1))]
Header=[ 'a', 'b', 'c']    
#print(Lnumcol)
if NumLasers>=13:
    Rack4ce=np.array(coefficientlist[0:13][:])
    
    #print(f'rack 4: {Rack4ce}')
    R04=pd.DataFrame(Rack4ce, columns = Header)
    name=writePath+'CurveCoefficients_Rack6.csv'
    R04.to_csv(name,header=True, index=False)
elif NumLasers<13:
    
    Rack4ce=np.array(coefficientlist[0:NumLasers][:])
    zeroarray=np.array([[0.0]*3]*(13-NumLasers))       
    np.concatenate(Rack4ce,zeroarray)
    R04=pd.DataFrame(Rack4ce, columns = Header)
    name=writePath+'CurveCoefficients_Rack6.csv'
    R04.to_csv(name,header=True, index=False)
    #print(f'rack 4: {Rack4ce}')
if NumLasers>=32:
    Rack5ce=np.array(coefficientlist[13:32][:])
    R05=pd.DataFrame(Rack5ce, columns = Header)
    name=writePath+'CurveCoefficients_Rack7.csv'
    R05.to_csv(name,header=True, index=False)
    #print(f'rack 5: {Rack5ce}')
# elif NumLasers<42 and NumLasers>21:
#     Rack5ce=np.array(coefficientlist[21:NumLasers][:])
#     zeroarray=np.zeros((int(42-NumLasers),3))
#     Rack5ce=np.vstack([Rack5ce,zeroarray])
#     R05=pd.DataFrame(Rack5ce, columns = Header)
#     name=writePath+'CurveCoefficients_Rack5.csv'
#     R05.to_csv(name,header=True, index=False)
#    # print(f'rack 5: {Rack5ce}')
# if NumLasers>=63:
#     Rack6ce=np.array(coefficientlist[42:63][:])
#     R06=pd.DataFrame(Rack6ce, columns = Header)
#     name=writePath+'CurveCoefficients_Rack6.csv'
#     R06.to_csv(name,header=True, index=False)
#     #print(f'rack 6: {Rack6ce}')
# elif NumLasers<63 and NumLasers>42:
#     Rack6ce=np.array(coefficientlist[42:NumLasers][:])
#     zeroarray=np.zeros((int(63-NumLasers),3))
#     Rack6ce=np.vstack([Rack6ce,zeroarray])
#     R06=pd.DataFrame(Rack6ce, columns = Header)
#     name=writePath+'CurveCoefficients_Rack6.csv'
#     R06.to_csv(name,header=True, index=False)
#    # print(f'rack 6: {Rack6ce}')
# if NumLasers>=84:
#     Rack7ce=np.array(coefficientlist[63:84][:])
#     R07=pd.DataFrame(Rack7ce, columns = Header)
#     name=writePath+'CurveCoefficients_Rack7.csv'
#     R07.to_csv(name,header=True, index=False)
#    # print(f'rack 7: {Rack7ce}')
# elif NumLasers<84 and NumLasers>63:
#     Rack7ce=np.array(coefficientlist[63:NumLasers][:])
#     zeroarray=np.zeros((int(84-NumLasers),3))
#     Rack7ce=np.vstack([Rack7ce,zeroarray])
#     R07=pd.DataFrame(Rack7ce, columns = Header)
#     name=writePath+'CurveCoefficients_Rack7.csv'
#     R07.to_csv(name,header=True, index=False)
#    # print(f'rack 7: {Rack7ce}')


    
    
        