#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:28:32 2020

author: jp

This module provides functions that impplement string matching for different
methods in voable.py
"""

# Standard library imports
import pandas as pd
from termcolor import colored
import terminal_commands as tc


def input_string_matching(input_str, column_name, h5_file):
    """This function matches strings between new input string and a string in a
    specified column of a Pandas DataFrame saved to a .h5 file to avoid
    duplicates. It displays a list of matching strings and returns a boolean.
    """
    database = pd.read_hdf(h5_file, 'df')
    if database[database[column_name].str.contains(input_str)].empty is False:
        print(colored('Duplicate warning:', 'red'))
        print(database[database[column_name].str.contains(input_str)])
        proceed = input('Proceed? [y/n]\n')
        if proceed == 'y':
            dupl = False
            # Delete lines of duplicate list
            tc.del_lines(len(database[database[column_name].str.contains
                                      (input_str)])+4)
        elif proceed == 'n':
            dupl = True
            # Delete lines of duplicate list
            tc.del_lines(len(database[database[column_name].str.contains
                                      (input_str)])+6)
    else:
        dupl = False

    return dupl


def edit_string_matching(search_str, column_name, h5_file):
    """This function matches strings between a search string and specified
    colummns in a Pandas DataFrame saved to a .h5 file. It returns a DataFrame
    containing the lines of the original DataFrame that string match.
    """
    database = pd.read_hdf(h5_file, 'df')
    search_results = pd.DataFrame()
    german_results = database[database['German'].str.contains(search_str)]
    search_results = search_results.append(german_results)
    print(search_results)
    return search_results
