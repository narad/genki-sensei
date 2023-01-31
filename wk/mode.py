
class Mode:
    
    def __init__(self, name, pretty_str):
        self.name = name
        self.pretty_str = pretty_str
    
    def __str__(self):
        return self.pretty_str


all_modes = [Mode('kanji_similarity', "Kanji Similarity"),
             Mode('radical_decomposition', "Radical Decomposition"),
             Mode('pronunciation', "Pronunciation"),
             Mode('kanji_from_meaning', "Kanji -> Meaning"),
             Mode('meaning_from_kanji', "Meaning -> Kanji"),
             Mode('pattern_understanding', "Usage Pattern Understanding"),
             Mode('conjugation', "Conjugation")
        ]
