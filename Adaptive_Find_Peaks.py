# -*- Adaptive Find Peaks Algorithum -*-
"""
Created on Wed Feb 10 11:14:22 2016

@author: jcb137 written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  

""" 

# ----------------------------------------------- BASIC PEAK FINDER -------------------------------------------------

# This function looks at points that are above the threshold and if a points two neighbouring points are smaller it concludes a 
# peak has been found.

# INPUTS ---------------------

# signal: array of full signal you are interested in finding peaks for
# threshold: the min value a data point can be for it to be considered a peak

def basic_peak_finder(signal, threshold = 'unspecified'):       # if thershold isnt specified it defaults it is replaced with the mean of the signal
    
    # -------------------------------------------  IMPORTED MODULES -----------------------------------------------
    from numpy import array, int_, append
    
    # -------------------------------------------------------------------------------------------------------------    

    # Checking inputs   

    if threshold == 'unspecified':
        threshold = signal.mean()
        
    # Initializing variables

    peak_index = int_([])                           # initializing a peak_index array where the index of the peak in the signal array will be stored as integers
    peak_value = array([])                          # initializing a peak_value array where the peak values will be stored
       
    # Performing function
    for i in range(1,signal.size-1):        # The reason we start at i = 1 and stop at signal.size-1 is inside the loop we compare signal[i] with its neighbours
                                            # for the first element it doesnt have a neighbour to its left and for the final element it doesnt have a neighbour to
                                            # its right and therefore would through an error.
    
        # With the threshold calculated we now check to see if the current point meets the criteria to be a peak
        if signal[i] >= threshold and signal[i] > signal[i-1]:  # checking that the current point of interest is above the threshold and above its previous neighbour
            j = 1
            
            while signal[i] == signal[i+j]: # If you have a point in the signal consisting of multiple signals, to see if you have a peak you must see if the point AFTER the flat part of the signal decreases! 
                j = j + 1                   # to do this we must step along the flat part of the signal until the gradient of the signal changes. then as seen below we check to see if the point at the change
                                            # in gradient is lower than our flat section. If it is, then the flat section is infact a peak. The index of this peak is considered to be the left most point in the flat section.
            
            # Second criteria to be a peak is that the neighbouring point must be less than signal[i]     
            if signal[i] > signal[i+j]:     # signal[i+j] will be the first point after signal[i] that isnt equal to signal[i]. see earlier notes for while statement
                peak_index = append(peak_index,i)
                peak_value = append(peak_value,signal[i])

            
    return(peak_index, peak_value)
    
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------    
    
    
    # DELETE THE BELOW FUNCTION DESCRIPTION IF NOT FINISHED
# ----------------------------------------------- DISCRETE MAX FINDER -------------------------------------------------

# This function takes an input signal and is given start and end indices to search between in the signal for a max value
# it is useful for finding a max where you know one should be. 

#For example finding the point of inflection in a pressure wveform:
# for a given beat if you know roughly where the foot of the waveform is (eg from an ECG R-wave time or just min of the
# pressure waveform) and you know when the max pressure is then you know between those is an inflection point. If you 
# pass the time derivative of the pressure waveform, along with the foot indice and the max indice then the max of the
# derivative of the pressure waveform between the indices will be the point of inflection of the pressure rise on the
# pressure signal.

# INPUTS ---------------------

# signal: array of full signal you are interested in finding peaks for
# start_index: indice to start searching from
# end_index: indice to stop searching from

# OUTPUTS --------------------
# max_index:  index of max in the signal
    
    
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------    
    

# ----------------------------------------------- ADAPTIVE PEAK FINDER -------------------------------------------------

# This function looks at points that are above the threshold and if a points two neighbouring points are smaller it concludes a 
# peak has been found. The threshold is adaptive, calculated as the mean over a certain number of points eitherside
# of the point of interest with a vertical offset then added.

# The function also includes the option of a min_peak_distance condtion where a local peak is only considered to be a peak if it
# is far enough away from a previously identified peak

# INPUTS ---------------------

# signal: array of full signal you are interested in finding peaks for
# vert_offset: the threshold is calculated as the mean + vert_offset
# window_length: window length defines the number of points in the moving average used to calculate the moving threshold. It must be odd as we want an even number of points either side of the current point of interest.
# min_peak_distance = minimum number of data points a possible peak must be from the previous positively identified peak. This is best worked out seperately.

