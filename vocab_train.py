 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 20:26:13 2019

@author: jp
"""

import pandas as pd
import terminal_commands as tc
import time
import datetime
from termcolor import colored
from tabulate import tabulate

#%% Ignore performance warning

import warnings
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

#%% Select language

language_choice = ['English', 'French']

def language_select(language_choice):

    lang = int(input('Select language: 0 = ' + language_choice[0] + ', 1 = ' + language_choice[1] + ':\n'))
    tc.del_lines(1)
    print('You have selected ' + language_choice[lang] + '. Enter <quit> to end. Enter <mod> to edit.')

    return lang

#%% Load vocab file

vocab_file = ['vocab_en.h5', 'vocab_fr.h5']

def load_vocab_file(lang):

    df = pd.read_hdf(vocab_file[lang], 'df')

    return df

#%% Determine vocab for training

def vocab_today(df):
    df_today = pd.DataFrame()
    vocab_max = 100 # Max number of items to train
    phase_interval = [0, 1, 3, 9, 29, 90, 300] # days before next ptractice
    # Determine elegible vocab based on time since last practice
    for k in range(len(df)):
        delta = datetime.date.today() - df.iloc[k]['Date'] # Days since last practice
        delta = delta.days
        if df.iloc[k]['Phase'] < len(phase_interval)-1: # If Phase > 6: Vocab in long-term memory (no practice)
            if delta > phase_interval[df.iloc[k]['Phase']]:
                df_today = df_today.append(df[k:k+1], ignore_index=True)
    # Randomly select 100 items from eligible vocab to train
    if len(df_today) > vocab_max:
        df_today = df_today.sample(vocab_max)
    # Total number of items to train
    vocab_total = len(df_today)
    return df_today, vocab_total

#%% Practice

def vocab_practice(vocab_total, lang, df, df_today):

    # Progress bar
    def progress_bar(count, total):
        prog = '█' * count
        prog += ' ' + str(count) + '/' + str(total)
        print(' ' + prog)

    # Display stats
    def print_table(language_choice, lang, df):
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

    mod_del = False

    df_today_corrections = pd.DataFrame() # Repeat incorrect items at the end
    incorrect_counter = 0 # To delete correct number of lines in case of incorrect answer
    correct_counter = 0 # Show progress as correct_counter/vocab_total
    ratio = 0 # Calculate ratio at the end, increase with every correct answer
    foreign = ''

    def correct_answer(foreign, correct_counter, vocab_total, ratio):
        tc.del_lines(7)
        correct_counter += 1
        progress_bar(correct_counter,vocab_total)
        print('')
        print(df_today.iloc[k]['German'])
        print(colored(foreign, 'green'))
        ratio += 1
        # Set phase += 1 in original DataFrame df (not df_today)
        df.loc[df['German'] == df_today.iloc[k]['German'], 'Phase'] += 1
        # Set date
        df_today.at[k, 'Date'] = datetime.date.today()
        # Delete lines of previous question
        time.sleep(1)
        tc.del_lines(13)
        return correct_counter, ratio

    def incorrect_answer(foreign, incorrect_counter, ratio, df_today_corrections, decrease_phase):

        mod_del = False

        while foreign != df_today.iloc[k][language_choice[lang]]:
            # Delete lines from previous mod
            if mod_del == True:
                tc.del_lines(4)
                mod_del = False
            # Delete previous answer
            if incorrect_counter > 0:
                tc.del_lines(6)
            #
            print(df_today.iloc[k]['German'])
            print(colored(foreign, 'red'))
            # Set phase -= 1 in original DataFrame df and in df_today)
            if decrease_phase == True:
                if df.loc[df['German'] == df_today.iloc[k]['German'], 'Phase'].iloc[0] > 0:
                    df.loc[df['German'] == df_today.iloc[k]['German'], 'Phase'] -= 1
                    df_today.loc[df_today['German'] == df_today.iloc[k]['German'], 'Phase'] -= 1
                incorrect_counter += 1
                ratio -= 1
                decrease_phase = False
            print('-> ' + df_today.iloc[k][language_choice[lang]] + '\n')
            foreign = input()
            # modify answer in df and df_today
            if foreign == 'mod':
                tc.del_lines(1)
                select_field = int(input('Select field to edit: 0 = question, 1 = answer:\n'))
                tc.del_lines(1)
                # Correct question
                if select_field == 0:
                    corrected = input('Enter correct question:\n')
                    df_today.loc[df_today[language_choice[lang]] == df_today.iloc[k][language_choice[lang]], 'German'] = corrected
                    df.loc[df[language_choice[lang]] == df.iloc[df_today.index.tolist()[k]][language_choice[lang]], 'German'] = corrected
                    foreign = df_today.iloc[k][language_choice[lang]]
                    tc.del_lines(15)
                    incorrect_counter = 0
                # Correct answer
                elif select_field == 1:
                    corrected = input('Enter correct answer:\n')
                    df_today.loc[df_today['German'] == df_today.iloc[k]['German'], language_choice[lang]] = corrected
                    df.loc[df['German'] == df.iloc[df_today.index.tolist()[k]]['German'], language_choice[lang]] = corrected
                    print('Corrected answer:\n' + str(df_today.loc[df_today['German'] == df_today.iloc[k]['German'], 'German':language_choice[lang]].iloc[0]))
                tc.del_lines(2)
                df.to_hdf(vocab_file[lang], key='df', mode='w')
                mod_del = True
                decrease_phase = False
            # Correct answer
            elif foreign == df_today.iloc[k][language_choice[lang]]:
                tc.del_lines(1)
                print(colored(foreign, 'green'))
        if mod_del == False:
            time.sleep(1)
            tc.del_lines(15)
        incorrect_counter = 0
        df_today_corrections = df_today_corrections.append(df_today.iloc[k])
        return incorrect_counter, ratio, df_today_corrections

    # Main loop
    while foreign != 'quit':

        while correct_counter <= vocab_total:

            # Break condition
            if foreign == 'quit':
                break

            for k in range(len(df_today)):

                # Delete lines from previous mod
                if mod_del == True:
                    tc.del_lines(13)
                    mod_del = False

                print_table(language_choice, lang, df)
                progress_bar(correct_counter,vocab_total)
                print('')

                # Verify input

                # Question
                foreign = input(df_today.iloc[k]['German'] + ': \n')
                tc.del_lines(1)

                # Break condition
                if foreign == 'quit':
                    abort_answer = input('Abort practice? [y/n]\n')
                    if abort_answer == 'y':
                        break
                    else:
                        tc.del_lines(2)
                        incorrect_counter, ratio, df_today_corrections = incorrect_answer(foreign, incorrect_counter, ratio, df_today_corrections, decrease_phase=False)
                        continue

                # mod condition: modify answer in df and df_today
                if foreign == 'mod':
                    corrected = input('Enter correct question:\n')
                    df_today.loc[df_today[language_choice[lang]] == df_today.iloc[k][language_choice[lang]], 'German'] = corrected
                    df.loc[df[language_choice[lang]] == df.iloc[df_today.index.tolist()[k]][language_choice[lang]], 'German'] = corrected
                    df.to_hdf(vocab_file[lang], key='df', mode='w')
                    mod_del = True
                    # Append to corrections to retrain at the end of practice
                    df_today_corrections = df_today_corrections.append(df_today.iloc[k])

                # Correct answer
                elif foreign == df_today.iloc[k][language_choice[lang]]:
                    correct_counter, ratio = correct_answer(foreign, correct_counter, vocab_total, ratio)

                # Incorrect answer
                else:
                    incorrect_counter, ratio, df_today_corrections = incorrect_answer(foreign, incorrect_counter, ratio, df_today_corrections, decrease_phase=True)

                # Save vocab file
                df.to_hdf(vocab_file[lang], key='df', mode='w')

            # end practice
            if correct_counter < vocab_total:
                df_today = df_today_corrections
                df_today_corrections = pd.DataFrame()
            else:
                print_table(language_choice, lang, df)
                progress_bar(correct_counter,vocab_total)
                break
        break

#%% Execute

if __name__ == '__main__':

    lang = language_select(language_choice)
    df = load_vocab_file(lang)
    df_today, vocab_total = vocab_today(df)
    vocab_practice(vocab_total, lang, df, df_today)
