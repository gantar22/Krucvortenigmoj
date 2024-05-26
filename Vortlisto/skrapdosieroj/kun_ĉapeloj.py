"""
filters .dict files for only words that have ĉapelojn
"""

import sys

def main():
    hats = ['ĉ','ŝ','ĝ','ŭ','ĵ','ĥ']
    word_scores = []
    input_file = sys.argv[1]
    with open(input_file,'r') as fd:
        word_scores = fd.readlines()

    word_scores = [w for w in word_scores if len([h for h in hats if h in w]) > 0]     
    output_file = input_file.split('.')[0] + '_kun_ĉapeloj.' + input_file.split('.')[1]    
    with open(output_file,'w') as fd:
        fd.writelines(word_scores)

    print('farite')



main()