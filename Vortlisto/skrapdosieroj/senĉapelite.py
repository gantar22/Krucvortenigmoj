"""
filters .dict files for only words that don't have ĉapelojn
"""

import sys


def unhat(c : str) -> str:
    unhat_map : dict[str,str] = {'ĉ':'c','ŝ':'s','ĝ':'g','ŭ':'u','ĵ':'j','ĥ':'h'}
    unhatted = unhat_map.get(c)
    if unhatted != None:
        return unhatted
    return c

def main():
    hats = ['ĉ','ŝ','ĝ','ŭ','ĵ','ĥ']
    word_scores = []
    input_file = sys.argv[1]
    with open(input_file,'r') as fd:
        word_scores = fd.readlines()

    word_scores = [''.join([unhat(c) for c in w]) for w in word_scores]  # todo deal with collisions    
    file_split = input_file.split('.')
    file_split[-2] = file_split[-2] + '_senĉapelite'
    output_file = '.'.join(file_split)
    with open(output_file,'w') as fd:
        fd.writelines(word_scores)

    print('farite')



main()