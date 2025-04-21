import string
from typing import Tuple
from radikoj import DecomposedWord, generate_derivative_words, load_roots, base_word_score, decompose_word
from bs4 import BeautifulSoup
import os
import glob
import re
import sys

def get_words(path_to_epub : str) -> set[str]:
    """Loads an epub and extracts all the valid words
    """
    remove_punctuation = lambda w: ''.join([c for c in w if not c in string.punctuation + '“”’‘‘0123456789-'])

    def get_text(path_to_epub : str) -> str:
        html_paths  = glob.glob(path_to_epub + '/**/*.html' ,recursive=True)
        html_paths += glob.glob(path_to_epub + '/**/*.xhtml',recursive=True)

        paragraphs = []
        for path in html_paths:
            soup = BeautifulSoup(open(path))
            paragraphs += [p.string for p in soup.find_all('p') if p.string != None]
        
        return ' '.join(paragraphs)
    
    words = get_text(path_to_epub).split()
    words = {remove_punctuation(w.lower()) for w in words}
    words = {w for w in words if len(w) > 1}
    
    return words

def get_word_pairs(path_to_epub : str) -> set[Tuple[str,str]]:
    """Loads an epub and extracts all the valid words
    """
    remove_punctuation = lambda w: ''.join([c for c in w if not c in string.punctuation + '“”’‘‘0123456789-'])

    def get_text(path_to_epub : str) -> list[str]:
        html_paths  = glob.glob(path_to_epub + '/**/*.html' ,recursive=True)
        html_paths += glob.glob(path_to_epub + '/**/*.xhtml',recursive=True)

        paragraphs = []
        for path in html_paths:
            soup = BeautifulSoup(open(path))
            paragraphs += [p.string for p in soup.find_all('p') if p.string != None]
        
        return paragraphs
    
    paragraphs = get_text(path_to_epub)
    pairs = set()
    def is_pair(first_word,second_word, rec = False):
        if len(first_word) < 3 or len(second_word) < 3:
            return False
        bad_adjectives = {'mia','ĝia','via','lia','sia','ŝia','ilia','ria','nia','onia'}
        bad_nouns = {'tio','kio'}
        if first_word[-1] == 'a' and second_word[-1] == 'o':
            if first_word not in bad_adjectives and second_word not in bad_nouns:
                return True
        if first_word[-2:] == 'aj' and second_word[-2:] == 'oj':
            if first_word[-1:] not in bad_adjectives and second_word[:-1] not in bad_nouns:
                return True
        if first_word[-2:] == 'an' and second_word[-2:] == 'on':
            if first_word[:-1] not in bad_adjectives and second_word[:-1] not in bad_nouns:
                return True
        if first_word[-3:] == 'ajn' and second_word[-3:] == 'ojn':
            if first_word[:-2] not in bad_adjectives and second_word[:-2] not in bad_nouns:
                return True
        pronouns = {'mi','ĝi','vi','li','si','ŝi','ili','ri','ni','oni'}
        if first_word[-1] == 'i' and second_word[-2:] == 'on':
            if first_word not in pronouns and second_word[:-1] not in bad_nouns:
                return True
        if first_word[-1] == 'i' and second_word[-3:] == 'ojn':
            if first_word not in pronouns and second_word[:-2] not in bad_nouns:
                return True
        verb_endings = {'is','as','os','us'}
        false_verbs = {'ĝis'}
        if first_word[-2:] in verb_endings and second_word[-2:] == 'on':
            if first_word not in false_verbs and second_word[:-1] not in bad_nouns:
                return True
        if first_word[-2:] in verb_endings and second_word[-3:] == 'ojn':
            if first_word not in false_verbs and second_word[:-2] not in bad_nouns:
                return True
        if first_word[-1] == 'e' and second_word[-1] == 'i':
            if second_word not in false_verbs and second_word not in pronouns:
                return True
        verb_endings = {'is','as','os','us'}
        if first_word[-1] == 'e' and second_word[-2:] in verb_endings:
            if second_word not in false_verbs:
                return True
        
        if rec and is_pair(second_word,first_word,False):
            return True
        return False

    for paragraph in paragraphs:
        sentences = re.split(r'[.;,]',paragraph)
        for sentence in sentences:
            words = sentence.split()
            words = [remove_punctuation(w.lower()) for w in words]
            for i in range(len(words) - 1):
                if is_pair(words[i],words[i+1]):
                    pairs.add((words[i],words[i+1]))
            for i in range(1,len(words)):
                if is_pair(words[i-1],words[i]):
                    pairs.add((words[i-1],words[i]))

    return pairs

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

def score_pairs(pair : Tuple[str], roots : dict[str,int], score_cache : dict[Tuple[str],int], appearance_count : dict[Tuple[str],int]):
    if pair in score_cache:
        appearance_count[pair] = appearance_count[pair] + 1
    else:
        decomped_0 = decompose_word(pair[0],roots)
        decomped_1 = decompose_word(pair[1],roots)
        if len(decomped_0) == 0:
            return
        if len(decomped_1) == 0:
            return
        scores_0 = [base_word_score(decomp,roots) for decomp in decomped_0]
        scores_1 = [base_word_score(decomp,roots) for decomp in decomped_1]
        score_cache[pair] = (max(scores_0) + max(scores_1)) / 2.0
        appearance_count[pair] = 1

def get_epub_paths() -> list[str]:
    """Return a list of all paths to epub.
    """
    dir = '../../libroj/Epubs/elpakitaj'
    paths = [p.path for p in os.scandir(dir) if p.is_dir()]
    return paths

def output_pairs():
    outputfile = open('./artefaktoj/bitlibroj_pairs.dict','w',encoding='utf8')
    score_cache : dict[str,int] = {}
    pair_count  : dict[str,int] = {}
    roots : dict[str,int] = load_roots()
    for path in get_epub_paths():
        pairs = get_word_pairs(path)
        for pair in pairs:
            score_pairs(pair,roots,score_cache,pair_count)
    for pair in pair_count.keys():
        if pair_count[pair] > 5:
            outputfile.write(f'{pair[0] + pair[1]};{int(score_cache[pair])}\n')

def main():
    outputfile = open('./artefaktoj/bitlibroj.dict','w',encoding='utf8')

    roots : dict[str,int] = load_roots()
    score_cache : dict[str,int] = {}
    words_that_appear_twice : set[str] = set()
    for path in get_epub_paths():
        raw_words = get_words(path)
        score_words(raw_words,roots,score_cache,words_that_appear_twice)

    #for word in words_that_appear_twice:
    for word in score_cache.keys():
        outputfile.write(f'{word};{score_cache[word]}\n')
    
    output_pairs()
    print('farite')

if __name__ == '__main__':
    main()