# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 15:55:23 2020

@author: ian
"""


from ftplib import FTP
import os
import glob2
csvpath='C:/LaserLUTfiles/LUTcsvFiles/'
binpath='C:/LaserLUTfiles/LUTbinaryFiles/'
IPs=['192.168.210.51','192.168.210.52', '192.168.210.53', '192.168.210.54', '192.168.210.55', '192.168.210.56', '192.168.210.57', '192.168.210.58' ]
os.chdir(binpath)
for R in range(7,8):
    ftp = FTP(IPs[R-1])
    ftp.login(user='admin', passwd='VFftp')
    ftp.cwd('/MachineParameters')
    rackstring='R'+str(R).zfill(2)
    searchscheme='*/*'+rackstring+'*.vflpc'
    #print(binpath+searchscheme)
    for fi in glob2.glob(binpath+searchscheme):
        filename = fi[36:]
        ftp.storbinary('STOR '+filename, open(fi, 'rb'))
        print('File Transferred:'+fi[36:])
    ftp.quit()