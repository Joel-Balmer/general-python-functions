# -*- coding: utf-8 -*-
"""
Created on Wed May  6 15:18:08 2020

@author: Joel Balmer
"""

import numpy as np

def rpm_to_rads(w_rpm):
    """
    To convert revolutions per minute (rpm) to radians per second (rad/s). 
    rad/s is the SI unit, while rpm tends to be how the industry expresses rotational velocity.
    
    1 rad/s = 60 rad/min = 60/(2*pi) rpm
    
    ∴ rad/s = rpm * (1 rad/s / (60/(2*pi)) rpm)
    
    Parameters
    ----------
    w_rpm : int or float
        The angular velocity in rpm.

    Returns
    -------
    w_rads : int of float
        The angular velocity in rads

    """
    
    w_rads = w_rpm/(60/(2*np.pi))
        
    return(w_rads)

def rads_to_rpm(w_rads):
    """
    To convert radians per second (rad/s) to revolutions per minute (rpm). 
    rad/s is the SI unit, while rpm tends to be how the industry expresses rotational velocity.
    
    1 rad/s = 60 rad/min = 60/(2*pi) rpm
    
    ∴ rad/s = rpm * (1 rad/s / (60/(2*pi)) rpm)
    
    Parameters
    ----------
    w_rpm : int or float
        The angular velocity in rpm.

    Returns
    -------
    w_rads : int of float
        The angular velocity in rads

    """
    
    w_rpm = w_rads*(60/(2*np.pi))
        
    return(w_rpm)

#%% Testing the function

if __name__ == "__main__":
    
    w_rpm = 7000
    
    w_rads = rpm_to_rads(w_rpm)
    
    w_rpm_return = rads_to_rpm(w_rads)