# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:38:39 2017

@author: jcb137 written in python 3.5

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  

                     
ABOUT THIS FUNCTION:
This is a basic function that rejects 'outliers' which are determined based on them
being m*standard deviations from the mean.
                     
"""

# INPUTS
# data: the data you want to remove outliers from
# std_multiplier: the number of standard deriations from the mean that if a data point is over it is considered an outlier

# OUTPUTS
# it outputs an array of the data points which werent considered outliers

# DEFINING FUNCTION
def outlier_remover(data, std_multiplier):
    # Importing modules
    import numpy as np
    
    return data[abs(data - np.mean(data)) < std_multiplier * np.std(data)]