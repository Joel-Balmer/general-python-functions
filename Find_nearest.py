# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 15:13:31 2017

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  
                     
                     ABOUT THIS FUNCTION
        This function takes a value and an array and returns the element of the array that is nearest
        the value as well as its index in the array.
"""

# INPUTS:
# array: the array you want to search
# value: the value you want the output to be nearest


def find_nearest(array,value):
    
    import numpy as np
    index = (np.abs(array-value)).argmin()
    array_value = array[index]
    return (index, array_value)