# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 14:40:49 2016

@author: jcb137 written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  

_________________________________________________ UNIQUE x,y PAIRS FUNCTION ________________________________________________________

This function works similar to the numpy.unique() function which takes an array and returns the unique elements along with other
optional outputs such as a count of the occurances of each unique element.

The only issue with numpy.unique is it only works for 1D arrays, if your array isnt 1D it will force it to be by concatenating rows.

So this function instead takes an array of x values and an array of y values which are pairs x,y and returns an x_unique and y_unique
as well as a count array which contains the number of times a unique pair occured.

NB remember x_unique != numpy.unique(x), x_unique are the x values of the unique x,y pairs!!!!!!
EG      x , y  
        1 , 7
        3 , 7
        3 , 5
        1 , 7
        4 , 6
    
So given the array of x and the array of y, this function would return a nx3 matrix were each column is:
 x_unique , y_unique , count
        1 , 7           2
        3 , 7           1
        3 , 5           1
        4 , 6           1

INPUTS --------------------------------------

x: the array of the x coordinates/values
y: the array of the y coordinates/values

OUTPUTS -------------------------------------

x_unique: the x coordinates/values from the unique pairs
y_unique: the y coordinates/values from the unique pairs

count: the number of times each unique pair was observed.

see example above for an example of the output array

"""

def unique_x_y_pairs(x,y):
    
    # IMPORTING NECESSARY MODULES:
    import numpy as np
    if len(x) != len(y):    # if this condition is true then an error statement is produced, followed by the function failing due to len(x) not being equal to len(y)
        print('ERROR: x and y are not the same length!'
              '\nThis function deals with x,y pairs/coordinates and therefore for each x value there should be a corrosponding y')

    # Creating an array of dimension len(x or y)*2, where column one are the x values and column 2 the y values.
    xy = np.column_stack((x, y))   
   
    # The 3rd column in the array a counter where we record the number of times a unique x, y pair was observed.
    unique_xy = np.zeros((len(x), 3))
    
    for pair in xy:
        
        for i, u_row in enumerate(unique_xy):   # u_row will be a row of [unique x, unique y, counter for number of observed pair]
            
            if u_row[2] == 0:   # if the current u_pair row count column is 0 then we know we have looked through all the previously found unique_xy pairs
            
                unique_xy[i,[0,1]] = pair   # adding the current pair to the unique_xy array
                unique_xy[i,2] = 1          # since it is the first pair of its kind to be found, we set the count column to 1
                break                
                
            elif np.array_equal(pair,u_row[0:2]) == True:   # if this is true, the current pair being considered matches a pair already in the unique_xy matirx
                unique_xy[i,2] += 1     # adding one to the counter for that unique pair
                break
    
    unique_xy = unique_xy[~(unique_xy==0).all(1)]   # deleting all rows whose elements are all zeros.
    x_unique = unique_xy[:,0]
    y_unique = unique_xy[:,1]
    count = unique_xy[:,2]
                          
    return(x_unique, y_unique, count)
    
    
#%% ------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------     
    
# Testing the function
    
if __name__ == "__main__":
    import numpy as np
    x = np.random.randint(0,2,10)
    x = np.random.randint(0,2,10)

    unique_xy = unique_x_y_pairs(x,y)
    