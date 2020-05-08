# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 10:58:02 2018

@author: jcb137

MOVING MEAN CALCULATOR

BREIF DESCRIPTION
This function is used to calculate the moving mean (aka windowed moving mean) of a signal, using a central point method. Ie a windowed mean using 5
points, calculates the mean value for a point n, using points, n-2,n-1,n,n+1,n+2. While this is easy to implement, because the start and end points
need to be treated seperately, it takes a few lines of code so this function can be called to keep other scripts tidy.

THINGS TO NOTE
- window length should be odd, so that you are drawing on an equal number of points either side of the point of interest
-The window length needs to be equal to or shorter than the array that is input. 
-If the window length is equal to the input array, then each element of the output array will just have the mean of the whole array.

INPUTS
arr: the array the moving mean is calculated for
window_length: the number of points to be included in the mean calculation, aka the window length

OUTPUT
mean_arr: an array of the windowed mean for each point
"""

import numpy as np

def moving_mean_and_std_finder(arr, window_length):
    
    if window_length&1 != 1:
        raise Exception('The window length input is not an odd number as it should be.')
    if window_length > len(arr):
        raise Exception('The length of the input array is less than the desired window length for which the mean is calculated.')
        
    mean_arr = np.zeros(len(arr))
    std_arr = np.zeros(len(arr))

    for i in range(0,len(arr)):    

        if i <= (window_length-1)/2:
            window_mean = np.mean(arr[0:window_length])   # using the mean of a full window length to approximate the mean of the first few points
            windowed_standard_deviation = np.std(arr[0:window_length])
      
        elif i >= len(arr) - (window_length-1)/2:
            window_mean = np.mean(arr[-window_length:])   # using the mean of a full window length to approximate the mean of the last few points where a moving mean would need more forward points than avalible
            windowed_standard_deviation = np.std(arr[-window_length:])
        
        else :
            window_mean = np.mean(arr[i-int((window_length-1)/2): i+int((window_length -1)/2)+1])     # NB we need to add one to the stop point as we want to include index i+(window-1)/2 in the calc        
            windowed_standard_deviation = np.std(arr[i-int((window_length-1)/2): i+int((window_length -1)/2)+1])
        
        mean_arr[i] = window_mean
        std_arr[i] = windowed_standard_deviation
        
    return(mean_arr, std_arr)
    
    
# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________

if __name__ == "__main__":  
    
    test_arr_1 = np.array([1,2,3,4,5,6,7,8,9])
    mean_arr_1,_ = moving_mean_and_std_finder(test_arr_1,3)
    print(mean_arr_1)
    
    test_arr_2 = np.array([1,2,3])
    mean_arr_2,_ = moving_mean_and_std_finder(test_arr_2,3)
    print(mean_arr_2)
    
    # This test below should throw an error as the input array is shorter than the input window length
    test_arr_3 = np.array([1,2])
    mean_arr_3,_ = moving_mean_and_std_finder(test_arr_3,3)
    