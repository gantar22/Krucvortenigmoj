import sys
from collections import defaultdict

def hat_pairs(words : set[str]) -> dict[str,int]:
    def unhat(c : str) -> str:
        unhat_map : dict[str,str] = {'ĉ':'c','ŝ':'s','ĝ':'g','ŭ':'u','ĵ':'j','ĥ':'h'}
        other_map : dict[str,str] = {'c':'s','t':'d'}
        unhatted = unhat_map.get(c,c)
        unhatted = other_map.get(unhatted,unhatted)
        return unhatted

    pairs : dict[str,list[tuple[str,int]]] = defaultdict(list) # Map from hatless string to all matching valid strings (the hatless one might not be a real word)
    for w in words:
        key = ''.join([unhat(c) for c in w])
        pairs[key].append((w,50))
        
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
                for word in [ww for w in line.split() for ww in w.split(';')]:
                    words[word] = 50
    return words

def write_words(out_file : str, scores : dict[str,int]):
    with open(out_file,'w') as fd:
        for (w,s) in scores.items():
            fd.write(f'{w};{s}\n')

roots = ['roots.txt']#['bitlibroj','sheetsdoc','tekstaro','vortlisto']
roots = [f'./Vortlisto/artefaktoj/{f}' for f in roots]
base_words = get_words(roots)

words = ['bitlibroj','permane','tekstaro','vortlisto']
words = [f'./Vortlisto/artefaktoj/{f}.dict' for f in words]
full_words = get_words(words)

words_to_use = set()
for (w,s) in full_words.items():
    if w[:-1] in base_words.keys():
        if w[-1] in ['o','i','e','a']:
            words_to_use.add(w)


pairs = hat_pairs(words_to_use)
pairs = {w:s + 100 for (w,s) in pairs.items()}
write_words('./Vortlisto/artefaktoj/hat_pairs.dict',pairs)