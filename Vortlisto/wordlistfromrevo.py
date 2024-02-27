import io
import xml.etree.ElementTree as ET
import os
import re
import itertools

def scorefromstil(stil):
    mapping = {
        'fraz': 10, #la senco estas frazaĵo mem, kiel havi aferon kun
        'fig': 10,
        'vulg': -15, #malfeliĉe temas pri famalieca eldonaĵo, do ni devas savi tion por postvespera programo
        'rar': -10,
        'poe': 10, #ne multaj artikoloj havas tion, sed ili ĉiuj estas bonaj
        'ark': -10,
        'evi': -50,
        'komune': 5,
        'neo': 0, #mi ŝatas, sed mi ne volas plioftigi ilin, se ili venas ili venas
    }
    return mapping.get(stil,0)

def scorefromfak(fak):
    # la granda celo estas ne uzi
    # tro de tre fakajn vortojn
    # precize tiujn de latina origino
    # kiuj ne havas nacilingvan komunana
    # tradukon

    # baze:
    # regiliaj aferoj bonas
    # artaj aferoj ne estas malbona
    # teknikaj aŭ inĝenieraj sciencoj malbonas
    # iu ajn kun multege de nomoj malbonas

    # verŝajne indas varii ĉi-tiun mapon
    # tiel ke ne ĉiu enigmo havas la saman
    # distribuon de fakvortoj

    
    mapping = {
        'agr':  -1, #agrokulturo
        'ana':   1, #anatomio
        'arke':  0, #arkeologio
        'arki': -1, #arkitekturo
        'ast':   1, #astronomio
        'aut':   1, #automobiloj
        'avi':  -1, #aviado
        'bak':  -2, #bakteriologio, suprize malmulte tro fakaj vortoj
        'bela': -1, #belartoj
        'bele': -1, #beletro
        'bib':  -1, #biblio
        'bio':  -5, #biologio
        'bot': -10, #botaniko
        'bud':   1, #budhismo
        'ekon': -2, #ekonomiko
        'ekol':  1, #ekologio
        'ele':  -5, #elektro
        'elet': -5, #elektrotekniko
        'esp':  10, #esperantismp
        'fer':  -2, #fervojoj
        'fil':  -5, #filozofio
        'fizl':-10, #fiziologio
        'fiz': -10, #fiziko
        'fon':  -5, #fonetiko
        'fot':  -7, #fotografio
        'gen':  -1, #genealogio
        'geod':  0, #geodezio
        'geog':-10, #geografio
        'geol': -2, #geologio
        'gra':   0, #gramatiko
        'her':  -3, #heraldiko
        'hin':   1, #hinduismo
        'his': -10, #historio
        'hor':  -2, #hortikulturo
        'isl':   1, #islamo
        'jur':  -5, #juro
        'kal':  -1, #kalendaro
        'kat':   1, #katolikismo
        'kem': -10, #kemio
        'kin':   0, #kinoarto
        'kir':   0, #kirurgio
        'komp': -5, #komputiko
        'kon':  -5, #konstrutekniko
        'kri':   1, #kristanismo
        'kui':  -1, #kuirarto
        'lin':  -1, #lingvistiko
        'mar':  -5, #maraferoj
        'mas':  -3, #maŝinoj
        'mat':  -6, #matematiko
        'mah':   0, #materialismo historia
        'med': -10, #medicino
        'met':  -1, #meteologio
        'mil':  -5, #militaferoj
        'min': -10, #mineralogio
        'mit':   1, #mitologio
        'muz': -10, #muziko
        'nom': -10, #nomoj
        'pal':  -1, #paleontologio
        'ped':  -5, #pedagogio
        'pers':-10, #personoj
        'poe':  -1, #poetiko mi ŝatus havi pli altan poentaron, sed ĝi ja estas faka
        'pol': -10, #politiko (landnomoj)
        'posx': -1, #poŝto
        'pra':   0, #prahistorio
        'psi':  -4, #psikologio
        'rad':   0, #radiofonio
        'rel':   1, #religioj
        'ret':   0, #interreto
        'sci':   0, #sciencoj, sufiĉe nefaka
        'spo':   1, #sporto kaj ludoj
        'shi':  -3, #ŝipkonstruado navigado
        'tea':   1, #teatro
        'tek':  -1, #teksindustrio
        'tel':   0, #telekomunikoj
        'tip':   0, #presarto, libroj
        'tra':   1, #trafiko
        'zoo': -10, #zoologio
    }
    return mapping.get(fak,0)

def replacehats(s):
    hatpairs = [('s','ŝ'),('g','ĝ'),('c','ĉ'),('j','ĵ'),('h','ĥ'),('S','Ŝ'),('G','Ĝ'),('C','Ĉ'),('J','Ĵ'),('H','Ĥ')]
    for pair in hatpairs:
        s = s.replace('&' + pair[0] + 'circ;',pair[1])
    s = s.replace('&ubreve;','ŭ').replace('&Ubreve;','Ŭ')
    return s

def removeallentities(s):
    return re.sub('&.*?;','',s)

