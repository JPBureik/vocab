#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:15:57 2024

@author: jp
"""
import time
import sys
import pandas as pd
from datetime import date


# Package imports:
from vocab.core.load_from_db import load_from_db, save_to_db
from vocab.core.language_select import language_select
from vocab.core.select_for_practice import select_for_practice
from vocab.vis.user_interface import UserInterface

class VocablApp():

    def __init__(self):
        
        # Initialize UI:
        self.ui = UserInterface()
    
        # Select foreign language:
        self.foreign_lang = language_select(self.ui.ti)
        
        # Load table from database:
        self.table_df = load_from_db(self.foreign_lang)
        
        # Select for practice:
        self.pract_df = select_for_practice(self.table_df)
        
        # Define overall volume for this session:
        self.total = self.pract_df.shape[0]
        
        # Display stats:
        self.ui.ti.print_table(self.foreign_lang, self.table_df)
        
        # Display progress:
        self.correct_counter = 0 # Show progress as correct_counter/vocab_total
        self.ui.ti.progress_bar(self.correct_counter, self.total)
        
        # Prepare repeat DataFrame:
        self.incorrect_df = pd.DataFrame(columns=self.pract_df.columns)
        
    def practice(self):
        for idx in self.pract_df.index:
            self._practice_single(idx)
        # Repeat items with incorrect answers:
        while not self.incorrect_df.empty:
            self.pract_df = self.incorrect_df.copy()
            self.incorrect_df = pd.DataFrame(columns=self.pract_df.columns)
            for idx in self.pract_df.index:
                self._practice_single(idx)
        self.user_exit()
                
    def user_exit(self):
        # Save:
        self._save()
        self.ui.ti.del_lines(1)
        print('Bye!')
        sys.exit(0)
        
    def _save(self):
        save_to_db(self.foreign_lang, self.table_df)
        
    def _mod_item(self, idx, context):
        self.ui.ti.del_lines(1)
        select_field = input(f'Select field to edit: <1> = {self.foreign_lang}, <2> = German.\n')
        if select_field=='1':
            self.ui.ti.del_lines(1)
            self.pract_df[f"{self.foreign_lang}"].at[idx] = self.ui.editable_input(f'{self.pract_df[f"{self.foreign_lang}"].loc[idx]}')
            self.table_df[f"{self.foreign_lang}"].at[idx] = self.pract_df[f"{self.foreign_lang}"].loc[idx]
        elif select_field=='2':
            self.ui.ti.del_lines(1)
            self.pract_df["German"].at[idx] = self.ui.editable_input(f'{self.pract_df["German"].loc[idx]}')
            self.table_df["German"].at[idx] = self.pract_df["German"].loc[idx]
        # Update UI:
        self.ui.update_ui(self.table_df, self.foreign_lang,
                          self.correct_counter, self.total,
                          context=context)
        
    def _correct_answer_condition(self, idx, answer):
        return answer == self.pract_df[self.foreign_lang].loc[idx]
            
    def _update_phase(self, idx, direction='increase'):
        # Set change to phase of vocable item and limit for applying change:
        if direction=='increase':
            phase_change = 1
            limit_test = lambda x: x < 7
        elif direction=='decrease':
            phase_change = -1
            limit_test = lambda x: x > 0
        # Apply phase change if not already in outermost phase:
        if limit_test(self.table_df['Phase'].loc[idx]):
            self.table_df['Phase'].at[idx] += phase_change
        # Set practice date to today:
        self.table_df['Date'].at[idx] = date.today()
            
    def _correct_answer(self, idx):
        
        # Update phase info:
        self._update_phase(idx, direction='increase')
        
        # Update practice progress:
        self.correct_counter += 1
        
        # Update UI:
        self.ui.update_ui(self.table_df, self.foreign_lang,
                          self.correct_counter, self.total,
                          context='correct answer', idx=idx)
        
    def _incorrect_answer(self, idx, answer):

        # Update phase info:
        self._update_phase(idx, direction='decrease')

        # Update UI:
        self.ui.update_ui(self.table_df, self.foreign_lang,
                          self.correct_counter, self.total,
                          context='initial incorrect answer', idx=idx,
                          answer=answer)
        
        # Add to repeat DataFrame:
        self.incorrect_df.loc[idx] = self.table_df.loc[idx]
        
        # Get new answer:
        answer = input()
        
        if answer=='mod':
            self._mod_item(idx, context='practice mod after answer')
        else:
            # Try again as long as necessary:
            while not self._correct_answer_condition(idx, answer):
                
                # Update UI:
                self.ui.update_ui(self.table_df, self.foreign_lang,
                                  self.correct_counter, self.total,
                                  context='subsequent incorrect answer', idx=idx,
                                  answer=answer)
                
                # Get new answer:
                answer = input()
                
            # Update UI:
            self.ui.update_ui(self.table_df, self.foreign_lang,
                              self.correct_counter, self.total,
                              context='corrected answer', idx=idx)

    
    # Check answer:
    def _check_answer(self, idx, answer):
        if answer=='mod':
            self._mod_item(idx, context='practice mod before answer')
        elif answer=='quit':
            self.user_exit()
        else:
            if self._correct_answer_condition(idx, answer):
                self._correct_answer(idx)
            
            else:
                self._incorrect_answer(idx, answer)
            
    def _practice_single(self, idx):
        # Display phase information of vocable:
        self.ui.ti.print_phase(self.pract_df['Phase'].loc[idx])
        # Query:
        answer = input(self.pract_df['German'].loc[idx] + ': \n')
        self._check_answer(idx, answer)
    

if __name__ == '__main__':
    app = VocablApp()
    # Practice:
    app.practice()
    
