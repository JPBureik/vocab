# Vocable class

from datetime import date
import pandas as pd
from tabulate import tabulate

class Vocable:
    """
    A vocable card and methods for input, editing and practice.
    
    Args:
        native_item(str): vocable item in native language
        foreign_item(str): vocable item in foreign language
    """
    
    # Modifiable class variables
    _native_language = 'German'
    _language_choice = ['English', 'French']    # These are the foreign
                                                # languages in which you have
                                                # vocab items
    _num_for_practice = 100 # Max number of cards for daily practice
    
    # Initialize class variables needed for methods
    _set_of_cards = set()   # This is your entire library of vocab items in a
                            # given foreign language
    
    def __init__(self, native, foreign):
        # Vocab attributes
        self._phase = 0
        self._date = date.today()
        self._native = native
        self._foreign = foreign

 
    """
    METHODS
    """
    
    
    # Initialization: Choose foreign language, display overview, then enter
    # main menu
    @classmethod
    def initialize(cls):
        # Select foreign language and store choice in class variable
        selection = int(input('Select language: 0 = ' +\
                                          cls._language_choice[0] + ', 1 = ' +\
                                          cls._language_choice[1] + ':\n'))
        cls._foreign_language = cls._language_choice[selection]
        # Load corresponding vocab library
        cls.load_vocab()
        # Print confirmation
        print('You have selected ' + cls._foreign_language + '.')
        # Display overview
        cls.overview()
        # Present main meu options
        cls.main_menu()
        
    # Load vocab from file (pandas DataFrame) and create set of vocable cards
    @classmethod
    def load_vocab(cls):
        # Load dataframe
        cls._vocab_file = 'vocab_' + cls._foreign_language[:2].lower() + '.h5'
        cls._df = pd.read_hdf(cls._vocab_file, 'df')
        # Compile set of vocable cards
        for item in cls._df.iterrows():
            card = Vocable(item[1][cls._native_language],
                           item[1][cls._foreign_language])
            card._phase = item[1]['Phase']
            card._date = item[1]['Date']
            cls._set_of_cards.add(card)
            
    # Display overview of vocab library for a given foreign language
    @classmethod
    def overview(cls):
        table_list = []
        header_column = cls._foreign_language
        header_line = ['','Total', 'Phase 0', 'Phase 1','Phase 2','Phase 3',\
                       'Phase 4','Phase 5', 'LTM', 'Last practiced']
        table_list.append(header_column)
        table_list.append(len(cls._df))
        for l in range(1,8,1):
            table_list.append(len(cls._df.loc[cls._df['Phase'] == l-1,\
                                              cls._foreign_language]))
        table_list.append(max(cls._df['Date']))
        # Print table
        print(tabulate([table_list],headers=header_line,tablefmt='fancy_grid',\
                       numalign='center',stralign = 'center'))
        
    # Main menu: present choice of all major class methods
    @classmethod
    def main_menu(cls):
        print('Main menu')
        selection = int(input('Select action: 0 = Input, 1 = Edit, 2 = '\
                              'Practice\n'))
        if selection == 0:
            pass
        elif selection == 1:
            pass
        else:
            pass

    

        
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
        
    # Input
    @classmethod
    def input(cls):
        pass
    
    # Edit
    @classmethod
    def edit(cls):
        pass

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