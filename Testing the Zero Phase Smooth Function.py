# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 10:17:18 2016

@author: jcb137
"""

# ---__________________________________________________________ DESCRIPTION ______________________________________________________________________________

# This function was made to look at how smoothing shifts peaks in time. Causal smoothing quite obviously would delay peaks to appear but it was expected
# central smoothing would not cause a phase shift. However what was not forseen is that smoothing still has the effect of changing the magnitude of the
# frequency spectrum. It still a form of filter! So by changing the frequency through filtering you may still lead to shifting peaks!

# This was confirmed by looking at the central smooth after a single smooth, some of the peaks have been shifted. Even when the signal goes through
# the smoothing a second time in reverse (like filt-filt in matlab, ie zero phase shift filter), the peaks of the central smooth are still the same
# as the shift wasnt due to a phase shift.

# ---_______________________________________________________ TESTING FUNCITION____________________________________________________________________________

# Importing modules
import numpy as np
import matplotlib.pyplot as plt
import sys

# --- IMPORTING FUNCTION ______________________________________
sys.path.append(r'C:\Users\jcb137\OneDrive\Python\General Functions')
from Smooth import zero_phase_shift_smooth   
from Smooth import central_smooth
from Smooth import causal_smooth
from Adaptive_Find_Peaks import max_peak_finder

# ---_____________________________________________ DEFINING FUNCTIONS SPECIFIC TO THIS FILE _____________________________________________________

#  RECTANGULAR CAUSAL SMOOTHING ___________________________________

# This is a rectangular central smooth function. It is like my central smooth function except it differs in how it handles the start
# and end points.

# Consider a signal y that is 100 points long and is being smoothed with a 7 point central smooth:

# y_smoothed[0] = y[0]/7
# y_smoothed[1] = (y[0] + y[1] + y[2])/7
# y_smoothed[2] = (y[0] + y[1] + y[2] + y[3] + y[4])/7
# y_smoothed[3] = (y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6])/7
# y_smoothed[4] = (y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7])/7
# .
# .
# .
# y_smoothed[95] = (y[92] + y[93] + y[94] + y[95] + y[96] + y[97] + y[98])/7
# y_smoothed[96] = (y[93] + y[94] + y[95] + y[96] + y[97] + y[98] + y[99])/7
# y_smoothed[97] = (y[95] + y[96] + y[97] + y[98] + y[99])/7
# y_smoothed[98] = (y[97] + y[98] + y[99])/7
# y_smoothed[99] = y[99]/7
    
def rect_central_smooth(signal, points_in_rolling_average):
    
    # Creating a simple function which will be used to check if points_in_rolling_average is an odd number
    def odd_number_checker(number_to_check):
        if number_to_check%2 == 0:  # if this condition is true then the number is even
            re_entered_number_to_check = int(input('Number of points used in rolling average should be odd, please re-enter the number: '))
            return(odd_number_checker(re_entered_number_to_check))
        return(number_to_check)
        
    #Using the function to check the points_in_rolling_average input
    points_in_rolling_average = odd_number_checker(points_in_rolling_average)
    
    import numpy
    smoothed_signal = numpy.zeros([len(signal)])
    
    for i in range(0,len(signal)):
        
        if i == 0:
            smoothed_signal[0] = signal[0]/points_in_rolling_average

        elif i <= (points_in_rolling_average-1)/2:
            smoothed_signal[i] = numpy.sum(signal[0:i+i+1])/points_in_rolling_average # if confused by this expression see the example in the function description AND remember that the stop condition value isnt used!
        
        elif i >= len(signal) - (points_in_rolling_average-1)/2:
            smoothed_signal[i] = numpy.sum(signal[i-((len(signal)-i)-1):])/points_in_rolling_average
            
        else:            
            smoothed_signal[i] = (signal[i-int((points_in_rolling_average -1)/2): i+(int((points_in_rolling_average-1)/2))+1].mean()) # Plus on in the stop argument ensures our stop point is more more than our forward most point we are averaging with.
        
    return(smoothed_signal)
    
#  RECTANGULAR CAUSAL SMOOTHING ___________________________________________

# This function is a rectangular causal smooth meaning the rolling average only uses current and past data points with a rect function.
# It is like my causal smooth function except in how it handles start and end points.
# Consider a signal y that is 100 points long and is being smoothed with a 4 point causal smooth:

# y_smoothed[0] = y[0]/4
# y_smoothed[1] = (y[0] + y[1])/4
# y_smoothed[2] = (y[0] + y[1] + y[2])/4
# y_smoothed[3] = (y[0] + y[1] + y[2] + y[3])/4
# y_smoothed[4] = (y[1] + y[2] + y[3] + y[4])/4
# .
# .
# .
# y_smoothed[99] = (y[96] + y[97] + y[98] + y[99])/4


# INPUTS: 
# signal: either an array of numbers you want to smooth
# points_in_rolling_average: number of points used in the rolling average. NB this number should be odd.
    
def rect_causal_smooth(signal, points_in_rolling_average):
    
    # Creating a simple function which will be used to check if points_in_rolling_average is an odd number
    def odd_number_checker(number_to_check):
        if number_to_check%2 == 0:  # if this condition is true then the number is even
            re_entered_number_to_check = int(input('Number of points used in rolling average should be odd, please re-enter the number: '))
            return(odd_number_checker(re_entered_number_to_check))
        return(number_to_check)
        
    #Using the function to check the points_in_rolling_average input
    points_in_rolling_average = odd_number_checker(points_in_rolling_average)
    
    import numpy
    smoothed_signal = numpy.zeros([len(signal)])
    
    for i in range(0,len(signal)):
        
        if i == 0:
            smoothed_signal[0] = signal[0]/points_in_rolling_average

        elif i <= points_in_rolling_average-1:
            smoothed_signal[i] = numpy.sum(signal[0:i+1])/points_in_rolling_average # if confused by this expression see the example in the function description AND remember that the stop condition value isnt used!
            
        else:            
            smoothed_signal[i] = numpy.sum(signal[i-(points_in_rolling_average-1):i+1])/points_in_rolling_average # Plus on in the stop argument ensures our stop point is more more than our forward most point we are averaging with.
        
    return(smoothed_signal)




# ---____________________________________________________________ RUNS SPACE ___________________________________________________
# below is a wave constructed out of sin waves of different frequencies.
t = np.linspace(0,2,1000) # time array

one_hert = 4*(np.cos(t*1*2*np.pi))  # one hert contribution
two_hert = 3*(np.cos(t*2*2*np.pi))  # two hert contribution
three_hert = 6*(np.cos(t*3*2*np.pi)) # three hert contribution
four_hert = 5*(np.cos(t*4*2*np.pi))  # four hert contribution

signal = 2 + one_hert + two_hert + three_hert + four_hert 

# Plotting the raw waveform contributors and the total
plt.figure
plt.title('Signal Created from Addition of Cosine Waves')
plt.xlabel('time (s)')
plt.ylabel('y')
plt.plot(t,2*np.ones(len(t)), 'red', label = 'DC contribution')     # plotting the DC offset of 2
plt.plot(t,one_hert, 'orange', label = '1 Hz contribution')
plt.plot(t,two_hert, 'purple', label = '2 Hz contribution')
plt.plot(t,three_hert, 'green', label = '3 Hz contribution')
plt.plot(t,four_hert, 'deepskyblue', label = '4 Hz contribution')
plt.plot(t,signal, 'royalblue', linewidth = '2', label = 'Combined Signal')
plt.legend(fontsize = 'small')

# Smoothing ------------------------------------------

# Causal Smoothing
causal_smooth_wave = causal_smooth(signal, 51)
rect_causal_smooth_wave = rect_causal_smooth(signal, 51)
fb_causal_smooth_wave = causal_smooth(causal_smooth_wave[::-1], 51)[::-1]     # NB fb stands for forward and backward signifying we are trying to achieve zero phase shift
fb_rect_causal_smooth_wave = rect_causal_smooth(rect_causal_smooth_wave[::-1],51)[::-1]     # NB fb stands for forward and backward signifying we are trying to achieve zero phase shift

# Central Smoothing
central_smooth_wave = central_smooth(signal, 51)
rect_central_smooth_wave = rect_central_smooth(signal, 51)
fb_central_smooth_wave = zero_phase_shift_smooth(signal, 51)     # NB fb stands for forward and backward signifying we are trying to achieve zero phase shift
fb_rect_central_smooth_wave = rect_central_smooth(rect_central_smooth_wave[::-1],51)[::-1]     # NB fb stands for forward and backward signifying we are trying to achieve zero phase shift

# Conducting Peak Analysis -----------------------------

# Raw Signal
signal_peak_detection_outputs = max_peak_finder(signal, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 201, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
signal_peak_indices = signal_peak_detection_outputs[0]
signal_peak_detection_thresholds = signal_peak_detection_outputs[2]
signal_peak_detection_outer_crossing_indices = signal_peak_detection_outputs[3]
signal_peak_detection_ignored_max_indices = signal_peak_detection_outputs[5]

# Causally Smoothed Signal
causal_smooth_peak_detection_outputs = max_peak_finder(causal_smooth_wave, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 101, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
causal_smooth_peak_indices = causal_smooth_peak_detection_outputs[0]
causal_smooth_peak_detection_thresholds = causal_smooth_peak_detection_outputs[2]
causal_smooth_peak_detection_outer_crossing_indices = causal_smooth_peak_detection_outputs[3]
causal_smooth_peak_detection_ignored_max_indices = causal_smooth_peak_detection_outputs[5]

rect_causal_smooth_peak_detection_outputs = max_peak_finder(rect_causal_smooth_wave, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 101, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
rect_causal_smooth_peak_indices = rect_causal_smooth_peak_detection_outputs[0]
rect_causal_smooth_peak_detection_thresholds = rect_causal_smooth_peak_detection_outputs[2]
rect_causal_smooth_peak_detection_outer_crossing_indices = rect_causal_smooth_peak_detection_outputs[3]
rect_causal_smooth_peak_detection_ignored_max_indices = rect_causal_smooth_peak_detection_outputs[5]

fb_causal_smooth_peak_detection_outputs = max_peak_finder(fb_causal_smooth_wave, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 101, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
fb_causal_smooth_peak_indices = fb_causal_smooth_peak_detection_outputs[0]
fb_causal_smooth_peak_detection_thresholds = fb_causal_smooth_peak_detection_outputs[2]
fb_causal_smooth_peak_detection_outer_crossing_indices = fb_causal_smooth_peak_detection_outputs[3]
fb_causal_smooth_peak_detection_ignored_max_indices = fb_causal_smooth_peak_detection_outputs[5]

fb_rect_causal_smooth_peak_detection_outputs = max_peak_finder(fb_causal_smooth_wave, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 101, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
fb_rect_causal_smooth_peak_indices = fb_rect_causal_smooth_peak_detection_outputs[0]
fb_rect_causal_smooth_peak_detection_thresholds = fb_rect_causal_smooth_peak_detection_outputs[2]
fb_rect_causal_smooth_peak_detection_outer_crossing_indices = fb_rect_causal_smooth_peak_detection_outputs[3]
fb_rect_causal_smooth_peak_detection_ignored_max_indices = fb_rect_causal_smooth_peak_detection_outputs[5]

# Centrally Smoothed Signal
central_smooth_peak_detection_outputs = max_peak_finder(central_smooth_wave, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 101, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
central_smooth_peak_indices = central_smooth_peak_detection_outputs[0]
central_smooth_peak_detection_thresholds = central_smooth_peak_detection_outputs[2]
central_smooth_peak_detection_outer_crossing_indices = central_smooth_peak_detection_outputs[3]
central_smooth_peak_detection_ignored_max_indices = central_smooth_peak_detection_outputs[5]

rect_central_smooth_peak_detection_outputs = max_peak_finder(rect_central_smooth_wave, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 101, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
rect_central_smooth_peak_indices = rect_central_smooth_peak_detection_outputs[0]
rect_central_smooth_peak_detection_thresholds = rect_central_smooth_peak_detection_outputs[2]
rect_central_smooth_peak_detection_outer_crossing_indices = rect_central_smooth_peak_detection_outputs[3]
rect_central_smooth_peak_detection_ignored_max_indices = rect_central_smooth_peak_detection_outputs[5]

fb_central_smooth_peak_detection_outputs = max_peak_finder(fb_central_smooth_wave, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 101, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
fb_central_smooth_peak_indices = fb_central_smooth_peak_detection_outputs[0]
fb_central_smooth_peak_detection_thresholds = fb_central_smooth_peak_detection_outputs[2]
fb_central_smooth_peak_detection_outer_crossing_indices = fb_central_smooth_peak_detection_outputs[3]
fb_central_smooth_peak_detection_ignored_max_indices = fb_central_smooth_peak_detection_outputs[5]

fb_rect_central_smooth_peak_detection_outputs = max_peak_finder(fb_rect_central_smooth_wave, threshold = 'unspecified', vert_offset = 'unspecified' , window_length = 101, min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified')
fb_rect_central_smooth_peak_indices = fb_rect_central_smooth_peak_detection_outputs[0]
fb_rect_central_smooth_peak_detection_thresholds = fb_rect_central_smooth_peak_detection_outputs[2]
fb_rect_central_smooth_peak_detection_outer_crossing_indices = fb_rect_central_smooth_peak_detection_outputs[3]
fb_rect_central_smooth_peak_detection_ignored_max_indices = fb_rect_central_smooth_peak_detection_outputs[5]

# Plotting comparison of smoothed waveform
single_smooths = plt.figure()
single_smooths.canvas.set_window_title('Single Smooths')
plt.title('Comparison of Single Smoothing Techniques')
plt.xlabel('time')
plt.ylabel('y')
plt.plot(t,signal, 'black', linewidth = '2')
plt.plot(t,causal_smooth_wave, 'darkblue')
plt.plot(t,central_smooth_wave, 'darkred')
plt.plot(t,rect_causal_smooth_wave, 'darkgreen')
plt.plot(t,rect_central_smooth_wave, 'darkorange')
plt.legend(labels = ['Unsmoothed Signal','Causal Smooth', 'Central Smooth', 'Rectanglar Causal Smooth', 'Rectangular Central Smooth'], fontsize = 'small')

# Plotting peak indices
plt.plot(t[signal_peak_indices], signal[signal_peak_indices], 'ko')
plt.plot(t[causal_smooth_peak_indices], causal_smooth_wave[causal_smooth_peak_indices], 'bo')
plt.plot(t[central_smooth_peak_indices], central_smooth_wave[central_smooth_peak_indices], 'ro')
plt.plot(t[rect_causal_smooth_peak_indices], rect_causal_smooth_wave[rect_causal_smooth_peak_indices], 'go')
plt.plot(t[rect_central_smooth_peak_indices], rect_central_smooth_wave[rect_central_smooth_peak_indices], color = 'orange', marker = 'o', linewidth = 0)

# Plotting comparison of smoothing techiques after using them twice,
# once forward and once backwards to see if they remove phase distortion
fb_smooths = plt.figure()
fb_smooths.canvas.set_window_title('Forward-Backward Smooths')
plt.title('Comparison of Forward-Backward Smoothing Techniques')
plt.xlabel('time')
plt.ylabel('y')
plt.plot(t,signal, 'black', linewidth = '2')
plt.plot(t,fb_causal_smooth_wave, 'darkblue')
plt.plot(t,fb_central_smooth_wave, 'darkred')
plt.plot(t,fb_rect_causal_smooth_wave, 'darkgreen')
plt.plot(t,fb_rect_central_smooth_wave, 'darkorange')
plt.legend(labels = ['Unsmoothed Signal','Causal Smooth', 'Central Smooth', 'Rectanglar Causal Smooth', 'Rectangular Central Smooth'], fontsize = 'small')

# Plotting peak indices
plt.plot(t[signal_peak_indices], signal[signal_peak_indices], 'ko')
plt.plot(t[fb_causal_smooth_peak_indices], fb_causal_smooth_wave[fb_causal_smooth_peak_indices], 'bo')
plt.plot(t[fb_central_smooth_peak_indices], fb_central_smooth_wave[fb_central_smooth_peak_indices], 'ro')
plt.plot(t[fb_rect_causal_smooth_peak_indices], fb_rect_causal_smooth_wave[fb_rect_causal_smooth_peak_indices], 'go')
plt.plot(t[fb_rect_central_smooth_peak_indices], fb_rect_central_smooth_wave[fb_rect_central_smooth_peak_indices], color = 'orange', marker = 'o', linewidth = 0)

# Plotting thresholds
#plt.plot(t, signal_peak_detection_thresholds, 'k')
#plt.plot(t, zero_phase_smoothed_peak_detection_thresholds, 'k')
#plt.plot(t,single_smooth_peak_detection_thresholds, 'k')

# Plotting outer crossings
#plt.plot(t[signal_peak_detection_outer_crossing_indices], signal[signal_peak_detection_outer_crossing_indices], 'cd')
#plt.plot(t[zero_phase_smoothed_detection_outer_crossing_indices], zero_phase_smoothed_wave[zero_phase_smoothed_detection_outer_crossing_indices], 'cd')
#plt.plot(t[single_smooth_peak_detection_outer_crossing_indices], single_smooth[single_smooth_peak_detection_outer_crossing_indices], 'cd')

# Plotting ignored max indices
#plt.plot(t[signal_peak_detection_ignored_max_indices], signal[signal_peak_detection_ignored_max_indices], 'c*')
#plt.plot(t[zero_phase_smoothed_detection_ignored_max_indices], zero_phase_smoothed_wave[zero_phase_smoothed_detection_ignored_max_indices], 'c*')
#plt.plot(t[single_smooth_peak_detection_ignored_max_indices], single_smooth[single_smooth_peak_detection_ignored_max_indices], 'c*')