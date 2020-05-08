# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 12:51:04 2016

@author: jcb137, written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  

"""

# --------------------------------------------------- ABOUT THE FUNCTION -----------------------------------------------

# This function is used to find the correlation between two variables X and Y. This correlation is measured using 'Linear Least
# Squares Data Fitting' and the Correlation Coefficient 'r' or the Coefficient of Determination 'r^2'

# INPUTS -----------------------------
# X & Y are the two varibles you wish to correlate in array format

# OUTPUTS
# r_squared: coefficient of determination
# m: slope of best fit line
# b: intercept of best fit line with the y axis

def linear_regression_line_analysis(X, Y):

# Finding the linear regression line that minimises the summed squared error between the two varibles

    if len(X) != len(Y):        # checking the inputs are the same size
        raise Exception('ERROR: the inputs for X and Y must be the same size as each X element should have a corresponding Y element that was observed')
        
    # Working out the arguments needed to calculate the gradient of the regression line, see notes I made stored in:
    # OneDrive\Documents\University\PhD\Math Notes\Regression Line Analysis and Correlation Coefficient.pdf
    # Or hard copy in my Uni PhD folder
        
    xybar =((X)*(Y)).mean()
    xbarybar = (X.mean())*(Y.mean())
    xbarsquared = (X.mean())**2
    xsquaredbar = ((X)**2).mean()

    m = (xybar - xbarybar)/(xsquaredbar - xbarsquared)  # Gradient of regression line that gives minimum sum of squared errors
    b = (Y.mean()) - m*(X.mean())    # y-intercept (at x=0) that corrosponds with the minimum sum of squared errors
    
    SSE_line = 0        # initilizing the sum squared error varible for the regression line
    SSE_ybar = 0        # initilizing the sum squared error varible for a line equal to the mean of y
    ybar = Y.mean()     # working out the mean once as it is used at each iteration but no point re-calculating the same value each iteration
    for i in range(0,Y.size):
        SSE_line = SSE_line + (Y[i] - (m*X[i] + b))**2
        SSE_ybar = SSE_ybar + (Y[i] - ybar)**2
        
    r_squared = 1 -(SSE_line/SSE_ybar)
    
    return(r_squared, m, b)