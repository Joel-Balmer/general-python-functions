# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 15:53:58 2016

@author: jcb137


SHEAR TRANSFORM (WITH INBUILD MAX SHEAR FINDER) -----------------------------------------------------------------------

BRIEF DESCRIPTION
This function finds the shear transform between a shearline and a signal (See my notes
on shear transforms on my onedrive). It can be used to identify the point of maximum change in curvature of a signal.

INPUTS
signal: The signal you want to shear transform. 
        
shearline_start_index: the index for which a shearline should start. NB if you want the whole signal to be shear transformed, shearline_start = 1
shearline_end_index: the index for which a shearline should end. NB if you want the whole signal to be shear transformed, shearline_end_index = len(signal)-1, NOT JUST -1

    NB shearline_start_index must occur before its corresponding  shearline_end_index. If the signal starts with a  shearline_end_index and
    ends with a shearline_start_index, an error is raised
    
OUTPUTS

delta_y: the array of the vertical distance between each shearline point and its corresponding signal point, useful for debugging

max_pos_shear_index: the index of the maximum POSITIVE vertical distance between a point on the signal and its corresponding point in time
                      on the shearline.
                        
max_neg_shear_index: the index of the maximum NEGATIVE vertical distance between a point on the signal and its corresponding point in time
                      on the shearline. IE the indice is a point on the signal curve that is furthest BELOW the shearline.
                      NB hesitant to call it min_shear_index as that implies that the shear was small, as opposed to the shear being big in magnitude but in
                      the negative direction.

"""

def shear_transform(signal, shearline_start_index,  shearline_end_index):
    
    import numpy as np
      
    # Checking if the shearline start occurs after the shearline end, in which case an error is raised
    if  shearline_start_index >  shearline_end_index:
        raise Exception('ERROR the first shearline_end_index point is before the first shearline start point')
        
    # Checking if shearline end index was entered as -1, indicating that the final point in the signal should be the shearline end point
    if  shearline_end_index == -1:
         shearline_end_index = len(signal)-1
        
    # Working out the line, y = mx+c, joining  shearline_start_index with a  shearline_end_index
    m = (signal[shearline_end_index]-signal[ shearline_start_index])/( shearline_end_index- shearline_start_index)
    c = signal[shearline_start_index]  
        
    # Getting the section of the signal between  shearline_start_index and  shearline_end_index
    signal_section = signal[shearline_start_index: shearline_end_index+1]

    # Finding the vertical difference between the curve and the shearline
    # NB it is this difference we define as the vertical lag (dy), hence the name
    delta_y = np.zeros(len(signal_section))
    for x in range(0, len(signal_section)):
        delta_y[x] = signal_section[x] - (m*x+c)
        
    # working out the max curvature location based on the max delta_y indice location
    max_pos_shear_index = np.argsort(delta_y)[-1] +  shearline_start_index
    max_neg_shear_index = np.argsort(delta_y)[0] +  shearline_start_index
        
    return(delta_y, max_pos_shear_index, max_neg_shear_index)