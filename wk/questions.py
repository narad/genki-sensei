import random

black="\u001b[30;1m"
red="\u001b[31;1m"
green="\u001b[32;1m"
yellow="\u001b[33;1m"
blue="\u001b[34;1m"
magenta="\u001b[35;1m"
cyan="\u001b[36;1m"
white="\u001b[37;1m"
                     
                     
qstyle_start = '<span style=\"color: yellow; font-size:150% \">'
qstyle_end = '</span>'
color = magenta
end_color = "\u001b[0m"

from random import randint

class Question():

    def __init__(self, show_html=False):
        if show_html:
            self.highlight_start = '<span style=\"color: yellow; font-size:150% \">'
            self.highlight_end = '</span>'
            self.list_sep_start = '<ul>'
            self.list_sep_end = '</ul><p>'
            self.list_elem_start = '<li>'
            self.list_elem_end = '</li>'
            self.line_end = '<p>'
        else:
            self.highlight_start = color
            self.highlight_end = end_color
            self.list_sep_start = "\n"
            self.list_sep_end = "\n"
            self.list_elem_start = ' -'
            self.list_elem_end = "\n"
            self.line_end = "\n"


class KanjiSimilarityQuestion(Question):
    
    def __init__(self, k, show_html=False):
        self.k = k
        super().__init__(show_html)
    

    def get_prompt(self, max_answers=4):
        show_html=self.show_html
        if len(self.k.similar) >= max_answers:
            cands = random.sample(self.k.similar, max_answers-1)
        else:
            cands = self.k.similar
            
        # Add the actual answer to the candidate list
        cands = cands + [self.k.symbol]
        random.shuffle(cands)
        
        self.cidx = cands.index(self.k.symbol)
        print(cands)
        print(self.k.symbol)
        print(self.cidx)

        choices = ''.join([f"{self.list_elem_start} ({i+1}) {k} {self.list_elem_end}" for i,k in enumerate(cands)])
        return f"Which of these kanjis means {self.highlight_start}{self.k.meaning}{self.highlight_end}? {self.list_sep_start}{choices}{self.list_sep_end}"

#         if show_html:
#             choices = ''.join([f"<li> ({i+1}) {k} </li>" for i,k in enumerate(cands)])
#             return f"Which of these kanjis means {qstyle_start}{self.k.meaning}{qstyle_end}? <ul>{choices}</ul><p>"
#         else:
#             choices = ''.join([f" - ({i+1}) {k} \n" for i,k in enumerate(cands)])
#             return f"Which of these kanjis means {color}{self.k.meaning}{end_color}? \n{choices}\n"
            
    
    def is_correct(self, ans):
        try:
            ans = int(ans)-1 # account for 1-offset in question statement
            return ans == self.cidx
        except:
            return ans == self.k.symbol

    
    def is_correct_with_feedback(self, ans):
        try:
            # account for 1-offset in question statement
            ans = int(ans)-1 
            hit = ans == self.cidx
#            print("is correct?", hit)
        except:
            hit = ans == self.k.symbol
        return hit, f"The answer is {green}{self.k}{end_color}"
    

    def question_type(self): return "kanji_similarity"
    
#     def explanation(self, ans):
#         return "The kanji for {self.k.meaning} is {self.k.symbol} ({})."


class RadicalDecompsitionQuestion(Question):
    
    def __init__(self, k, show_html=False):
        self.k = k
        self.show_html = show_html
        super().__init__(show_html)
    

    def get_prompt(self):
        if self.show_html:
            return f"What radicals make up the kanji for {qstyle_start}{self.k.meaning}{qstyle_end}?"
        else:
            return f"What radicals make up the kanji for {color}{self.k.meaning}{end_color}?"


    def is_correct(self, ans):
        gold_rad_names = set([r.name for r in self.k.radicals])
        ans_rad_names = set(ans.strip().split(" "))
        return gold_rad_names == ans_rad_names

    def question_type(self): return "radical_decomposition"


