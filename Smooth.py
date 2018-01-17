# -*- coding: utf-8 -*-
"""
Created on Fri May 13 13:19:35 2016

@author: jcb137
"""

# ----------------------------------------------- CENTRAL SMOOTHING FUNCTION ------------------------------------------
# this just takes the central rolling average of a signal, like the matlab smooth fucntion. 

# As you step through the signal points, indices < (points_in_rolling_average-1)/2 cannot be centrally averaged
# (ie there arent enough previous points!) so they get special treatment as follows:

# Consider a signal y that is 100 points long and is being smoothed with a 7 point central smooth:

# y_smoothed[0] = y[0]
# y_smoothed[1] = (y[0] + y[1] + y[2])/3
# y_smoothed[2] = (y[0] + y[1] + y[2] + y[3] + y[4])/5
# y_smoothed[3] = (y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6])/7
# y_smoothed[4] = (y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7])/7
# .
# .
# .
# y_smoothed[95] = (y[92] + y[93] + y[94] + y[95] + y[96] + y[97] + y[98])/7
# y_smoothed[96] = (y[93] + y[94] + y[95] + y[96] + y[97] + y[98] + y[99])/7
# y_smoothed[97] = (y[95] + y[96] + y[97] + y[98] + y[99])/5
# y_smoothed[98] = (y[97] + y[98] + y[99])/3
# y_smoothed[99] = y[99]


# INPUTS: 
# signal: either an array of numbers you want to smooth
# points_in_rolling_average: number of points used in the rolling average. NB this number should be odd.

def central_smooth(signal, points_in_rolling_average):
    
    # Creating a simple function which will be used to check if points_in_rolling_average is an odd number
    def odd_number_checker(number_to_check):
        if number_to_check%2 == 0:  # if this condition is true then the number is even
            re_entered_number_to_check = int(input('Number of points used in rolling average should be odd, please re-enter the number: '))
            return(odd_number_checker(re_entered_number_to_check))
        return(number_to_check)
    
    #Using the function to check the points_in_rolling_average input
    points_in_rolling_average = odd_number_checker(points_in_rolling_average)
    
    from numpy import zeros  
    smoothed_signal = zeros([len(signal)])
    
    for i in range(0,len(signal)):
        
        if i == 0:
            smoothed_signal[0] = signal[0] 

        elif i <= (points_in_rolling_average-1)/2:
            smoothed_signal[i] = (signal[0:i+i+1].mean()) # if confused by this expression see the example in the function description AND remember that the stop condition value isnt used!
        
        elif i >= len(signal) - (points_in_rolling_average-1)/2:
            smoothed_signal[i] = (signal[i-((len(signal)-i)-1):].mean())
            
        else:            
            smoothed_signal[i] = (signal[i-int((points_in_rolling_average -1)/2): i+(int((points_in_rolling_average-1)/2))+1].mean()) # Plus on in the stop argument ensures our stop point is more more than our forward most point we are averaging with.
        
    return(smoothed_signal)

# ---_______________________________ CAUSAL SMOOTHING FUNCTION _________________________________________________________

# This function is a causal smooth meaning the rolling average only uses current and past data points.
# Consider a signal y that is 100 points long and is being smoothed with a 4 point causal smooth:

# y_smoothed[0] = y[0]
# y_smoothed[1] = (y[0] + y[1])/2
# y_smoothed[2] = (y[0] + y[1] + y[2])/3
# y_smoothed[3] = (y[0] + y[1] + y[2] + y[3])/4
# y_smoothed[4] = (y[1] + y[2] + y[3] + y[4])/4
# .
# .
# .
# y_smoothed[99] = (y[96] + y[97] + y[98] + y[99])/4


# INPUTS: 
# signal: either an array of numbers you want to smooth
# points_in_rolling_average: number of points used in the rolling average. NB this number should be odd.

def causal_smooth(signal, points_in_rolling_average):
    
    # Creating a simple function which will be used to check if points_in_rolling_average is an odd number
    def odd_number_checker(number_to_check):
        if number_to_check%2 == 0:  # if this condition is true then the number is even
            re_entered_number_to_check = int(input('Number of points used in rolling average should be odd, please re-enter the number: '))
            return(odd_number_checker(re_entered_number_to_check))
        return(number_to_check)
        
    #Using the function to check the points_in_rolling_average input
    points_in_rolling_average = odd_number_checker(points_in_rolling_average)
    
    from numpy import zeros  
    smoothed_signal = zeros([len(signal)])
    
    for i in range(0,len(signal)):
        
        if i == 0:
            smoothed_signal[0] = signal[0] 

        elif i <= points_in_rolling_average-1:
            smoothed_signal[i] = (signal[0:i+1].mean()) # if confused by this expression see the example in the function description AND remember that the stop condition value isnt used!
            
        else:            
            smoothed_signal[i] = ((signal[i-(points_in_rolling_average-1):i+1]).mean()) # Plus on in the stop argument ensures our stop point is more more than our forward most point we are averaging with.
        
    return(smoothed_signal)
    

# ---_______________________________ ZERO PHASE SHIFT SMOOTHING FUNCTION _________________________________________________________

# This function will apply the central smooth function twice to a signal. The first time will cause a phase shift, but by reversing the output
# of the first smooth and putting through the filter the same phase shift occurs but back in the opposite direction, cancelling the first
# shift.    
    
def zero_phase_shift_smooth(signal, points_in_rolling_average):
    first_smooth = central_smooth(signal, points_in_rolling_average)
    second_smooth = central_smooth(first_smooth[::-1], points_in_rolling_average)
    smoothed_signal = second_smooth[::-1]
    
    return(smoothed_signal)




        