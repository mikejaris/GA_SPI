# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:39:21 2022

@author: jaris
"""

import numpy as np
import oct2py
import sys


def TVAL3(A,b,nx,ny,mu=2**8,beta=2**5,iters=1e3,tol=1e-5,cnt=1e4,TVnorm=1,nneg=2,TVL2=1):
    ##the following functions call a module oct2py that
    ##allows you to call octave (i.e., free matlab) inside python
    oc = oct2py.octave#create octave variable
    try:
        print(oc.eval("testlm"))#try to run a test function to see if octave is working
    ##if the above function doesn't work, program restarts octave
    except:
        oc.restart()
        oc.addpath(oc.genpath('C:/Users/Jaris/Documents/TVAL3_beta2.4/TVAL3_beta2.4/'))
        # try:
        #     print(oc.eval("testlm"))
        # except:
        #     sys.exit(1)

    return oc.CSimg2(A,b.flatten(),nx,nx,mu,beta,iters,tol,cnt,TVnorm,nneg,TVL2)