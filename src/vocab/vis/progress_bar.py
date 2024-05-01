#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:21:28 2024

@author: jp
"""

def progress_bar(count, total):
    prog = '█' * count
    prog += ' ' + str(count) + '/' + str(total)
    print(' ' + prog)
