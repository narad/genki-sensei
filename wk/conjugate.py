

def te_form(vocab, hiragana=False):
    if hiragana:
        word = vocab.readings[0]
    else:
        word = vocab.symbol
    if 'godan verb' in vocab.word_types:
        if word[-1] in ['う','つ','る']:
            return word[:-1] + 'って'
        elif word[-1] in ['ぬ', 'ぶ', 'む']:
            return word[:-1] + 'んで'
        elif word[-1] == 'す':
            return word[:-1] + 'して'
        elif word[-1] == 'く':
            return word[:-1] + 'いて'
        elif word[-1] == 'ぐ':
            return word[:-1] + 'いで'

    elif 'ichidan verb' in vocab.word_types:
        return word[:-1] + 'て'
    else:
#         print("not a verb?")
#         print(vocab.word_types)
        sys.exit(1)