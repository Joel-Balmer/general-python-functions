# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:52:06 2020

@author: Owner
"""

# Root Mean Square function

# inputs:
# x: the array you want the RMS value for

# outputs:
# the x_rms, the RMS value of the input array x

import numpy as np

def rms (x):
    return(np.sqrt(np.mean(x**2)))