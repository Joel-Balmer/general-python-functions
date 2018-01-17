# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 12:14:04 2017

@author: jcb137
"""

# PROCEEDING NUMBER FINDER -------------------------------------------------------------

# BRIEF DESCRIPTION
# This function was made to take in two arrays, we will call them Leaders and Searched. The Leaders array will be an array containing numbers, 
# the Searched array will also be an array of numbers. The function is designed to return an array could Followers, which contains the numbers
# from Searched array that immediately follow each of the numbers in the Leaders array.

# NB the function was originally designed to find the heart beats that followed the max pressure in the breathing cycle, where the Leader array 
# had the indices of the max peaks in the airway pressure signal and the Searched array had the foot or start of every pulse way of the aorta. 
# The Follower array output the indices for the start of the pulse arriving in the aorta following each breath. 

# LIMITATIONS
# The input arrays values must both be in assending order and nonnegetive. 

# EXAMPLE
# Leaders array = 3,8,19,36
# Searched array = 1,6,10,16,24
# Followers array = 6 (follows 3), 10 (follows 8), 24 (follows 19)
# Locations array = 1 (location index of 6), 3 (location index of 10), 4 (location index of 24)

# Ignored indices = 1 in Searched array, no leader indice proceeded it
#                   16 in Searched, followed 8 but 10 was closer to 10 so 10 followed and 16 was ignored
#                   36 in Leader array, since no indices in Searched array fell after it.

# INPUTS
# Leaders array: the array of indices that are used to find the proceeding indices of Searched array
# Searched array: the array of indices from which the indices that proceed the indices of Leader array are found and returned


# OUTPUTS
# Followers array: this array contains the indices of Searched array that immediately follow Leader arrays values
# Locations array: this array contains the location indices of the followers in the original Searched array


def proceeding_number_finder(leaders, searched):
    
    import numpy as np
    
    # Initializing arrays
    followers = np.zeros_like(leaders)
    locations = np.zeros_like(leaders)
    i = 0   # the iterater for the followers array
    m = 0   # creating an iterator that is used to avoid re-searching the searched arrays elements that have already been considered
    
    for j in range(0,len(leaders)):
        for k in range(m,len(searched)):
            if j != len(leaders)-1 and searched[k] > leaders[j+1]:
                break
            
            elif searched[k] > leaders[j]:
                followers[i] = searched[k]
                locations[i] = k
                m = k+1
                i+=1
                break
            
    followers = np.trim_zeros(followers,'b')
    locations = np.trim_zeros(locations,'b')
    
    return(followers,locations)
            

# _____________________________________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________________________________
# TESTING FUNCTION

if __name__ == '__main__':

    import numpy as np

    lead = np.array([3,8,19,20,36])
    search = np.array([1,6,10,16,24])
    
    follow,locat = proceeding_number_finder(lead,search)
    