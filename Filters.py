# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 12:40:00 2016

@author: jcb137
"""
# ___________________________________________________________________________________________________________________________________________________

""" --- CREATING HAMMING LOW PASS FILTER -------------------------------------------

INPUTS:
fc: is the cutoff frequency
transition_width: is the width of the transition band in Hz. NB it is then normalized by dividing it by the sampling frequency
signal: is the time domain signal you want to filter once the filter is created.
dt: is the step size between successive samples in the time domain for the signal IN SECONDS, so df is calculated in Hz in the function.
time_shift_removed: is a yes 'y', no 'n' input which the user enter to indicate whether they want the output filtered signal to have been corrected so it has zero time shift
applied_domain: is a string which dictates which domain the filter is applied, either in the 'time' domain using convolution or in the 'frequency' domain taking advantage of 
                fft, ifft and multiplication.

OUTPUTS:
filtered_signal is the filtered signal
    NB! Filtering results in Nf-1 unusable points at the start of the signal in the time domain. This is because, for a data point (call it point x) in the signal, we need 
    itself and Nf-1 previous data points to calculate the filtered data point at x.
    
        Example: say len(h) = Nf = 3 (ie filter coefficients), therefore, filtered_signal[2] (= filtered_signal[Nf-1]) depends on signal[2-0] (ie its own unfilted point), 
                 signal[2-1], signal[2-2] (= signal[2-Nf-1]) (ie Nf-1 points before its own unfilted point). 
                 
                 So filtered_signal[Nf-1] has Nf-1 points before it and therefore is ok.
                 
                 But filtered_signal[1] (= filtered_signal[Nf-2]) will depend on signal[1-0], signal[1-1], signal[1-2] (=signal[1-Nf-1]) and since this refers
                 to a point before data was collected, we cant correctly filter signal[1] according to our filter properties, namely cut off frequency and transition width.
                 
                 Therefore Nf-1 points at the start and end of the signal will be garbage and need to be trimmed with the filtered_signal_trimmer function below this one.
    
    The exception to this when the output has had its time_shift_removed, (see input above) this leads an output which is (Nf-1)/2 = samples_shift shorter and hence only 
    needs the second half, a further (Nf-1)/2 trimmed from the front of the signal. 
    For more detail, see "Smith - 2013 - Digital Signal Processing A Practical Guide for Engineers and Scientists A Practical Guide for Engineers and Scientists"
    pages 119-121. But note in there example they need to trim the end of there signal, which we dont here. I have the book in Mendeley.
    
h is the filter impulse responce in the time domain
Nf is the filter length ie the number of filter coefficients
freq_spec_filt is an array of the discrete frequencies for which filter coefficients exist, making up the filter frequency spectrum (useful for plotting)
t_array_filt is an array of the discrete times for which filter impulse responce is known. (useful for plotting)
t_shift is the time shift or delay in seconds caused by the filter on the output when compared to the input
samples_shift is the shift or delay in SAMPLES caused by the filter on the output when compared to the input
w is the hamming window function in the time domain
trunc_sinc is our truncated sinc function aka our truncated ideal filter responce in the time domamin

