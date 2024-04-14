import re

def konverti_xml_ĉapelojn(s : str) -> str:
    """ Anstataŭigi xml-ajn simbolojn kiuj reprezentas ĉapelitajn literojn al la ĝustajn literojn.
    """
    hatpairs = [('s','ŝ'),('g','ĝ'),('c','ĉ'),('j','ĵ'),('h','ĥ'),('S','Ŝ'),('G','Ĝ'),('C','Ĉ'),('J','Ĵ'),('H','Ĥ')]
    for pair in hatpairs:
        s = s.replace('&' + pair[0] + 'circ;',pair[1])
    s = s.replace('&ubreve;','ŭ').replace('&Ubreve;','Ŭ')
    return s


def tondi_xml_entoj(s : str) -> str:
    return re.sub('&.*?;','',s)