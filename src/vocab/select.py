#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:32:15 2024

@author: jp
"""
# Standard library imports:
import pandas as pd
from os import path
import datetime
from sqlalchemy import create_engine

# Package imports:
from config import mysql_user, mysql_password, session_volume, phase_intervals


engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@localhost/vocab")



N = 100

foreign_lang = 'French'

import_query = f"""SELECT * FROM {foreign_lang};"""

table_df = pd.read_sql(import_query, con=engine)

# Use ID column as index:
table_df.set_index('ID', inplace=True)

# Select for practice:

# Determine days since last practice
days_since_last_practice = (datetime.date.today() - table_df['Date']).apply(lambda x: x.days)
