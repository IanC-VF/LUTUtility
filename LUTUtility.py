# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 13:51:31 2020

@author: ian
"""


#from BNRopcuaTag import BNRopcuaTag
#from ftplib import FTP
from LUTConv import Convert_LUT_to_vflpc
import os
#import glob2
csvpath='C:/Users/iancl/Documents/LUTcsvFiles/'
binpath='C:/Users/iancl/Documents/LUTbinFiles/'
IPs=['192.168.210.51','192.168.210.52', '192.168.210.53', '192.168.210.54', '192.168.210.55', '192.168.210.56', '192.168.210.57', '192.168.210.58' ]
os.chdir(binpath)
Convert_LUT_to_vflpc(csvpath,binpath)
# for R in range(1,8):
#     ftp = FTP(IPs[R-1])
#     ftp.login(user='admin', passwd='VFftp')
#     ftp.cwd('/media/ssd1')
#     rackstring='R'+str(R).zfill(2)
#     searchscheme='*/*'+rackstring+'*.vflpc'
#     #print(binpath+searchscheme)
#     for fi in glob2.glob(binpath+searchscheme):
#         #print(fi)
#         filename = fi
#         #ftp.storbinary('STOR '+filename, open(filename, 'rb'))
        
#     #ftp.quit()
    