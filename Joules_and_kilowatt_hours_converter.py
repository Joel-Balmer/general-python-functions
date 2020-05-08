# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 12:54:20 2020

@author: Joel Balmer

"""

def j_to_kWh(E_joules):
    """
    To convert energy expressed in joules to kilowatt hours. 
    J is the SI unit, while kWh tends to be how the industry expresses energy capacity.
 
    CONVERSION EQUATION:
    
    1 W = 1 J/s = 1 J/s * 60s/min * 60 min/h = 3.6kJ/h
    ∴ 1 Wh = 3.6kJ
    ∴ 1 kWh = 3.6MJ
    
    INPUTS
    -----
    E_joules: Energy in joules
    
    OUTPUTS
    -----
    E_kWh: Energy in kilowatt hours
    """
    
    E_kWh = E_joules/3.6e6
    
    return(E_kWh)

def kWh_to_j(E_kWh):
    """
    To convert energy expressed in kilowatt hours to joules. 
    J is the SI unit, while kWh tends to be how the industry expresses energy capacity.
 
    CONVERSION EQUATION:
    
    1 W = 1 J/s = 1 J/s * 60s/min * 60 min/h = 3.6kJ/h
    ∴ 1 Wh = 3.6kJ
    ∴ 1 kWh = 3.6MJ
    
    INPUTS:
    -----
    E_kWh: Energy in kilowatt hours
    
    OUTPUTS:
    -----
    E_joules: Energy in joules
    """
    
    E_joules = E_kWh*3.6e6
    
    return(E_joules)

