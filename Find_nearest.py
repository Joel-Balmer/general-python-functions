# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 15:13:31 2017

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  
                     
"""


def find_nearest(array,value):
    """
    This function takes a value and an array and returns the element of the array that is nearest
    the value as well as its index in the array.

    Parameters
    ----------
    array : numpy array
        the array you want to search.
    value : int or float
        the value you want the output to be nearest.

    Returns
    -------
    index : int
        the index of the array element that is nearest 'value' input.
    array_value : int or float
        the value of the array element that is nearest the 'value' input.

    """
    
    import numpy as np
    index = (np.abs(array-value)).argmin()
    array_value = array[index]
    return (index, array_value)


#%% ---------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

import numpy as np

def value_between(x_array,x_val):
    """
    This function takes a value x_val, and an array of x values x_array. It returns the values from x_array, that are either side of
    x_val, as well as the indices of those values. Easier to understand this with math nomeclature than words, specifically it returns:
        
        * x_a : the value closest-from-below to x_val
        * i_a : the index of x_a
        * x_b : the value closest-from above-x_val
        * i_b : the index of x_b
        
    Such that: x_array[i_a] = x_a <= x_val <= x_b = x_array[i_b]
    
    Eg, say x_array = np.array([1, 4, 2.3, 8, 6.2]) and x_val = 3, the function would return x_a=2.3, i_a=2, x_b=4, i_b=1. NB the zero
    indexing of python.
    
    NOTE:
    If x_val is exactly equal to one of the values in x_array, the function returns x_a = x_b = x_val and i_a = i_b. Coding it in this
    way means the return of the function is consistant.
    
    If x_array has multiple elements of the same value, and that value happens to be x_a or x_b, the index returned will be the first
    instance of said value.

    Parameters
    ----------
    x_array : numpy array
        An array of ints or floats.
    x_val : TYPE
        An int or float, where min(x_array) <= x_val <= max(x_array).

    Returns
    -------
    x_a : int or float
        The value closest-from-below to x_val
    i_a : int
        The index of x_a
    x_b : int or float
        The value closest-from-above x_val
    i_b : int
        The index of x_b
    """
    
    if x_val < min(x_array) or x_val > max(x_array):
        raise Exception ("x_val is outside of x_array min and max")
       
    indices_below = np.where(x_array-x_val <= 0)[0]     # NB the [0] on the end is just because np.where returns a tuple
    indices_above = np.where(x_array-x_val >= 0)[0]     # NB the [0] on the end is just because np.where returns a tuple
    
    i_a = indices_below[x_array[indices_below].argmax()]
    i_b = indices_above[x_array[indices_above].argmin()]
    
    x_a = x_array[i_a]
    x_b = x_array[i_b]
    
    return(x_a,i_a,x_b,i_b)

#%% Testing the function

if __name__ in "__main__":
    
    test_array = np.array([1,20,3.5,3.5,2,10])
    test_val = 5
    # test_val = 3.5
    # test_val = 30
    
    (x_a,i_a,x_b,i_b) = value_between(test_array, test_val)
    print(f'x_a = {x_a}\ni_a = {i_a}\nx_b = {x_b}\ni_b = {i_b}')