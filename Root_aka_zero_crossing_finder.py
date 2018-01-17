# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 17:07:26 2017

@author: jcb137

__________________________________________ ABOUT THE FUNCTION _______________________________________________________

This function is a root finding method know as the Bisection Method: https://en.wikipedia.org/wiki/Bisection_method
where you have a function f(x) where you are trying to find the x that satisfies f(x) = 0

INPUTS
f: the function for which you are trying to find the root of (NB here, f input is a python function which calculates the function f(x))
    to input a function, use the lambda function, an example follows:
        
        Consider trying to find the zero crossing for the following function y(x) = mx+c. Your function for y might be a script
        saved that looks like the following:
            
            def y(x,m,c):
                y = m*x + c
                return (y)
                
        To pass this function to the bisection method and find the x that makes y = 0, you use the lambda function:
            
            x_root = bisection_method(f = lambda x: y(x, m = boo, c = bla), a = ble, b = something, tol = something_else)
            
        In this arrangement, the bisection method input f recieves a lambda function. Lambda functions format are as follows:
            
            lambda arg_1, arg_2, ..., arg_n : g(arg_1, arg_2, ..., arg_n)   where arg is short for arguments (aka variables)
            
        where on the right of the colon we have some equations which depend on the arguments listed on the left of the colon.
        
        So in our case, the bisection method f input receives f = lambda x: y(x, m = boo, c = bla), where lambda has one argument, x,
        (m and c have been defined as boo and bla! and now are constant, since these are NOT arguments of lambda). So inside the 
        bisection method, when f is called, needs one argument, the argument for x! Hopefully that makes sense :-).

a,b: the range x = [a,b] where a and b are the lower and upper starting guesses of x respectively, such that you can be sure
     the root f(x) = 0, lies somewherein the interval a<= x <= b. NB while you input the initial range [a,b] the method updates
     a and b each iteration such that the range it searches for the root in continues to reduce until it has converged to the root
          
     See the wiki link above if still confused. 
    
tol: the tolerance where tol > error in order for a root to be considered found

OUTPUT
root_val: the value of the parameter/variable that satisfies the tolerance corresponding to a root

"""

def bisection_method(f, a, b, tol):
    
    if f(a)*f(b) > 0:
        print('a = {0}, f(a) = {1}, b = {2}, f(b) = {3}]'.format(a, f(a), b, f(b)))
        raise Exception("WARNING!!!!! f(a) and f(b) have the same sign\nsuggesting either multiple roots or a too smaller range has been given.")
    
    else:   # f(x=a) and f(x=b) have different signs so there is at least one root between them
        
        i = 0   # creating an indice to count the iterations done before tolerance is meet for a found root    
        
        c = (a+b)/2.0  # the point x = c is defined as the point halve way between the points x = a and x = b
        
        while abs(f(c)) > tol and (b-a)/2.0 > tol:     # while BOTH abs(f(c)) > tol and (b-a)/2.0 > tol neither tolerance has been met!
        
#            # DEBUGGING ------------------------------------------------------------------------------------------
#            print('iteration {0}: c = {1}, f(c) = {2} [a = {3}, f(a) = {4}, b = {5}, f(b) = {6}]'.format(i, c, f(c), a, f(a), b, f(b)))  # printing the result of the current iteration
#            # ----------------------------------------------------------------------------------------------------
        
            if f(a)*f(c) > 0:              # if f(x=c) has the same sign as f(x=a), update a with c
                a = c
            else :                         # else f(x=c) has the same sign as f(x=b) so uptdate b with c 
                b = c
            
            c = (a+b)/2.0  # find next iterations new x = c point, again halfway between x = a and x = b points 
        
            i += 1         # incremeting the number of iterations counter
        
    return(c)
    