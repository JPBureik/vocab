#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:49:36 2024

@author: jp
"""

import time
from termcolor import colored


from vocab.vis.terminal_interface import TerminalInterface


class UserInterface():
    
    WAIT_UPDATE = 1  # s
    
    def __init__(self):
        # Initialize terminal interface:
        self.ti = TerminalInterface()
        
    def update_ui(self, table_df, foreign_lang, correct_counter=None,
                  total=None, context='correct answer', idx=None,
                  answer=None):
        
        if context=='correct answer':
            # Close previous UI:
            self.ti.close_phase_plot()
            self.ti.del_lines(12)
            
            # Update UI:
            self.ti.print_table(foreign_lang, table_df)
            self.ti.progress_bar(correct_counter, total)
            
            # Display phase information of vocable:
            self.ti.print_phase(table_df['Phase'].loc[idx])
            
            # Show updated UI for 1 s before moving on to next item:
            time.sleep(self.WAIT_UPDATE)
            self.ti.close_phase_plot()
            self.ti.del_lines(10)
            self.ti.print_table(foreign_lang, table_df)
            self.ti.progress_bar(correct_counter, total)
            
        elif context=='initial incorrect answer':
            # Close previous UI:
            self.ti.close_phase_plot()
            self.ti.del_lines(12)
            
            # Update UI:
            self.ti.print_table(foreign_lang, table_df)
            self.ti.progress_bar(correct_counter, total)
            
            # Display phase information of vocable:
            self.ti.print_phase(table_df['Phase'].loc[idx])
            
            # Display error:
            print(table_df['German'].loc[idx])
            print(colored(answer, 'red'))
            print('-> ' + table_df[foreign_lang].loc[idx] + '\n')
            
        elif context=='subsequent incorrect answer':
            # Close previous UI:
            self.ti.close_phase_plot()
            self.ti.del_lines(15)
            
            # Update UI:
            self.ti.print_table(foreign_lang, table_df)
            self.ti.progress_bar(correct_counter, total)
            
            # Display phase information of vocable:
            self.ti.print_phase(table_df['Phase'].loc[idx])
            
            # Display error:
            print(table_df['German'].loc[idx])
            print(colored(answer, 'red'))
            print('-> ' + table_df[foreign_lang].loc[idx] + '\n')
            
        elif context=='corrected answer':
            # Close previous UI:
            self.ti.close_phase_plot()
            self.ti.del_lines(15)
            
            # Update UI:
            self.ti.print_table(foreign_lang, table_df)
            self.ti.progress_bar(correct_counter, total)
            
        elif context=='added new vocable':
            # Close previous UI:
            self.ti.del_lines(13)
            
            # Update UI:
            self.ti.print_table(foreign_lang, table_df)
            self.ti.progress_bar(correct_counter, total)
