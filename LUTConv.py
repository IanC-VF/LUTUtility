# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 12:55:19 2020

@author: ian
"""


import numpy as np
import pandas as pd
import os
import glob2
import zlib

nameprefix='VF-LaserPowerLUT_'


def Convert_LUT_to_vflpc(csvpath,binpath, ID):
    os.chdir(csvpath)
    print('Starting Conversion')
    for csv in glob2.glob(csvpath+'*/*.csv'):
        #print(csvpath+'*/*.csv')
        data=pd.read_csv(csv, dtype = np.uint16, header=None)
        filebinname=csv[-27:-4]+'.vflpc'
        racknumber=filebinname[0:3]
        lasernumber=filebinname[4:6]
        fullpath=binpath+racknumber+'/'+nameprefix+racknumber+'_P'+lasernumber+'_ID'+str(ID).zfill(5)+'.vflpc'
        bites=np.asarray(data.values).tobytes()
        crccode=zlib.crc32(bites)
        ba=bytearray(crccode.to_bytes(4, 'little'))
        crcbites=np.asarray(ba).tobytes()
        final=bites+crcbites
        #print(fullpath)
        np.asarray(final).tofile(fullpath)
    print('Conversion done')
