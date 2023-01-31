
from wk.questions import *
from IPython.display import display, HTML

#background_color = '#A4E7F7'
background_color = '#111111'

def ask_question(k, qtype, wk, idx, show_html=False):
    qtype = qtype.lower().replace(" ", "_")
    if qtype == 'kanji_similarity':
        q = KanjiSimilarityQuestion(k, show_html)
    elif qtype == 'radical_decomposition':
        q = RadicalDecompsitionQuestion(k, show_html)
    elif qtype == 'pronunciation':
        q = PronunciationQuestion(k, show_html)
    elif qtype == 'kanji_from_meaning':
        q = KanjiFromMeaningQuestion(k, show_html)
    elif qtype == 'pattern_understanding':
        q = PatternUnderstandingQuestion(k, show_html)
    elif qtype == 'conjugation':
        q = ConjugationQuestion(k, show_html)
    else:
        raise Exception(f"Invalid question type [{qtype}]")

    if show_html:
        html = f"<div style=\"background-color:{background_color};width:500px;height:50px;border:1px solid #000;\"><b>" + \
        q.get_prompt() + '</b></br></div>'
    
        display(HTML(html))
    else:
        print(str(idx) + ") " + q.get_prompt())

    ans = input().strip()
    
    return q.is_correct_with_feedback(ans, wk)


from random import choice
def choose_kanji(q, wk):
    if str(q) == 'kanji_similarity':
        return wk.next_kanji_by_similarity(threshold=1)
    elif str(q) == 'pattern_understanding':
        return wk.next_vocab()
    elif str(q) == 'conjugation':
        verbs = [v for v in wk.vocab.values() if (v.is_ichidan_verb() or v.is_godan_verb())]
        return choice(verbs)
    else:
        return wk.next_kanji()

