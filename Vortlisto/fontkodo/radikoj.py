

from typing import Optional


DecomposedWord = tuple[str,...]

def generate_derivative_words(word : DecomposedWord) -> list[DecomposedWord]:
    """
    """
    additions = []
    # remove accusatives
    if word[-1] == 'n':
        word = word[:-1]
        additions.append(word)
    if len(word) == 0:
        return additions

    # remove plurals
    if word[-1] == 'j':
        word = word[:-1]
        additions.append(word)
    if len(word) == 0:
        return additions

    # remove o from nouns
    if len(word[-1]) == 1 and word[-1] == 'o':
        additions.append(word[:-1])
    # remove verb tenses
    if len(word[-1]) >= 2:
        if word[-1][-1] == 's' and (word[-1][-2] in 'iaou'):
            additions.append(tuple(list(word[:-1]) + ['i']))

        # todo remove participles

    return additions


        
def load_roots() -> dict[str,int]:
    """Loads up the dictionary word lists and gets the scores from them
    """
    vortlisto = open('./artefaktoj/vortlisto.dict','r',encoding='utf8') # todo: I'm okay with being conservative, but this list is like 3 times bigger than a list of just roots. Maybe its worth filtering it to reduce spell checking time
    radiklisto = open('./artefaktoj/roots.txt','r',encoding='utf8')

    words = vortlisto.readlines()

    validroots = {}
    for pair in [w.split(';') for w in words]:
        key = pair[0]
        value = int(pair[1])
        # if the key isn't already there and higher
        if not (key in validroots and validroots[key] > value):
            validroots[key] = value
            
    # we get extra roots because vortaro.dict leaves out stuff like -o and other small roots
    extraroots = {r[:-1]:50 for r in radiklisto.readlines()}

    return extraroots | validroots
        
def base_word_score(word : DecomposedWord, roots : dict[str,int]) -> int:
    """Given a scoring mapping "roots", calculates a score for "word" based off of its parts
    """
    score = 19
    if len([r for r in word if not (r in roots)]) == 0:
        score = 50
        scores = [roots[r] for r in word]
        for s in scores:
            if abs(s - 50) > abs(score - 50):
                score = s
    return score


def decompose_word(word : str, roots : dict[str,int]) -> list[DecomposedWord]:
    if word == '':
        return [()]
    possible_interpretations = []
    for i in range(0,len(word)):
        subword = word[0:i + 1]
        if subword in roots:
            possible_interpretations += [tuple([subword]) + ending for ending in decompose_word(word[i+1:],roots)]

    return possible_interpretations
            

roots = load_roots()
print(decompose_word('trafiko',roots))
print(decompose_word('memamaj',roots))
print(decompose_word('ver',roots))