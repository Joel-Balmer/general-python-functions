# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 13:06:37 2018

@author: jcb137, written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  

ABOUT THE FUNCTION

This function minimizes the error between a best fit line and a bunch of x,y data point observations by
minimizing the area of the triangles from each point x,y to the line. The triangle is bound by the line
and the delta x and delta y distances to the line.

This method is also known as minimising the geometric mean deviations.

I have two reasonable papers that explain the process:
    
At a high level: Model Fitting for Multiple Variables by Minimising the Geometric Mean Deviation - Tofallis 2002

At a detailed level: The Method of Minimized Areas as a Basis for Correlation Analysis - Woolley 1941

INPUTS
X: the array of the x data you want to correlate with the y data
Y: the array of the y data you want to correlate with the x data

OUTPUTS
r_squared: coefficient of determination
m: slope of best fit line
b: intercept of line of best fit with the y axis
"""

import numpy as np

def minimised_areas_linear_correlation_analysis(X,Y):
    
    if len(X) != len(Y):        # checking the inputs are the same size
        print('ERROR: the inputs for X and Y must be the same size as each X element should have a corresponding Y element that was observed')
        return()
        
    # Working out the arguments needed to calculate the gradient of the regression line, for a summary of these equations,
    # see the summary section of The Method of Minimized Areas as a Basis for Correlation Analysis - Woolley 1941
    # NB however that in this paper, they use 'a' for the intercept and 'b' for the slope of the best fit line.
    
    N = len(Y)                                          # N is simply the number of data points which should be the same for both the X and Y arrays
    
    y_bar = np.mean(Y)                                  # mean of Y array
    SD_y = (np.sum(((Y-y_bar)**2))/(N-1))**0.5          # standard deviation of y values
    
    x_bar = np.mean(X)                                  # mean of X array
    SD_x = (np.sum(((X-x_bar)**2))/(N-1))**0.5          # standard deviation of the x value
    
    m = SD_y/SD_x                                       # slope of best fit line that minimises the error as measured as the area from an observation
    b = (np.sum(Y) - m*np.sum(X))/N                     # y intercept of best fit line that minimises the error as measured as the area from an observation
    
    r_squared = (np.sum(X*Y)/(N*SD_x*SD_y))**2          # coefficient of determination.
    
    return(r_squared, m, b)