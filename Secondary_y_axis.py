# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 15:09:42 2020

@author: Joel Balmer
    
"""

# importing modules
import numpy as np
import matplotlib.pyplot as plt

def secondary_y_axis(ax, secondary_axis_label, secondary_axis_label_colour = 'k', x_data = 'undefined', y_data = 'undefined', legend_label = 'undefined', colour = 'C0', plot_linestyle = '-', plot_linewidth = 1.5, lims_converter = 'undefined', secondary_axis_offset = 'undefined', tick_lab_rot = 0):
    """
    Adds a secondary y-axis just left of the primary one (useful when expressing data in two units and the
    right hand side axis is already occupied).

    Parameters
    ----------
    ax : matplotlib.axes_subplots.AxesSubplot
        an axes of a subplot. If not use plt.subplots, and just standard plt.plot, you can use
        plt.gca() to get the axes.
    secondary_axis_label : string
        Secondary axis label.
    x_data : numpy array (optional)
        Array of x data to plot.
    y_data : numpy array (optional)
        Array of y data to plot.
    colour : string (optional)
        A string corresponding to the desired colour of the plot, axis and label. Defaults to C0.
    plot_linestyle : string (optional)
        Appropriate string for matplotlib linestyles: https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html
    plot_linewidth : int or float (optional)
        Appropriate value for matplotlib linewidth.
    legend_label : string
        A label for the data in the legend.
    lims_convert : lambda function (optional)
        As an alternative to supplying y_data, a lambda function can be supplied which generates the secondary axis
        limits by converting the limits of the primary axis.
    secondary_axis_offset : int or float (optional)
        If passed, the secondary axes is plotted left of the primary axis, the distance left depends on the value passed to secondary_axis_offset.
    tick_lab_rot : int
        the tick label rotation angle in degrees. Defaults to 0 degrees.

    Returns
    -------
    y_sec : matplotlib.axes_subplots.AxesSubplot
        the axes instance for the secondary axis that the bus stop locations are on.
    
    """
    
    if (type(y_data) == str and lims_converter == 'undefined') or (type(y_data) != str and lims_converter != 'undefined'):
        raise Exception ("One of either y_data or lims_lambda_convert must be supplied.")
        
    if (type(x_data) != str and type(y_data) == str) or (type(x_data) == str and type(y_data) != str):
        raise Exception ("If supplying data to plot, both x_data and y_data must be supplied.")
        
    if (type(x_data) == str and type(y_data) == str) and legend_label != 'undefined':
        raise Exception ("Legend label was supplied but no x_data or y_data was supplied to plot.")
        
    if (type(x_data) == str and type(y_data) == str) and plot_linestyle != '-':
        raise Exception ("plot_linestyle was supplied but no x_data or y_data was supplied to plot.")

    
    y_sec = ax.twinx()     # Hate the name of this function, twinx makes a second y axis sharing the y axis.
    
    if lims_converter != 'undefined':
        ax_min, ax_max = ax.get_ylim()
        # NB I dont know why, but at the time of creating this function, ax.get_yticks returns with one tick below and one above the y limits,
        # hence why I apply y_sec ticks excluding the first and last ax.get_yticks.
        y_sec_ticks_loc = ax.get_yticks()[1:-1]                 # getting the primary axis (visible (see note above)) tick locations, going to use them for the secondary axis below.
        y_sec.set_ylim(ax.get_ylim())                           # ensuring the secondary axis limits are the same as the primary axis
        y_sec.set_yticks(y_sec_ticks_loc)                       # setting the secondary axis tick locations to match the primary axis
        y_sec.set_yticklabels(lims_converter(y_sec_ticks_loc))  # updating the secondary axis tick labels to show the converted values (but still in the location of the primary axis ticks)       
        
    else:
        if legend_label != 'undefined': y_sec.plot(x_data,y_data, c = colour, linestyle = plot_linestyle, linewidth = plot_linewidth,  label = legend_label)
        else: y_sec.plot(x_data,y_data, c = colour, linestyle = plot_linestyle, linewidth = plot_linewidth)
        y_sec.set_yticks(np.linspace(min(y_data), max(y_data), len(ax.get_yticks())-2))
        
    y_sec.set_ylabel(secondary_axis_label, c = secondary_axis_label_colour)
    
    if secondary_axis_offset != 'undefined':
        # setting the position of the secondary y-axis to left (by primary axis) by the user defined offset amount
        y_sec.yaxis.set_ticks_position('left')
        y_sec.yaxis.set_label_position('left')
        y_sec.spines['left'].set_position(('outward', secondary_axis_offset))   # offsetting the left axis to the 
    
    return(y_sec)

#%% Testing the function

if __name__ == "__main__":
    
    plt.close('all')
    
    x = np.arange(0,11,1)
    y = np.arange(0,11,1)
    
    square_y = lambda y : y**2
    
    y2 = square_y(y)
    
    plt.plot(x,y, label = 'test')
    plt.legend(loc = 'upper left')    
    plt.xlabel('x')
    plt.ylabel('y')
    ax = plt.gca()
    
    secondary_y_axis(ax, 'y^2', 'C0', lims_converter = square_y, secondary_axis_offset = 40)
    # secondary_y_axis(ax, '2y', x_data = x, y_data = y2, colour = 'k', plot_linestyle = '--', plot_linewidth = 1.5, legend_label = 'test2')
    plt.legend(loc = 'upper right')    
    plt.subplots_adjust(left = 0.2)