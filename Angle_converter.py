# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:57:07 2021

@author: joelb

Converts angles between units of degrees, radians and also (percentage) grade, and visa versa. This is pretty easy to do on the fly, but using a function avoids typo errors.

See here for general discussion of grade: https://en.wikipedia.org/wiki/Grade_(slope)
"""

import numpy as np

def rads_to_degrees(angle_in_radians):
    """
    This function converts an angle in radians to an angle in degrees.

    Parameters
    ----------
    angle_in_radians : int or float or numpy array of ints or floats

    Returns
    -------
    angle_in_degrees : dtype(angle_in_radians)
        The equivalent of angle_in_radians but in units of degrees.
    """
    
    angle_in_degrees = angle_in_radians*180/np.pi
    return(angle_in_degrees)

def degrees_to_rads(angle_in_degrees):
    """
    This function converts an angle in degrees to an angle in radians.

    Parameters
    ----------
    angle_in_degrees : int or float or numpy array of ints or floats

    Returns
    -------
    angle_in_radians : dtype(angle_in_degrees)
        The equivalent of angle_in_degrees but in units of radians.
    """
    
    angle_in_radians = angle_in_degrees*np.pi/180
    return(angle_in_radians)

def degrees_to_grade(angle_in_degrees):
    """
    This function converts an angle in degrees to an angle in (percentage) grade.
    percentage grade = 100*rise/run of a slope, where rise/run = tan(theta). 
    Therefore percentage grade = 100*tan(theta), where theta is the angle of the slope.

    Parameters
    ----------
    angle_in_degrees : int or float or numpy array of ints or floats

    Returns
    -------
    angle_in_grade : dtype(angle_in_degrees)
        The equivalent of angle_in_degrees but in units of (PERCENTAGE) grade.
    """
    if np.any(angle_in_degrees>90):     #np.any works if angle_in_degrees is a single value or array
        raise Exception('Can only convert an angle between 0 to 90 degrees to a percentage grade.\nSee: https://en.wikipedia.org/wiki/Grade_(slope)')
    angle_in_grade = 100*np.tan(angle_in_degrees*np.pi/180)
    return(angle_in_grade)

def grade_to_degrees(angle_in_grade):
    """
    This function converts an angle in (percentage) grade to an angle in degrees.
    percentage grade = 100*rise/run of a slope, where rise/run = tan(theta). 
    Therefore percentage grade = 100*tan(theta), where theta is the angle of the slope.

    Parameters
    ----------
    angle_in_grade : int or float or numpy array of ints or floats
        Angle measured as PERCENTAGE grade.

    Returns
    -------
    angle_in_degrees : dtype(angle_in_grade)
        The equivalent of angle_in_grade but in units of degrees.
    """
    
    angle_in_degrees = np.arctan(angle_in_grade/100)*180/np.pi
    
    return(angle_in_degrees)

def rads_to_grade(angle_in_radians):
    """
    This function converts an angle in radians to an angle in (percentage) grade.
    percentage grade = 100*rise/run of a slope, where rise/run = tan(theta). 
    Therefore percentage grade = 100*tan(theta), where theta is the angle of the slope.

    Parameters
    ----------
    angle_in_radians : int or float or numpy array of ints or floats

    Returns
    -------
    angle_in_grade : dtype(angle_in_radians)
        The equivalent of angle_in_radians but in units of (PERCENTAGE) grade.
    """
    if np.any(angle_in_radians>0.5*np.pi):      #np.any works if angle_in_degrees is a single value or array
        raise Exception('Can only convert an angle between 0 to pi/2 radians to a percentage grade.\nSee: https://en.wikipedia.org/wiki/Grade_(slope)')
    angle_in_grade = 100*np.tan(angle_in_radians)
    return(angle_in_grade)

def grade_to_rads(angle_in_grade):
    """
    This function converts an angle in (percentage) grade to an angle in radians.
    percentage grade = 100*rise/run of a slope, where rise/run = tan(theta). 
    Therefore percentage grade = 100*tan(theta), where theta is the angle of the slope.

    Parameters
    ----------
    angle_in_grade : int or float or numpy array of ints or floats
        Angle measured as PERCENTAGE grade.

    Returns
    -------
    angle_in_rads : dtype(angle_in_grade)
        The equivalent of angle_in_grade but in units of radians.
    """
    
    angle_in_rads = np.arctan(angle_in_grade/100)
    
    return(angle_in_rads)


#%% Testing the functions

if __name__ == "__main__":
        
    degrees_in = 90
    rads_in = 0.5*np.pi
    grade_in = 15.5  # a grade of 119% is equivalent to just under 50 degrees
    print('{0} radians is equivalent to {1} degrees and {2}% grade'.format(rads_in, rads_to_degrees(rads_in), rads_to_grade(rads_in)))
    print('{0} degrees is equivalent to {1} radians and {2}% grade'.format(degrees_in, degrees_to_rads(degrees_in), degrees_to_grade(degrees_in)))
    print('{0}% grade is equivalent to {1} degrees and {2} radians'.format(grade_in, grade_to_degrees(grade_in), grade_to_rads(grade_in)))
