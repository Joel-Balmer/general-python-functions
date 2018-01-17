# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 12:34:14 2017

@author: jcb137
     ____.             .__    __________        .__                        
    |    | ____   ____ |  |   \______   \_____  |  |   _____   ___________ 
    |    |/  _ \_/ __ \|  |    |    |  _/\__  \ |  |  /     \_/ __ \_  __ \
/\__|    (  <_> )  ___/|  |__  |    |   \ / __ \|  |_|  Y Y  \  ___/|  | \/
\________|\____/ \___  >____/  |______  /(____  /____/__|_|  /\___  >__|   
                     \/               \/      \/           \/     \/  
                     
                     ABOUT THIS FUNCTION
        This function searches for substrings in dictionary keys and returns a dictionary
        containing the key and value pairs that match the substring. 
        If return_elements_missing_substring = 'y', it will return the stuff in the main dictionary
        that doesnt contain the substring. By default if return_elements_missing_substring isnt input,
        or is input incorrectly, it returns as tho return_elements_missing_substring = 'n'.

"""

# INPUTS -----------------------------------------------------
# main_dict: the dictionary I want to search through
# substring: the substring you want to find in main_dict's keys, can be a list containing multiple substrings
# return_elements_missing_substring: a 'n' for no or 'y' for yes input. If yes, the output dictionary is the key value pairs from the main_dict that
#                                 do not contain the substring  

# OUTPUTS ----------------------------------------------------
# sub_dict: a dictionary which contains the key, value pairs for those keys in main_dict that matched the substring
#           OR key, value pairs for those keys in main_dict that DID NOT match the substring, depending on what
#           return_elements_missing_substring was set too.

def dict_substring_searcher(main_dict, substrings, return_elements_missing_substring = 'n'):
    sub_dict = {}
    
    if type(substrings) == str:
        substrings = [substrings]   # if a single string was entered not in a list, put it in a list that is length one.
                                    # if we dont do this, (string in key for string in substrings) will iterate through
                                    # the individual letters of the substring, since a type str is itself an iterable.
                                    # It would then try and see if a letter in string is in keys, but we dont want to 
                                    # see if a single letter is in there, we want to know if the whole string is.
                                    # This issue only arose when I added the any(stuff in brackets) and the all(stuff in brackets)
                                    # which handles the passing of multiple strings in a list.
        
    if return_elements_missing_substring == 'y':
        for key in main_dict:
            if all(string not in key for string in substrings):
                sub_dict[key] = main_dict[key]
    
    else:
        for key in main_dict:
            if any(string in key for string in substrings):
                sub_dict[key] = main_dict[key]
                
    return(sub_dict)
    
    
# Testing the function:
if __name__ == "__main__":  
    main_dict = {'x': 1, 'dx':10, 'y':3, 'dy':5}
    
    sub_dict = dict_substring_searcher(main_dict, 'x')

