# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 16:09:28 2017

@author: jcb137

________________________________________ PURPOSE OF THIS FUNCTION ____________________________________________

This function was developed to generate linear model that best fit data that is assumed to follow a linear
function.

Specicifically it fits a polynomial to the data of order (aka degree) choosen by the user.

General form of polynomial:
    y(x) = p0 + p1*x + p2*x^2 + .... + pn*x^n
    
Matrix form (for vector of x and y values):
    [y0      [[1, x0, x0^2, ..., x0^n]        [p0
     y1       [1, x1, x1^2, ..., x1^n]         p1
     y2       [1, x2, x2^2, ..., x2^n]         p2
     .     =   .                            *  .
     .         .                               .
     .         .                               .
     yi]      [1, xi, xi^2, ..., xi^n]]        pi]

INPUTS
x_array:    the independent variable array
y_array:    the dependent variable array or measured data that corrosponds with x
n:          the highest order/degree of polynomial you want to fit to the data

calc_y_int: it is possible that the y_int for a model may be known prior to needing to regression (for example, in finding RC for Shuns SV method)
            if this is the case, ensure y and x data are of form y = p1x + p2*x^2 + .... + pn*x^n, then set calc_y_int = True so the function knows
            that p0 has omitted. See the notes in the testing function section at the bottom of this script for more details.
                                    

OUTPUTS:
p_array: the parameter vector where the zeroth element is p0 and the nth is pn.
    
    
"""

def polynomial_regression( x_array, y_array, n, calc_y_int = True):
    
    # importing necessary modules
    import numpy as np
    
    # Calculating the number of parameters we desired to find
    if calc_y_int == False:
        num_para = n       # if we dont want to calc parameter p0, we have the same number of parameters as we do degrees of our polynomial
                           
        k = 1              # we will also no longer have the 1's in the first column of the X matrix, since these are multiplied by p0 which we are no longer looking for (see notes above)
                           # k = 1 then ensures our first column is the x^1 terms instead of x^0 (=1)
                           # see my onedrive notes on linear regression for more details
                           
    
    else:       # the reason it is n+1 accounts for the y_int term, assuming it is being calculated, degree n = 2 means we want p0, p1 and p2
        num_para = n + 1
        k = 0
        
    # Generating matrix equations based on n:
    p_array = np.zeros(num_para)                 
    X = np.ones([len(x_array),num_para])   # initializing the matrix of polynomial x terms which multiple the parameters, ie x^0, x^1, x^2..., x^n are, for each value of x
    
    # Setting up X matrix elements
    for i, x in enumerate(x_array):
        for j in range(0,num_para):
            X[i,j] = x**(j+k)             # NB ** is how you do an exponent in python, instead of ^ (annoying I know!)
            
    p_array = np.matmul(np.matmul(np.linalg.inv(np.matmul(np.transpose(X),X)),np.transpose(X)),y_array)      # This looks messy because of the np inbuilt functions but is just p_array = invert(transpose(X)*X)*transpose(X)*y_array
            
    return(p_array, X)
            
# ________________________________________________________________________________________________________________    
# ________________________________________________________________________________________________________________        
# ________________________________________________________________________________________________________________    
# _____________________________________ TESTING THE FUNCTION _____________________________________________________

# Fitting a line to 4 data points:
#   (1,6), (2,5), (3,7), (4,10)
# linear model: y(x) = p0 + p1*x
# p0 should be 3.5
# p1 should be 1.4
# Example taken from: https://en.wikipedia.org/wiki/Linear_least_squares_(mathematics)

if __name__ == "__main__":
    
    import numpy as np
    x1 = np.array([1,2,3,4])
    y1 = np.array([6,5,7,10])
    n1 = 1
    
    p_array1, X_matrix1 = polynomial_regression(x1,y1,n1)
    

# Fitting a line to 4 data points:
# (1,2.5), (2,1.5), (3,3.5), (4,6.5)
# Where the above data points are the same as the first example except the y_int parameter p0 = 3.5 has been subtracted from
# the measured y values, as though the parameter was known prior to the regression. By setting calc_y_int and ensuring the y_int
# was subtracted from the measured data before passing to the function, the function now solves for the model assuming the y_int
# is being forced to zero (ie being ignored)
# linear model: y(x) = p2*x
# p1 should be 1.4

    x2 = np.array([1,2,3,4])
    y2 = np.array([2.5,1.5,3.5,6.5])
    n2 = 1
    
    p_array2, X_matrix2 = polynomial_regression(x2,y2,n2, calc_y_int = False)
    

# Fitting a quadratic to 13 data points
# linear model: y(x) = p0 + p1*x + p2*x^2
# p0 should be -21.89774466
# p1 should be 14.52117133
# p2 should be -0.17371411
# example taken from: https://mathbits.com/MathBits/TISection/Statistics2/quadratic.html

    x3 = np.array([10,15,20,24,30,34,40,45,48,50,58,60,64])
    y3 = np.array([115.6,157.2,189.2,220.8,253.8,269.2,284.8,285.0,277.4,269.2,244.2,231.4,180.4])
    n = 2
    
    p_array3, X_matrix3 = polynomial_regression(x3,y3,n)
    
# Finding an exponential functions parameters:
# y = p0*exp(p1*x) (nonlinear function with nonlinear parameters)
# Linearise the function:
# ln(y) = ln(p0) + p1*x
# let p0 = 2 and p1 = 2 and test our function works by finding these values
# NB that the parameters output by the linearized function will be ln(p0) and p1
# so to get p0 that fits the exponenetial function we need to do p0 = np.exp(ln(p0))

    p0_actual = 2
    p1_actual = 2
    x4 = np.array([1,2,3,4])
    y4 = p0_actual*np.exp(p1_actual*x4)
    n = 1
    
    p_array4, X_matrix4 = polynomial_regression(x4,np.log(y4)-np.log(p0_actual),n, calc_y_int=False)
    
#    p0 = np.exp(p_array4[0])
#    p1 = p_array4[1]
    p1 = p_array4[0]
    
    