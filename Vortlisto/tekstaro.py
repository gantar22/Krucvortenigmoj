import os
import re
import string
import xml.etree.ElementTree as ET

def get_extras(roots : list[tuple[str]]) -> list[tuple[str]]:
    additions = []
    for word in roots:
        w = word
        # remove accusatives
        if w[-1] == 'n':
            w = w[:-1]
            additions.append(w)
        if len(w) == 0:
            continue

        # remove plurals
        if w[-1] == 'j':
            w = w[:-1]
            additions.append(w)
        if len(w) == 0:
            continue

        # remove o from nouns
        if len(w[-1]) == 1 and w[-1] == 'o':
            additions.append(w[:-1])
        # remove verb tenses
        if len(w[-1]) >= 2:
            if w[-1][-1] == 's' and (w[-1][-2] in 'iaou'):
                additions.append(tuple(list(w[:-1]) + ['i']))

        # todo remove participles

    return additions

def extract_roots(text : str) -> list[tuple[str]]:
    words = text.split()
    roots = [tuple(w.split('_')) for w in words]
    remove_punctuation = lambda w: ''.join([c for c in w if not c in string.punctuation + '“”’‘‘0123456789-'])
    roots = [tuple([''.join([c.lower() for c in w]) for w in r]) for r in roots]
    roots = [tuple([remove_punctuation(w) for w in r]) for r in roots]
    roots = [r for r in roots if len(r) > 0]

    roots += get_extras(roots)
    return roots

def extract_eo_text(tree : ET.Element) -> list[str]:
    output : list[str | None] = []
    for p in tree.iter('{http://www.tei-c.org/ns/1.0}p'): #todo also do '{}note' elements
        lang = p.get('{http://www.w3.org/XML/1998/namespace}:lang')
        if lang != None and lang != 'eo' or p.get('{http://www.w3.org/XML/1998/namespace}id') == None:
            continue
        output.append(p.text)
        for child in p.findall('*'):
            output.append(child.tail)

    return [o for o in output if o != None]
        
def load_roots() -> dict[str,int]:
    vortlisto = open('./vortlisto.dict','r',encoding='utf8')
    radiklisto = open('./roots.txt','r',encoding='utf8')

    words = vortlisto.readlines()

    # todo this gets whole words but we only want roots
    validroots = {p[0]:int(p[1]) for p in [w.split(';') for w in words]}
    extraroots = {r[:-1]:50 for r in radiklisto.readlines()}

    return extraroots | validroots
        
def base_word_score(word : tuple[str], roots :dict[str,int]) -> int:
    score = 19
    if len([r for r in word if not (r in roots)]) == 0:
        score = 50
        scores = [roots[r] for r in word]
        for s in scores:
            if abs(s - 50) > abs(score - 50):
                score = s
    return score


def words_in_text(text : str, roots : dict[str,int] = {}) -> set[tuple[str]]:
    tree = ET.fromstring(text)
    strings : list[str] = extract_eo_text(tree)
    output : set[tuple[str]] = set()
    for line in strings:
        for word in extract_roots(line):
            output.add(word)
    return output


def main():
    countfile = open("./tekstaro.dict","w",encoding='utf8')

    dir = os.fsencode("./tekstaroxml")
    roots = load_roots()
    words_by_source : list[set[tuple[str]]] = []
    for filebytes in os.listdir(dir):
        # get the text from the xml files
        filename = os.fsdecode(filebytes)
        if not os.path.isfile('tekstaroxml/' + filename): 
            continue
        file = open("tekstaroxml/" + filename,"r",encoding='utf8')
        filetext = file.read()
        file.close()

        # extract the roots from the text
        words_by_source.append(words_in_text(filetext,roots))
    
    words : set[tuple[str]] = {w for src in words_by_source for w in src if len([s for s in words_by_source if w in s]) > 1}
    for w in words:
        countfile.write(f"{''.join(w)};{base_word_score(w,roots)}\n")
    

main()