# -*- coding: utf-8 -*-
"""
Created on Tue May 18 10:52:05 2021

@author: joelb

These functions is based on analysis that can be found in a file named:
    "Heavy vehicle acceleration for a known torque or power at wheels.pdf"
    
The pdf can be found in my "Simulation Design Decisions.one" file and also in my personal math notes file. 

"""

import numpy as np

def change_in_velocity_quadratic_for_known_propulsive_force(F_p,F_n,F_g,m,v_i,C_d,A,dt,rho=1.29, T_s=1.2, C_s=1.5):
    """
    This function takes a known force of propulsion and calculates the acceleration of the vehicle without needing
    to know the resistive drag force and roll resistance. 
    
    Essentially, it finds the change in velocity of the vehicle and the retarding forces to the vehicles motion, all
    in one step. This is achieved thanks to the (summary) derivation below. For the full detail see 
    "Heavy vehicle acceleration for a known torque or power at wheels.pdf" which can be found in the 
    "Simulation Design Decisions.one" at the time of writing.

    Derivation
    ==========
    
    a = (v_f - v_i)/dt = ΣF/m = (F_p + F_d + F_r + F_g)/m
    where critically, F_p defines the +ve direction and F_d and F_r upon substitution of there equations have the 
    opposite sign showing they oppose the motion. Thus the values of F_d and F_r output from the function have the
    opposite sign to the F_p input. F_g can contribute to motion or opposite it depending on whether the bus is going
    down or uphill.
    
    F_d = -0.5*rho*v_f^2*C_d*A
    (NB that the equation for F_d is -ve indicating its direction opposes F_p)
    
    F_r = -T_s*(0.0041 + 0.000091714v_f)*C_s*F_n
    (NB that the equation for F_r is -ve indicating its direction opposes F_p)
    (For more details on the roll resistance equation, see the note later below)
    
    F_n = F_w*cos(theta)    (theta is the slope angle of the road surface)
    
    F_g = ±F_w*cos(theta)   (NB can be +ve or negative depending on whether it acts with or agains F_p)
    
    F_w = m*9.81ms^-2
    
    Via substitution and rearranging find that:
    
    (dt/m)*0.5*rho*C_d*A * v_f^2 + (1+(dt/m)*0.000091714*T_s*C_s*F_n) * v_f - (dt/m)*(F_p-0.0041*T_s*C_s*F_n-F_g) - v_i = 0
    
    Which is in the form:
    
    a*v_f^2 + b*v_f + c = 0
    
    And thus can be solved with the quadratic formula:
    
    v_f = (-b ± (b^2 - 4ac)^0.5)/(2a)
    
    Roll Resistance Equation Note
    -----------------------------
    The equation for F_r comes from Fundamentals of Ground Vehicle Dynamics by Thomas D. Gillespie, pg 118,
    NB however, there are some important differences between the form of the equation in the book and in this function: 
        
        1.  Velocity in the book is in mph, in this function the form has been converted to use m/s.
        2.  A factor "Tyre_state" (Ts) can be applied as a 1.2 multiplier to the equation in this function. This is because, in 
            the book above, on page 112, it states the roll resistance is approximately 20% higher for cold tyres. Thus, when
            tests of roll resistance are performed (including those that lead to the standard equation on page 118) apparently
            the vehicles are driven for 20 miles first to ensure they are warm. Because buses stop and start so much, it seems
            wisest to assume the tyres will not get very warm, hence why this 20% additional roll resistance can be applied.

    Parameters
    ----------
    F_p : int or float (N)
        Force of propulsion, ie the force that actually results from torque at the wheels trying to overcome the retarding forces and
        accelerate the vehicle.
    F_n : int or float (N)
        Normal force, the component of weight force that is perpendicular to the road surface.
    F_g : int or float (N)
        Grade force, the component of weight force that is parallel to the road surface ie the component of weight force that tries to 
        either slow (when travelling uphill) the vehicle or speed it up (when travelling downhill).
    m : int or float (kg)
        The mass of the vehicle.
    v_i : int or float (m/s)
        The initial velocity of the vehicle. If iterating over time steps, v_i is the final velocity of the previous time step.
    C_d : int or float (unitless)
        Drag coefficient.
    A : int or float (m^2)
        Vehicle Frontal area ie the area perpindicular to the direction of travel).
    dt : int or float (s)
        The duration of time between v_i and v_f.
    rho : int or float (kg/m^3) (optional input)
        The density of the air in kg/m^3, defaults to the value (two 2 decimal places) at 0 degrees and 1 atm of pressure.
    T_s : int or float (unitless) (optional input)
        Tyre state factor, taking a value of 1.0 for warm tyres and 1.2 for cold tyres. Defaults to 1.2.
    C_s : int or float (unitless) (optional input)
        Road surface coefficient, 1 for concrete, 1.2 for rough concrete or regular bitumen and 1.5 for hot bitumen. Defaults to 1.5.

    Returns
    -------
    v_f : int or float (m/s)
        The final velocity of the vehicle due to the F_p input.
    accel : int or float (ms^-2)
        The acceleration of the vehicle over the time step according to (v_f-v_i)/dt. NB 'a' is not used since it is used for the polynomial coefficient.
    F_d : int or float (N)
        The drag force opposing the motion in untis N (whose size opposes the direction of velocity).
    F_r : int or float (N)
        The roll resistance force opposing the motion provided by F_p.

    """
    
    # Calculating the quadratic coefficients
    
    a = (dt/m)*0.5*rho*C_d*A
    b = (1+(dt/m)*0.000091714*T_s*C_s*abs(F_n))
    c = -(dt/m)*(F_p-0.0041*T_s*C_s*abs(F_n)-F_g)-v_i
    
    # Solving the quadratic formula for the roots
    v1 = (-b + (b**2 - 4*a*c)**0.5)/(2*a)
    v2 = (-b - (b**2 - 4*a*c)**0.5)/(2*a)
    
    # Assigning v_f to the logical root:
    v_f = v1 if abs(v1)<abs(v2) else v2
    
    # Calculating acceleration
    accel = (v_f - v_i)/dt
    
    # Calculating the drag force
    F_d = -1*0.5*rho*(v_f**2)*C_d*A
    
    # Calculating the roll resistance
    # NB the boolean condition accommodates F_n being passed as -ve or +ve and ensures F_r opposes F_p
    F_r = T_s*(0.0041 + 0.000091714*v_f)*C_s*F_n*(-1 if F_n>0 else 1)
    
    return(v_f,accel,F_d,F_r)

