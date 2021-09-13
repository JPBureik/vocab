#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 01:42:30 2019

@author: jp

This function deletes a specified number of previous lines from the terminal

"""

def del_lines(number_of_lines):
    import sys
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    for k in range(number_of_lines):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)