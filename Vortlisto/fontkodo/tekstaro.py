import os
import string
from typing import Optional
import xml.etree.ElementTree as ET
from radikoj import DecomposedWord, generate_derivative_words, load_roots, base_word_score


def words_in_text(text : str) -> set[DecomposedWord]:
    """Extracts the words from the raw xml string
    """

    def extract_eo_text(tree : ET.Element) -> list[str]:
        """Get the text part out of a tekstaro xml file
        """
        output : list[Optional[str]] = []
        for p in tree.iter('{http://www.tei-c.org/ns/1.0}p'): #todo also do '{}note' elements
            lang = p.get('{http://www.w3.org/XML/1998/namespace}:lang')
            if lang != None and lang != 'eo' or p.get('{http://www.w3.org/XML/1998/namespace}id') == None: 
                continue
            output.append(p.text)
            for child in p.findall('*'):
                output.append(child.tail) # by only using the tail, we exclude the insides of all children which are often names or non-language components

        return [o for o in output if o != None]
        

    def extract_roots(text : str) -> list[DecomposedWord]:
        """Given a text from the tekstaro, returns the words broken up by root.
        vort_ar_o -> (vort,ar,o)
        """
        words = text.split()
        roots = [tuple(w.split('_')) for w in words]
        remove_punctuation = lambda w: ''.join([c for c in w if not c in string.punctuation + '“”’‘‘0123456789-'])
        roots = [tuple([w.lower() for w in r]) for r in roots]
        roots = [tuple([remove_punctuation(w) for w in r]) for r in roots]
        roots = [r for r in roots if len(r) > 0]

        roots += [addition for root in roots for addition in generate_derivative_words(root)]
        return roots

    tree = ET.fromstring(text)
    strings : list[str] = extract_eo_text(tree)
    output : set[DecomposedWord] = set()
    for line in strings:
        for word in extract_roots(line):
            output.add(word)
    return output


def main():
    countfile = open("./artefaktoj/tekstaro.dict","w",encoding='utf8')

    dir = os.fsencode("./font_datumoj/tekstaro") # todo: I'm pretty sure I don't need to do this encoding stuff
    roots = load_roots()
    words_by_source : list[set[DecomposedWord]] = []
    for filebytes in os.listdir(dir):
        # get the text from the xml files
        filename = os.fsdecode(filebytes)
        if not os.path.isfile('./font_datumoj/tekstaro/' + filename): 
            continue
        file = open("./font_datumoj/tekstaro/" + filename,"r",encoding='utf8')
        filetext = file.read()
        file.close()

        # extract the roots from the text
        words_by_source.append(words_in_text(filetext))
    
    # score them all and write them to file
    words : set[DecomposedWord] = {w for src in words_by_source for w in src if len([s for s in words_by_source if w in s]) > 1}
    scored_words : dict[str,int] = {}
    for w in words:
        raw_word = ''.join(w)
        score = base_word_score(w,roots)
        if scored_words.get(raw_word,score) <= score:
            scored_words[raw_word] = score
    for (word,score) in scored_words.items():
        countfile.write(f"{word};{score}\n")
    

main()