#%%

def change_in_velocity_cubic_for_known_propulsive_power(P_p,F_n,F_g,m,v_i,C_d,A,dt,rho='undefined', T_s=1.2, C_s=1.5):
    """
    This function takes a known power of propulsion and calculates the acceleration of the vehicle without needing
    to know the force of propulsion, resistive drag force and roll resistance. 
    
    Essentially, it finds the change in velocity of the vehicle, propulsive force and the retarding forces to the 
    vehicles motion, all in one step. This is achieved thanks to the (summary) derivation below. For the full detail
    see "Heavy vehicle acceleration for a known torque or power at wheels.pdf" which can be found in the 
    "Simulation Design Decisions.one" at the time of writing.

    Derivation
    ==========
    
    a = (v_f - v_i)/dt = ΣF/m = (F_p + F_d + F_r + F_g)/m
    where critically, F_p defines the +ve direction and F_d and F_r upon substitution of there equations have the 
    opposite sign showing they oppose the motion. Thus the values of F_d and F_r output from the function have the
    opposite sign to the F_p input. F_g can contribute to motion or opposite it depending on whether the bus is going
    down or uphill.
    
    F_p = P_p/v_f
    
    F_d = -0.5*rho*v_f^2*C_d*A
    (NB that the equation for F_d is -ve indicating its direction opposes F_p)
    
    F_w = m*9.81ms^-2
    
    F_n = F_w*cos(theta)    (theta is the slope angle of the road surface)
    
    F_r = -T_s*(0.0041 + 0.000091714v_f)*C_s*F_n
    (NB that the equation for F_r is -ve indicating its direction opposes F_p. To ensure this, the F_n input is checked
     so if it is -ve valued (as is common for F_w and F_n) it can be made positive where necessary to ensure F_r < 0.
    (For more details on the roll resistance equation, see the note later below)
    
    F_g = ±F_w*cos(theta)   (NB can be +ve or negative depending on whether it acts with or agains F_p)
    
    Via substitution and rearranging find that:
    
    (dt/m)*0.5*rho*C_d*A * v_f^2 + (1+(dt/m)*0.000091714*T_s*C_s*F_n) * v_f - (dt/m)*((P_p/v_f)-0.0041*T_s*C_s*F_n-F_g) - v_i = 0
    
    Which when multiplied through by v_f becomes:
        
    (dt/m)*0.5*rho*C_d*A * v_f^3 + (1+(dt/m)*0.000091714*T_s*C_s*F_n) * v_f^2 + ((dt/m)*(0.0041*T_s*C_s*F_n+F_g)-v_i) * v_f - dt*P_p/m = 0
        
    Which is a cubic of the form:
    
    a*v_f^3 + b*v_f^2 + c*v_f + d = 0
    
    And thus the roots can be solved with the cubic formula (function simply uses numpy cubic root finder).
    
    Roll Resistance Equation Note
    -----------------------------
    The equation for F_r comes from Fundamentals of Ground Vehicle Dynamics by Thomas D. Gillespie, pg 118,
    NB however, there are some important differences between the form of the equation in the book and in this function: 
        
        1.  Velocity in the book is in mph, in this function the form has been converted to use m/s.
        2.  A factor "Tyre_state" (Ts) can be applied as a 1.2 multiplier to the equation in this function. This is because, in 
            the book above, on page 112, it states the roll resistance is approximately 20% higher for cold tyres. Thus, when
            tests of roll resistance are performed (including those that lead to the standard equation on page 118) apparently
            the vehicles are driven for 20 miles first to ensure they are warm. Because buses stop and start so much, it seems
            wisest to assume the tyres will not get very warm, hence why this 20% additional roll resistance can be applied.

    Parameters
    ----------
    P_p : int or float (N)
        Power of propulsion, ie the power that actually reaches the wheels trying to overcome the retarding forces and
        accelerate the vehicle.
    F_n : int or float (N)
        Normal force, the component of weight force that is perpendicular to the road surface.
    F_g : int or float (N)
        Grade force, the component of weight force that is parallel to the road surface ie the component of weight force that tries to 
        either slow (when travelling uphill) the vehicle or speed it up (when travelling downhill).
    m : int or float (kg)
        The mass of the vehicle.
    v_i : int or float (m/s)
        The initial velocity of the vehicle. If iterating over time steps, v_i is the final velocity of the previous time step.
    C_d : int or float (unitless)
        Drag coefficient.
    A : int or float (m^2)
        Vehicle Frontal area ie the area perpindicular to the direction of travel).
    dt : int or float (s)
        The duration of time between v_i and v_f.
    rho : int or float (kg/m^3) (optional input)
        The density of the air in kg/m^3, defaults to the value at 0 degrees and 1 atm of pressure.
    T_s : int or float (unitless) (optional input)
        Tyre state factor, taking a value of 1.0 for warm tyres and 1.2 for cold tyres. Defaults to 1.2.
    C_s : int or float (unitless) (optional input)
        Road surface coefficient, 1 for concrete, 1.2 for rough concrete or regular bitumen and 1.5 for hot bitumen. Defaults to 1.5.

    Returns
    -------
    v_f : int or float (m/s)
        The final velocity of the vehicle due to the F_p input.
    accel : int or float (ms^-2)
        The acceleration of the vehicle over the time step according to (v_f-v_i)/dt. NB 'a' is not used since it is used for the polynomial coefficient.
    F_p : int or float (N)
        The propulsion force, ie the force that results from P_p input at the wheels, trying to overcome the retarding forces and
        accelerate the vehicle.
    F_d : int or float (N)
        The drag force opposing the motion in untis N (whose size opposes the direction of velocity).
    F_r : int or float (N)
        The roll resistance force opposing the motion provided by F_p.

    """
    
    # Checking if rho was passed, else calculating it for air at 1 Atm and 0 degrees celcius
    if rho == 'undefined':
        rho = 101325/(287.058*273.15)   # based on rho = P/R*T
    
    # Calculating the quadratic coefficients
    
    # As per the documentation, the coefficients below are derived assuming F_d and F_r are negative, opposing the positive direction of F_p. 
    # However, ensuring that this is the case in practice involves careful handling of the F_n (normal force) input. As per the docs above, 
    # F_n = F_w*cos(theta), where F_w = ±m*9.81ms^-2, depending on whether the user has considered F_w to have a downward direction as is common,
    # or has only considered F_w's magnitude in their F_n calculation. Thus, the coefficients are defined in a way where F_n > 0 ensures F_r < 0
    # as desired.
    a = (dt/m)*0.5*rho*C_d*A
    b = (1+(dt/m)*0.000091714*T_s*C_s*abs(F_n))     
    c = (dt/m)*(0.0041*T_s*C_s*abs(F_n)+abs(F_g))-v_i    #NB F_n needs to be treated as +ve here for the derivation
    d = -dt*P_p/m
    
    # Solving the quadratic formula for the roots
    roots = np.polynomial.Polynomial([d,c,b,a]).roots()
    
    # Assigning v_f to the logical root based on which is closest to v_i:
    v_f = roots[np.argmin(abs(roots - v_i))]
    
    # Calculating acceleration
    accel = (v_f - v_i)/dt
    
    # Calculating the force of propulsion
    F_p = P_p/v_f
    
    # Calculating the drag force
    F_d = -1*0.5*rho*(v_f**2)*C_d*A
    
    # Calculating the roll resistance
    # NB the boolean condition accommodates F_n being passed as -ve or +ve and ensures F_r opposes F_p
    F_r = T_s*(0.0041 + 0.000091714*v_f)*C_s*F_n*(-1 if F_n>0 else 1)
    
    return(v_f,accel,F_p,F_d,F_r)


