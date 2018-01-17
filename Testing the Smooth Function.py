# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 21:04:12 2016

@author: jcb137
"""

# _________________________________________________ TESTING THE SMOOTH FUNCTION ____________________________________________
        
# --- IMPORTING MODULES ________________________________________
import numpy
import matplotlib.pyplot as plt
import sys

# --- IMPORTING FUNCTIONS ______________________________________
sys.path.append(r'C:\Users\jcb137\OneDrive\Python\General Functions')

# Importing smoothing function
from Smooth import central_smooth        
        
import numpy
import random
import matplotlib.pyplot as plt

# --- RUN SPACE ________________________________________________

random_array = numpy.array(random.sample(range(0,1001),101))
smoothed_random_array = central_smooth(random_array,10)

plt.plot(random_array)
plt.plot(smoothed_random_array)
plt.legend(labels = ['Unsmoothed', 'Smoothed'])