import os
import string
import xml.etree.ElementTree as ET


def extract_roots(text : str) -> list[list[str]]:
    words = text.split()
    words = [''.join([c.lower() for c in s if not c in string.punctuation + '“”’‘‘0123456789-']) for s in words]
    roots : list[list[str]] = [w.split('_') for w in words]
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
        
        
def count_words_in_xml(text : str) -> dict[str,int]:
    word_count : dict[str,int] = {}
    tree = ET.fromstring(text)
    strings : list[str] = extract_eo_text(tree)
    for line in strings:
        for word in extract_roots(line):
            whole_word = ''.join(word)
            word_count[whole_word] = word_count.get(whole_word,0) + 1    

    return word_count


def main():
    word_count : dict[str,int] = {}
    outfile = open("./tekstaro.dict","w")
    dir = os.fsencode("./tekstaroxml")
    for filebytes in os.listdir(dir):
        filename = os.fsdecode(filebytes)
        if not os.path.isfile('tekstaroxml/' + filename): 
            continue
        file = open("tekstaroxml/" + filename,"r")
        filetext = file.read()
        for item in count_words_in_xml(filetext).items():
            word_count[item[0]] = word_count.get(item[0],0) + item[1]
        file.close()
    for item in word_count.items():
        outfile.write(f'{item[0]}->{item[1]}\n')
    outfile.close()

main()