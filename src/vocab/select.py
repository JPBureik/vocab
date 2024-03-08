#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:32:15 2024

@author: jp
"""
# Standard library imports:
import pandas as pd
from os import path
from sqlalchemy import create_engine

# Package imports:
from config import mysql_user, mysql_password


engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@localhost/vocab")



N = 100

foreign_lang = 'French'

import_query = f"""SELECT * FROM {foreign_lang};"""

table_df = pd.read_sql(import_query, con=engine)



datadirpath = '/Users/jp/prog/personal/vocab'

datapath = path.join(datadirpath, f'vocab_{foreign_lang[:2].lower()}.h5')

# Load from .hdf-5:
df = pd.read_hdf(datapath, 'df')
