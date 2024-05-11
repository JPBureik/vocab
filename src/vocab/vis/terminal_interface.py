#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 01:42:30 2019

@author: jp

All functions that interact with the terminal interface take the instance of
ti as argument.

"""
import os
import sys
import subprocess
import pandas as pd
from tabulate import tabulate
from matplotlib import pyplot as plt

from vocab.core.config import session_volume, phase_intervals
from vocab.vis import radial_bar_chart as rbc

import matplotlib


import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class TerminalInterface(metaclass=Singleton):
    
    # Class Attributes:
        
    # Terminal commands:
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    
    def __init__(self):
        self._t = sys.stdout
        # Set backend for Matplotlib:
        matplotlib.use('module://itermplot')
        
    def del_lines(self, number_of_lines):
        for k in range(number_of_lines):
            self._t.write(self.CURSOR_UP_ONE)
            self._t.write(self.ERASE_LINE)
            
    def print_phase(self, phase):
        chart_data = pd.DataFrame([[phase, len(phase_intervals) - 1]])
        self.phase_plot = rbc.create_radial_chart(chart_data, figsize = (0.8,0.8), fontsize = 14, color_theme = 'Purple')
        
    def close_phase_plot(self):
        plt.close(self.phase_plot)
            
    @staticmethod
    def print_table(foreign_lang, table_df):
        table_list = []
        header_column = foreign_lang
        header_line = ['', 'Total', 'Phase 0', 'Phase 1', 'Phase 2', 'Phase 3',
                       'Phase 4', 'Phase 5', 'LTM', 'Last practiced']
        table_list.append(header_column)
        table_list.append(len(table_df))
        for l in range(1, 8, 1):
            table_list.append(len(table_df.loc[table_df['Phase'] == l-1, foreign_lang]))
        table_list.append(max(table_df['Date']))
        # Print table
        print(tabulate([table_list],headers=header_line,tablefmt='fancy_grid',numalign='center',stralign = 'center'))
            
    @staticmethod
    def progress_bar(count, total):
        prog = '█' * count
        prog += ' ' + str(count) + '/' + str(total)
        print(' ' + prog)
        
        