"""

def hamming_low_pass_filter(fc, transition_width, signal, dt, time_shift_removed = 'n', applied_domain = 'unspecified'):
    
    # Importing necessary modules
    import numpy
    from scipy.signal import fftconvolve    
    
    # Generating the low pass filter impulse responce_____________
        
    fs = 1/dt                           # sampling frequency of the input signal
    N = len(signal)                     # number of points in signal
    fc_norm = fc/fs                     # normalized cutoff frequency
    tw_norm = transition_width/fs       # normalized transition width
    Nf = int(numpy.ceil(3.3/tw_norm))   # working out the number of filter coefficients (filter length) required for the hamming window.
    if Nf%2 == 0:
        Nf = Nf+1       # if Nf is worked out to be even, we add one to make it odd. This isnt always necessary, but
                        # even and odd filter impulse responces are slightly different and the odd type is more versatile
                        # see Ifeachor Emmanuel, Jervis Barrie - 1993 - Digital Signal Processing Chpt on FIR filter design. (pg 284 in 1st Edition)
        
    # Working out the Delay caused by the filter
    t_shift = ((Nf-1)/2)*dt     # time shift, see Ifeachor Emmanuel, Jervis Barrie - 1993 - Digital Signal Processing Chpt on FIR filter design.
    samples_shift = int((Nf-1)/2)  # working out the shift as the equivalent of sample rather than seconds.
    
    # Initilizing arrays
    filtered_signal = numpy.zeros(N)   # y_filtered will be the output signal from the filter
    h = numpy.zeros(Nf)    # h will be the filter impulse responce
    w = numpy.zeros(Nf)    # w will be the filter window
    trunc_sinc = numpy.zeros(Nf)    # trunc_sinc is our ideal low pass filter impulse responce truncated to Nf points    

    # working out frequency spectrum and time arrays
    df_filt = 1/(Nf*dt)
    t_array_filt = numpy.arange(0, Nf*dt, dt)[:Nf]
    freq_spec_filt = numpy.arange(0, Nf*df_filt, df_filt)[:Nf]
        
    for n in range(0,Nf):
        w[n] = (25/46) - (21/46)*numpy.cos(2*numpy.pi*n/(Nf-1))
        if n-(Nf-1)/2 == 0:
            trunc_sinc[n] = 2*numpy.pi*fc_norm
            h[n] = w[n]*trunc_sinc[n]
        else:
            trunc_sinc[n] = numpy.sin(2*numpy.pi*fc_norm*(n-(Nf-1)/2))/(n-(Nf-1)/2)
            h[n] = w[n]*trunc_sinc[n]
    
    h_unnorm = numpy.copy(h)    # before I normalize h (necessary for using filter) I want to keep h as it was calculated,
                                # in case the person wants to actually look at the calculated h=w*trunc_sinc, could be useful for debugging
            
    # normalize the low pass filter impulse responce
    h = h/numpy.sum(h)
    
    if applied_domain == 'time':
        # Performing the Convolution
        for j in range(0, N):      # NB with a stopping condition of N in the range function, the final computed itereation will be j= N-1
            for n in range(0,Nf):     # NB with a stopping condition of Nf in the range function, the final computed itereation will be n= Nf-1
                if j-n < 0:    # we need this else when j-n<0, signal[-ve number] will start getting points at the end of the signal array
                    break
                else:
                    filtered_signal[j] = filtered_signal[j] + (signal[j-n]*h[n])
                    
    else:   # if applied_domain is not 'time', then frequency is used.
        # Performing the fft and ifft using a scipy function
        filtered_signal = fftconvolve(signal, h)    # utilizes the fact that multiplication in the frequency domain is convolution in the time domain.
        
        # Removing the zero padding applied by fftconvolve
        filtered_signal = filtered_signal[:len(signal)]
                                          
        if applied_domain != 'frequency':
           print('WARNING --------------- \n"applied_domain" input was not "time" or "frequency", "frequency" was used by default.')
    
    # Accounting for the time shift caused by filtering______________
            
    # The user can choose to remove the time shift caused by filtering. If they define time_shift_removed = 'y' the output filtered_signal 
    # will be have zero phase delay/time shift. The output signal is shifted to have zero time shift and as a result is 'samples_shift' shorter.
    
    # This function is used to check the user input is either 'y' for yes or 'n' for no.
    def yes_no_input_checker(user_input):
        if user_input != 'y' and user_input != 'n':
            user_input = input('Invalid input, please re-enter y for yes or n for no: ')
            return(yes_no_input_checker(user_input))
        else:
            return(user_input)
    
    time_shift_removed = yes_no_input_checker(time_shift_removed)
    
    if time_shift_removed == 'y':
        filtered_signal = filtered_signal[samples_shift:len(filtered_signal)]  # shifting the filtered_signal 'samples_shift' left so it now has zero time delay.
            
    return(filtered_signal, h, Nf, freq_spec_filt, t_array_filt, t_shift, samples_shift, w, trunc_sinc)
 
# --------------------------------------------------------------------------------------------------------------------------------    
# -------------------------------------------------------------------------------------------------------------------------------- 
# --------------------------------------------------------------------------------------------------------------------------------    
# -------------------------------------------------------------------------------------------------------------------------------- 
# --------------------------------------------------------------------------------------------------------------------------------    
# -------------------------------------------------------------------------------------------------------------------------------- 

""" _____________________________________________ FILTER TRIM FUNCTION ______________________________________________

 This function is used after filtering is complete to trim the unusable data points that result from the FIR filter fucntion. This is 
 explained in the filter function details above.
 NB that this function does not replace the time_shift_removed, which ensures there is no phase shift by trimming (Nf-1)/2 points
 from the start of the signal. Hence the time_shift_removed should still be used in the filter function if zero phase shift is
 required.
 
 However, this function still needs to know if the time shift was removed, because if it wasnt removed there is Nf-1 unusable points
 at the start of the signal (rather than (Nf-1)/2) since time_shift_removed didnt trim any.
 
 Example:
 Consider a signal that was filtered with a filter length of 11. Nf-1 (=10) points are unusable, that is points 0--->9 inclusive are unusable.
 If the signal had its time_shift_removed, (Nf-1)/2 (=5) points, namely 0--->4 inclusive, have already been removed, leaving just point 5--->9 
 inclusive still to be removed.
 
 Not only will this function trim the unusable data from the filtered signal, it will trim the other signals so that they are the same
 length as the trimmed filtered signal.

 INPUTS ----------------------------
 signals: either an array of data if a single data array is to be trimmed, or a dictionary, whose values are as many signals as you like, 
          filtered and unfiltered ones.
 Nfs: is the number of filter coefficients used to filter the signal. 
      If multiple signals were filtered, pass the Nf's of each signal in as a dictionary using the naming nominclature in the example below.
      The filtered signal with the longest Nf (number of filter coefficeints) has the most unusable data, this Nf defines the trim that will
      be applied to all other signals. 

 INPUT EXAMPLE:
 If just a single array of data is to be trimmed:
 signal: P_vent array
 Nf: the number of filter coefficients used to filter the P_vent data as an integer

 If it is multiple arrays of data that need to be trimmed but only one of the signals was filtered:
 signal: is a dictionary where the keys, signal_dict.keys(): 'P_vent', 'P_vent_filtered', 'ECG' and the values are the respective arrays
 Nf: is a dictionary with only a single key value pair, the key being a string "Nf_P_vent_filtered" and the value being an integer thats the number of filter coefficients.
     the reason it needs to be a dictionary with key of name format Nf_ followed by the corresponding signal name, is the signal that was filtered is
     trimmed slightly differently to others, if time_shift_removed was 'yes' when the filtering occurred.

 If it is multiple arrays of data for which more than one was filtered:
 signal: is a dictionary where the keys, signal_dict.keys(): 'P_vent', 'P_vent_filtered', 'ECG', 'ECG_filtered' and the values are the respective arrays
 Nf: is a dictionary where Nf.keys(): 'Nf_P_vent_filtered', 'Nf_ECG_filtered' and the values are the number of filter coefficients for the respective filtered signals
 The naming for this instance is important, Nf_ followed by the signal name, as the signal assosiated with the max Nf is trimmed slightly differently to the others if
 time_shift_removed was 'yes'when the filtering occurred.

 OUTPUTS ---------------------------
 trimmed_signals: the trimmed signals
 trim: the amount of elements that were trimmed
