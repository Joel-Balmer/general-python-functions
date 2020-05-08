# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 15:31:07 2018

@author: jcb137

PURPOSE OF SCRIPT:
    To assess the frequency spectrum of a signal EXCLUDING THE DC COMPONENT ie the time domain mean offset is removed.
    
OTHER USEFUL NOTES THAT MAY EXPLAIN BEHAVIOUR SEENS AS A RESULT OF THIS SCRIPT:
    Effect of Sampling Frequency on generating discrete signals.png
    What to be aware of when FFTing Filtered Signals, (or any signals for that matter!).pptx
    
    Both of these documents are found on my Onedrive under OneDrive\\Documents\\University\\PhD\\Math Notes
    
INPUTS
signal: the signal you want to find the frequency spectrum for
dt: the time step (IN SECONDS) between each element of signal, used to determine the time step in the frequency domain
pad: an optional input which defaults to 'n' for no. Pad is short for padding and can be used to add zeros padding to the input signal.
     this is useful for bigg fft's which run faster if the length of the input is a power of 2. Ie, 2,4,8,16,32 etc. If you want padding
     so the signal length is a power of 2, let the pad input be 'y' for yes.

"""
import numpy as np
import matplotlib.pyplot as plt
import time

def freq_spectrum_finder(signal,dt, pad = 'n'):
    
    # Taking the mean or DC offset out of the signal.
    signal = signal - np.mean(signal)
    
    # Padding input signal to have a length which is a power of 2, apparently this makes the fft faster
    if pad == 'y':
        next_higher_power_of_two = 1<<(len(signal)-1).bit_length() # uses bit shift operator << (if you cant understand this, its ok, had to use examples online 
                                                                   # for it) to calculate the power of two that is equal too or greater than the length of the 
                                                                   # input signal. NB if length of signal is already a power of two then next_higher_power_of_two
                                                                   # will be equal to len(signal) hence below no padding will be added to signal.
            
        num_padding_zeros = next_higher_power_of_two - len(signal)
        padded_signal = np.concatenate((signal,np.zeros(num_padding_zeros)))
        
        # Checking the padded signal length is a power of 2:
        if (len(padded_signal) & (len(padded_signal)-1)) == 0: 
            print('Padded signal length is a power of 2')
        else:
            print('Padded signal length is not a power of 2')
        
        start = time.time()       # timing the fft algorithm run
        S = np.fft.fft(padded_signal)  # S is the complex amplitude and phase data of the signal. To get the amplitude just take the magnitude of the complex number.
                                       # magnitude = square_root(RE^2+IM^2), but python is smart and abs(complex) = magnitude
            
    elif pad != 'n' and pad != 'y':
        raise Exception ('Error, function input pad must be either n for no or y for yes')
    
    else: # pad must have defaulted to 'n' so no padding is to be added
        start = time.time()     # timing the fft algorithm run
        S = np.fft.fft(signal)  # S is the complex amplitude and phase data of the signal. To get the amplitude just take the magnitude of the complex number.
                                       # magnitude = square_root(RE^2+IM^2), but python is smart and abs(complex) = magnitude

    print('FFT analysis duration = {0}sec'.format(time.time()-start))
    
    N = len(S)              # the number of sampled points (including any padding)
    t = np.arange(0,len(signal)*dt,dt)   # creating a time array to use to plot the input signal
    
    df = 1/(N*dt)   # step size in the frequency spectrum (not to be confused with the sample frequency!)
                    # remember, your sampling frequency is 1/dt, but the step size in the frequency spectrum, df, is dependent on the frequency the data was
                    # sampled at (1/dt) AND the number of sampled points! So the more data points you sampled, the finer the resolution of frequency steps on
                    # the spectrum you can achieve.
    
    freq_spec = np.arange(len(S))*df    # creating an array of the frequency spectrum in Hertz
    
    #PLOTTING ---------------------------------------------------------------------
    fig, ax = plt.subplots(nrows = 1, ncols = 2)
    fig.canvas.set_window_title('Freq Spec')
    ax[0].set_title('Time Domain')
    ax[0].set_xlabel('time (s)')
    ax[0].set_ylabel('signal magnitude')
    ax[0].plot(t, signal)
    
    ax[1].set_title('Frequency Domain')
    ax[1].set_xlabel('frequency (Hz)')
    ax[1].set_ylabel('signal magnitude')    
    # NB stem plots can be notoriously slow in matplotlib so I dont use it very often
    #ax[1].stem(freq_spec,abs(S), markerfmt=' ', label = 'Frequency content')     # last key is just turning of the annoying markers
    
    # Making modified copies of the frequency spectrum and magnitude arrays for plotting custom stem plot
    # Basically I am making stems occur using a normal plot by imagining the following:
    # Eg, we want a stem (vertcal line) at x=1 to a height y = 4 (ie (1,4)) and another at (2,8). If we use a normal plot, these to 
    # points are joined by a line between them. To create the stems we add in some points between (1,0) and (2,0) so the order of points
    # plotted is now (1,4), (1,0), (2,0), (2,8) or in array format x = np.array([1,1,2,2]), y = np.array([4,0,0,8]) and this is what I am
    # doing below. 
    freq_spec_mod = np.zeros(len(freq_spec)*3)
    S_mod_abs = np.zeros(len(freq_spec)*3)
    
    for i in range(0,len(freq_spec)):
        freq_spec_mod[3*i:3*i+3] = freq_spec[i]
        S_mod_abs[2*i+i+1] = abs(S[i])
    
    ax[1].plot(freq_spec_mod,S_mod_abs, label = 'Frequency content')     # last key is just turning of the annoying markers
    
    ax[1].axvline(max(freq_spec)/2, color = 'g', label = 'Nyquest Frequency')   # Plotting the nyquest frequency for each generated signal
    ax[1].legend()
    
    return(freq_spec, S)


# _____________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________
# _____________________________________________________________________________________________________________________
# TESTING THE FUNCTION

if  __name__ == "__main__":

    # Generating a sign wave with frequency of 10 Hz   
    f = 10  # frequency of our sin wave       
    dt = 0.001  # step size in time domain NB generally want the sampling frequency of a signal to be at least 10 times higher than freq of interest, 
               #  see my .py and .pdf docs 'Effects of Sampling Frequency on Signal Processing' for more details
    t_final = 1                         # duration in seconds
    N = t_final/dt                      # Number of sampled points to represent the highest frequency of interest
                    
    t = np.arange(0, t_final, dt)    # time array of N points  
    y = np.zeros(len(t))             # initializing an array to store the signal at each time t
    
    for j in range(0, len(t)):          
        y[j] = np.sin(t[j]*2*np.pi*f)     # working out the signal y for each time
    
    # Getting frequency spectrum of our sign wave
#    freq_spec,S = freq_spectrum_finder(y, dt, pad = 'n')
    
    # The line below is just here for me to convieniently check pig data
    freq_spec,S = freq_spectrum_finder(pig['sepsis']['3']['control']['Q_ao_filtered'], dt = 0.004, pad = 'y')