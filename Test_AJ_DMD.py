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
 
tst=AJ_DMD.AJ_DMD()
tst.frametime=500
tst.Init_Project()

nx=8
H_ = wh.walsh_matrix(nx**2)
H_=H_.reshape((nx,nx,nx**2))
H_[H_<0]=0
tst.custom_xy=True
tst.X, tst.Y = 500,500
tst.Load_Streaming(H_)
tst.driver.StartSequence(tst.sequenceID,tst.dmdIndex)
time.sleep(1)
while tst.Get_Seq_RunState() == aj.RUN_STATE_RUNNING: pass
tst.Disconnect_DMD()
