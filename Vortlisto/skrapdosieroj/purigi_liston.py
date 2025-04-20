import sys

def remove_empty_words(input_file):
    word_scores = []
    with open(input_file,'r') as fd:
        word_scores = fd.readlines()

    word_scores = [s for s in word_scores if len(s.split(';')[0]) > 0]

        
    file_split = input_file.split('.')
    file_split[-2] = file_split[-2] + '_purigite'
    output_file = '.'.join(file_split)
    with open(output_file,'w') as fd:
        fd.writelines(word_scores)

    print('farite')


def __main__():
    remove_empty_words(sys.argv[1])

if __name__ == '__main__':
    __main__()