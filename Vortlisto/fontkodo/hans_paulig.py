
import sys
import radikoj as RAD

def remove_empty_words():
    words_A = {}
    words_O = {}
#   with open(in_A,'r') as fd:
#       for line in fd.readlines():
#           split = line.split(';')
#           words_A[split[0][:-1]] = split[1]
#   with open(in_B,'r') as fd:
#       for line in fd.readlines():
#           split = line.split(';')
#           words_O[split[0][:-1]] = split[1]

    roots = RAD.load_roots()
    roots = {r for r in roots if roots[r] > 50}
    roots = {r.lower() for r in roots if len(r) != 0}
    words_A = {r for r in roots if r[-1] == 'a'}
    words_O = {r for r in roots if r[-1] == 'o'}
    
        
    banned_words = {'kelka','trava','piceo','cia','pamiro','ŝanĝa','bora','torio'}
    lettercount = 12
    output_file = f'spoonerisms_{lettercount}.dict'
    with open(output_file,'w') as fd:
        fd.write('.\n')
        for a_word in words_A:
            for o_word in words_O:
                if a_word[0] == o_word[0]:
                    continue
                if a_word[1:-1] == o_word[1:-1]:
                    continue
#               if a_word in banned_words or o_word in banned_words:
#                   continue
#               if a_word[0] + o_word[1:] in o_word:
#                   if o_word[0] + a_word[1:] in a_word:
#                       fd.write(f'{a_word}a -> {o_word}o\n')
#               if a_word[0] + o_word[1:] in a_word:
#                   if o_word[0] + a_word[1:] in o_word:
#                       fd.write(f'{o_word}o -> {a_word}a\n')
                if len(a_word + o_word) == lettercount:
                    if o_word[0] + a_word[1:] in words_A and a_word[0] + o_word[1:] in words_O:
                        if o_word[1:] != a_word[1:] and o_word[0] != a_word[0]:
                            fd.write(f'{a_word} {o_word}\n')


    print('farite')


def __main__():
    remove_empty_words()

if __name__ == '__main__':
    __main__()