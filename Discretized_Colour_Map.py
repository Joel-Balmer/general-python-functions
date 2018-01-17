# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:35:35 2016

@author: jcb137 written in python 3.4

     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  

THIS FILE HAS BEEN SET TO READ ONLY

"""

# ___________________________________________ Colour Map Discretizer ___________________________________________

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
    
#%% ------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------     
    
# Testing the function
if __name__ == "__main__":

   import matplotlib   
   import matplotlib.pyplot as plt

   z = [0.3,0.4,0.5,0.6,0.7,0.2,0.3,0.4,0.5,0.8,0.9]
   y = [3, 7, 5, 6, 4, 8, 3, 4, 5, 2, 9]
   cm = cmap_discretize(matplotlib.cm.jet, 6) 

   test = plt.scatter(range(len(y)), y, s=60, c=z, cmap=cm)
   plt.colorbar(test)