import xml.etree.ElementTree as ET
import os
import re

def replacehats(s):
    hatpairs = [('s','ŝ'),('g','ĝ'),('c','ĉ'),('j','ĵ'),('h','ĥ'),('S','Ŝ'),('G','Ĝ'),('C','Ĉ'),('J','Ĵ'),('H','Ĥ')]
    for pair in hatpairs:
        s = s.replace('&' + pair[0] + 'circ;',pair[1])
    s = s.replace('&ubreve;','ŭ').replace('&Ubreve;','Ŭ')
    return s

def removeallentities(s):
    return re.sub('&.*?;','',s)

def getwordsfromxml(xml):
    def getwordsfromkap(kap,radiko):
        words = []
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
                output.append(word)
                word = ""
                innerkap = child.find('kap')
                if innerkap != None:
                    words += getwordsfromkap(innerkap,radtext)
            if child.tail != None:
                word += child.tail
        word = word.strip()
        if len(word) > 0:
            words.append(word)
        return words



    output = []
    tree = ET.fromstring(xml)
    radtext = None
    try:
        radtext = tree.find('art').find('kap').find('rad').text
    except:
        print(xml)
        return []
    for drv in tree.find('art'):
        word = ""
        kap = drv.find('kap')
        if kap != None:
            output += getwordsfromkap(kap,radtext)
    if radtext + "o" in output and not radtext in output:
        output.append(radtext)
    # todo add versions without hyphens
    ouput += [w.replace('-','') for w in output if '-' in w]
    return list(set(output))



def main():
    outfile = open("./vortlisto.dict","w")
    dir = os.fsencode("./revo")
    for filebytes in os.listdir(dir):
        filename = os.fsdecode(filebytes)
        if not os.path.isfile('revo/' + filename): 
            continue
        file = open("revo/" + filename,"r")
        filetext = file.read()
        filetext = removeallentities(replacehats(filetext))
        for word in getwordsfromxml(filetext):
            word = ''.join(word.split())
            if len(word) > 0:
                outfile.write(word + ";5\n")
        file.close()
    outfile.close()


main()
