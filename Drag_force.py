# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:33:06 2020

@author: Joel Balmer

"""

def drag_force(v, C_d, A, P = 101325, T = 273.15, R = 287.058, rho = 'undefined'):
    
    """
    
    PURPOSE
    ----------
    To return the drag force imposed on a object given its drag coefficient and frontal area. The equation is of the form:
        
        F_drag = -1*0.5*rho*(v^2)*C_d*A
        
        NB rho = P/(RT) where P is pressure, T is temperature and R is the specific gas constant
        
    Where 0.5*rho*v is the dynamic pressure, thus multiple by A we simply have F = Pressure*Area
    The factor C_d is an experimental coefficient capturing how aerodynamic the frontal area is, ie what fraction of dynamic 
    pressure actually acts to retard motion, since a streamlined shape will more easy slip through a medium at high speed etc.
    
    NB the -1 is included to ensure the direction of the drag force is opposite to the velocity vector. ie, drag always opposes
    the direction of motion.
        
    NB some useful drag coefficients and references gathered from different projects
    - C_d = 0.7 for a bus: from page 270 of Ground Vehicle Dynamics by Karl Popp
    
    INPUTS
    ----------
    - v: velocity of the object in m/s
    - C_d: drag coefficient. 
    - A: frontal area in m^2 (ie the area perpindicular to the direction of travel)
    - P: (optional input) the static pressure the fluid is under in Pascals. Default value is atmospheric pressure at sea level SI units 101325 Pa (aka 1 atm)
    - T: (optional input) the temperature of the fluid in Kelvin. Default value is 273.15 K (aka 0 degrees celcius)
    - R: (optional input) the specific gas constant in J/kgK. If not supplied it defaults to air: 287.058 J/kgK.
    - rho: (optional input) the density of the fluid in kg/m^3. If not supplied, defaults to value based on rho = P/(RT)
    
    OUTPUTS
    ----------
    - F_drag: the drag force opposing the motion in untis N (whose size opposes the direction of velocity).
    - P_drag: the power (rate of energy) loss associated with the F_drag, in units W (whose sign opposes the direction of velocity).
    
    """
    
    # Checking to see if density (rho) was explicitly defined, if not we calculate it
    # from P, R and T, where default values of those are used if they too were not explicitly passed
    if rho == 'undefined':
        rho = P/(R*T)

    # Working out the drag force
    F_drag = -1*0.5*rho*(v**2)*C_d*A
    
    # Working out the power
    P_drag = F_drag*v
    
    return(F_drag,P_drag)

  
#%% TESTING THE FUNCTION ----------------------------------------------------------------------------------        

if __name__ == "__main__":  
    
    v_kmh = 100         # velocity in kilometers per hour
    v_ms = v_kmh/3.6    # velocity in meters per second
    C_d = 0.7           # Approx bus drag function
    A = 2.52*4.39       # approx bus frontal area

    print(drag_force(v_ms, C_d, A))