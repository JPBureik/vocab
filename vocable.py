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
        self.phase = 0
        self.date = date.today()
        self.native = native
        self.foreign = foreign
    
    def edit(self):
        ''' Edit any public attribute of vocable class instance.'''
        select = input('Specify attribute to change:\n')
        try:
            print('Current: ' + str(getattr(self, select)))
            change = input('Edit: ')
            setattr(self, select, change)
            print('Changed ' + select + ' to ' + change + '.')
        except:
            print('Attribute not found')
    
    def practice(self):
        pass