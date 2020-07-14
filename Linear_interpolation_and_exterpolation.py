# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 13:56:31 2020

@author: joelb
"""


def linear_interpolation_and_exterpolation(x1,y1,x2,y2,xn):
    """
    This function performs linear interpolation (x1<xn<x2 or x2<xn<x1) or exterpolation (xn<x1,x2 or x1,x2<xn), to find yn.

    Parameters
    ----------
    x1 : int or float
        A known x value.
    y1 : int or float
        x1's corresponding known y value.
    x2 : int or float
        A second known x value.
    y2 : int or float
        x2's corresponding known y value.
    xn : int or float
        x value for which you want to approximate a y value via inter/exterpolation.

    Returns
    -------
    yn : int or float
        estimate of xn's corresponding y value via inter/exterpolation.

    """
    
    m = (y2-y1)/(x2-x1)
    c = y1-m*x1
    
    yn = m*xn+c
    
    return(yn)

#%% Testing the function

if __name__ == "__main__":
    
    y = linear_interpolation_and_exterpolation(1,1,3,3,2)