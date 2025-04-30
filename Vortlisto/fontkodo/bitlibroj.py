import string
from typing import List, Optional, Tuple
from radikoj import DecomposedWord, generate_derivative_words, load_roots, base_word_score, decompose_word
from bs4 import BeautifulSoup
import os
import glob
import re
import sys

def get_paragraphs(path_to_epub : str) -> list[str]:
    """Loads an epub and extracts all the valid sentences
    """
    html_paths  = glob.glob(path_to_epub + '/**/*.html' ,recursive=True)
    html_paths += glob.glob(path_to_epub + '/**/*.xhtml',recursive=True)

    paragraphs = []
    for path in html_paths:
        soup = BeautifulSoup(open(path))
        paragraphs += [p.string for p in soup.find_all('p') if p.string != None]
    
    return paragraphs

def get_clauses(path_to_epub : str) -> set[str]:
    """Loads an epub and extracts all the valid sentences/clauses
    """
    remove_punctuation = lambda w: ''.join([c for c in w if not c in string.punctuation + '“”’‘‘0123456789-'])

    sentences = []
    paragraphs = get_paragraphs(path_to_epub)
    for paragraph in paragraphs:
        sentence = re.split(r'[.;,?!\-\n]',paragraph)
        sentence = remove_punctuation(sentence)
        sentences.append(sentence)
    
    return sentences

def get_words(path_to_epub : str) -> set[str]:
    """Loads an epub and extracts all the valid words
    """
    remove_punctuation = lambda w: ''.join([c for c in w if not c in string.punctuation + '“”’‘‘0123456789-'])
    
    words = ' '.join(get_paragraphs(path_to_epub)).split()
    words = {remove_punctuation(w.lower()) for w in words}
    words = {w for w in words if len(w) > 1}
    
    return words



def score_words(words : set[str], roots : dict[str,int], score_cache : dict[str,int], multiple_appearences : set[str]):
    for word in words:
        if word in score_cache:
            multiple_appearences.add(word)
        else:
            decomped = decompose_word(word,roots)
            if len(decomped) == 0:
                continue
            decomped += [w for d in decomped for w in generate_derivative_words(d)]
            scores = [base_word_score(decomp,roots) for decomp in decomped]
            score_cache[word] = max(scores)

def get_epub_paths() -> list[str]:
    """Return a list of all paths to epub.
    """
    dir = '../../libroj/Epubs/elpakitaj'
    paths = [p.path for p in os.scandir(dir) if p.is_dir()]
    return paths

def main():
    outputfile = open('./artefaktoj/bitlibroj.dict','w',encoding='utf8')

    roots : dict[str,int] = load_roots()
    score_cache : dict[str,int] = {}
    words_that_appear_twice : set[str] = set()
    for path in get_epub_paths():
        raw_words = get_words(path)
        score_words(raw_words,roots,score_cache,words_that_appear_twice)

    # todo only count words that appear twice and maybe even twice in different works
    for word in score_cache.keys():
        outputfile.write(f'{word};{score_cache[word]}\n')
    
    print('farite')

if __name__ == '__main__':
    main()