# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:24:11 2020

@author: Joel Balmer

"""

import numpy as np
import matplotlib.pyplot as plt

def subplot_variables(x_key, y_keys, d, labels = 'undefined', means = 'n'):
    
    """A line/space saving function that simply plots n variables in an nx1 subplot
    
    INPUTS
    -----
    - x_key: a string which when passed to the dictionary d is the key for the x variable
    - y_keys: a list of strings which when each is passed to the dictionary d is the key to get a particular y variable
    - d: a dictionary of the data
    - labels (optional): a dictionary, where the keys are the x_key and y_keys, the values are the labels to use for the graph
    - means (optional): a string input 'y' for yes or 'n' for no. When 'y' is passed, a thin dashed line for the mean is passed.
    
    """
    
    fig, ax = plt.subplots(len(y_keys),1, sharex = True)
    
    for i,y in enumerate(y_keys):
        ax[i].plot(d[x_key],d[y], c = f'C{i}')
        ax[i].axhline(np.mean(d[y]), c = f'C{i}', linestyle = '--', linewidth = 0.5)
        if labels == 'undefined':
            ax[i].set_ylabel(y)
        else:
            ax[i].set_ylabel(labels[y])
    
    if labels == 'undefined':
        ax[-1].set_xlabel(x_key)
    else:
        ax[-1].set_xlabel(labels[x_key])
        
    plt.tight_layout()