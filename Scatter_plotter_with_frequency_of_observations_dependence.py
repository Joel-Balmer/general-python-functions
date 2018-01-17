# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 11:04:23 2016

@author: jcb137 written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  
                     
                     
___________________________________________ FREQUENCY SCATTER PLOTTER _____________________________________________________                     

This function is useful for plotting x,y pairs which are quite discrete and often multiple observations of the same x,y pair are seen
simply because the data isnt very continuous or the resolution isnt very high etc.

What this function does is takes the unique_x_y_pairs function outputs (unique observations of x,y pairs and also the number of observations
of each pair) and then it plots a scatter of the unique pairs with the colour of the scatter point representing the number of observations.
This colour can then be cross referenced with a colour bar in the place of a secondary y axis.

It uses one other functions which gets the discretized colour map.

INPUTS:
    x_unique: the unique x values observed
    y_unique: the unique y values observed
    NB!!!! You need to make sure the order of x_unique and y_unique is such that x_unique[0],y_unique[0] are infact an observation x,y.
    I.e say your x data is a PEP measure and y is a PTT measure, you dont want to accidently sort or mix the order of PTT data (y) and end
    up pairing a PEP measure and PTT measure from different beats!
    
    num_observations: the number of times a x_unique,y_unique pair was observed. Again like NB'd above, you need to make sure the count array order
           matches up with the correct x,y pairs. See my unique_x_y_pairs function description for more details. 

    size: the size of scatter points, default is 20 if unspecified
    
     xlim: are the manually constrained limits/range you want the scatter window to plot over. It should be an array or list containing 2 elements, the min and max
     ylim: are the manually constrained limits/range you want the scatter window to plot over. It should be an array or list containing 2 elements, the min and max
"""

def scatter_plot_with_number_observations_dependence(x_unique, y_unique, num_observations, size = 20, xlim = 'unspecified', ylim = 'unspecified'):
    
    import matplotlib
    import numpy as np
    
    # Creating function to handle the discretization of the colour map used____________________________________________
        
    def cmap_discretize(cmap, N):
        """Return a discrete colormap from the continuous colormap cmap.
        
            cmap: colormap instance, eg. cm.jet. 
            N: number of colors.
        
        Example
            import matplotlib   
            import matplotlib.pyplot as plt
    
            z = [0.3,0.4,0.5,0.6,0.7,0.2,0.3,0.4,0.5,0.8,0.9]
            y = [3, 7, 5, 6, 4, 8, 3, 4, 5, 2, 9]
            cm = cmap_discretize(matplotlib.cm.jet, 6) 
    
        test = plt.scatter(range(len(y)), y, s=60, c=z, cmap=cm)
        plt.colorbar(test)
        """
        import matplotlib
        from numpy import concatenate, linspace
        
        if type(cmap) == str:
            cmap = matplotlib.pyplot.cm.get_cmap(cmap)
        colors_i = concatenate((linspace(0, 1., N), (0.,0.,0.,0.)))
        colors_rgba = cmap(colors_i)
        indices = linspace(0, 1., N+1)
        cdict = {}
        for ki,key in enumerate(('red','green','blue')):
            cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) for i in range(N+1) ]
        # Return colormap object.
        return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)
        
    # _________________________________________________________________________________________________________________________________
    # MAIN PLOTTING PART OF THE FUNCTION ______________________________________________________________________________________________
    
    
    number_colours = int(max(num_observations))     # working out the number of colours needed = max number of observations as we want a different colours for
                                                    # 1 observations through n observations.

    # NB NB NB NB cmap_discretize is defined as a seperate function in this script above.    
    
    cbar_colours = cmap_discretize(matplotlib.cm.jet, number_colours)   # getting the discretized colour bar from the cmap_discretize function
    
    # Manually adjusting colour bar ticks to occur in the middle of each discrete colour block.
    # By default the ticks are layout for the continuous colour bars which we dont use.
    cbar_range = max(num_observations) - min(num_observations) # cbar stands for colour bar
    cbar_block_centers = np.linspace(min(num_observations)+(cbar_range/(2*number_colours)), max(num_observations)-(cbar_range/(2*number_colours)), number_colours)
    cbar_tick_labels = np.linspace(min(num_observations),max(num_observations),number_colours, dtype = np.int_)
    
    # Plotting the scatter plot NB title and axis labels are not added in the function
    fig, ax = matplotlib.pyplot.subplots()
    scatter = ax.scatter(x_unique, y_unique, c = num_observations, s = size, cmap = cbar_colours)
    
    # If specified, the following code will set the x and y limits of the plot window
    if xlim != 'unspecified':
        plt.xlim(xlim[0],xlim[1])
    if ylim != 'unspecified':
        plt.ylim(ylim[0],ylim[1])
        
    cbar = matplotlib.pyplot.colorbar(scatter, ticks = cbar_block_centers)     #NB the tick locations are the centre of the coloured blocks of the colorbar, I set the tick labels manually after.
    cbar.set_ticklabels(cbar_tick_labels)   # setting the tick labels
    cbar.set_label('No. observations')
    
    return(fig, ax)
    
    
    
    