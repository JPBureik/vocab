#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 01:59:10 2019

@author: JP

This class defines the Vocable class including methods for creating, editing
and practicing vocable items.
"""

# Standard library imports
from datetime import date
import pandas as pd
import sys
import warnings
from tabulate import tabulate
from termcolor import colored

# Local application imports
import terminal_commands as tc  # Use tc.del_lines(int) to delete int previous
# lines in terminal
import string_matching as sm  # Check for duplicates during input

# Ignore warning for inefficient pickling when storing mixed data types
warnings.filterwarnings('ignore', category=pd.io.pytables.PerformanceWarning)

''' EDIT THIS FOR V1.0 RELEASE'''
# Dev flags
save = False

'''
BEFORE PRINTING ANYTHING ALWAYS REPRINT HEADER FOR LAYOUT
'''


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
    _language_choice = ['English', 'French']    # Foreign languages in which
    # you have vocab items
    _num_for_practice = 100  # Max number of cards for daily practice

    # Initialize class variables needed for methods
    _set_of_cards = set()   # This is your entire library of vocab items in a
    # given foreign language

    """
    INIT
    """

    def __init__(self, native, foreign):
        """Initialize a vocab card with native and foreign vocable, set phase
        to 0 and date to today."""
        # Vocab attributes
        self._phase = 0
        self._date = date.today()
        self._native = native
        self._foreign = foreign

    """
    PRIVATE METHODS
    """

    @classmethod
    def __load_vocab(cls):
        """Load vocab from file (pandas DataFrame) and create set of vocable
        cards."""
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

    @classmethod
    def __overview(cls):
        """Display overview of vocab library for a given foreign language."""
        table_list = []
        header_column = cls._foreign_language
        header_line = ['', 'Total', 'Phase 0', 'Phase 1', 'Phase 2', 'Phase 3',
                       'Phase 4', 'Phase 5', 'LTM', 'Last practiced']
        table_list.append(header_column)
        table_list.append(len(cls._df))
        for l in range(1, 8, 1):
            table_list.append(len(cls._df.loc[cls._df['Phase'] == l-1,
                                              cls._foreign_language]))
        table_list.append(max(cls._df['Date']))
        # Print table
        print(tabulate([table_list], headers=header_line,
                       tablefmt='fancy_grid', numalign='center',
                       stralign='center'))

    @classmethod
    def __main_menu(cls):
        """Main menu: present choice of all other public class methods after
        setup."""
        print('MAIN MENU')
        selection = input('Select action: 0 = Input, 1 = Edit, 2 = Practice;'
                          ' q = Exit\n')
        # Delete input from terminal
        tc.del_lines(1)
        if selection == '0':
            cls.input_loop()
        elif selection == '1':
            cls.edit_loop()
        elif selection == '2':
            pass
        elif selection == 'q':
            # exit
            print('Exit')
            sys.exit()
        else:
            # Throw error
            pass

    """
    PUBLIC METHODS
    """

    @classmethod
    def initialize(cls):
        """Initialization: Choose foreign language, display overview, then enter
        main menu."""
        # Display name of program
        tc.del_lines(1)
        print('VOCAB TRAINING PROGRAM')
        # Select foreign language and store choice in class variable
        selection = int(input('Select language: 0 = ' +
                              cls._language_choice[0] + ', 1 = ' +
                              cls._language_choice[1] + ':\n'))
        cls._foreign_language = cls._language_choice[selection]
        # Delete input from terminal
        tc.del_lines(2)
        # Load corresponding vocab library
        cls.__load_vocab()
        # Print confirmation
        print('You have selected ' + cls._foreign_language + '.')
        # Display overview
        cls.__overview()
        # Present main meu options
        cls.__main_menu()

    @classmethod
    def input_loop(cls):
        """Input: Enter and save new vocab items"""
        # Add new entries to DataFrame and save
        def save_input(native_input_str, foreign_input_str):
            # Create new vocable card:
            new_card = Vocable(native_input_str, foreign_input_str)
            # Parameters for DataFrame
            col = ['German', cls._foreign_language, 'Phase', 'Date']
            # Create DataFrame containing the new input item
            df_new = pd.DataFrame([[new_card._native, new_card._foreign,
                                    new_card._phase,  new_card._date]],
                                  columns=col)
            # Add to existing DataFrame
            cls._df = cls._df.append(df_new, ignore_index=True)
            # Save appended DataFrame to original vocab .h5 file
            cls._df.to_hdf(cls._vocab_file, key='df', mode='w')

        # Define local aux functions
        def foreign_input(native_input_str):
            # Change enclosed variable to exit input function
            nonlocal continue_input
            # Update enclosed counter variable
            nonlocal counter
            # Input new vocab item: answer
            foreign_input_str = input('Enter question [' +
                                      cls._foreign_language + ']:\n')
            # Check for exit command
            if foreign_input_str not in ['q', 'm']:
                # Check for duplicates
                dupl_foreign = sm.input_string_matching(foreign_input_str,
                                                        cls._foreign_language,
                                                        cls._vocab_file)
                if dupl_foreign is False:
                    # Update progress counter
                    counter += 1
                    # Delete lines from previous input
                    if counter == 1:
                        tc.del_lines(15)
                    else:
                        tc.del_lines(16)
                    # Save
                    if save is True:
                        save_input(native_input_str, foreign_input_str)
                    # Display updates: Reload vocab file to update changes
                    cls.__load_vocab()
                    # Display updates: Reprint header
                    print('VOCAB TRAINING PROGRAM\nYou have selected ' +
                          cls._foreign_language + '.')
                    # Display updates: Print updated overview
                    cls.__overview()
                    # Display updates: Reprint main menu and input confirmation
                    print('MAIN MENU\nSelect action: 0 = Input, 1 = Edit, 2'
                          ' = Practice; q = Exit\nYou have selected INPUT. '
                          'Enter m to modify previous item. Enter q to exit.'
                          '\n')
                    # Display progress counter
                    if counter == 1:
                        print('{} new entry added.'.format(counter))
                    else:
                        print('{} new entries added.'.format(counter))
                else:
                    foreign_input(native_input_str)  # Recursion
            elif foreign_input_str == 'q':
                # Delete lines from previous input
                if counter < 1:
                    tc.del_lines(8)
                else:
                    tc.del_lines(9)
                continue_input = False
            elif foreign_input_str == 'm':
                # Go back to modify native input
                tc.del_lines(4)
                native_input()

        def native_input():
            # Change enclosed variable to exit input function
            nonlocal continue_input
            # Input new vocab item: question
            native_input_str = input('Enter question [' +
                                     cls._native_language + ']:\n')
            # Check for exit command
            if native_input_str != 'q':
                # Check for duplicates
                dupl_native = sm.input_string_matching(native_input_str,
                                                       cls._native_language,
                                                       cls._vocab_file)
                if dupl_native is False:
                    foreign_input(native_input_str)
                else:
                    native_input()  # Recursion
            else:
                # Delete lines from previous input
                if counter < 1:
                    tc.del_lines(6)
                else:
                    tc.del_lines(7)
                continue_input = False

        # Confirm selection choice
        print('You have selected INPUT. Enter m to modify previous item. Enter'
              ' q to exit.\n')

        counter = 0  # Variable that indicates the progress
        continue_input = True  # Variable that exits the input function

        while continue_input is True:
            native_input()

        # Return to main menu after input
        cls.__main_menu()

    @classmethod
    def edit_loop(cls):
        """Edit"""
        # Find a vocab item and edit it
        def search_vocab():
            # Change enclosed variable to exit edit function
            nonlocal continue_edit
            search_str = input('Search ' + cls._foreign_language + ' vocab '
                               'database:\n')
            # Check for exit command
            if search_str not in ['q']:
                # Search vocab database
                search_results = sm.edit_string_matching(search_str,
                                                         cls._foreign_language,
                                                         cls._vocab_file)
                # Edit
                # Save
                # Option for multiple edits off same search
                # Option to delete items
                # Delete previous lines
                # Recursion
            else:
                continue_edit = False

        # Confirm selection choice
        print('You have selected EDIT. Enter m to modify an item. Enter q to '
              'exit.\n')

        continue_edit = True  # Variable that exits the input function

        while continue_edit is True:
            search_vocab()

        # Return to main menu after input
        cls.__main_menu()

    @classmethod
    def practice(cls):
        """Practice"""
        for card in cls._set_of_cards:
            question = card._native_item
            answer = input(question + '\n')
            if answer == card._foreign_item:
                print('Correct!\n')
            else:
                print('Incorrect!\n')


# %% EXECUTE

if __name__ == "__main__":
    Vocable.initialize()
