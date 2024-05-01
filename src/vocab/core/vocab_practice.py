#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 23:15:57 2024

@author: jp
"""

# Package imports:
from vocab.core.load_from_db import load_from_db
from vocab.core.language_select import language_select
from vocab.core.select_for_practice import select_for_practice
from vocab.vis.display_stats import print_table, progress_bar

# Select foreign language:
foreign_lang = language_select()

# Load table from database:
table_df = load_from_db(foreign_lang)

# Display stats:
print_table(foreign_lang, table_df)

# Display progress:
correct_counter = 0 # Show progress as correct_counter/vocab_total
progress_bar(correct_counter)

# Select for practice:
pract_df = select_for_practice(table_df)

# Practice:


