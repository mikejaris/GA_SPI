# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 12:47:51 2022

@author: jaris
"""
import numpy as np
import ajiledriver as aj
import time
import sys
sys.path.append('C:/users/jaris/documents/single pixel')
import AJ_DMD
import cv2
import spyrit.misc.walsh_hadamard as wh
import MCC_DAQ
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

#load images
nx=32
H_=np.zeros((nx,nx,2*nx**2))
H_[:,:,::2] = wh.walsh_matrix(nx**2).reshape((nx,nx,nx**2))
H_[H_<0]=0
H_[:,:,1::2]=abs(H_[:,:,::2]-1)

#connect instruments
daq=MCC_DAQ.MCC_DAQ()
try: dmd.Disconnect_DMD()
except: None
dmd = AJ_DMD.AJ_DMD()
dmd.frametime=1
dmd.Init_Project()
dmd.custom_xy=True
dmd.X, dmd.Y = 500,500
dmd.Load_Streaming(H_)
daq.Start_DAQUISITION()
time.sleep(0.01)
dmd.Run()
time.sleep(0.1)
while dmd.Get_Seq_RunState() == aj.RUN_STATE_RUNNING: pass
time.sleep(0.01)
data=daq.Grab_Data()
dmd.Disconnect_DMD()

#process data
y = data[::2]
trig=data[1::2]
dtrig=np.diff(trig)*-1
im = find_peaks(dtrig,height=dtrig.max()*0.25)
ims=im[0]
y=y[ims]
y=y[1::2]-y[::2]

if len(ims)==nx**2:
    H_=H_[:,:,1::2]-H_[:,:,::2]
    img=(H_.reshape((nx**2,nx**2))*y).sum(axis=1).reshape((nx,nx))
    plt.figure()
    plt.imshow(img[1:,1:])