class PronunciationQuestion(Question):
    
    def __init__(self, k, show_html=False):
        self.k = k
        self.show_html = show_html
        super().__init__(show_html)
    
    def get_prompt(self):
        if self.show_html:
            return f"How do you pronounce the kanji {qstyle_start}{self.k.symbol}{qstyle_end}?"
        else:
            return f"How do you pronounce the kanji {color}{self.k.symbol}{end_color}?"
    
    def is_correct(self, ans):
        return ans.strip() in self.k.onyomi()

    def question_type(self): return "pronunciation"


class KanjiFromMeaningQuestion(Question):
    
    def __init__(self, k, show_html=False):
        self.k = k
        self.show_html = show_html
        super().__init__(show_html)
    
    def get_prompt(self):
        if self.show_html:
            return f"What is the kanji with the meaning {qstyle_start}{self.k.meaning}{qstyle_end}?"
        else:
            return f"What is the kanji with the meaning {color}{self.k.meaning}{end_color}?"
    
    def is_correct(self, ans):
        return ans.strip() == self.k.symbol

    def question_type(self): return "kanji_from_meaning"


class PatternUnderstandingQuestion(Question):

    def __init__(self, v, show_html):
        self.v = v
        self.show_html = show_html
        super().__init__(show_html)
    
        
    def get_prompt(self):
        print(self.highlight_start)
        self.pattern = self.v.patterns[randint(0, len(self.v.patterns)-1)]
        return f"What is the meaning of the phrase {self.highlight_start}{self.pattern[0]}{self.highlight_end}?"


    def is_correct(self, ans):
        for usage in self.pattern[1].split(","):
            if ans.strip().lower() == self.pattern[1].strip().lower():
                return True
        return False

    
    def is_correct_with_feedback(self, ans, wk):
        hint = f"The answer is: {green}{self.pattern[1]}{end_color}" + \
               f"{self.line_end}from the word:{self.line_end}{self.list_elem_start} {self.v.symbol} ({', or '.join(self.v.readings)}), meaning {', or '.join(self.v.meanings)}{self.list_elem_end}"
        phrase = self.pattern[0]
        matches = []
        for v in wk.vocab.values():
            if v != self.v and v.symbol not in self.v.symbol and v.symbol in phrase:
                matches.append(v)
        parts = []
        for m1 in matches:
            for m2 in matches:
                if m1.symbol in m2.symbol and len(m1.symbol) < len(m2.symbol):
                    parts.append(m1)
        if len(parts) > 0:
            print("parts: ", parts)

        matches = [m for m in matches if m not in parts]
        if len(matches) > 0:
            hint += "Other words found:\n"
            for m in matches:
                hint += f"{self.list_elem_start} {m.symbol}, meaning {', or '.join(m.meanings)}{self.list_elem_end}"
        return self.is_correct(ans), hint
    

    def question_type(self): return "pattern_understanding"

    
from wk.conjugate import te_form 
import romkan

class ConjugationQuestion(Question):
    
    def __init__(self, v, show_html=False):
        self.v = v
        self.show_html = show_html
        super().__init__(show_html)
    
    def get_prompt(self):
        if self.show_html:
            return f"What is the -te form of {self.highlight_start}{self.v.symbol}{self.highlight_end}?"
    
    def is_correct(self, ans):
        print(romkan.to_hiragana(ans.strip()))
        return (ans.strip() == te_form(self.v) or
               romkan.to_hiragana(ans.strip()) == te_form(self.v, hiragana=True))

    def is_correct_with_feedback(self, ans, wk):
        v = self.v
        verb_type = self.v
        hint = f"From {v.symbol} ({', or '.join(v.readings)}) meaning {', or '.join(v.meanings)}{self.line_end} is a {v.verb_type()}, so the -te form is {te_form(v)}"
        return self.is_correct(ans), hint

    def question_type(self): return "conjugation"
    