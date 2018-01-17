# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 12:19:24 2017

@author: jcb137

"""

"""
ROTATION TRANSFORMATION -----------------------------------------------------------------------

BRIEF DESCRIPTION
This function returns the rotation matrix required to rotate a vector (about the origin) by a certain angle theta.

INPUTS           
theta: an angle in degrees that you are interested in constructing a 2 dimensional rotation matrix for. (NB the rotation matrix also depends on theta_type below)
theta_type: a string defining how the angle is be treated from the options below:
           'relative': the vector is to be rotated through theta relative to its current position (NB notation is +ve theta are counter clockwise rotations.)
           'position': the vector is to be rotated TO the polar coordinate position theta (ie 0 theta is would move the vector onto the x axis pointing in
                       the positive direction.)
           
vector_array: if theta_type is 'position', then an input vector is required, its current location is used to determine the rotation matrix that will successfully
              rotate the vector to the desired polar coordinate location.
              Hence vector_array contains the x and y values of the vector. NB the input should be np.size = 2 (np.array([x,y])), since a vector only has size 
              and direction, originating at the origin of a reference frame.
    
# OUTPUTS
# rot_matrix: the rotation matrix of the form:
              np.array([(cos(ß),-sin(ß)),
                        (sin(ß), cos(ß))])
              where ß = theta if theta_type = 'relative', else if theta_type = 'position', ß will be the angle of rotation required to for the vector
              to be moved to theta w.r.t the polar coordinate position.
"""

# Importing necessary modules
import numpy as np
from numpy import sin as sin
from numpy import cos as cos
from numpy import arctan as arctan

def rotation_matrix_finder(theta, theta_type, vector_array = np.array([])):
    
    
    # Checking the theta_type input is valid
    if theta_type != 'relative' and theta_type != 'position':
        raise Exception('ERROR, invalid theta_type input, must be one of the following: "relative" or "position".')
        
    # Checking if a vector_array was entered if theta_type was input as 'position'    
    if theta_type == 'position' and (type(vector_array) != np.ndarray or vector_array.size != 2 or vector_array.size == 0):
        raise Exception('ERROR, theta_type = "position", however vector_array was either invalid or not specified.')
    
    # Converting theta into radians
    theta_rad = (np.pi/180)*theta
        
    # Calculating beta ß ----------------------------------------------------------------------------------------------------------------
    if theta_type == 'relative':
        beta = theta_rad
        
    elif theta_type == 'position':
                    
        x = vector_array[0]     # end coordinate of vector in x direction
        y = vector_array[1]     # end coordinate of vector in y direction
        
        # Calculating the input vectors polar coordinate system angle (in radians)
        if x>=0 and y>=0:
            initial_polar_angle = arctan(y/x)
            
        elif x<0 and y>=0: # arctan(y/x) will be POSITIVE
            initial_polar_angle = np.pi - arctan(y/x)
            
        elif x<0 and y<0: # arctan(y/x) will be NEGATIVE
            initial_polar_angle = np.pi + abs(arctan(y/x))
            
        elif x>=0 and y<0: # arctan(y/x) will be NEGATIVE
            initial_polar_angle = (2*np.pi) + arctan(y/x)
            
        beta = (2*np.pi) - initial_polar_angle - theta_rad                                
    
    # Calculating the rotation matrix that will rotate the input vector to the desired location
    rot_matrix = np.array([[cos(beta),-sin(beta)],
                           [sin(beta), cos(beta)]])
    return(rot_matrix)
    
#%% ------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------   
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------Testing the function---------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------  

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    
    plt.close('all')
    
    import numpy as np
    
    v = np.array([ 1,
                  -1])
    
    # getting the rotation matrix to shift it to point along the x axis in the postive direction
    rot_matrix = rotation_matrix_finder(0,'position', v)
    
    # rotated vector
    v_rot = np.dot(rot_matrix,v)
    
    # -------------------------------------------------
    
    v2 = np.array([-1,
                   2])
    
    rot_matrix2 = rotation_matrix_finder(-90,'relative')
    
    v2_rot = np.dot(rot_matrix2, v2)
    
    # PLOTTING ----------------------------------------
    
    plt.figure()
    plt.grid()
    plt.plot([0,v[0]], [0,v[1]], 'b')
    plt.plot([0,v_rot[0]], [0,v_rot[1]], 'b--')
    plt.plot([0,v2[0]], [0,v2[1]], 'r')
    plt.plot([0,v2_rot[0]], [0,v2_rot[1]], 'r--')
    plt.xlim(-3,3)
    plt.ylim(-3,3)
    plt.plot(0,0,'k', label = 'original vectors')
    plt.plot(0,0,'k--', label = 'rotated vectors')
    plt.legend(fontsize = 'small')
    
    # APPLYING THIS FUNCTION TO ROTATE A SHAPE----------------------------------------------------------------------------------------------
    
    # creating a basic parabola whose turning point is at coordinate (1,1)
    x = np.arange(-1,3.1,0.1)
    y = (x-1)**2 + 1    # equation for parabola
    
    # To rotate by 270 degrees, treat each point in parabola as a vector and multiple the vectors by the rotation matrix
    # By making a matrix of the individual vectors describing the parabola, we can do just one matrix multiplication, ie
    # each column of the vector matrix is one of the vectors describing the size and direction to a point of the parabola
    
    vector_matrix = np.zeros((2,len(x)))    # initializing our vector matrix with zeros
    
    for i in range(0,len(x)):
        vector_matrix[0,i] = x[i]
        vector_matrix[1,i] = y[i]
        
    rotation_matrix = rotation_matrix_finder(270, 'relative')
    
    rot_vec_mat = np.dot(rotation_matrix, vector_matrix)
    
    plt.figure()
    plt.grid()
    plt.plot(vector_matrix[0,:], vector_matrix[1,:], 'b', label = 'original')
    plt.plot(rot_vec_mat[0,:], rot_vec_mat[1,:], 'g', label = 'rotated')
    plt.legend(fontsize = 'small')