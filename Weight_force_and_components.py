# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 20:24:59 2020

@author: Joel Balmer

"""

# important numpy
import numpy as np

def weight_force_and_components(m, theta, theta_units = 'radians'):
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
    m : int or array
        mass of the object in kg.
    theta : int or array (by default in the SI unit radians, see theta_units below)
        the incline/decline of the surface in by default in RADIANS (0 --> pi/2) but can be degress (0 --> 90) if theta_units = 'degrees'
    theta_units : str (optional, defaults to the SI unit 'radians')
        A string input indicating the units of the angle theta, can be either the SI unit radians (the default value) or degrees.
        
    OUTPUTS:
    ----------
    F_w : int if both inputs are int, else array
        the weight of a mass
    F_norm :  int if both inputs are int, else array
        the normal force in units of Newtons.
    F_grad :  int if both inputs are int, else array
        the gradable force, that is the weight forces component that acts to move a mass down an incline/decline
    
    """
    
    # Checking the theta_units string input:
    if theta_units != 'radians' and theta_units != 'degrees':
        raise Exception(f"theta_units input of '{theta_units}' is invalid, it must be either 'radians' (the default value) or 'degrees'")
    
    F_w = -9.81*m
    
    # NB theta should be in degrees, below it is converted to radians for numpy trig functions!
    F_norm = F_w*np.cos(theta*((np.pi/180) if theta_units == 'degrees' else 1))
    F_grad = F_w*np.sin(theta*((np.pi/180) if theta_units == 'degrees' else 1))
    
    return(F_w,F_norm,F_grad)

  
#%% TESTING THE FUNCTION ----------------------------------------------------------------------------------        

if __name__ == "__main__":  
    
    m = 20480           # mass in kg
    theta_degrees = 15          # slope/grade in degrees
    theta_radians = theta_degrees*np.pi/180
    theta_degrees_array = np.array([15,10,20])
    theta_radians_array = np.array([15,10,20])*(np.pi/180)
    
    print(weight_force_and_components(m, theta_radians))
    print(weight_force_and_components(m, theta_degrees, theta_units = 'degrees'))
    print(weight_force_and_components(m, theta_degrees_array, theta_units = 'degrees'))
    print(weight_force_and_components(m, theta_radians_array, theta_units = 'radians'))
    
    # the below line should fail
    # weight_force_and_components(m,theta_degrees, 'test for failure')