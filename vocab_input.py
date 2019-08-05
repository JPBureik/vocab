#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 20:26:13 2019

@author: jp
"""

# Standard library imports
import pandas as pd
import terminal_commands as tc
import datetime
from termcolor import colored
from tabulate import tabulate


# Local application imports
from . import vocable

#card = vocable.Vocable('english', 'Jahr', 'year')

#%% Select language

language_choice = ['English', 'French']

def language_select(language_choice):

    lang = int(input('Select language: 0 = ' + language_choice[0] + ', 1 = ' + language_choice[1] + ':\n'))
    tc.del_lines(1)
    print('You have selected ' + language_choice[lang] + '. Enter <quit> to end. Enter <mod> to edit.')

    return language_choice[lang]

#%%
    
lang = language_select(language_choice)
    
list_of_cards = []
input_str = ''

''' Loop structure:
    1- Create function
    2- Create object
    3- Map function onto object
    '''

for k in range(100):
    while input_str != 'quit':
        card = vocable.Vocable('lang', '', '')
        input_str = input('Type native: ')
        if input_str != 'quit':
            card.native = input_str
            input_str = input('Type ' + lang + ': ')
            card.foreign = input_str
            list_of_cards.append(card)

#%% Îgnore performance warning

import warnings
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

#%% Input new vocab

def vocab_input(lang):

    # Display stats
    def print_table(counter, language_choice, lang, df):
        table_list = []
        header_column = language_choice[lang]
        header_line = ['','Total', 'Phase 0', 'Phase 1','Phase 2','Phase 3','Phase 4','Phase 5', 'LTM', 'Last practiced']
        table_list.append(header_column)
        table_list.append(len(df))
        for l in range(1,8,1):
            table_list.append(len(df.loc[df['Phase'] == l-1, language_choice[lang]]))
        table_list.append(max(df['Date']))
        # Print table
        print(tabulate([table_list],headers=header_line,tablefmt='fancy_grid',numalign='center',stralign = 'center'))
        # Print one line before question
        if counter == 0:
            print('\n')

    # Display progress
    def display_progress():
        if counter == 1:
            print(str(counter) + ' new entry added\n')
        else:
            print(str(counter) + ' new entries added\n')

    # During input check for duplicates
    def check_for_duplicates(german):
        if df[df['German'].str.contains(german)].empty == False:
            print(colored('Duplicate warning:', 'red'))
            print(df[df['German'].str.contains(german)])
            proceed = input('Proceed? [y/n]\n')
            if proceed == 'y':
                dupl = False
                # Delete lines of duplicate list
                tc.del_lines(len(df[df['German'].str.contains(german)])+4)
            elif proceed == 'n':
                dupl = True
                # Delete lines of duplicate list
                tc.del_lines(len(df[df['German'].str.contains(german)])+3)
        else:
            dupl = False
        return dupl

    # Add new vocab items to existing vocab df
    def register_new_vocab(counter, language_choice, lang, german, df):
        # Parameters for df
        col = ['German', language_choice[lang], 'Phase', 'Date']
        alignment = ['', ' ']
        # Append new items to existing vocab df
        foreign = input ('Type answer  ' + alignment[lang] + '[' + language_choice[lang] +  ']: ')
        # Check for abort signal
        if foreign != 'quit' and foreign != 'mod':
            df2 = pd.DataFrame([[german, foreign, 0, datetime.date.today()]], columns=col)
            df = df.append(df2,ignore_index=True)
            # Count number of added items
            counter += 1
            mod = False
        elif foreign == 'mod':
            mod = True
            tc.del_lines(1)
        elif foreign == 'quit':
            mod = False
            german = 'quit' # In order to break main loop
        return counter, df, german, mod

    # Initialize parameters
    vocab_file = ['vocab_en.h5', 'vocab_fr.h5']
    german = ''
    counter = 0
    mod = False

    # Main loop
    while german != 'quit':
        # Load vocab file (inside loop so that changes are immediate)
        df = pd.read_hdf(vocab_file[lang], 'df')
        # Display overview
        print_table(counter, language_choice, lang, df)
        # Display progress after first saved card
        if counter > 0:
            display_progress()
        # Input new vocab
        german = input('Type question [German]: ')
        if german != 'quit':
            # Check for duplicates
            dupl = check_for_duplicates(german)
            if dupl == False:
                # Add new vocab items to existing vocab df
                counter, df, german, mod = register_new_vocab(counter, language_choice, lang, german, df)
                # Save to vocab file
                df.to_hdf(vocab_file[lang], key='df', mode='w')
            # Delete lines of previous question
            if mod == True: # mod already deletes one line
                tc.del_lines(8)
            else:
                tc.del_lines(9)

#%% Execute

if __name__ == '__main__':

    lang = language_select(language_choice)
    vocab_input(lang)
