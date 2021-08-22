# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 11:33:34 2021

@author: joelb

This function was written to resample (interpolate and extrapolate) tabulated (pandas dataframe) data.

"""

import numpy as np
import pandas as pd

def dataframe_resampler(df, dx, x_min = None, x_max = None, Y = None, dy = None, y_min = None, y_max = None):
    """
    This function takes a dataframe input with tabulated data and resamples it (interpolating) to improve

    Parameters
    ----------
    df : pandas dataframe
        A dataframe containing the data to be resampled. The dataframe should be in the following formats, a table whose
        data 'z' is dependent on one independent variable 'x'.
            
            
            =====  ======  ========
            index  X       Z
            =====  ======  ========
            0      x1      z1=z(x1)
            1      x2      z2=z(x2)
            .      .       .       
            .      .       .       
            n      xn      zn=z(xn)
            =====  ======  ========
            
        A table whose data 'z' is dependent on two independent variables 'x' and 'y':
            
            =====  ======  ========  ========  =======  =========
            index  X       y1        y2         .        ym
            =====  ======  ========  ========  =======  =========
            0      x1      z(x1,y1)  z(x1,y2)   .        z(x1,ym)
            1      x2      z(x2,y1)  z(x2,y2)   .        z(x2,ym)
            .      .       .         .          .        .
            .      .       .         .          .        .
            n      xn      z(xn,y1)  z(xn,y2)   .        z(xn,ym)
            =====  ======  ========  ========  =======  =========
            
        NB 'index' is just the default index column provided by pandas to dataframes.           
            
    dx : TYPE
        DESCRIPTION.
    x_min : TYPE, optional
        DESCRIPTION. The default is df.iat[0,0].
    x_max : TYPE, optional
        The maximum x value (associated with the last row) in the output table. The default is df.iat[0,0].
    dy : TYPE, optional
        DESCRIPTION. The default is None z_min = None.
    y_min : TYPE, optional
        DESCRIPTION. The default is None.
    y_max : TYPE, optional
        The maximum y value (associated with the last row) in the output table. The default is None.

    Returns
    -------
    ndf : pandas dataframe
        The new pandas dataframe (ndf) containing the resampled, higher frequency data.

    """
    
    if x_min == None: x_min = df.iat[0,0]
    if x_max == None: x_max = df.iat[-1,0]
        
    X = df.iloc[:,0].values                      # an array of the original df x data column
    Xn = np.arange(x_min, x_max+dx, dx)          # an array whose elements become the row look up values in the new table ie the new X (Xn) data range
    # The below array contains the indices such that 0 < (Xn[indices_of_Xn_above_X] - X) < dx in other words, if X and Xn were merged, the indices of X in
    # the merged array would be indices_of_Xn_above_X - 1
    indices_of_Xn_above_X = np.ceil((X - X[0])/dx).astype(int)   # ie Xn[indices_of_X_in_Xn] = X
    
    Zn = np.zeros((len(Xn),df.shape[1]-1))               # an array to store the new resampled, dependent variable Z data
   
    # Interpolating and/or extrapolating in x (down columns)
    for i in range(0,Zn.shape[1]):            # forloop to step through the columns of Z data in the original dataframe
    
        Z = df.iloc[:,i+1].values                # an array of the original df z data for the column of interest
               
        # To interpolate/extrapolate for the resample, using z = mx + c, need to find m (=dz_dx below) and c
        # finding it in an array like manner, since m and c need not be constant over the original range of tabulated data
        dz_dx = np.diff(Z)/np.diff(X)       # getting the gradient dz/dx that occurs down the column of the original table
        c = Z[1:] - dz_dx*X[1:]             # getting the linear constant
        
        # Extrapolating
        if x_min < df.iat[0,0]:
            Zn[0:indices_of_Xn_above_X[0],i] = dz_dx[0]*Xn[0:indices_of_Xn_above_X[0]]+c[0]
        if x_max > df.iat[-1,0]:
            Zn[indices_of_Xn_above_X[-1]:,i] = dz_dx[-1]*Xn[indices_of_Xn_above_X[-1]:]+c[-1]
        
        elif x_max == df.iat[-1,0]:
            Zn[-1,i] = df.iat[-1,i+1]
            
        # Interpolating
        for j in range(0,len(dz_dx)):
            Zn[indices_of_Xn_above_X[j]:indices_of_Xn_above_X[j+1],i] = dz_dx[j]*Xn[indices_of_Xn_above_X[j]:indices_of_Xn_above_X[j+1]]+c[j]
             
            
    # if dy != None:
    #     Yn = np.arange(y_min, y_max+dy, dy)      # an array whose elements become the column look up values in the new table ie the new Y (Yn) data range
    #     # Zn = np.zeros((len(Xn), len(Yn)))        # an array to store the new resampled, dependent variable Z data
    #     indices_of_Yn_above_Y = np.ceil((Y-Y[0])/dy).astype(int)
    
    ndf = pd.DataFrame(np.insert(Zn,0,Xn,axis =1),columns = df.columns)
        
    return(ndf)
    
#%% Testing the function

if __name__ == "__main__":
    
    df = pd.DataFrame(np.array([[1,1,1],[2,2,2],[3,3,3]]), columns = ['X', 1, 2])
    
    new_df = dataframe_resampler(df, 0.1)
    new_df2 = dataframe_resampler(df, 0.1, x_max = 3.5)
    new_df3 = dataframe_resampler(df, 0.1, x_min = -0.5, x_max = 3.5)
    new_df4 = dataframe_resampler(df, 0.1, x_min = 1.5, x_max = 2.5)
    
