import io
import xml.etree.ElementTree as ET
import os
import re
import itertools
import utililoj

def scorefromstil(stil):
    mapping = {
        'fraz': 10, # la senco estas frazaĵo mem, kiel havi aferon kun
        'fig': 10,
        'vulg': -100, # malfeliĉe temas pri familieca eldonaĵo, do ni devas savi tion por postvespera programo
        'rar': 5, # kelkaj raraj vortoj estas bona afero
        'poe': 10, # ne multaj artikoloj havas tion, sed ili ĉiuj estas bonaj
        'ark': -10,
        'evi': -100,
        'komune': 5,
        'neo': 0, # mi ŝatas, sed mi ne volas plioftigi ilin, se ili venas ili venas
    }
    return mapping.get(stil,0)

def scorefromfak(fak):
    # la granda celo estas ne uzi
    # tro da tre fakaj vortoj
    # precize tiujn de latina origino
    # kiuj ne havas nacilingvan komunanan
    # tradukon

    # baze:
    # regiliaj aferoj bonas
    # artaj aferoj bonas
    # teknikaj aŭ inĝenieraj sciencoj malbonas
    # iu ajn kategorio kun multege da nomoj malbonas

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
        'bak':  -2, #bakteriologio, suprize malmulte da tro-fakaj vortoj
        'bela': -1, #belartoj
        'bele': -1, #beletro
        'bib':  -5, #biblio
        'bio':  -5, #biologio
        'bot': -10, #botaniko
        'bud':   2, #budhismo
        'ekon': -2, #ekonomiko
        'ekol':  1, #ekologio
        'ele':  -5, #elektro
        'elet': -5, #elektrotekniko
        'esp':  15, #esperantismo
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
        'isl':   2, #islamo
        'jur':  -5, #juro
        'kal':  -1, #kalendaro
        'kat':   1, #katolikismo
        'kem': -10, #kemio
        'kin':   1, #kinoarto
        'kir':   0, #kirurgio
        'komp': -5, #komputiko
        'kon':  -5, #konstrutekniko
        'kri':   0, #kristanismo
        'kui':  -1, #kuirarto
        'lin':   0, #lingvistiko
        'mar':  -5, #maraferoj
        'mas':  -3, #maŝinoj
        'mat':  -9, #matematiko
        'mah':   0, #materialismo historia
        'med': -10, #medicino
        'met':  -1, #meteologio
        'mil':  -5, #militaferoj
        'min': -10, #mineralogio
        'mit':   2, #mitologio
        'muz': -10, #muziko
        'nom': -10, #nomoj
        'pal':  -1, #paleontologio
        'ped':  -5, #pedagogio
        'pers':-10, #personoj
        'poe':  -1, #poetiko mi ŝatus havi pli altan poentaron, sed ĝi ja estas faka
        'pol': -10, #politiko (landnomoj)
        'posx': -1, #poŝto
        'pra':   0, #prahistorio
        'psi':  -1, #psikologio
        'rad':   0, #radiofonio
        'rel':   1, #religioj
        'ret':   0, #interreto
        'sci':   1, #sciencoj, sufiĉe nefaka
        'spo':   2, #sporto kaj ludoj
        'shi':  -3, #ŝipkonstruado navigado
        'tea':   2, #teatro
        'tek':  -4, #teksindustrio
        'tel':  -3, #telekomunikoj
        'tip':   1, #presarto, libroj
        'tra':   1, #trafiko
        'zoo': -10, #zoologio
    }
    return mapping.get(fak,0)

