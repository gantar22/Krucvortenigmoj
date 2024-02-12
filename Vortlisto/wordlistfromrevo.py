import xml.etree.ElementTree as ET
import os
import re
import itertools

def replacehats(s):
    hatpairs = [('s','ŝ'),('g','ĝ'),('c','ĉ'),('j','ĵ'),('h','ĥ'),('S','Ŝ'),('G','Ĝ'),('C','Ĉ'),('J','Ĵ'),('H','Ĥ')]
    for pair in hatpairs:
        s = s.replace('&' + pair[0] + 'circ;',pair[1])
    s = s.replace('&ubreve;','ŭ').replace('&Ubreve;','Ŭ')
    return s

def removeallentities(s):
    return re.sub('&.*?;','',s)

def getwordsfromxml(xml) -> dict[str,int]:
    def getwordsfromkap(kap,radiko) -> dict[str,int]:
        words = {}
        word = ""
        if kap.text != None:
            word += kap.text
        for child in kap:
            if child.tag == 'tld':
                word += radiko
            if child.tag == 'var':
                commaindex = word.find(',')
                if commaindex != -1:
                    word = word[:commaindex]
                words[word] = 50
                word = ""
                innerkap = child.find('kap')
                if innerkap != None:
                    words |= getwordsfromkap(innerkap,radtext)
            if child.tail != None:
                word += child.tail
        word = word.strip()
        if len(word) > 0:
            words[word] = 50
        return words



    output : dict[str,int] = {} 
    tree = ET.fromstring(xml)
    radtext : str = ''
    try:
        art = tree.find('art')
        if art != None:
            kap = art.find('kap')
            if kap != None:
                rad = kap.find('rad')
                if rad != None:
                    radtext = rad.text or ""
    except:
        print(xml)
        return {}
    for drv in tree.find('art') or []:
        kap = drv.find('kap')
        if kap != None:
            output |= getwordsfromkap(kap,radtext)
    for verbi in [w for w in output.keys() if len(w) > 0 and w[-1] == 'i']: #gotta skip pronouns somehow
        try:
            verb = verbi[:-1]
            output[verb + 'us'] = 40
            output[verb + 'u'] = 40
            for v in ['i','a','o']:
                output[verb + v + 's'] = 40
                for fin in ['a','o','']:
                    pass
                    #output[verb + v + 'nt' + fin] = 40
                    #output[verb + v +  't' + fin] = 30 # 30 because the verb might not be transitive. todo check for trans. in the file. also some verbs don't very sensible at constructions as they concern results and/or lack duration
        except:
            pass

    if radtext + "o" in output.keys() and output.get(radtext,-1) < 50:
        output[radtext] = 50
        output[radtext + "on"] = 35 # might not be be something that appears often as the object 
        output[radtext + 'oj'] = 35 # might not be something that apperas often in plural
        output[radtext + "ojn"] = 30 # see above

    # todo if theres an adjective ending we could throw on igi and iĝi

    for ending in ["a","e","i","o"]:
        pass
        #output[radtext + ending] = output.get(radtext + ending,30) # 30 cause we have no idea what this means

    # todo add versions without hyphens
    output |= {w.replace('-',''):output[w] for w in output.keys() if '-' in w}
    # make versions without any nonalpha chars
    output |= {''.join([c for c in w if c.isalpha()]):output[w] for w in output.keys() if len([c for c in w if c.isalpha()]) > 0}
    return output



def main():
    outfile = open("./vortlisto.dict","w",encoding='utf8')
    dir = os.fsencode("./revo")
    for filebytes in os.listdir(dir):
        filename = os.fsdecode(filebytes)
        if not os.path.isfile('revo/' + filename): 
            continue
        file = open("revo/" + filename,"r",encoding='utf8')
        filetext = file.read()
        filetext = removeallentities(replacehats(filetext))
        wordlist = getwordsfromxml(filetext)
        for word in wordlist.keys():
            wordspaceless = ''.join(word.split())
            if len(wordspaceless) > 0:
                outfile.write(wordspaceless + f";{wordlist[word]}\n") #todo make one big dict with maximized values then write after
        file.close()
    outfile.close()


main()
