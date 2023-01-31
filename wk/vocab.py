from collections import namedtuple
# >>> Person = namedtuple('Person', 'first_name last_name zip_code')
# >>> p1 = Person('Joe', 'Schmoe', '93002')

from wk.kanji import Reading, Radical

class Vocab:
    
    def __init__(self, symbol, meanings, readings, kanjis, word_types, level=None, patterns=[]):
        self.symbol = symbol
        self.meanings = meanings
        self.readings = readings
        self.kanjis = kanjis
        self.word_types = word_types
        self.level = level
        self.patterns = patterns

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol

    def onyomi(self):
        for r in self.readings:
            if r.label == 'on’yomi':
                return r.sounds
        return []
    
    def is_verb(self):
        return self.is_ichidan_verb() or self.is_godan_verb()
    
    def is_ichidan_verb(self):
        return "ichidan verb" in self.word_types
    
    def is_godan_verb(self):
        return "godan verb" in self.word_types
    
    def verb_type(self):
        if self.is_godan_verb():
            return "godan verb"
        elif self.is_ichidan_verb():
            return "ichidan verb"
        else:
            raise Exception(f"Verb type not found for {self.symbol}")
