# -*- coding: utf-8 -*-
"""
Created on Tue May 18 10:10:49 2021

@author: joelb

Quadratic formula root finder, aka quadratic formula

"""

def quadratic_root_solver(a,b,c):
    """
    Function solves the equation: 
        ax^2+bx+c = 0 
    
    using the quadratic formula:    
        x = (-b ± (b^2 - 4ac)^0.5)/2a

    Parameters
    ----------
    a : int or float
        The coefficient of the x^2 term.
    b : int or float
        The coefficient of the x term.
    c : int or float
        The constant term.

    Returns
    -------
    x1 : int or float
        One of the two roots, ie one of the two x intercept values when y = 0.
    x2 : int or float
        Second of the two roots, ie second of the two x intercept values when y = 0.

    """
    
    x1 = (-b + (b**2 - 4*a*c)**0.5)/(2*a)
    x2 = (-b - (b**2 - 4*a*c)**0.5)/(2*a)
    
    return(x1,x2)

#%% Testing the function

if __name__ == '__main__':
    a = 1
    b = 2
    c = 1
    
    x1,x2 = quadratic_root_solver(a,b,c)
    print(f'x1 = {x1}, x2 = {x2}')