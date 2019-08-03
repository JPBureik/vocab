# Vocable class

from datetime import date

class Vocable:
    """
    A vocable card.
    
    Args:
        language(str): foreign language (e.g. 'english', 'french', etc)
        native(str): vocable item in native language
        foreign(str): vocable item in foreign language
    """
    def __init__(self, language, native, foreign):
        self._language = language
        self._phase = 0
        self._date = date.today()
        self._native = native
        self._foreign = foreign
        
    @property
    def language(self):
        return self._language
        
    @property
    def phase(self):
        return self._phase
        
    @property
    def date(self):
        return self._date
    
    @property
    def native(self):
        return self._native
    
    @native.setter
    def native(self, input_string):
        self._native = input_string
        
    @property
    def foreign(self):
        return self._foreign
    
    @foreign.setter
    def foreign(self, input_str):
        self._foreign = input_str
    