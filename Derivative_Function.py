# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:22:31 2016

@author: jcb137 written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  
"""

# _____________________________________________ FIRST DERIVATIVE FUNCTION ______________________________________________

# This derivative function uses the central difference method:

# df/dx = (f(x+0.5*h) - f(x-0.5*h))/h this is true when the limit of h tends to zero. So numerically the smaller h is the better

# Obviously with a descrete signal, h is the distance between consecutive points and therefore you dont have a value for
# 0.5*h. therefore we can re-write df/dx:

# df/dx = 0.5(f(x+h) - f(x-h))/h

# If you are unconvinced this is equivalent, try drawing out graphically to see it is true.

# For the first point in the signal f(x=0), we dont have a poing f(0-h), nor for the final point f(x=end) do we have a f(end+h)
# therefore we use the single sided difference at these points:

# df/d(x=0) = (f(h) - f(0))/h
# df/d(x=end) = (f(end) - f(end-h))/h


# INPUTS ----------------------------
# f is your function, either an array or a list
# h is your step size along x

# OUTPUTS ---------------------------
# df is an array of the derivative of the function. 

def first_derivative(f,h):

    from numpy import zeros
    
    df = zeros([len(f)])    # defining an array which we will store the derivative of the function in    
    
    for i in range(0,len(f)):
        
        if i == 0: # for the first point in the signal we use the single sided difference approach
            df[0] = (f[1] - f[0])/h
        
        elif i == len(f)-1:     # for the final point we use the single sided difference approach
            df[i] = (f[i] - f[i-1])/h
        
        else:                   # for all other points we use the central difference method
            df[i] = 0.5*(f[i+1] - f[i-1])/h
        
    return(df)
    

# _____________________________________________ SECOND DERIVATIVE FUNCTION ______________________________________________

# You could just use the equation for the central difference method twice, ie calculate df/dx then pass it through the
# first_derivative function again to get d2f/dt2, but as you will see from my PhD notes book, this gives a less accurate 
# second derivative approximation than the method below.

# Once again the method is a central difference method, except for the first and last elements of the matrix, which use 
# forward and backward difference respectively.

# INPUTS ----------------------------
# f is your function, either an array or a list
# h is your step size along x

# OUTPUTS ---------------------------
# d2f is an array of the derivative of the function. 

def second_derivative(f,h):

    from numpy import zeros
    
    d2f = zeros([len(f)])    # defining an array which we will store the derivative of the function in    
    
    for i in range(0,len(f)):
        
        if i == 0: # for the first point in the signal we use the single sided difference approach
            d2f[0] = (f[2] - 2*f[1] + f[0])/(h**2)
        
        elif i == len(f)-1:     # for the final point we use the single sided difference approach
            d2f[i] = (f[i] - 2*f[i-1] + f[i-2])/(h**2)
        
        else:                   # for all other points we use the central difference method
            d2f[i] = (f[i+1] - 2*f[i] + f[i-1])/(h**2)
        
    return(d2f)