# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 14:57:02 2016

@author: jcb137 written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  
"""

# --- BLAND-ALTMAN PLOTS ________________________________________________________________________

# This function takes variables X and Y which usually are two difference measures of the same thing.
# Eg two devices trying to measure the temperature in a room.
# The analysis then shows the bias between the two methods.

# INPUTS------------------
# X, one array of the two measures
# Y, the second array of the two measures

# OUTPUTS ----------------
# A plot! 

# ------------------------------------------------------------------------------------------------
# Importing Modules
import matplotlib.pyplot as plt
import numpy as np

def bland_altman_plot(X, Y, *args, **kwargs):
    X     = np.asarray(X)
    Y     = np.asarray(Y)
    mean      = np.mean([X, Y], axis=0)     # The mean of a beats pair of rPTT and PTT. NOT a single mean of the two arrays, but an array of means
    diff      = X - Y                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference

    plt.scatter(mean, diff, *args, **kwargs)
    plt.axhline(md,           color='gray', linestyle='--')
    plt.axhline(md + 1.96*sd, color='gray', linestyle='--')
    plt.axhline(md - 1.96*sd, color='gray', linestyle='--')
    return()