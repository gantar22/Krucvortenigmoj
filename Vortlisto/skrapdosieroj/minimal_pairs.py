import sys
from collections import defaultdict

def hat_pairs(words : dict[str,int]) -> dict[str,int]:
    def unhat(c : str) -> str:
        unhat_map : dict[str,str] = {'ĉ':'c','ŝ':'s','ĝ':'g','ŭ':'u','ĵ':'j','ĥ':'h'}
        unhatted = unhat_map.get(c)
        if unhatted != None:
            return unhatted
        return c


    pairs : dict[str,list[tuple[str,int]]] = defaultdict(list) # Map from hatless string to all matching valid strings (the hatless one might not be a real word)
    for (w,s) in words.items():
        key = ''.join([unhat(c) for c in w])
        pairs[key].append((w,s))
    
    result : dict[str,int] = {}
    for scores in [scores for (k,scores) in pairs.items() if len(scores) > 1]:
        for (w,s) in scores:
            result[w] = s

    return result 


def get_words(paths : list[str]) -> dict[str,int]:
    words : dict[str,int] = {}
    for p in paths:
        with open(p,'r') as fd:
            for line in fd.readlines():
                if not ';' in line:
                    continue
                (word,score_str) = line.split(';')
                words[word] = int(score_str)
    return words

def write_words(out_file : str, scores : dict[str,int]):
    with open(out_file,'w') as fd:
        for (w,s) in scores.items():
            fd.write(f'{w};{s}\n')

files = ['vortlisto']#['bitlibroj','sheetsdoc','tekstaro','vortlisto']
files = [f'./artefaktoj/{f}.dict' for f in files]
base_words = get_words(files)
pairs = hat_pairs(base_words)
pairs = {w:s + 100 for (w,s) in pairs.items()}
write_words('./artefaktoj/hat_pairs.dict',pairs)