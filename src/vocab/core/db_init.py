#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 11:29:23 2024

@author: jp
"""

# Standard library imports;
import pandas as pd
from os import path
# from tqdm import tqdm

# Package imports:
from vocab.core.config import mysql_user, mysql_password
from vocab.core.to_db import to_db
from vocab.core.vocable import Vocable

# Datapaths to init dfs:
datadirpath = '/Users/jp/prog/personal/vocab'
languages = ['English', 'French', 'Spanish']

for foreign_lang in ('Spanish',):
    
    datapath = path.join(datadirpath, 'vocab_es.h5')

    # Load from .hdf-5:
    df = pd.read_hdf(datapath, 'df')
    
    for idx in df.index:
        
        native = df.iloc[idx]['German'].replace("'", "\\'")
        foreign = df.iloc[idx][foreign_lang].replace("'", "\\'")
        phase = df.iloc[idx]['Phase']
        date = df.iloc[idx]['Date']
        
        voc = Vocable(foreign_lang, native, foreign, phase=phase)
    
        to_db(voc, phase=voc.phase, date=date)
