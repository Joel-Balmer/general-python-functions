# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 20:24:59 2020

@author: Joel Balmer

"""

# important numpy
import numpy as np

def weight_force_and_components(m, theta):
    """
    PURPOSE:
    -----
    To establish the weight force (F_w) of an object AND, if on an incline, work out the components of normal force (F_norm)
    and gradable force (F_grad). (NB the name gradable force comes from gradability, a measure of a trucks uphill pulling power).
    
    Where:  
        F_w = mg
        
        F_norm = F_w*cos(theta) (the force perpendicular to the surface the mass is on.)
        
        F_grad = F_w*sin(theta) (the force parallel to the surface the object is on, acting on it to move downhill)
        
    NOTE ON VECTORS
    -----
    F_w by convention acts downwards and therefore the function values are -ve, since gravity when given direction is -9.81ms^-2.
    Thus F_w < 0. As a result:
    - F_norm will be -ve, since F_w < 0 and for -90 <= theta <= 90 0 <= cos(theta) <= 1.
    - F_grad will be +ve or -ve, since F_w < 0 and -90 <= theta <= 90 -1 <= sin(theta) <= 1.
    
    The function assumes a right hand coordinate system (increasing x from left to right). Thus, +ve theta is an upward (counter
    clockwise) slope, meaning F_grad will act back down the slope (towards decreasing x), opposing the incline. For -ve theta, 
    the slope is downward, meaning F_grad will act forward down the slope (towards increasing x), acting with the incline. 
    Thus, it can be seen that F_grad's direction is opposite to that of theta's:
        - Incline: theta > 0 --> F_grad < 0
        - Decline: theta < 0 --> F_grad > 0
                 
    INPUTS:
    ----------
    - m: mass of the object in kg.
    - theta: the incline/decline of the surface in DEGREES (0 --> 90) (function converts to radians for the numpy trig functions)
        
    OUTPUTS:
    ----------
    - F_w: the weight of a mass
    - F_norm: the normal force in units of Newtons.
    - F_grad: the gradable force, that is the weight forces component that acts to move a mass down an incline/decline
    
    """
    
    F_w = -9.81*m
    
    # NB theta should be in degrees, below it is converted to radians for numpy trig functions!
    F_norm = F_w*np.cos(theta*np.pi/180)
    F_grad = F_w*np.sin(theta*np.pi/180)
    
    return(F_w,F_norm,F_grad)

  
#%% TESTING THE FUNCTION ----------------------------------------------------------------------------------        

if __name__ == "__main__":  
    
    m = 20480           # mass in kg
    theta = 15          # slope/grade in degrees
    theta_array = np.array([15,10,20])
    
    print(weight_force_and_components(m, theta))
    print(weight_force_and_components(m, theta_array))    