def adaptive_peak_finder(signal, vert_offset = 'unspecified' , window_length = 'unspecified', min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified'):       # if threshold isnt specified it defaults it is replaced with the mean of the signal
    
    # -------------------------------------------  IMPORTED MODULES -----------------------------------------------
    from numpy import array, int_, append, zeros, ceil, trim_zeros
    
    # -------------------------------------------------------------------------------------------------------------    
    # Checking inputs

    if vert_offset == 'unspecified':
        print('No vert_offset was entered, therefore default of 0 will be used making the threshold = moving mean')          
        vert_offset = 0
        
    if window_length == 'unspecified':
        print('ERROR, no window_length was provided, if you dont want to update the threshold use the basic_peak_finder function')
        window_length = int(input('Please re-enter the window length: '))
        return(adaptive_peak_finder(signal, vert_offset, window_length))
    
    if window_length%2 == 0:
        print('ERROR, an even number was entered for the window length, the window length should be odd')
        window_length = int(input('Please re-enter the window length: '))
        return(adaptive_peak_finder(signal, vert_offset, window_length))
          
    # Initializing varibles (NB when initializing, the most peaks possible would come from a sawtooth wave
    # where every point was either a peak or trough, therefore arrays are initialized to half the signal
    # input length)
    peak_index = zeros(int(ceil(len(signal)/2)), dtype = int_)                  # initializing a peak_index array where the index of the peak in the signal array will be stored as integers
    peak_value = zeros(int(ceil(len(signal)/2)))                  # initializing a peak_value array where the peak values will be stored
    m = 0   # m is the iterator that will step through peak_ arrays indices filling the array with the peak locations and values
    
    ignored_peak_index = zeros(int(ceil(len(signal)/2)), dtype = int_)          # initializing an ignored_peak_index array where the index of the peak that didnt meet the min distance requirement between it and the previous peak are stored.
    ignored_peak_value = zeros(int(ceil(len(signal)/2)))          # initializing a ignored_peak_value array where the ignored peak values that didnt meet the min distance requirement between it and the previous peak will be stored
    k = 0   # k is the iterator that will step through ignored_peak_ arrays indices filling the array with the ignored peak locations and values    
    
    thresholds = zeros(len(signal)-1)
    thresholds[0] = (signal[0:int((window_length-1)/2)+1].mean())+ vert_offset         # creating a list to store the thresholds as these can be graphed or used for debugging
                                                                                       # NB the first threshold point is also initilized within. 

    for i in range(1,signal.size-1):      # NB the reason we start at i=1 is because the threshold list is initilized with the threshold for i=0 in it, see above.
                                          # Also the reason we stop at signal.size-1 is we need to stop and not go through the loop for the final element in signal
                                          # because inside the loop we look at signal[i+1] which doesnt exist if i = final element in signal.
        
        # Calculating threshold at each point
        if i <= (window_length-1)/2:
            window_mean = (signal[0: i+(int((window_length-1)/2))+1].mean())                                                # NB we need to add one to the stop point as we want to include index i+(window-1)/2 in the window mean calc
            thresholds[i] = window_mean + vert_offset            
            
        elif i >= signal.size - (window_length-1)/2:
            window_mean = (signal[i-int((window_length-1)/2): signal.size].mean())                                          # NB we dont need to add one to the stop point as a stop point of signal.size = len(signal) defines the stop point as the end of signal
            thresholds[i] = window_mean + vert_offset                                                                           # Incase the threshold is -ve, we need to work out the threshold this way rather than just window_mean*multiple of mean

        else :
            window_mean = (signal[i-int((window_length-1)/2): i+(int((window_length -1)/2))+1].mean())        # NB we need to add one to the stop point as we want to include index i+(window-1)/2 in the threshold calc        
            thresholds[i] = window_mean + vert_offset                                                                           # Incase the threshold is -ve, we need to work out the threshold this way rather than just window_mean*multiple of mean
        
        # With the threshold calculated we now check to see if the current point meets the criteria to be a peak
        if signal[i] >= thresholds[i] and signal[i] > signal[i-1]:  # checking that the current point of interest is above the threshold and above its previous neighbour
            j = 1
            
            while signal[i] == signal[i+j]: # If you have a point in the signal consisting of multiple signals, to see if you have a peak you must see if the point AFTER the flat part of the signal decreases! 
                j = j + 1                   # to do this we must step along the flat part of the signal until the gradient of the signal changes. then as seen below we check to see if the point at the change
                                            # in gradient is lower than our flat section. If it is, then the flat section is infact a peak. The index of this peak is considered to be the left most point in the flat section.
            
            # Second criteria to be a peak is that the neighbouring point must be less than signal[i]     
            if signal[i] > signal[i+j]:     # signal[i+j] will be the first point after signal[i] that isnt equal to signal[i]. see earlier notes for while statement
                
                if min_peak_distance != 'unspecified' and peak_index[0] != 0 and i - peak_index[m-1] < min_peak_distance:        # this condition is only true if min_peak_distance has been specified and and if it is far enough from the previous positively identified peak we have found at least one previous peak needed to compare the min_peak_distance to.  
                    ignored_peak_index[k] = i           # we store the ignored peak data incase the user wants to check what was ignored in the signal
                    ignored_peak_value[k] = signal[i]
                    k = k+1     # k is used to step through ignored_peak arrays as an index is filled
                        
                elif min_amount_from_threshold != 'unspecified' and abs(signal[i] - thresholds[i]) < min_amount_from_threshold:    # we can set an amount a peak must be above the threshold for it to be a true peak, this is handy for when a signal may jump around the threshold a tiny amount and may not be an actual peak.
                    ignored_peak_index[k] = i           # we store the ignored peak data incase the user wants to check what was ignored in the signal
                    ignored_peak_value[k] = signal[i]
                    k = k+1     # k is used to step through ignored_peak arrays as an index is filled
                    
                else:                                                   # You need the peak_index and peak_value twice, once for if min_peak_distance is specified and once for if it isnt
                    peak_index[m] = i
                    peak_value[m] = signal[i]
                    m = m+1     # m is used to step through peak_ arrays as an index is filled
                    
    # trimming all unfilled indices of peak_index, peak_value, ignored_peak_index and ignored_peak_values
    peak_index = trim_zeros(peak_index)   # as we cannot possible have a peak at an index location 0, we can trim peak_index and use its length to define the peak_value array. As a peaks value could be 0, so we cant use the trim_zeros function of the peak_value array.
    peak_value = peak_value[:len(peak_index)]   # trimming the peak_value array to the length of peak_index, as they must be the same length, each index is information on the same peak.
    
    ignored_peak_index = trim_zeros(ignored_peak_index)   # the code is such that we cannot possible have an ignored_peak at an index location 0, so we can trim peak_index and use its length to define the ignored_peak_value array. As an ignored_peak_value could be 0, so we cant use the trim_zeros function of that array.
    ignored_peak_value = ignored_peak_value[:len(ignored_peak_index)]# trimming the ignored_peak_value array to the length of ignored_peak_index, as they must be the same length, each index is information on the same peak.
    
         
    return(peak_index, peak_value, ignored_peak_index, ignored_peak_value, thresholds)          # a list of the thresholds is stored so it can be plotted or used for debugging purposes

# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

# --------------------------------------------- MAX PEAK FINDER ---------------------------------------------------------

# The function is similar to the basic peak finder, but instead of finding all peaks above the threshold, it looks for  
# 3 crossings of the threshold signifiying there will be a peak and trough between the two outer crossings. This means if there
# are a few peaks/troughs within 3 crossing that only the largest peak/trough is considered.

# EXCEPTIONS
# If the signal ends with an inner crossing, and the points in the signal between the inner crossing and its prior outer
# crossing are above the threshold, we can still be sure there was a max peak in there. This exception is handed in
# using the end_check boolian variable

# THINGS TO NOTE:
# If the signal has a very prominant peak consisting of only one or two data points it is possible to have a crossing point as
# a peaks, this can results in two peaks being between two outer crossings and as the maximum is taken, the other peak being 
# missed. This can occur on signals such as ECG, but more smooth signals have less of this problem.

# LIMITATIONS
# It is possible that the first peak can be missed if the signal begins above the threshold, therefore the first crossing
# is a -ve gradient crossing which could have been preceeded by a peak, but as only one crossing has occured it would be 
# missed. If the first crossing is negetive, you could look between the start of the signal and the first crossing for a peak
# but even if you find a local peak, there is no guarantee that it is the max peak in a period, if the signal before the first
# crossing is short, you may have just found a local peak and this algorithms design intent was to avoid those! Hence it
# doesnt consider signal before the first crossing. Similarly, you can have a peak at the end of the signal that is missed. 
    
# You could implement a fancy check where if you look at the start/end of the signal before/after the first/last crossing and
# find a local peak, you could check with resonable likelihood if it is a peak by finding the mean distance peaks within
# the signal are from there crossings. But again this hasnt been implemented.

# INPUTS --------------------------
# signal: array of full signal you are interested in finding peaks for
# threshold: can either be a single value chosen by the user, or if not given will be a moving average of the signal based on the window length.
# initial_thres: lets you manually set the first point in the signals thereshold independently. If initial_threshold = 'unspecified' AND thershold was specified, initial_threshold = threshold, else if initial_threshold and threshold both were unspecified, initial_thres defaults to the mean of a window length OR if threthe value 
# vert_offset: the threshold is calculated as the mean + vert_offset
# window_length: window length defines the number of points in the moving average used to calculate the moving threshold. It must be odd as we want an even number of points either side of the current point of interest.
# min_peak_distance: minimum number of data points a possible peak must be from the previous positively identified peak. This is best worked out seperately.
# min_amount_from_threshold: minimum amount a peak must be from the threhold, meaning if it gets too close it is still ignored... was useful at some point so I wouldnt remove this feature!
# peak_value_consistancy_fraction: another optional user input. If the signal peaks are expected to be fairly consistant, peak_value_consistancy_fraction input can be a fraction = x, where a suspected peak must have a value satisfying: (1-x)*previous peak value < suspected peak value < (1+x)*previous peak value, for the suspected peak to be considered a true peak. 


def max_peak_finder(signal, threshold = 'unspecified', initial_thres = 'unspecified', vert_offset = 'unspecified' , window_length = 'unspecified', min_peak_distance = 'unspecified', min_amount_from_threshold = 'unspecified', peak_value_consistancy_fraction = 'unspecified'):       # if thershold isnt specified it defaults it is replaced with the mean of the signal
    
    # -------------------------------------------  IMPORTED MODULES -----------------------------------------------
    from numpy import array, int_, append, argmax, argsort, zeros, ceil, trim_zeros
    # -------------------------------------------------------------------------------------------------------------

    # Checking inputs      
    if threshold == 'unspecified': 

        if vert_offset == 'unspecified':
            # No vert_offset was entered, therefore default of 0 will be used making the threshold = moving mean        
            vert_offset = 0
        
        if window_length == 'unspecified':
            print('ERROR, no window_length was provided, if you dont want to update the threshold use the basic_peak_finder function')
            window_length = int(input('Please re-enter the window length: '))
            return(max_peak_finder(signal, threshold, vert_offset, window_length, min_peak_distance, min_amount_from_threshold,peak_value_consistancy_fraction))
    
        if window_length%2 == 0:
            print('ERROR, an even number was entered for the window length, the window length should be odd')
            window_length = int(input('Please re-enter the window length: '))
            return(max_peak_finder(signal, threshold, vert_offset, window_length, min_peak_distance, min_amount_from_threshold,peak_value_consistancy_fraction))
            
        if peak_value_consistancy_fraction != 'unspecified' and peak_value_consistancy_fraction <= 0 and peak_value_consistancy_fraction >= 1:
            print('ERROR, peak_value_consistancy_persentage received an input that was not a fraction between 0 and 1')
            peak_value_consistancy_fraction = int(input('Please re-enter the fraction: '))
            return(max_peak_finder(signal, threshold, vert_offset, window_length, min_peak_distance, min_amount_from_threshold,peak_value_consistancy_fraction))
            
    elif threshold != 'unspecified' and vert_offset != 'unspecified' or window_length != 'unspecified':
        print('ERROR! Threshold has been defined as a constant, but so too has one or more of the adaptive arguments: vert_offset or window_length')
        print('If the threshold is fixed as a constant the adaptive arguments are not needed and should be left undefined')
        return()
        
    # Initilzing varibles   
    ignored_peak_index = zeros(int(ceil(len(signal)/2)), dtype = int_)       # initializing an ignored_peak_index array where the index of the peak that didnt meet the min distance requirement between it and the previous peak are stored
    ignored_peak_value = zeros(int(ceil(len(signal)/2)))      # initializing a ignored_peak_value array where the ignored peak values that didnt meet the min distance requirement between it and the previous peak will be stored
    m = 0     # m is an iterator that ensures once an index is filled in the ignored_peak_ arrays, the next ignored_peak_ is placed in the next empty index location.
    
    ignored_max_index = zeros(int(ceil(len(signal)/2)), dtype = int_)        # initializing an ignored_max_index array where indexs of max values that werent actually local peaks are stored for debugging    
    k = 0     # k is an iterator that moves through ignored_max_index array. see later
    
    max_peak_index = zeros(int(ceil(len(signal)/2)), dtype = int_)            # initializing a max_peak_index array where the index of the peak in the signal array will be stored as integers
    max_peak_value = zeros(int(ceil(len(signal)/2)))           # initializing a max_peak_value array where the peak values will be stored
    n = 0   # n is an iterator that moves through max_peak_ arrays. see later
    
    crossing_index = zeros(3, dtype = int_)                  # creating a list to store the indices of the crossing points
    j = 0   # j is the iterate with a range of 0-2 (ie the 3 indices of crossing_index) after j = 2 it will be reset to 0. See later.
    
    outer_crossings = zeros(len(signal), dtype = int_)                    # Storing the outer_crossings for debugging purposes
    p = 0   # p is an iterator that moves through outer_crossings arrays. see later
    
    inner_crossings = zeros(len(signal), dtype = int_)                    # Storing the inner_crossings for debugging purposes
    q = 0   # q is an iterator that moves through inner_crossings arrays. see later
    
    thresholds = zeros(len(signal)) # creating an array to store the thresholds as these are used to check when crossings have occured and can be graphed
    
    # Determining how the first point in the signal is treated w.r.t a threshold
    if initial_thres != 'unspecified':
        thresholds[0] = initial_thres   
        start = 1                   # with the 0th thershold determine, we want our for loop to start at the second point (1th iteration)

    else: # a seperate threshold for the first point in signal was not entered, therefore it is treated like every other point and the function starts at the zeroth point in signal
        start = 0
            
    end_check = False   # setting an end_check variable which is set to true if the signal ends with an inner crossing and was above the threshold before it.
                                                                                     
    # Peforming function   
    for i in range(start, len(signal)): # NB the reason we start at i=1 is because the threshold list is initilized with the threshold for i=0 in it, see above.
        
        if threshold == 'unspecified':     # this insures if threshold = 'unspecified' then an adaptive threshold is calculated at each iteration

            # Calculating threshold at each point using a central smooth algorithm like matlabs smooth function
            # if confused by this expression see the example in my Smooth Functions description AND remember that the stop condition value isnt used!
            if i <= (window_length-1)/2:
                window_mean = (signal[0:window_length].mean())   # using the mean of a full window length to approximate the mean of the first few points until i > window length
                thresholds[i] = window_mean +  vert_offset         
            
            elif i >= len(signal) - (window_length-1)/2:
                window_mean = (signal[-window_length:].mean())   # using the mean of a full window length to approximate the mean of the last few points where a moving mean would need fewer forward points than avalible
                thresholds[i] = window_mean + vert_offset       # Incase the threshold is -ve, we need to work out the threshold this way rather than just window_mean*multiple of mean

            else :
                window_mean = (signal[i-int((window_length-1)/2): i+(int((window_length -1)/2))+1].mean())     # NB we need to add one to the stop point as we want to include index i+(window-1)/2 in the threshold calc        
                thresholds[i] = window_mean + vert_offset                                                          # Incase the threshold is -ve, we need to work out the threshold this way rather than just window_mean*multiple of mean
        
        else:
            thresholds[i] = threshold   # if thershold was specified, the thresholds array, for every point is just the specified threshold.
            
        # With the threshold calculated we now check to see if the current point meets the criteria to be a peak or trough
        # checking to see if point is a positive gradient crossing of the threshold
        if signal[i] >= thresholds[i] and signal[i-1] <= thresholds[i-1] and i != 0:    # NB if i = 0, signal[i-1]>=thresholds[i-1] --> signal[-1]>=thresholds[-1] which is looking at the end of the signal
            crossing_index[j] = i
            j = j+1     # j steps forward one to fill the next index of crossing_index next time a crossing is found.
            
        # checking to see if point is a negetive gradient crossing of the threshold    
        elif signal[i] <= thresholds[i] and signal[i-1] >= thresholds[i-1] and i != 0:  # NB if i = 0, signal[i-1]>=thresholds[i-1] --> signal[-1]>=thresholds[-1] which is looking at the end of the signal
            crossing_index[j] = i        
            j = j+1     # j steps forward one to fill the next index of crossing_index next time a crossing is found.
            
        # Once 3 crossing have occured we can know there is a peak and trough between the two outer crossings and we can
        # go about finding them.
        
        # END PEAK CHECKER (I have the end_check variable just for improved readability)
        if i == len(signal)-1 and j==2 and  signal[crossing_index[1]-1] > thresholds[crossing_index[1]-1]: 
            end_check = True    # the signal was above the threshold between the last outer crossing and final inner crossing which means we need to check for a end peak between these crossings
        
        if j == 3 or end_check == True:    
          
            # Argsort returns the INDICES of the sorted VALUES of an array
            # I.E. sorted data is the indices of the maximum to minimum values of the data between the crossings, the [::-1] ensures it is max to min values
            sorted_data_indices = (argsort(signal[crossing_index[0]:crossing_index[j-1]])[::-1]) + crossing_index[0]
            
            # Checking if the max value between two crossings is infact a local peak or if it is a false positive.
            for index in sorted_data_indices:            
                # the condition below is: if the suspected_index_of_max_peak is not the first element or last element in the total signal and it is a local peak and its above its threshold then it is our max local peak.
                if index != 0 and index != len(signal) - 1 and signal[index - 1] < signal[index] and signal[index + 1] <= signal[index] and signal[index] >= thresholds[index]:
                    index_of_max_peak = index   # if the above condition is true, the suspected_index_of_max_peak has been shown to be a local peak! And hence it is 
                                                # the true index of the max peak between the current outer crossings.
                    break   # once the max peak has been found we want to break.
    
                else: # there was no max peak (which would be weird if we have crossings!) or the index was the first or last point in the signal
                    ignored_max_index[k] = i
                    k = k+1     # k is an iterator that moves through ignored_max_index array.
                    index_of_max_peak = 'none found'
     
            if index_of_max_peak != 'none found':          
                if min_peak_distance != 'unspecified' and n > 0 and index_of_max_peak - max_peak_index[n-1] < min_peak_distance:  # Checking if the max peak in possible peaks is far enough from the previous positively identified max peak
                    ignored_peak_index[m] = index_of_max_peak           # we store the ignored peak data incase the user wants to check what was ignored in the signal
                    ignored_peak_value[m] = signal[index_of_max_peak]
                    m = m+1     # m is an iterator that ensures once an index is filled in the ignored_peak_ arrays, the next ignored_peak_ is placed in the next empty index location.
                        
                elif min_amount_from_threshold != 'unspecified' and abs(signal[index_of_max_peak] - thresholds[index_of_max_peak]) < min_amount_from_threshold:    # we can set an amount a peak must be above the threshold for it to be a true peak, this is handy for when a signal may jump around the threshold a tiny amount and may not be an actual peak.
                    ignored_peak_index[m] = index_of_max_peak           # we store the ignored peak data incase the user wants to check what was ignored in the signal
                    ignored_peak_value[m] = signal[index_of_max_peak]
                    m = m+1     # m is an iterator that ensures once an index is filled in the ignored_peak_ arrays, the next ignored_peak_ is placed in the next empty index location.
                        
                elif peak_value_consistancy_fraction != 'unspecified' and n > 0 and signal[index_of_max_peak] <= (1+peak_value_consistancy_fraction)*signal[max_peak_index[n-1]] and signal[index_of_max_peak] >= (1-peak_value_consistancy_fraction)*signal[max_peak_index[n-1]]:    # checking to see that the value of the peak found is within + or -5% of the previous peaks value, if it is, it is deemed too different to be a correct peak identification. Hence some foward knowledge of the signal is required before using this test.
                    ignored_peak_index[m] = index_of_max_peak           # we store the ignored peak data incase the user wants to check what was ignored in the signal
                    ignored_peak_value[m] = signal[index_of_max_peak]
                    m = m+1     # m is an iterator that ensures once an index is filled in the ignored_peak_ arrays, the next ignored_peak_ is placed in the next empty index location.
                    
                else:
                    max_peak_index[n] = index_of_max_peak           # adding the index of the current maximum peak to a list of all the peaks
                    max_peak_value[n] = signal[index_of_max_peak]    # adding the value of the current max peak to a list of all the peaks
                    n = n+1     # n is an iterator that ensures once an index is filled in the max_peak_ arrays, the next max_peak_ is placed in the next empty index location.
            
            # STORING AND RESETTING THE CROSSING ARRAY DATA
            # Also NB that when finding the argmin or argmax of signal[crossing_index[0]: crossing_index[2]+1], this is just a view of the array signal meaning it will treat this view first
            # as its own array with the first element of the array indexed back at 0. To work out the peaks index in the whole signal array we need to add crossing_index[0].
            if p == 0:
                outer_crossings[p] = crossing_index[0]
                outer_crossings[p+1] = crossing_index[2]
                p = p+2     # p is an iterator that ensures once an index is filled in the outer_crossings, the outer crossing is placed in the next empty index location.
            
            elif j == 3:   # if end_check is true, the signal ends on an inner crossing and the for loop ends with j == 2, so we dont want to add crossing_index[2] if j == 2
                outer_crossings[p] = crossing_index[2]  # since crossing_index[2] becomes crossing_index[0] (see below) for successive peak finding, if we store crossing_index[0], it will just be the crossing_index[2] of the last peak
                p = p+1                                 # p is an iterator that ensures once an index is filled in the outer_crossings, the outer crossing is placed in the next empty index location.
 
            inner_crossings[q] = crossing_index[1]
            q = q+1     # q is an iterator that ensures once an index is filled in the inner_crossings arrays, the next inner crossing is placed in the next empty index location.
            
            crossing_index[0] = crossing_index[2]   # Setting the last crossing crossing to be the first crossings in the crossing_index, so we start looking for another two crossings from our current last crossing.
                                            # I.E. our final crossing now becomes our first crossing to continue searching from
            
            j = 1 # resetting j to one so we find our next 2 crossing. NB our first crossing will be the last crossing from the prevous set of 3 crossings as outlined above.  
    
            
     # trimming all unfilled indices of max_peak_ arrays, ignored_peak_ arrays, and crossing arrays
    max_peak_index = trim_zeros(max_peak_index)   # as we cannot possible have a peak at an index location 0, we can trim peak_index and use its length to define the peak_value array. As a peaks value could be 0, so we cant use the trim_zeros function of the peak_value array.
    max_peak_value = max_peak_value[:len(max_peak_index)]   # trimming the peak_value array to the length of peak_index, as they must be the same length, each index is information on the same peak.
    
    ignored_peak_index = trim_zeros(ignored_peak_index)   # the code is such that we cannot possible have an ignored_peak at an index location 0, so we can trim peak_index and use its length to define the ignored_peak_value array. As an ignored_peak_value could be 0, so we cant use the trim_zeros function of that array.
    ignored_peak_value = ignored_peak_value[:len(ignored_peak_index)]# trimming the ignored_peak_value array to the length of ignored_peak_index, as they must be the same length, each index is information on the same peak.
    
    ignored_max_index = trim_zeros(ignored_max_index,'b')

    outer_crossings = trim_zeros(outer_crossings, 'b')
    inner_crossings = trim_zeros(inner_crossings)      
            
    return(max_peak_index, max_peak_value, thresholds, outer_crossings, inner_crossings, ignored_peak_index)