def getwordsfromxml(xml : ET.ElementTree, rootsfile : io.TextIOWrapper) -> dict[str,int]:
    def getwordsfromkap(kap :ET.Element, radiko : dict[str,str]) -> dict[str,int]:
        words = {}
        word : str = ""
        if kap.text != None:
            word += kap.text
        for child in kap:
            if child.tag == 'tld': 
                var = child.get('var')
                if var != None:
                    word += radiko[var]
                else:
                    word += radiko[''] 
            if child.tag == 'var':
                commaindex = word.find(',')
                if commaindex != -1:
                    word = word[:commaindex]
                words[word] = 50
                word = ""
                innerkap = child.find('kap')
                if innerkap != None:
                    words |= getwordsfromkap(innerkap,radiko)
            if child.tail != None:
                word += child.tail
        word = word.strip()
        if len(word) > 0:
            words[word] = 50
        return words


    def getscorefordrv(drv : ET.Element):
        sencoj = list(drv.iter('snc')) 
        senc_kalk_sojloj = [2,3,5,8]
        scores = []
        for snc in sencoj:
            score = 0
            for uzo in snc.iter('uzo'):
                tip = uzo.get('tip')
                if tip == "fak" and uzo.text != None:
                    score += scorefromfak(uzo.text.lower())
                if tip == "stl" and uzo.text != None:
                    score += scorefromstil(uzo.text.lower())
            scores.append(score)
        score = min(max(scores + [0]),39) + len([sojlo for sojlo in senc_kalk_sojloj if sojlo <= len(sencoj)])
        return score

    outter_output : dict[str,int] = {} 
    tree = ET.fromstring(xml)
    radtexts : dict[str,str] = {}
    
    art = tree.find('art')
    if art == None:
        return {}
    kap = art.find('kap')
    if kap == None:
        return {}
    rad = kap.find('rad')
    if rad != None and rad.text != None:
        radtexts[''] = rad.text
        rootsfile.write(f'{rad.text}\n')
    for var in kap.iter('var'):
        varrad = var.find('kap/rad')
        if varrad != None:
            radtexts[varrad.get('var')] = varrad.text
            rootsfile.write(f'{varrad.text}\n')
    
    
    for drv in art.iter('drv'): #should I be using iter('drv') here?
        output : dict[str,int] = {} 
        extra_score = getscorefordrv(drv)
        kap = drv.find('kap')
        if kap != None:
            output |= {w:(p + extra_score) for w,p in getwordsfromkap(kap,radtexts).items()}

        for verbi in [w for w in output.keys() if len(w) > 0 and w[-1] == 'i']: # we should really ensure that the i isn't part of a gramatical word 
            try:
                verb = verbi[:-1]
                output[verb + 'us'] = 30
                output[verb + 'u'] = 30
                for v in ['i','a','o']:
                    output[verb + v + 's'] = 30
                    for fin in ['a','o','']:
                        pass
                        #output[verb + v + 'nt' + fin] = 40 + extra_score
                        #output[verb + v +  't' + fin] = 30 + extra_score # 30 because the verb might not be transitive. todo check for trans. in the file. also some verbs don't very sensible at constructions as they concern results and/or lack duration
            except:
                pass

        for radtext in radtexts.values():
            if radtext + "o" in output.keys() and output.get(radtext,-1) < 50 + extra_score:
                output[radtext] = 50 + extra_score
                #output[radtext + "on"] = 35 + extra_score# might not be be something that appears often as the object 
                #output[radtext + 'oj'] = 35 + extra_score# might not be something that apperas often in plural
                #output[radtext + "ojn"] = 30 + extra_score# see above

        # todo if theres an adjective ending we could throw on igi and iĝi

        for ending in ["a","e","i","o"]:
            pass
            #output[radtext + ending] = output.get(radtext + ending,30) # 30 cause we have no idea what this means
        
        for w in output:
            outter_output[w] = max(output[w],outter_output.get(w,output[w]))

    # todo add versions without hyphens
    outter_output |= {w.replace('-',''):output[w] for w in output.keys() if '-' in w}
    # make versions without any nonalpha chars
    outter_output |= {''.join([c for c in w if c.isalpha()]):output[w] for w in output.keys() if len([c for c in w if c.isalpha()]) > 0}
    return outter_output



def main():
    outfile = open("./vortlisto.dict","w",encoding='utf8')
    dir = os.fsencode("./revo")
    rootsfile = open('./roots.txt','w',encoding='utf8')
    for filebytes in os.listdir(dir):
        filename = os.fsdecode(filebytes)
        if not os.path.isfile('revo/' + filename): 
            continue
        file = open("revo/" + filename,"r",encoding='utf8')
        filetext = file.read()
        filetext = removeallentities(replacehats(filetext))
        wordlist = getwordsfromxml(filetext,rootsfile)
        for word in wordlist.keys():
            wordspaceless = ''.join(word.split())
            if len(wordspaceless) > 0:
                outfile.write(wordspaceless + f";{wordlist[word]}\n") #todo make one big dict with maximized values then write after
        file.close()
    outfile.close()


main()
