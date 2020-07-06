# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 13:52:42 2020

@author: Joel Balmer
"""

import datetime
import numpy as np

def add_seconds_to_time(time, secs, dtype = 'datetime.time'):
    """
    
    Parameters
    ----------
    time : datetime.time
        A datetime.time object (https://docs.python.org/3/library/datetime.html#available-types) Example of format:
        time = datetime.time(5,10,30) for 05:10:30 or 5:10am and 30 seconds. 
        (NB to convert datetime.time to string time.strftime("%H:%M:%S") returns "hour:min:sec")
                    
    secs : int
        Number of seconds to add to time. Note that seconds CAN be greater than 1min ie, can be greater than 60sec as the function will
        convert secs > 60 to appropriate minutes and hours automatically.
    
    dtype : str, optional
        A string defining the data type of the output, either 'datatime.time' for the same format as the input, or as a 'str' to return
        a string in the format "hour:min:sec" (24 hour format). Defaults to 'datatime.time'.
        
    Returns
    -------
    fulldate.time() : datetime.time
        time + secs, in the output data type specified by the dtype input. 

    """
    if type(secs) != float: secs = float(secs)
    fulldate = datetime.datetime(100, 1, 1, time.hour, time.minute, time.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    if dtype =='str': 
        return(fulldate.time().strftime("%H:%M:%S"))
    elif dtype != 'datetime.time': 
        raise Exception("f{dtype} invaild for dtype input, must be either 'datetime.time' or 'str'")
    else: 
        return (fulldate.time())


#%% Testing function

if __name__ == "__main__":
    
    time = datetime.time(5,0,0)
    print(time)
    print(add_seconds_to_time(time,0.5))
    print(add_seconds_to_time(time,10,'str'))
    print(add_seconds_to_time(time,60*60))
    print(add_seconds_to_time(time, np.int32(1)))