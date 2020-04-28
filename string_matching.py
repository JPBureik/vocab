#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:28:32 2020

author: jp

This function matches strings between new input and a string in a specified
column of a Pandas DataFrame saved to a .h5 file to avoid duplicates. It
displays a list of matching strings and returns a boolean.
"""

# Standard library imports
import pandas as pd
from termcolor import colored
import terminal_commands as tc

def string_matching(input_str, column_name, h5_file):

    database = pd.read_hdf(h5_file, 'df')


    if database[database[column_name].str.contains(input_str)].empty == False:
        print(colored('Duplicate warning:', 'red'))
        print(database[database[column_name].str.contains(input_str)])
        proceed = input('Proceed? [y/n]\n')
        if proceed == 'y':
            dupl = False
             # Delete lines of duplicate list
            tc.del_lines(len(database[database[column_name].str.contains\
                                     (input_str)])+4)
        elif proceed == 'n':
            dupl = True
            # Delete lines of duplicate list
            tc.del_lines(len(database[database[column_name].str.\
                                     contains(input_str)])+5)
        else:

            dupl = False

    return dupl