"""

def filtered_signals_trimmer(signal, Nf, time_shift_removed):
    
    
    if str(type(signal)) == "<class 'numpy.ndarray'>":
    # A SINGLE SIGNAL NEEDING TRIMMING ------------------------------------------------------------
        if str(type(Nf)) != "<class 'int'>":
            print("ERROR, a single signal was passed to the function, but the number of filter coefficients Nf was not of integer type\n please refer to function comments for more details")
        
        # Calculating the trim to be applied
        else:
            if time_shift_removed == 'y':
                trim = int((Nf-1)/2)
            elif time_shift_removed == 'n':
                trim = Nf-1
            else:
                print("for trim to be defined, time_shift_removed argument\n should be passed as 'n' for no or 'y' for yes")
    
            # Applying the trim
            signal = signal[trim:]  # trimming the filtered signal
    
        
    elif str(type(signal)) == "<class 'dict'>":
    # MULTIPLE SIGNALS NEEDING TRIMMING, USES DICTIONARIES ----------------------------------------
        if str(type(Nf)) != "<class 'dict'>":
            print("ERROR, multiple signals were input for trimming, but Nf was not passed as a dict as expected\n read the function documentation for more details")
    
        # Finding longest filter (ie most coefficients Nf)
        Nf_max_name = max(Nf, key=lambda dict_key: Nf[dict_key])  
        # NB key= in this line refers to the key of the inbuilt max function! ie key= tells how the input to max is sorted 
        # for the max to be identified. In our case max's key is the values of the dictionary, as output by the lambda function,
        # which does used the dictionary keys.
        # So here max is returning the attribute, in this case the dictionary key!, for max's key, in this case the dictionary values!
        
        # Getting the length of the raw unfiltered signals before trimming
        N = len(max(signal.values(), key=lambda signal_arrays: len(signal_arrays)))   # I know this is horrible to read but it keeps it in one line!
                                                                                            # it returns the length of the unfiltered signals in signals_dict
        
        # Working out the trim
        if time_shift_removed == 'y':
            trim = int((Nf[Nf_max_name]-1)/2)
        elif time_shift_removed == 'n':
            trim = int(Nf[Nf_max_name])
        else:
            print("for trim to be defined, time_shift_removed argument\n should be passed as 'n' for no or 'y' for yes")
        
        # Applying the trim
        if time_shift_removed == 'y':
            for key in signal:
                if Nf_max_name[3:] in signal and 'filt' in signal :
                    signal[key] = signal[key][trim:]  # trimming the filtered signal which had the largest Nf
                else:
                    signal[key] = signal[key][trim:N-trim]    # trimming all other signals
                    
        else:   # time_shift_removed is 'n' and so we only need to trim the front unusable points from everything
            for key in signal:
                signal[key] = signal[key][trim:]
                
    else:
        print("Error, the signal(s) entered were not of the array or dictionary type,\n refer to the function documentation")
        
    return(signal)
    
#%% ------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------   
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------Testing the filter function---------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------        


if __name__ == "__main__":  
    
    # Importing modules
    import numpy
    import matplotlib.pyplot as plt
    import sys
    # Adding path to directory where general functions are stored
    sys.path.insert(0, r'C:\Users\jcb137\OneDrive\Python\General Functions')
    from Filters import hamming_low_pass_filter
    
    # Initializing Arrays
    N = 5020    # defining signal length
    #Nf = 101    # defining Filter length
    y = numpy.zeros(N)   # y will be the input signal to the filter
    
    # Filter characteristics
    fc = 3.5     # cutoff frequency
    tw = 3       # tranisiton width
    
    # generating input signal _________________________
    fa = 0.5    # low frequency component of signal input y
    fb = 5      # high frequency component of signal input y
    
    # Working out sampling frequency, frequency spectrum and time arrays
    fs = 5*(max(fa,fb))     # fs = 25, see 'Effects of Sampling Frequency on Signal Processing' in Onedrive python folder
    
    dt = 1/fs       # 0.02sec per step
    df = 1/(len(y)*dt)   # 0.01Hz per step
    t = numpy.arange(0, N*dt, dt)  # time array starting at t[0] = 0sec to t[4999] = 9.998sec
    freq_spec = numpy.arange(0, N*df, df)
    
    for i in range(0,N):
        y[i] = numpy.sin(2*numpy.pi*fa*t[i]) + numpy.sin(2*numpy.pi*fb*t[i])

    import time
    
    time_start = time.time()    
    
    y_filt, h, Nf_y, freq_spec_filt, t_array_filt, t_shift, samples_shift, w, trunc_sinc = hamming_low_pass_filter(fc, tw, y, dt, applied_domain = 'frequency')
    
    y_filt2,_, Nf_y2,_,_,_,_,_,_ = hamming_low_pass_filter(fc,tw,y,dt, time_shift_removed ='y', applied_domain = 'frequency') 
    
    trimmed_data = filtered_signals_trimmer({'y_filt2':y_filt2, 't':numpy.copy(t), 'y':numpy.copy(y)}, {'Nf_y2':Nf_y2}, time_shift_removed ='y')
    
    time_to_filter2 = time.time()-time_start
            
    #%% Plotting Results
    Y = numpy.fft.fft(y)     
    H = numpy.fft.fft(h)
    Y_filtered = numpy.fft.fft(y_filt)
    
    fig, axs = plt.subplots(nrows= 1, ncols = 2)
    fig.suptitle('Filtering the 5Hz component out of: \n $y = sin(2 \pi t 0.5Hz) + sin(2 \pi t 5Hz)$', fontsize = 20)
    
    # Plotting Time Domain Signals
    axs[0].set_title('Signal in the Time Domain')
    axs[0].set_xlabel('t (sec)')
    axs[0].set_ylabel('y')
    axs[0].plot(t, y, color = 'b', label = 'Original Signal')
    axs[0].plot(t, y_filt, color = 'r', label = 'Filtered Signal')
    axs[0].plot(t[:len(t)-samples_shift], y_filt[samples_shift:len(y_filt)], color = 'darkorange', linewidth = 2, label = 'Delay Corrected Filtered Signal')
    axs[0].legend(fontsize = 'small')
    
    # Plotting Frequency Responce
    axs[1].set_title('Normalised Signals in Frequency Domain')
    axs[1].set_xlabel('f (Hz)')
    axs[1].set_ylabel('Magnitude')
    axs[1].stem(freq_spec,abs(Y)/max(abs(Y)), linefmt = 'b', basefmt = 'b', markerfmt = ' ', label = 'Orignal signal')
    axs[1].stem(freq_spec,abs(Y_filtered)/max(abs(Y_filtered)),linefmt = 'r', basefmt = 'r', markerfmt = ' ', label = 'Filtered Signal' )
    axs[1].plot(freq_spec_filt, abs(H), color = 'g', label = 'Filter Freq Responce')
    axs[1].legend(fontsize = 'small')
    
    # Plotting Hamming Window and Truncated Ideal Filter
    plt.figure()
    plt.title('Filter Impulse Responce and its Components')
    plt.xlabel('t (sec)')
    plt.ylabel('y')
    plt.plot(t_array_filt ,trunc_sinc, color = 'orange', label = 'Truncated Ideal Filter Impulse Responce')
    plt.plot(t_array_filt, w, color = 'purple', label = 'Hamming Window')
    plt.plot(t_array_filt, h, color = 'g', label = 'Normalized Filter Impulse Responce norm(h = ideal x window)')
    plt.legend(fontsize = 'small')
    
    # Plotting Time Domain Signals of Trimmed Signal
    plt.figure()
    plt.title('Trimmed Filtered Signal')
    plt.xlabel('time')
    plt.ylabel('y')
    plt.plot(trimmed_data['t'], trimmed_data['y'], label = 'Unfiltered')
    plt.plot(trimmed_data['t'], trimmed_data['y_filt2'], label = 'Filtered')
    plt.legend(fontsize = 'small')
