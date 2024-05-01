#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:20:58 2024

@author: jp
"""

# Standard library imports:
from tabulate import tabulate

from vocab.core.config import session_volume

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
    
def progress_bar(count):
    prog = '█' * count
    prog += ' ' + str(count) + '/' + str(session_volume)
    print(' ' + prog)
