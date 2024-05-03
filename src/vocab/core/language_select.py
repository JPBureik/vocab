#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:36:55 2024

@author: jp
"""

from vocab.core.config import foreign_languages

def language_select(ti):
    
    # Ask for user input to select foreign language:
    query_str = 'Select language: {}:\n'.format(
        ', '.join([f'{str(idx)} = {lang}'
                   for (idx, lang) in enumerate(foreign_languages)])
        )
    foreign_lang = foreign_languages[int(input(query_str))]
    
    # Delete user input from terminal and print confirmation:
    ti.del_lines(1)
    print(f'You have selected {foreign_lang}. Enter <quit> to end.'
          'Enter <mod> to edit.')

    return foreign_lang