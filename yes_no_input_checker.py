# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 12:05:12 2016

@author: jcb137
"""

# This function simply takes a user input which should either be 'y' for yes or 'n' for no. If the input is anything other
# than those two options the function simply asks the user to re-enter there input.

# YES_NO_INPUT_CHECKER ----------------------------

# This function is used to check the user input is either 'y' for yes or 'n' for no.
def yes_no_input_checker(user_input):
    if user_input != 'y' and user_input != 'n':
        user_input = input('Invalid input, please re-enter y for yes or n for no: ')
        return(yes_no_input_checker(user_input))
    else:
        return(user_input)