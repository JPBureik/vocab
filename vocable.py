#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 01:59:10 2019

@author: JP

This class defines the Vocable class including methods for creating, editing and
practicing vocable items.
"""

# Standard library imports
from datetime import date
import pandas as pd
from tabulate import tabulate
from termcolor import colored

# Local application imports
import terminal_commands as tc # Use tc.del_lines(int) to delete int previous
                               # lines in terminal
import string_matching as sm # Check for duplicates during input

#%%

class Vocable:
    """
    A vocable card and methods for input, editing and practice.

    Init args:
        native_item(str): vocable item in native language
        foreign_item(str): vocable item in foreign language
    """


    """
    TOP-LEVEL PRIVATE ATTRIBUTES
    """

    # Modifiable class variables
    _native_language = 'German'
    _language_choice = ['English', 'French']    # Foreign languages in which you
                                                # have vocab items
    _num_for_practice = 100 # Max number of cards for daily practice

    # Initialize class variables needed for methods
    _set_of_cards = set()   # This is your entire library of vocab items in a
                            # given foreign language

    """
    INIT
    """

    def __init__(self, native, foreign):
        # Vocab attributes
        self._phase = 0
        self._date = date.today()
        self._native = native
        self._foreign = foreign


    """
    PRIVATE METHODS
    """

    # Load vocab from file (pandas DataFrame) and create set of vocable cards
    @classmethod
    def __load_vocab(cls):
        # Load dataframe
        cls._vocab_file = 'vocab_' + cls._foreign_language[:2].lower() + '.h5'
        cls._df = pd.read_hdf(cls._vocab_file, 'df')
        # Compile set of vocable cards
        for item in cls._df.iterrows():
            card = Vocable(item[1][cls._native_language],
                           item[1][cls._foreign_language])
            card._phase = item[1]['Phase']
            card._date = item[1]['Date']
            cls._set_of_cards.add(card)

    # Display overview of vocab library for a given foreign language
    @classmethod
    def __overview(cls):
        table_list = []
        header_column = cls._foreign_language
        header_line = ['','Total', 'Phase 0', 'Phase 1','Phase 2','Phase 3',\
                       'Phase 4','Phase 5', 'LTM', 'Last practiced']
        table_list.append(header_column)
        table_list.append(len(cls._df))
        for l in range(1,8,1):
            table_list.append(len(cls._df.loc[cls._df['Phase'] == l-1,\
                                              cls._foreign_language]))
        table_list.append(max(cls._df['Date']))
        # Print table
        print(tabulate([table_list],headers=header_line,tablefmt='fancy_grid',\
                       numalign='center',stralign = 'center'))

    # Main menu: present choice of all other public class methods after setup
    @classmethod
    def __main_menu(cls):
        print('MAIN MENU')
        selection = int(input('Select action: 0 = Input, 1 = Edit, 2 = '\
                              'Practice\n'))
        # Delete input from terminal
        tc.del_lines(1)
        if selection == 0:
            cls.input_loop()
        elif selection == 1:
            pass
        else:
            pass


    """
    PUBLIC METHODS
    """


    ''' Initialization: Choose foreign language, display overview, then enter
    main menu
    '''
    @classmethod
    def initialize(cls):
        # Select foreign language and store choice in class variable
        selection = int(input('Select language: 0 = ' +\
                                          cls._language_choice[0] + ', 1 = ' +\
                                          cls._language_choice[1] + ':\n'))
        cls._foreign_language = cls._language_choice[selection]
        # Delete input from terminal
        tc.del_lines(1)
        # Load corresponding vocab library
        cls.__load_vocab()
        # Print confirmation
        print('You have selected ' + cls._foreign_language + '.')
        # Display overview
        cls.__overview()
        # Present main meu options
        cls.__main_menu()

    ''' Input: Enter and save new vocab items
    '''
    @classmethod
    def input_loop(cls):

        # Define local aux functions
        def foreign_input():
            # Change enclosed variable to exit input function
            nonlocal continue_input
            # Update enclosed counter variable
            nonlocal counter
            # Input new vocab item: answer
            foreign_input_str = input('Enter question [' +\
                cls._foreign_language + ']:\n')
            # Check for exit command
            if foreign_input_str != 'q':
                # Check for duplicates
                dupl_foreign = sm.string_matching(foreign_input_str,\
                    cls._foreign_language, cls._vocab_file)
                if dupl_foreign == False:
                    # Update progress counter
                    counter += 1
                    # Delete lines from previous input
                    if counter == 1:
                        tc.del_lines(5)
                    else:
                        tc.del_lines(6)
                    '''' save '''
                    print('')
                    # Display progress
                    if counter == 1:
                        print('{} new entry added.'.format(counter))
                    else:
                        print('{} new entries added.'.format(counter))
                else:
                    foreign_input() # Recursion
            else:
                # Delete lines from previous input
                tc.del_lines(9)
                continue_input = False

        def native_input():
            # Change enclosed variable to exit input function
            nonlocal continue_input
            # Input new vocab item: question
            native_input_str = input('Enter question [' +\
                cls._native_language + ']:\n')
            # Check for exit command
            if native_input_str != 'q':
                # Check for duplicates
                dupl_native = sm.string_matching(native_input_str,\
                    cls._native_language, cls._vocab_file)
                if dupl_native == False:
                    foreign_input()
                else:
                    native_input() # Recursion
            else:
                # Delete lines from previous input
                tc.del_lines(7)
                continue_input = False

        # Confirm selection choice
        print('You have selected INPUT. Enter q to exit.\n')

        counter = 0 # Variable that indicates the progress
        continue_input = True # Variable that exits the input function

        while continue_input == True:
            native_input()

        # Return to main menu after input
        cls.__main_menu()

    '''Edit
    '''
    @classmethod
    def edit(cls):
        pass

    '''Practice
    '''
    @classmethod
    def practice(cls):
        for card in cls._set_of_cards:
            question = card._native_item
            answer = input(question + '\n')
            if answer == card._foreign_item:
                print('Correct!\n')
            else:
                print('Incorrect!\n')


#%% EXECUTE

if __name__ == "__main__":
    Vocable.initialize()
