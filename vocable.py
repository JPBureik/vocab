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

# Ignore warning for inefficient pickling when storing mixed data types
warnings.filterwarnings('ignore', category=pd.io.pytables.PerformanceWarning)

''' EDIT THIS FOR V1.0 RELEASE'''
# Dev flags
save = False


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

        def input_string_matching(input_str, column_name):
            """String matching for input loop.

            This function matches strings between new input string and a
            string in a specified column of a Pandas DataFrame saved to a .h5
            file to avoid duplicates. It displays a list of matching strings
            and returns a boolean."""
            if (cls._df[cls._df[column_name].str.contains(input_str)].empty is
                    False):
                print(colored('Duplicate warning:', 'red'))
                print(cls._df[cls._df[column_name].str.contains(input_str)])
                proceed = input('Proceed? [y/n]\n')
                if proceed == 'y':
                    dupl = False
                    # Delete lines of duplicate list
                    tc.del_lines(len(cls._df[cls._df[column_name].str.contains
                                             (input_str)])+4)
                elif proceed == 'n':
                    dupl = True
                    # Delete lines of duplicate list
                    tc.del_lines(len(cls._df[cls._df[column_name].str.contains
                                             (input_str)])+6)
            else:
                dupl = False
            return dupl

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
                dupl_foreign = input_string_matching(foreign_input_str,
                                                     cls._foreign_language)
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
                dupl_native = input_string_matching(native_input_str,
                                                    cls._native_language)
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

        def edit_string_matching(search_str, column_name):
            """This function matches strings between a search string and
            specified colummns in a Pandas DataFrame saved to a .h5 file. It
            returns a DataFrame containing the lines of the original DataFrame
            that string match."""
            search_results = pd.DataFrame()
            # Search native items and append to search results
            native_results = cls._df[cls._df[cls._native_language].str.
                                     contains(search_str)]
            search_results = search_results.append(native_results)
            # Search foreign items and append excluding duplicate finds
            foreign_results = cls._df[cls._df[cls._foreign_language].str.
                                      contains(search_str)]
            for k in range(len(foreign_results)):
                if (foreign_results.index.tolist()[k] not in native_results.
                        index.tolist()):
                    search_results = search_results.append(foreign_results.
                                                           iloc[k])
            return search_results

        def edit_search_results(search_results):
            nonlocal continue_edit
            # If one result:
            if len(search_results) == 1:
                select_field = int(input('Select field to edit: 0 = ' +
                                         'question, 1 = answer:\n'))
                tc.del_lines(1)
                # Correct question
                if select_field == 0:
                    correct_question = input('Enter correct question:\n')
                    cls._df.at[search_results.index.tolist()[0],
                               cls._native_language] = correct_question
                # Correct answer
                elif select_field == 1:
                    correct_answer = input('Enter correct answer:\n')
                    cls._df.at[search_results.index.tolist()[0],
                               cls._foreign_language] = correct_answer
            # If multiple results
            else:
                select_item = input('Select item to edit:\n')
                tc.del_lines(1)
                if select_item != 'q':
                    select_item = int(select_item)
                    print(search_results.loc[select_item][0] + '\t' +
                          search_results.loc[select_item][1])
                    select_field = int(input('Select field to edit: 0 = ' +
                                             'question, 1 = answer:\n'))
                    tc.del_lines(1)
                    # Correct question
                    if select_field == 0:
                        correct_question = input('Enter correct question:\n')
                        cls._df.at[select_item, cls._native_language] =\
                            correct_question
                    # Correct answer
                    elif select_field == 1:
                        correct_answer = input('Enter correct answer:\n')
                        cls._df.at[select_item, cls._foreign_language] =\
                            correct_answer
                else:
                    continue_edit = False

        # Find a vocab item and edit it
        def search_vocab(multi_edit_str):
            # Change enclosed variable to exit edit function
            nonlocal continue_edit
            if multi_edit_str == '':
                search_str = input('Search ' + cls._foreign_language +
                                   ' vocab database:\n')
            else:
                search_str = multi_edit_str
            # Check for exit command
            if search_str != 'q':
                # Search vocab database
                search_results = edit_string_matching(search_str,
                                                      cls._foreign_language)
            else:
                continue_edit = False
                search_results = ''
            return search_results, search_str

        # Confirm selection choice
        print('You have selected EDIT. Enter q to exit.\n')

        continue_edit = True  # Variable that exits the input function
        saved_items = False  # Delete additional saved statement after exit
        multi_edit_str = ''

        while continue_edit is True:
            lines_to_delete = 6  # For deleting previous search results
            if saved_items is True:
                lines_to_delete += 1  # Delete previous 'Saved' statement
            search_results, search_str = search_vocab(multi_edit_str)
            # Set up multi-item edit off same search
            if len(search_results) > 1:
                multi_edit_str = search_str
                lines_to_delete -= 2
            else:
                multi_edit_str = ''
            if continue_edit is not False:
                if len(search_results) == 0:
                    tc.del_lines(lines_to_delete - 4)
                    saved_items = False
                    cont = input('No entries found! <Enter> = continue' +
                                 '\n')
                    tc.del_lines(2)
                    if cont == 'q':
                        continue_edit = False
                        tc.del_lines(4)
                else:
                    print(search_results)
                    edit_search_results(search_results)
                    if continue_edit is not False:
                        if save is True:
                            cls._df.to_hdf(cls._vocab_file, key='df', mode='w')
                            cls.__load_vocab()
                        # Delete previous search results before next search
                        if len(search_results) > 1:
                            lines_to_delete += 2
                        tc.del_lines(lines_to_delete + len(search_results))
                        saved_items = True
                        print('Saved')
                        # Option to delete items
                    else:
                        tc.del_lines(lines_to_delete + len(search_results) + 4)
            else:
                tc.del_lines(lines_to_delete)
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
