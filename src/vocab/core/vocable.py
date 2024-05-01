#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 00:37:36 2024

@author: jp
"""

# Package imports:
from vocab.core.config import native_lang

class Vocable:
    
    def __init__(self, foreign_lang, native_vocable, foreign_vocable, phase=0):
        self.native_lang = native_lang
        self.foreign_lang = foreign_lang
        self.native_vocable = native_vocable
        self.foreign_vocable = foreign_vocable
        self.phase = phase