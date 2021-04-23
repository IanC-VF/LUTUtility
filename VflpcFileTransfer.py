# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:55:23 2020

@author: ian
"""


from ftplib import FTP
import os
import glob2
binpath='C:/LUTDataGeneration/BIN/'
IPs=['192.168.210.51','192.168.210.52', '192.168.210.53', '192.168.210.54', '192.168.210.55', '192.168.210.56', '192.168.210.57' ]
os.chdir(binpath)
for R in range(1,8):
    ftp = FTP(IPs[R-1])
    ftp.login(user='admin', passwd='VFftp')
    ftp.cwd('/MachineParameters')
    rackstring='R'+str(R).zfill(2)
    searchscheme='*/*'+rackstring+'*.vflpc'
    print(binpath+searchscheme)
    for fi in glob2.glob(binpath+searchscheme):
        filename = fi[29:]
        ftp.storbinary('STOR '+filename, open(fi, 'rb'))
        print('File Transferred:'+fi[29:])
    ftp.quit()