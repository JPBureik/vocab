#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:29:23 2024

@author: jp
"""

# Standard library imports;
import pandas as pd
from os import path
from tqdm import tqdm

# Package imports:
from config import mysql_user, mysql_password
from to_db import to_db
from vocable import Vocable

# Datapaths to init dfs::
datadirpath = '/Users/jp/prog/personal/vocab'
languages = ['English', 'French']

for foreign_lang in languages:
    
    datapath = path.join(datadirpath, f'vocab_{foreign_lang[:2].lower()}.h5')

    # Load from .hdf-5:
    df = pd.read_hdf(datapath, 'df')
    
    for idx in tqdm(df.index, desc=foreign_lang):
        
        native = df.iloc[idx]['German'].replace("'", "\\'")
        foreign = df.iloc[idx][foreign_lang].replace("'", "\\'")
        phase = df.iloc[idx]['Phase']
        date = df.iloc[idx]['Date']
        
        voc = Vocable(foreign_lang, native, foreign, phase=phase)
    
        to_db(voc, phase=voc.phase, date=date)
