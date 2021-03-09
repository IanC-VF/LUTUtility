import csv 

import glob
import numpy as np
from matplotlib import pyplot as plt


pulseEnergy=0.004*300
calibration=1
powerLevels=[i/10 for i in range(2,8)]
print(powerLevels)
with open('TotalDataCollection.csv','w') as output:
	with open('TotalDataAveraged.csv','w') as averaged:
		
		for r in range(1,61):
				
				laserFiles="955521_"+str(r).zfill(2)+'.txt'
				laserMeasurement=[]
				with open(laserFiles, 'r') as input:
					reader= csv.reader(input,delimiter='\t')
					for i in range(35):
						row=next(reader)
					for row in reader:
						# print(row)
						output.write(','.join([laserFiles[:-4],str(np.floor(r/20)),str(r%20),row[0],row[1]])+'\n')
						laserMeasurement.append([np.floor(r/19),r%19,float(row[0]),float(row[1])])
				for i in range(0,60,10):
					# try:
						# print(i)
						pulses=laserMeasurement[i:i+10]
						pulses=[p[3] for p in pulses]
						laserNumber=laserMeasurement[i+1][1]
						rackNumber=laserMeasurement[i+1][0]
						pulseData=[rackNumber,laserNumber,powerLevels[int(i/10)],np.mean(pulses),np.max(pulses),np.min(pulses),np.std(pulses)]
						averaged.write(laserFiles+','+str(np.mean(pulses))+','+str(r)+','+str(powerLevels[int(i/10)])+','+str(np.floor(r/19))+","+str(r%19)+'\n')
					# except:
						print(laserFiles)

					