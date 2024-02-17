import os
import re
import string
import xml.etree.ElementTree as ET

def get_extras(roots : list[list[str]]) -> list[list[str]]:
    additions = []
    for word in roots:
        w = word
        # remove accusatives
        if w[-1] == 'n':
            w = w[:-1]
            additions.append(w)
        if len(w) == 0:
            continue

        # remove plurals
        if w[-1] == 'j':
            w = w[:-1]
            additions.append(w)
        if len(w) == 0:
            continue

        # remove o from nouns
        if len(w[-1]) == 1 and w[-1] == 'o':
            additions.append(w[:-1])
        # remove verb tenses
        if len(w[-1]) >= 2:
            if w[-1][-1] == 's' and (w[-1][-2] in 'iaou'):
                additions.append(w[:-1] + ['i'])

        # todo remove participles

    return additions

def extract_roots(text : str) -> list[list[str]]:
    words = text.split()
    roots : list[list[str]] = [w.split('_') for w in words]
    remove_punctuation = lambda w: ''.join([c for c in w if not c in string.punctuation + '“”’‘‘0123456789-'])
    roots = [[''.join([c.lower() for c in w]) for w in r] for r in roots]
    roots = [[remove_punctuation(w) for w in r] for r in roots]
    roots = [r for r in roots if len(r) > 0]

    roots += get_extras(roots)
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
        
def load_roots() -> set[str]:

    def replacehats(s):
        hatpairs = [('s','ŝ'),('g','ĝ'),('c','ĉ'),('j','ĵ'),('h','ĥ'),('S','Ŝ'),('G','Ĝ'),('C','Ĉ'),('J','Ĵ'),('H','Ĥ')]
        for pair in hatpairs:
            s = s.replace('&' + pair[0] + 'circ;',pair[1])
        s = s.replace('&ubreve;','ŭ').replace('&Ubreve;','Ŭ')
        return s

    def removeallentities(s):
        return re.sub('&.*?;','',s)

    roots : set[str] = set()
    for filename in [os.fsdecode(f) for f in os.listdir(os.fsencode("./revo"))]:
        if not os.path.isfile('revo/' + filename):
            continue
        text = open(f"revo/{filename}","r",encoding="utf8").read()
        text = removeallentities(replacehats(text))
        tree = ET.fromstring(text)
        try:
            roots.add(tree.find('art').find('kap').find('rad').text.lower())
        except:
            pass

    return roots

        
def count_words_in_xml(text : str, must_be_dictionary : bool = True, roots : set[str] = {}) -> dict[str,int]:
    word_count : dict[str,int] = {}
    tree = ET.fromstring(text)
    strings : list[str] = extract_eo_text(tree)
    for line in strings:
        for word in extract_roots(line):
            is_vortara = len([r for r in word if not (r in roots)]) == 0
            if is_vortara == must_be_dictionary:
                whole_word = ''.join(word)
                word_count[whole_word] = word_count.get(whole_word,0) + 1    

    return word_count




def main():
    countfile = open("./tekstaro.count","w",encoding='utf8')
    vortarajfile = open("./tekstaro_vortara.dict","w",encoding='utf8')
    vortaraj = {}
    nevortarajfile = open("./tekstaro_nevortara.dict","w",encoding='utf8')
    nevortaraj = {}
    dir = os.fsencode("./tekstaroxml")
    roots = load_roots()
    for filebytes in os.listdir(dir):
        filename = os.fsdecode(filebytes)
        if not os.path.isfile('tekstaroxml/' + filename): 
            continue
        file = open("tekstaroxml/" + filename,"r",encoding='utf8')
        filetext = file.read()
        file.close()
        for item in count_words_in_xml(filetext,True,roots).items():
            vortaraj[item[0]] = vortaraj.get(item[0],0) + item[1]
        for item in count_words_in_xml(filetext,False,roots).items():
            nevortaraj[item[0]] = nevortaraj.get(item[0],0) + item[1]
    for item in vortaraj.items():
        countfile.write(f'{item[0]}->{item[1]}\n')
        vortarajfile.write(f'{item[0]};{60}\n')
    for item in nevortaraj.items():
        countfile.write(f'{item[0]}->{item[1]}\n')
        nevortarajfile.write(f'{item[0]};{19}\n')
    countfile.close()

main()