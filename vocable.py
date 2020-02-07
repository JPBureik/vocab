# Vocable class

from datetime import date
import pandas as pd

class Vocable:
    """
    A vocable card and methods for input, editing and practice.
    
    Args:
        native_item(str): vocable item in native language
        foreign_item(str): vocable item in foreign language
    """
    num_of_cards = 0
    _set_of_cards = set()
    _native_language = 'German'
    _language_choice = ['English', 'French']
    _df = pd.DataFrame
    _num_for_practice = 100
    
<<<<<<< HEAD
    def __init__(self, language, native, foreign):
        self._language = language
        self._phase = 0
        self._date = date.today()
        self._native = native
        self._foreign = foreign

        
        self._remove_from_practice_set = False
        
=======
    def __init__(self, native_item, foreign_item, new_card = True):
        self._native_item = native_item
        self._foreign_item = foreign_item
        if new_card:
            self._phase = 0
            self._date = date.today()
                
>>>>>>> 18e1ed3078fa5945561e4bb770466bcdda976615
        Vocable.num_of_cards += 1
        
    # Alternative constructor for webscraping
    @classmethod
    def from_html(cls, webpage):
        pass
    
    # Load vocab from df and create set of vocable cards
    @classmethod
    def load_vocab(cls):
        # Load dataframe
        cls._vocab_file = 'vocab_' + cls._foreign_language[:2].lower() + '.h5'
        cls._df = pd.read_hdf(cls._vocab_file, 'df')
        # Compile set of vocable cards
        for item in cls._df.iterrows():
            card = Vocable(item[1][cls._native_language],
                           item[1][cls._foreign_language], new_card = False)
            card._phase = item[1]['Phase']
            card._date = item[1]['Date']
            cls._set_of_cards.add(card)
    
    # Language choice before input/practice
    @classmethod
    def select_foreign_language(cls):
        selection = int(input('Select language: 0 = ' +\
                                          cls._language_choice[0] + ', 1 = ' +\
                                          cls._language_choice[1] + ':\n'))
        cls._foreign_language = cls._language_choice[selection]
        # Load corresponding vocab
        cls.load_vocab()
        # Print confirmation
        print('You have selected ' + cls._foreign_language + '.')
        
    @property
    def phase(self):
        return self._phase
        
    @property
    def date(self):
        return self._date
    
    @property
    def native_item(self):
        return self._native_item
    
    @native_item.setter
    def native_item(self, input_string):
        self._native_item = input_string
        
    @property
    def foreign_item(self):
        return self._foreign_item
    
    @foreign_item.setter
    def foreign_item(self, input_str):
        self._foreign_item = input_str

    # Practice
    @classmethod
    def practice(cls):
        for card in cls._set_of_cards:
            question = card._native_item
            answer = input(question + '\n')
            if answer == card._foreign_item:
                print('Correct!\n')
            else:
                print('Incorrect!\n')