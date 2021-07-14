#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 23:59:24 2020

@author: JP

Vocable class.

"""

# Standard library imports
from datetime import date


class Vocable:
    """
    A vocable card and methods for input, editing and practice.

    Init args:
        native_item(str): vocable item in native language
        foreign_item(str): vocable item in foreign language
    """

    """
    TOP-LEVEL PRIVATE ATTRIBUTES
    """

    _phase_intervals = [0, 1, 3, 9, 29, 90, 300]  # days before next practice]
    _phases = dict(zip(range(len(_phase_intervals)), _phase_intervals))
    _native_lang = 'German'
    _foreign_lang_choice = ['English', 'French']
    _practice_items = 100  # per practice session and foreign language

    """
    INIT
    """

    def __init__(self, foreign_lang, foreign, native):
        self._foreign_lang = foreign_lang
        self._foreign = foreign
        self._native = None
        self._last_pract_date = date.today()
        self._phase = 0
        self._practiced_ctr = 0
        self._false_ctr = 0

    """
    PRIVATE METHODS
    """

    def _pull_from_leo_org(self):
        ...

    def _pull_from_dict_cc(self):
        ...

    def _enter_manually(self):
        ...

    def _load_vocab(self):
        ...

    """
    PUBLIC METHODS
    """

    @classmethod
    def input(cls):
        ...

    @classmethod
    def edit(cls):
        ...

    @classmethod
    def practice(cls):
        ...


# Execution:
if __name__ == '__main__':
    vocable_card = Vocable('English', 'lake', 'See')
