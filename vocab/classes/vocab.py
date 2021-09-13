#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 21:52:28 2021

@author: jp

Vocab class.

A class for training vocab.
"""

# Standard library imports:
import os
import pandas as pd

# Local imports:
from vocab.config import native_lang, foreign_languages

class VocabCollection():

    """ ---------- INIT ---------- """

    def __init__(self, foreign_language):
        self.native_lang = native_lang
        self.foreign_language = foreign_language
        # Create directory for data:
        self._data_dir = os.getcwd() + '/data'
        self._mkdir()
        # File I/O:
        self._filepath = self._data_dir + '/' + self.foreign_language + '.h5'

    """ ---------- PROPERTIES ---------- """

    """ ---------- PRIVATE METHODS ---------- """

    def _mkdir(self):
        """Create directory in ./data if not already present."""
        # Check if directory for this collection exists:
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)

    def _load(self):
        """Load vocab file from ./data."""
        self._df = pd.read_hdf(self._filepath, 'df')

    def _dump(self):
        """Save vocab file to ./data."""
        pass


    """ ---------- PUBLIC METHODS ---------- """    