from collections import namedtuple
# >>> Person = namedtuple('Person', 'first_name last_name zip_code')
# >>> p1 = Person('Joe', 'Schmoe', '93002')

class Kanji:
    
    def __init__(self, symbol, meaning, readings, radicals, level=None, similar=[]):
        self.symbol = symbol
        self.meaning = meaning
        self.readings = readings
        self.radicals = radicals
        self.level = level
        self.similar = similar

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.symbol

    def onyomi(self):
        for r in self.readings:
            if r.label == 'on’yomi':
                return r.sounds
        return []

    
class Reading:
    
    # labels should be {On'yomi, Kun'yomi, Nanori}
    # sounds is an array of pronunciations
    def __init__(self, label, sounds):
        self.label = label
        self.sounds = sounds
    
    def __str__(self):
        return ', '.join(self.sounds)
    
    def __repr__(self):
        return self.__str__()

    
class Radical:
    
    def __init__(self, name, symbol): #(name, symbol)
        self.name = name
        self.symbol = symbol
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()


    
#class Kanji(symbol, meaning, radicals)