def getwordsfromxml(tree : ET.Element, rootsfile : io.TextIOWrapper) -> dict[str,int]:
    """ Eltiras uzeblajn vortojn el xml arbo kaj redonas mapo de vorto al poentaro
    Aldone, elskribos radikojn al rootsfile.
    """
    def getwordsfromkap(kap :ET.Element, radiko : dict[str,str]) -> dict[str,int]:
        """
        Essence, ĉi-tiu funkcio anstataŭigas la tildojn per radikoj. Ĝi iome komplikiĝas pro
        la fakto ke povas esti alternitivaj literumoj kaj en la radiko mem kaj en la <kap> elemento.
        """
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
        """
        Kalkuli la baza poentaro de unu senco de iu radikoj.
        """
        sencoj = list(drv.iter('snc')) 
        senc_kalk_sojloj = [2,3,5,8,13]
        scores = []
        drv_uzoj = []
        for child in drv:
            if child.tag == "uzo":
                drv_uzoj.append(child)
        
        for snc in sencoj:
            score = 0
            for uzo in list(snc.iter('uzo')) + drv_uzoj:
                tip = uzo.get('tip')
                if tip == "fak" and uzo.text != None:
                    score += scorefromfak(uzo.text.lower())
                if tip == "stl" and uzo.text != None:
                    score += scorefromstil(uzo.text.lower()) # investigate: letala scored 50, but it should have got the -50 hit from stl = evi
            scores.append(score)
        score = min(max(scores + [-50]),39) + len([sojlo for sojlo in senc_kalk_sojloj if sojlo <= len(sencoj)])
        return score

    outter_output : dict[str,int] = {} 
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
            varval = varrad.get("var")
            if varval != None and varrad.text != None:
                radtexts[varval] = varrad.text
                rootsfile.write(f'{varrad.text}\n')
    
    
    for drv in art.iter('drv'): 
        output : dict[str,int] = {} 
        extra_score = getscorefordrv(drv)
        kap = drv.find('kap')
        if kap != None:
            # Ĉi-tie ni trovas la vortarajn terminojn
            output |= {w:(p + extra_score) for w,p in getwordsfromkap(kap,radtexts).items()}

        # jen ni vidas ĉu la drv estas verbo
        sncs = drv.iter('snc')
        gras = [gra for gra in drv.iter('gra')] + [gra for snc in sncs for gra in snc.iter('gra')]
        vspecs = [vspec for gra in gras for vspec in gra.iter('vspec')]
        # ne traktu sonimitoj kiel verboj
        vspecs = [vspec for vspec in vspecs if vspec != "sonimito"]
        # vspecs estas ajna etikedo kiu indikas ke nia drv estas verbsenca
        if len(vspecs) > 0:
            for radtext in radtexts.values():
                if radtext != None and radtext != "":
                    output[radtext + 'us'] = 30
                    output[radtext + 'u']  = 19
                    output[radtext + 'is'] = 30
                    output[radtext + 'as'] = 35
                    output[radtext + 'os'] = 30
            # se ne volus, ni povus aldoni igi/iĝi kontrolante la vpsec-on por ntr/tr/x

        for radtext in radtexts.values():
            if radtext + "o" in output.keys() and output.get(radtext,-1) < 50 + extra_score:
                output[radtext] = 50 + extra_score

        # todo if theres an adjective ending we could throw on igi and iĝi
        
        for w in output:
            outter_output[w] = max(output[w],outter_output.get(w,output[w]))

    # todo add versions without hyphens
    outter_output |= {w.replace('-',''):output[w] for w in output.keys() if '-' in w}
    # make versions without any nonalpha chars
    outter_output |= {''.join([c for c in w if c.isalpha()]):output[w] for w in output.keys() if len([c for c in w if c.isalpha()]) > 0}
    return outter_output

def main():
    outfile = open("./artefaktoj/vortlisto.dict","w",encoding='utf8')
    dir = os.fsencode("./font_datumoj/revo")
    rootsfile = open('./artefaktoj/roots.txt','w',encoding='utf8')
    for filebytes in os.listdir(dir):
        filename = os.fsdecode(filebytes)
        if not os.path.isfile('./font_datumoj/revo/' + filename): 
            continue
        file = open("./font_datumoj/revo/" + filename,"r",encoding='utf8')
        filetext = file.read()
        filetext = utililoj.tondi_xml_entoj(utililoj.konverti_xml_ĉapelojn(filetext))
        wordlist = getwordsfromxml(ET.fromstring(filetext),rootsfile)
        for word in wordlist.keys():
            wordspaceless = ''.join(word.split())
            if len(wordspaceless) > 0:
                outfile.write(wordspaceless + f";{wordlist[word]}\n") #todo make one big dict with maximized values then write after
        file.close()
    outfile.close()


main()
