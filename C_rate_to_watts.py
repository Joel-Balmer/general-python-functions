# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 12:54:20 2020

@author: Joel Balmer

"""

def C_rate_to_watts(C,E_cap,E_unit):
    """
    To convert power expressed as C-rate to  SI unit of Watts. For example, an 80kWh battery outputing 80kW is said to output 1C.
    
    NOTE, that the power expressed as a C-rate is not the usual way C-rate is expressed:
    https://batteryuniversity.com/article/bu-402-what-is-c-rate
     
    CONVERSION EQUATION:
    
    1 C = E_cap/h ≡ E_cap/h * 1h/60min * 1min/60sec = E_cap/3600 with units J/s ≡ Watts 
    
    INPUTS
    -----
    C : int or float (unitless)
        The C-rate, describing power as a proportion of the energy capacity. For example, an 80kWh battery has 288000kJ, this battery discharging at
        1C is ≡ 288000kJ/h ≡ 288000/3600 kJ/s ≡ 80kW. Thus, a 80kWh battery discharging at 1C is discharging at 80kW and thus will fully discharge in
        1 hour. Similarly, an 80kWh battery discharging at 0.5C will discharge at 40kW and thus discharge in 2 hours.
    E_cap : int or float (J or kWh)
        Energy capacity of the storage element (eg battery) for which the C-rate applies. NB units must be passed with E_unit.
    E_unit : str
        The units of E_cap, strictly either 'j' for joules or 'kWh' or 'kilowatt hours'.
    
    OUTPUTS
    -----
    P : int or float (W)
        Power in Watts.
    """
    
    if E_unit == 'j': P = E_cap*C/3600
    elif E_unit == 'kWh': P = E_cap*C*1000
    else: raise Exception(f"Invalid E_unit input = {E_unit}, must be either 'j' or 'kWh'")
    
    return(P)

#%% TESTING THE FUNCTION

if __name__ == "__main__":
    
    E_kWh = 80
    E_j = E_kWh*3.6e6
    P1 = C_rate_to_watts(1,E_kWh,'kWh')
    P2 = C_rate_to_watts(1,E_j,'j')
    # should_fail = C_rate_to_watts(1,E_j,'fail')