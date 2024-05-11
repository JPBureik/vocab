#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 00:37:36 2024

@author: jp
"""

from tabulate import tabulate
from datetime import date as dt


# Package imports:
from vocab.core.config import native_lang

class Vocable:
    
    def __init__(self, foreign_lang, native_vocable, foreign_vocable, phase=0, date='today'):
        self.native_lang = native_lang
        self.foreign_lang = foreign_lang
        self.native_vocable = native_vocable
        self.foreign_vocable = foreign_vocable
        self.phase = phase
        self.date = dt.today() if date=='today' else date
        
    def __repr__(self):
        header_line = [f'{self.foreign_lang}', f'{self.native_lang}', 'Phase', 'Date']
        table_list = [f'{self.foreign_vocable}', f'{self.native_vocable}', f'{self.phase}', f'{self.date}']
        # Print table
        return tabulate(
            [table_list], headers=header_line, tablefmt='rounded_grid',
            numalign='center', stralign = 'center'
            )