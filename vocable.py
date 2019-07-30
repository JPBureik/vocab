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
        self.phase = 0
        self.date = date.today()
        self.language = language
        self.native = native
        self.foreign = foreign
    
    def edit(self):
        pass
    
    def practice(self):
        pass