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
import datetime

# Local imports:
from vocab.config import native_language, daily_pract_amt


class VocabCollection():

    """ ---------- INIT ---------- """

    def __init__(self, foreign_language):
        self.native_lang = native_language.lower()
        self.foreign_language = foreign_language.lower()
        self._daily_pract_amt = daily_pract_amt
        # Phases = Days before next practice:
        self._phase_intvls = dict(enumerate([0, 1, 3, 9, 29, 90, 300]))
        # File I/O:
        self._data_dir = os.getcwd() + '/data'
        self._filepath = self._data_dir + '/' + self.foreign_language + '.h5'

    """ ---------- PROPERTIES ---------- """

    # Use setters for config input.

    """ ---------- PRIVATE METHODS ---------- """

    def _mkdir(self):
        """Create directory in ./data if not already present."""
        # Check if directory for this collection exists:
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)

    def _load(self):
        """Load vocab file from ./data."""
        try:
            self._df = pd.read_hdf(self._filepath, 'df')
        except FileNotFoundError:
            self._mkdir()

    def _save(self):
        """Save vocab file to ./data."""
        self._df.to_hdf(self._filepath, key='df', mode='w')

    def _sel_for_practice(self):
        """Select daily_pract_amt from vocab collection."""
        self._df_pract = self._df.copy()
        # Determine items eligible for practice based on their phase:
        for i in range(len(self._df)):
            # Discard all | today - last practiced date < phase intvl:
            if ((datetime.date.today() - self._df.Date.iloc[i]).days <
                    self._phase_intvls[self._df.Phase.iloc[i]]):
                self._df_pract.drop(i, inplace=True)
        # Randomly select defined amount for daily practice:
        if len(self._df_pract) > self._daily_pract_amt:
            self._df_pract = self._df_pract.sample(self._daily_pract_amt)

    """ ---------- PUBLIC METHODS ---------- """
