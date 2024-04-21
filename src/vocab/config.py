#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 22:48:15 2024

@author: jp
"""

# Standard library imports:
from os import path

# Vocab database parameters:
native_lang = 'German'

# MySQL credentials:
mysql_user = 'python'
mysql_password = 'H!C4DMKNi&'

# Local directory path where vocab data is stored:
local_vocab_data_savedir = path.join(path.expanduser( '~' ), 'Data/Vocab')

# Training parameters:
session_volume = 100  # max. number of items per training session
phase_intervals = [0, 1, 3, 9, 29, 90, 300] # days before next practice