#%% Testing the function

if __name__ == "__main__":
    
    m = 20000
    rho = 1.3
    F_p = 6480/0.275
    F_p = 22000/0.275
    F_n = 9.81*m
    F_g = 0
    v_i = 2
    C_d = 0.7
    A = 11
    dt = 1
    
    v_f,a,F_d,F_r = change_in_velocity_quadratic_for_known_propulsive_force(F_p,F_n,F_g,m,v_i,C_d,A,dt,rho)
    print(f'v_f = {v_f} m/s')
    print(f'a = {a} ms^-2')
    print(f'F_d = {F_d} N')
    print(f'F_r = {F_r} N')
    print()
    
    P_p = 200000
    v_i2 = 10
    
    v_f,a,F_p2,F_d,F_r = change_in_velocity_cubic_for_known_propulsive_power(P_p,F_n,F_g,m,v_i2,C_d,A,dt,rho)
    print(f'v_f = {v_f} m/s')
    print(f'a = {a} ms^-2')
    print(f'F_p = {F_p} N')
    print(f'F_d = {F_d} N')
    print(f'F_r = {F_r} N')    
    
    # Below useful for debugging, for checking the forces out of the quadratic are correct
    import sys
    sys.path.insert(0, r'C:\Users\joelb\OneDrive\Documents\Kinetic EV\Kinetic_EV_Analyses\Specific_Functions')
    from Propulsion_force_power_and_energy_consumption import propulsion_force_power_and_energy_consumption
    F_p_check,P_p_check,_ = propulsion_force_power_and_energy_consumption(m,a,v_f,F_d,F_r,F_g,dt)