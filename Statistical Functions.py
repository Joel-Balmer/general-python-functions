# -*- Statistical functions -*-
"""
Created on Tue Apr 12 09:13:16 2016

@author: jcb137 written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  

"""

# ------------------------------- MEAN & STANDARD DEVIATION -------------------------------------------

def mean_and_standard_deviation(X):
    import numpy
    if isinstance(X,list) == True:
        mean = sum(X)/len(X)
        sd = (sum([(observation-mean)**2 for observation in X])/(len(X)-1))**0.5
        return(mean,sd)
    elif isinstance(X,numpy.ndarray) == True:
        mean = sum(X)/len(X)
        sd = (sum(array([(observation-mean)**2 for observation in X]))/(len(X)-1))**0.5
        return(mean,sd)
    else:
        return(print('The input wasnt given as a list or an array, please redefine the input.'))
        
# ------------------------------------------------------------------------------------------------------
        
# ------------------------------ DISTRIBUTION PLOTTER --------------------------------------------------
        
