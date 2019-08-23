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
    num_of_cards = 0
    
    def __init__(self, language, native, foreign):
        self._language = language
        self._phase = 0
        self._date = date.today()
        self._native = native
        self._foreign = foreign
        
        self._remove_from_practice_set = False
        
        Vocable.num_of_cards += 1
        
    # Alternative constructor for webscraping
    @classmethod
    def from_html(cls, webpage):
        pass
    
    # Set your native language:
    @classmethod
    def set():
        pass
     
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
        
    @foreign.deleter
    def foreign(self):
        print('Deleted foreign.')
        self._foreign = None
        
    @staticmethod
    def set_language():
        return 0
    
    @staticmethod
    def train(set_of_cards):
        for card in set_of_cards:
            question = input(card._native + '\n')
            if question == card._foreign:
                print('Correct')
                card._phase += 1
                card._remove_from_practice_set = True
            else:
                print('False')
                card._phase -= 1
        return set_of_cards
        
    def __repr__(self):
        return "Vocable('{}', '{}', '{}')".format(self.language, self.native, self.foreign)
    
    def __str__(self):
        return '{} for {}: {}'.format(self.language.capitalize(), self.native, self.foreign)