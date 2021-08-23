# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 11:33:34 2021

@author: joelb

This function was written to resample (interpolate and extrapolate) tabulated (pandas dataframe) data.

"""

import numpy as np
import pandas as pd

def dataframe_resampler(df, dx = None, x_min = None, x_max = None, Y = None, dy = None, y_min = None, y_max = None):
    """
    This function takes a dataframe input with tabulated data and resamples it (linearly interpolating and/or extrapolating) to a new desired
    resolution.

    Parameters
    ----------
    df : pandas dataframe
        A dataframe containing the data to be resampled. The dataframe should be in one of the following two formats, a table whose
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
            
        OR a table whose data 'z' is dependent on two independent variables 'x' and 'y':
            
            =====  ======  ========  ========  =======  =========
            index  X       y1        y2         .        ym
            =====  ======  ========  ========  =======  =========
            0      x1      z(x1,y1)  z(x1,y2)   .        z(x1,ym)
            1      x2      z(x2,y1)  z(x2,y2)   .        z(x2,ym)
            .      .       .         .          .        .
            .      .       .         .          .        .
            n      xn      z(xn,y1)  z(xn,y2)   .        z(xn,ym)
            =====  ======  ========  ========  =======  =========
            
        WHERE x1<x2<...<xn and y1<y2<...<ym FAILURE TO DO SO WILL RESULT IN ERROR. A useful reminder on reordering dataframe columns:
        df = df[new_cols] where new_cols is an iterable of the new column order.
            
        NB 'index' is just the default index column provided by pandas to dataframes.           
            
    dx : int or float
        The desired step size between the rows of the X columns for the resampled table.
    x_min : int or float, optional
        The desired minimum value of the X column for the resampled table. The default is df.iat[0,0].
    x_max : int or float, optional
        The desired maximum x value of the X column for the resampled table. The default is df.iat[0,0].
    Y : list or array, optional
        A list or array of ints or floats that are the y look up values for the different columns of the table with two independent variables. By default, if it is not passed, 
        within the function it tries to get the column headers using df.columns[1:] assuming they are ints or floats, if they are not an error is thrown. By giving the option
        to pass Y separately, df can have column headers that are strings for example.
    dy : int or float, optional
        The desired step size between the Y columns for the resampled table, when the input df is the two independent type. The default is None.
    y_min : int or float, optional
        The desired minimum y column in the resampled table, when the input df is the two independent type. The default is None.
    y_max : int or float, optional
        The desired maximum y column in the resampled table, when the input df is the two independent type. The default is None.

    Returns
    -------
    ndf : pandas dataframe
        The new pandas dataframe (ndf) containing the resampled table.

    """
    
    # Performing input checks
    if dx is None and (x_min is not None or x_max is not None):
        raise Exception("x_min or x_max was passed, but the step size dx was not.")
    if dy is None and (y_min is not None or y_max is not None):
        raise Exception("y_min or y_max was passed, but the step size dy was not.")
    
    # Interpolating and/or extrapolating in x (down each columns)
    if dx is not None:
        X = df.iloc[:,0].values                      # an array of the original df x data column
        if x_min is None: x_min = X[0]
        if x_max is None: x_max = X[-1]
        Xn = np.arange(x_min, x_max+dx, dx)          # an array whose elements become the row look up values in the new table, where the n significes 'new' X
        # The below array contains the indices such that 0 < (Xn[indices_of_Xn_equal_or_above_X] - X) < dx in other words, if X and Xn were merged, the indices of X in
        # the merged array would be indices_of_Xn_equal_or_above_X - 1
        indices_of_Xn_equal_or_above_X = np.ceil((X - X[0])/dx).astype(int)
        Znx = np.zeros((len(Xn),df.shape[1]-1))               # an array to store the new dependent variable Z data after resampling has occured in the x direction (down the columns)
       
        for i in range(0,Znx.shape[1]):            # forloop to step through the columns of Z data in the original dataframe
        
            Z = df.iloc[:,i+1].values                # an array of the original df z data for the column of interest
                   
            # To interpolate/extrapolate for the resample, using z = mx + c, need to find m (=dz_dx below) and c
            # finding it in an array like manner, since m and c need not be constant over the original range of tabulated data
            dz_dx = np.diff(Z)/np.diff(X)       # getting the gradient dz/dx that occurs down the column of the original table
            c = Z[1:] - dz_dx*X[1:]             # getting the linear constant
            
            # Extrapolating
            if x_min < df.iat[0,0]:
                Znx[0:indices_of_Xn_equal_or_above_X[0],i] = dz_dx[0]*Xn[0:indices_of_Xn_equal_or_above_X[0]]+c[0]
            if x_max > df.iat[-1,0]:
                Znx[indices_of_Xn_equal_or_above_X[-1]:,i] = dz_dx[-1]*Xn[indices_of_Xn_equal_or_above_X[-1]:]+c[-1]
            
            elif x_max == df.iat[-1,0]:
                Znx[-1,i] = df.iat[-1,i+1]
                
            # Interpolating
            for j in range(0,len(dz_dx)):
                Znx[indices_of_Xn_equal_or_above_X[j]:indices_of_Xn_equal_or_above_X[j+1],i] = dz_dx[j]*Xn[indices_of_Xn_equal_or_above_X[j]:indices_of_Xn_equal_or_above_X[j+1]]+c[j]
    
    # if dx is None, then no resampling occurs in the x direction (down the columns). 
    # Therefore, the Xn and Znx arrays used in the y direction resampling are simply the original (non-resampled) data in the df input.
    else:
        Xn = df.iloc[:,0].values
        Znx = df.iloc[:,1:].values
             
    # Interpolating and/or extrapolating in y (along each row)      
    if dy is not None:
        if Y is None:
            if all(isinstance(i,float) or isinstance(i,int) for i in df.columns[1:]):
                Y = df.columns[1:].values
            else:
                raise Exception("The columns headers for df are not all floats or ints. Thus (per the docs), the Y input must be used to pass the values associated with each column in the original dataframe.")
        if any(Y != np.sort(Y)):
            raise Exception("The column headers for df passed were not in ascending order. Per the docs, please ensure y1<y2<y3 etc.")
        if y_min is None: y_min = Y[0]
        if y_max is None: y_max = Y[-1]
        Yn = np.arange(y_min, y_max+dy, dy)     # an array whose elements become the column look up values in the new table, where the n significes 'new' Y
        indices_of_Yn_equal_or_above_Y = np.ceil((Y-Y[0])/dy).astype(int)    # see comment for indices_of_Xn_equal_or_above_X above
        Zn = np.zeros((len(Xn),len(Yn)))      # an array to store the new dependent variable Z data after resampling has occured in BOTH the x (down the columns) and y (across rows) directions
        
        for i in range(0,len(Zn)):  # where length of a 2D array returns the number of rows
            
            dz_dy = np.diff(Znx[i,:])/np.diff(Y)
            c = Znx[i,1:] - dz_dy*Y[1:]
            
            # Extrapolating
            if y_min < Y[0]:
                Zn[i,0:indices_of_Yn_equal_or_above_Y[0]] = dz_dy[0]*Yn[0:indices_of_Yn_equal_or_above_Y[0]]+c[0]
            if y_max > Y[-1]:
                Zn[i,indices_of_Yn_equal_or_above_Y[-1]:] = dz_dy[-1]*Yn[indices_of_Yn_equal_or_above_Y[-1]:]+c[-1]
            elif y_max == Y[-1]:
                Zn[i,-1] = Znx[i,-1]
                
            # Interpolating
            for j in range(0,len(dz_dy)):
                Zn[i, indices_of_Yn_equal_or_above_Y[j]:indices_of_Yn_equal_or_above_Y[j+1]] = dz_dy[j]*Yn[indices_of_Yn_equal_or_above_Y[j]:indices_of_Yn_equal_or_above_Y[j+1]]+c[j]
        
        ndf = pd.DataFrame(Zn, columns = Yn)
        ndf.insert(0,df.columns[0],Xn)  # inserting Xn separately from Znx, in case Xn has a different dtype, eg may be int while Znx is float. 
        
    else:
        ndf = pd.DataFrame(Znx,columns = df.columns[1:])
        ndf.insert(0,df.columns[0],Xn)  # inserting Xn separately from Znx, in case Xn has a different dtype, eg may be int while Znx is float. 
        
    return(ndf)
    
#%% Testing the function

if __name__ == "__main__":
    
    df = pd.DataFrame(np.array([[1,1,1],[2,2,2],[3,3,3]]), columns = ['X', 1, 2])
    
    new_df = dataframe_resampler(df, 0.1)
    new_df2 = dataframe_resampler(df, 0.1, x_max = 3.5)
    new_df3 = dataframe_resampler(df, 0.1, x_min = -0.5, x_max = 3.5)
    new_df4 = dataframe_resampler(df, 0.1, x_min = 1.5, x_max = 2.5)
    new_df5 = dataframe_resampler(df, 0.1, x_max = 3, dy = 1, y_max = 3)
    new_df6 = dataframe_resampler(df, dy = 1, y_max = 3)
    
    # df2 = pd.DataFrame(np.array([[1,1,1],[2,2,2],[3,3,3]]), columns = ['X', 2, 1])
    # new_df7 = dataframe_resampler(df2, dy = 1, y_max = 3)   # THIS SHOULD CAUSE AN ERROR
    
    
    # Testing the function with Kinetic EV AMG Frictional loss data
    # fric_df = pd.read_pickle(r'C:\Users\joelb\OneDrive\Documents\Kinetic EV\Kinetic_EV_Analyses\Flywheel_Efficiency_and_Losses\Friction_losses_Prof_Keith_Pullen\A3_friction_loss_in_watts_at_1_Pa.pkl')
    # rfric_df = dataframe_resampler(fric_df, dx = 10, x_min = np.floor(fric_df.iat[0,0]).astype(int), x_max = np.ceil(fric_df.iat[-1,0]).astype(int))
    
    
    # # Testing the function with Kinetic EV AMG P_max and e data
    # amg_df = pd.read_pickle(r'C:\Users\joelb\OneDrive\Documents\Kinetic EV\Kinetic_EV_Analyses\Flywheel_Efficiency_and_Losses\Electrical_efficiency_Sheffield_Uni\A3_elec_efficiency_and_P_max.pkl')
    # dw = 10
    # dP = 100
    # w_min = np.floor(amg_df.iat[0,0]).astype(int)
    # w_max = np.ceil(amg_df.iat[-1,0]).astype(int)
    # resampled_P_max = dataframe_resampler(amg_df.iloc[:,:2],dw,w_min,w_max)
    # e_df = amg_df.drop(['e_P_max','P_max'], axis = 1)
    # integer_column_labels = np.array([int(''.join(filter(str.isdigit, header))) for header in amg_df.columns[1:] if any(map(str.isdigit,header))])
    # indices_to_sort_columns = np.insert(np.argsort(integer_column_labels)+1,0,0)
    # e_df_sorted = e_df[e_df.columns[indices_to_sort_columns]]
    # r_e_df = dataframe_resampler(e_df_sorted,dw,w_min,w_max, np.sort(integer_column_labels), dP, y_max = 25000)
