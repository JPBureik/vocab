#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 06:04:51 2019

@author: jp
"""

import pandas as pd
import terminal_commands as tc
from tabulate import tabulate


# %% Ignore performance warning

import warnings
warnings.filterwarnings('ignore', category=pd.io.pytables.PerformanceWarning)

# %% Select language

language_choice = ['English', 'French']


def language_select(language_choice):

    lang = int(input('Select language: 0 = ' +
                     language_choice[0] + ', 1 = ' + language_choice[1] + ':\n'))
    tc.del_lines(1)
    print('You have selected ' + language_choice[lang] +
          '. Enter <quit> to end. Enter <mod> to edit.')

    return lang


def search():

    # Load vocab file

    def load_vocab_file(lang):

        df = pd.read_hdf(vocab_file[lang], 'df')

        return df

    # Print overview

    # Display stats
    def print_table(language_choice, lang, df):
        table_list = []
        header_column = language_choice[lang]
        header_line = ['', 'Total', 'Phase 0', 'Phase 1', 'Phase 2',
                       'Phase 3', 'Phase 4', 'Phase 5', 'LTM', 'Last practiced']
        table_list.append(header_column)
        table_list.append(len(df))
        for l in range(1, 8, 1):
            table_list.append(len(df.loc[df['Phase'] == l-1, language_choice[lang]]))
        table_list.append(max(df['Date']))
        # Print table
        print(tabulate([table_list], headers=header_line,
                       tablefmt='fancy_grid', numalign='center', stralign='center'))
        # Print one line before search line
        print('\n')

    # Search

    def search_vocab(mod_pass, mod_pass_search_term, df, language_choice, lang):
        search_results = pd.DataFrame()
        # Mod_pass: enable easy editing of multiple terms from same search -> reprint same search results
        if mod_pass == False:
            search_term = input('Enter search term: ')
        else:
            print('Enter search term: ' + mod_pass_search_term)
            search_term = mod_pass_search_term
        mod_pass = False
        if search_term != 'quit':
            # Search German entries
            german_results = df[df['German'].str.contains(search_term)]
            search_results = search_results.append(german_results)
            # Search foreign entries while discounting duplicate results
            foreign_results = df[df[language_choice[lang]].str.contains(search_term)]
            for k in range(len(foreign_results)):
                if foreign_results.index.tolist()[k] not in german_results.index.tolist():
                    search_results = search_results.append(foreign_results.iloc[k])
        return search_results, search_term, mod_pass

    def display_search_results(search_results):
        if search_results.empty == True:
            lines_to_del = 7
            org_index_list = []
            print('No entries found!')
        else:
            lines_to_del = len(search_results) + 5
            # Display entire DataFrame of search results
            pd.set_option('display.expand_frame_repr', False)
            pd.set_option('display.max_colwidth', 75)
            # Change indeces for display while saving old indices for mod ref
            org_index_list = search_results.index.tolist()
            if len(search_results) > 1:
                lines_to_del += 2
                print_index_list = list(range(0, len(search_results), 1))
                search_results.index = print_index_list
            # Print search results
            print(search_results)
        return lines_to_del, org_index_list

    def ask_continue(search_term, search_results, lines_to_del):
        cont = input('\nNext: <Enter>\nEdit: <mod>\nQuit: <quit>\n')
        if cont == '':
            if len(search_results) == 1:
                lines_to_del += 2
            search_results = pd.DataFrame()
            tc.del_lines(lines_to_del)
            mod = False
        elif cont == 'mod':
            mod = True
        else:
            search_term = 'quit'
            mod = False
        return mod, search_term, search_results

    def edit_vocab(search_results, df, org_index_list, language_choice, lang, lines_to_del):
        # If one result:
        if len(search_results) == 1:
            tc.del_lines(4)
            select_field = int(input('Select field to edit: 0 = question, 1 = answer:\n'))
            tc.del_lines(1)
            # Correct question
            if select_field == 0:
                correct_question = input('Enter correct question:\n')
                df.loc[org_index_list[0], 'German'] = correct_question
            # Correct answer
            elif select_field == 1:
                correct_answer = input('Enter correct answer:\n')
                df.loc[org_index_list[0], language_choice[lang]] = correct_answer
            tc.del_lines(lines_to_del + 1)
            mod_pass = False
            mod_pass_search_term = ''
        # If multiple results
        else:
            tc.del_lines(4)
            select_item = int(input('Select item to edit:\n'))
            tc.del_lines(1)
            print(search_results.iloc[select_item][0] + '\t' + search_results.iloc[select_item][1])
            select_field = int(input('Select field to edit: 0 = question, 1 = answer:\n'))
            tc.del_lines(1)
            # Correct question
            if select_field == 0:
                correct_question = input('Enter correct question:\n')
                df.loc[org_index_list[select_item], 'German'] = correct_question
            # Correct answer
            elif select_field == 1:
                correct_answer = input('Enter correct answer:\n')
                df.loc[org_index_list[select_item], language_choice[lang]] = correct_answer
            tc.del_lines(lines_to_del + 1)
            mod_pass = True
            mod_pass_search_term = search_term
        return df, mod_pass, mod_pass_search_term

    vocab_file = ['vocab_en.h5', 'vocab_fr.h5']
    search_term = ''
    mod_pass = False
    mod_pass_search_term = ''

    # Main loop
    while search_term != 'quit':

        # Load vocab file (inside loop so that changes are immediate)
        df = load_vocab_file(lang)
        # Print overview (inside loop so that changes are immediate)
        print_table(language_choice, lang, df)

        search_results, search_term, mod_pass = search_vocab(
            mod_pass, mod_pass_search_term, df, language_choice, lang)

        # Display search results unless abort
        if search_term != 'quit':
            lines_to_del, org_index_list = display_search_results(search_results)

            # Ask to continue
            mod, search_term, search_results = ask_continue(
                search_term, search_results, lines_to_del)

            # Edit vocab
            if mod == True:
                df, mod_pass, mod_pass_search_term = edit_vocab(
                    search_results, df, org_index_list, language_choice, lang, lines_to_del)
                # Save vocab_file
                df.to_hdf(vocab_file[lang], key='df', mode='w')

        # Delete table before reprinting
        if search_term != 'quit':
            tc.del_lines(7)

# %% Execute


if __name__ == '__main__':

    lang = language_select(language_choice)
    search()
