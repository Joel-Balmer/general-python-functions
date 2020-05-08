# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 12:40:00 2016

About this script:
    
    This script contains my origianl filter function which was retired on 23/09/2016 as it uses convolution in the time domain
    to apply the filter which makes it slow and particularly inefficient with longer data sets.
    
    The function test at the end was used to look at the effects of ffting the filtered signal. In particular it looked at ffting
    the trimmed raw signal to see the effects of spectral leakage, caused by discontinuities or using a number of points in the 
    fft'd signal that leads to a df which cannot exactly represent the frequency component. 
    
    For more details on this I made a (shitty) powerpoint which I stored here:
        C:\\Users\\jcb137\\OneDrive\\Documents\\University\\PhD\Math Notes


@author: jcb137
"""

# ---____ Creating a Hamming Filter_________________________________

# INPUTS:
# fc is the cutoff frequency
# transition_width is the width of the transition band in Hz. NB it is then normalized by dividing it by the sampling frequency
# signal is the time domain signal you want to filter once the filter is created.
# dt is the step size between successive samples in the time domain for the signal.
# time_shift_removed is a yes 'y', no 'n' input which the user enter to indicate whether they want the output filtered signal to have been corrected so it has zero time shift

# OUTPUTS:
# filtered_signal is the filtered signal
    # NB! Filtering results in Nf unusable points at the start of the signal in the time domain. This is becauase we need Nf previous points to filter 
    # (see Nf output below) any given data point, hence the first Nf points in a signal cant actually be filtered. So unusable points are set to zero
    # and the filtered signal output is kept the same length as the input signal. The exception to this when the output has its time_shift_removed,
    # (see input above) this leads an output which is (Nf-1)/2 = samples_shift shorter.
# h is the filter impulse responce in the time domain
# Nf is the filter length ie the number of filter coefficients
# freq_spec_filt is an array of the discrete frequencies for which filter coefficients exist, making up the filter frequency spectrum (useful for plotting)
# t_array_filt is an array of the discrete times for which filter impulse responce is known. (useful for plotting)
# t_shift is the time shift or delay in seconds caused by the filter on the output when compared to the input
# samples_shift is the shift or delay in SAMPLES caused by the filter on the output when compared to the input
# w is the hamming window function in the time domain
# trunc_sinc is our truncated sinc function aka our truncated ideal filter responce in the time domamin

def hamming_low_pass_filter(fc, transition_width, signal, dt, time_shift_removed = 'n'):
    
    # Importing necessary modules
    import numpy
        
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

    # working out the filter frequency spectrum and time arrays
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
    
    # Performing the Convolution
    for j in range(0, N):      # NB with a stopping condition of N in the range function, the final computed itereation will be j= N-1
        filtered_signal[j] = 0
        for n in range(0,Nf):     # NB with a stopping condition of Nf in the range function, the final computed itereation will be n= Nf-1
            if j-n <= 0:    # we need this else when j-n<0 signal[-ve number] will start getting points at the end of the signal array
                break
            else:
                filtered_signal[j] = filtered_signal[j] + (signal[j-n]*h[n])    # NB signal[j-n] will start grabing points from the end of the signal array if j-n<0 so we cant let it do that!
            
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
    
    
#%% ------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------   
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------Testing the function---------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------    
# --------------------------------------------------------------------------------------------------------------------------------        


if __name__ == "__main__":    

    # NB NB NB I think the phase graph shown is incorrect... havent sorted it yet... Professor Phil Bones thought
    # it may be due to the way the fft is being implemented, might be something to do with the discountinuity of
    # the filtered signal. I.E. The signal starts at y = 0 and ends at y=-1, so periodising the wavefrom for the
    # fft results in a discountinuity. Anyway, just thoughts, havent tested if ffting the 'useful' and periodic
    # part of the waveform (ie the waveform without the zeros and ensuring it is a complete number of wavelengths)
    # fixes the problem.
    
    # Creating filter based on 'Digital Signal Processing: a practical guide for engineers and scientists' By Steven 2003 pg 294
    
    # Low pass Hamming Filter
    
    # NB NB NB NB NB NB
    # One of the most important things I recognised from this example is:
    # 1) You MUST use the NORMALISED cut off frequency in calculation your filter impulse responce.
    # 2) fc_norm = fc/fs, so the higher your sampling frequency the smaller fc_norm will be. This can 
    #    lead to issues. For example:
    #
    #           Say you want to generate y = sin(2*pi*0.5*t) + sin(2*pi*5*t) so your highest frequency is 5Hz
    #           
    #           to make the signal smooth you use fs = 100*highest_freq_interest = 100*5 = 500Hz.
    #           now say you want to filter out the 5Hz component from your generated signal. Let
    #           fc = 3.5Hz. In order to not affect our 0.5Hz component and fully remove the 5Hz using fc=3.5Hz
    #           we would need a transition width of tw <= 3Hz, meaning the f_stop <= 5Hz (where f_stop = 3.5Hz + 3Hz/2) 
    #           while f_pass <= 2Hz (whre f_pass = 3.5Hz - 3Hz/2).
    #
    #           The next step is to take our filter characteristics and normalize them to find the number of filter
    #           coefficients we need.  fc_norm = 3.5Hz/500Hz = 0.007 (eq from above). Now this is where we start to 
    #           see the issue with using very high fs, our normalized 0.5Hz component is 0.001 (=0.5Hz/500Hz), which 
    #           now appears VERY close to our fc_norm of 0.007 when inspecting these in the normalized frequency
    #           spectrum. This means normalized transition band tw_norm = 0.006 (= 3Hz/500Hz) is VERY VERY NARROW!
    #           It is narrow because the roll off of the filter reponce needs to be between 0.001 (0.5Hz) and 0.01
    #           (5Hz). In order to get such incredibly fast roll off we will need a large number of filter coefficients
    #           for example the hamming filter would need around Nf = 3.3/tw_norm = 550. Now this isnt huge by absolute
    #           standards, BUT when you consider 10sec of our signal is 5000 points, we require 11% of our signal. 
    #
    #
    #           What if we wanted to fix the filter length:
    #           Now lets say we wanted to only use a filter length of Nf = 101, our tw_norm would need to be approx
    #           0.033 --> tw = tw_norm*fs = 16.5Hz! So our transition band is waaaaaaayyyyyy to big! Both the frequency
    #           we want to filter (5Hz) and the one we want to preserve (0.5Hz) will now be in the transition band!
    #
    #           To fix this we could change our fs to 25Hz, still 5 times higher than the highest frequency in our
    #           original signal y. Then our new fc_norm will be fc_norm = 3.5Hz/25Hz = 0.14, new tw_norm = 3Hz/25Hz
    #           = 0.12, 20 times wider than when tw_norm = 0.006! So now we can get away with far less filter coefficients
    #           and our filtered signal frequency of 0.5Hz is still 50 times smaller than fs so our filtered signal
    #           will still look good as well!
    
    # Importing modules
    import numpy
    import matplotlib.pyplot as plt
    import sys
    # Adding path to directory where general functions are stored
    sys.path.insert(0, r'G:\Testing filter.py')
    from Filters import hamming_low_pass_filter
    
    # Initializing Arrays
    N = 5000    # defining signal length
    #Nf = 101    # defining Filter length
    y = numpy.zeros(N)   # y will be the input signal to the filter
    
    # Filter characteristics
    fc = 3.5         # normalized cutoff frequency
    tw = 3       # normalized tranisiton width tw_norm = 5.5/101 based on Ifeachor Signal Processing book
    
    # generating input signal _________________________
    fa = 0.5    # low frequency component of signal input y
    fb = 5      # high frequency component of signal input y
    
    # Working out sampling frequency, frequency spectrum and time arrays
    fs = 5*(max(fa,fb))     # fs = 25, see 'Effects of Sampling Frequency on Signal Processing' in Onedrive python folder
    
    dt = 1/fs       # 0.02sec per step
    df = 1/(len(y)*dt)   # 0.01Hz per step
    t = numpy.arange(0, N*dt, dt)  # time array starting at t[0] = 0sec to t[4999] = 9.998sec
    freq_spec = numpy.arange(0, N*df, df)   # working out the freq_spec x axis for the signal with N points
                                            # NB once you trim your filtered data you wont have N points and
                                            # therefore your df will change so that the frequency range is still the same.
    
    for i in range(0,N):
        y[i] = numpy.sin(2*numpy.pi*fa*t[i]) + numpy.sin(2*numpy.pi*fb*t[i])
        
    import time
    
    time_start = time.time()    
    
    y_filtered, h, Nf, freq_spec_filt, t_array_filt, t_shift, samples_shift, w, trunc_sinc = hamming_low_pass_filter(fc, tw, y, dt)
    
    time_to_filter = time.time()-time_start
    
    # Trimming the unusable points after the convolution (See 'Digital Signal Processing: a practical guide for engineers and scientists' Convolution chapter for more details)
    # And removing the time shift from the filtered signal (See)
    trim = int((Nf-1)/2)    # the number of unusable points, after removing the time shift in the filter function
    y_filtered_trimmed = y_filtered[trim + samples_shift:]
    df_trimmed = 1/(len(y_filtered_trimmed)*dt)
    freq_spec_trimmed = numpy.arange(0, len(y_filtered_trimmed)*df_trimmed, df_trimmed)    
    
    # A Note on the FFT! The fft treats an inputed signal as a period of an infinitely repeating signal as part of its assumption to compute the algorithm.
    # These means we need to be sure the input into the fft starts and ends at the same value, else when it joins repeating periods of our input there will be discontinuities
    # these disconinuites will cause ripple in the frequency domain as you need infinite frequencies to represent any square edges, which a discontinuity is.
    
    # You can also
    # This ripple is known as spectral leakage and can be read about here http://www.gaussianwaves.com/2011/01/fft-and-spectral-leakage-2/.

    # With this example, we can very easily just pass the filtered output to the fft such that we are only fft'ing a periodic signal. If our signal was not periodic, such
    # as an earthquake signal, the best we can do is pad the signal with zeros which increases the resolution of our frequency spectrum (df = 1/N*x, where N is the number of
    # points in the signal we pass to the fft). The padding will mean that the signal will appear periodic to the fft, but if the signal in the time domain has sharp edges, it will
    # still require many frequencies to represent it exactly and hence some leakage may still appear.
    
    # Performing the FFTs
    H = numpy.fft.fft(h)                        # frequency content of the filter responce
    Y = numpy.fft.fft(y)                        # frequency content of the unfiltered signal that was input to the filter    
    Y_filtered = numpy.fft.fft(y_filtered)      # frequency content of the filtered signal
    
    #%% Plotting Results
    
    fig, axs = plt.subplots(nrows= 1, ncols = 2)
    fig.suptitle('Filtering the 5Hz component out of: \n $y = sin(2 \pi t 0.5Hz) + sin(2 \pi t 5Hz)$', fontsize = 20)
    
    # Plotting Time Domain Signals
    axs[0].set_title('Signal in the Time Domain')
    axs[0].set_xlabel('t (sec)')
    axs[0].set_ylabel('y')
    axs[0].plot(t, y, color = 'b', label = 'Original Signal')
    axs[0].plot(t, y_filtered, color = 'r', label = 'Filtered Signal')
    axs[0].plot(t[trim:N-samples_shift], y_filtered_trimmed, color = 'darkorange', linewidth = 2, label = 'Delay Corrected & Trimmed Filtered Signal')
    axs[0].legend(fontsize = 'small')
    
    # Plotting Frequency Responce
    axs[1].set_title('Normalised Signals in Frequency Domain')
    axs[1].set_xlabel('f (Hz)')
    axs[1].set_ylabel('Magnitude')
    axs[1].stem(freq_spec,abs(Y)/max(abs(Y)), linefmt = 'b', basefmt = 'b', markerfmt = ' ', label = 'Orignal signal')
    axs[1].stem(freq_spec,abs(Y_filtered)/max(abs(Y_filtered)),linefmt = 'r', basefmt = 'r', markerfmt = ' ', label = 'Filtered Signal')
    axs[1].plot(freq_spec_filt, abs(H), color = 'g', label = 'Filter Freq Responce' )
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