#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs


class Entry(object):

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.attrs = {}

    def __str__(self):
        output = "%s:%s {\n" % (self.name, self.parent)
        for attr in self.attrs:
            output += "%s = %s\n" % (self.attrs.get(attr), attr)
        output += "\n}"
        return output.encode("utf8")

class WrapFeatures(object):
    def __init__(self):
        self.attrs = {}
        # self.otherstuff = otherstuff
    def __str__(self):
        output = "{"
        for attr in self.attrs:
            output += "%s = %s\n" %(attr, self.attrs.get(attr))
        # output += "%s" %self.otherstuff
        output += "}"
        return output

### Structure:
# 1. treure totes les paraules d'acoranet-es.xml + features
# 2. per cada word obrir el seu fitxer word.lex.xml
# 3. en obrir el fitxer, extreure cada una de les seves features
# 4. adjuntar el conjunt de features de cada fitxer amb el verb corresponent
# 5. en cas que no hi hagi verb a ancoranet-es, afegir-lo a continuació

# fets: 1, 2,

# obrim el fitxer ancoranet-es.xml (codificant-lo a UTF8)

# ancoranet_es = ET.parse(unicode('../OriginalFiles/ancoranet-es.xml', errors='replace'))

ancoranet_es = ET.parse(codecs.open('../OriginalFiles/ancoranet-es.xml', encoding="utf8"))


# generem la root:
root_ancoranet = ancoranet_es.getroot()

props = ['anc_vtype', 'pbcls', 'pbID']



def ParseName(name_verb):
    ntilde = u'ñ'
    a_dieresi = u'ä'
    e_dieresi = u'ë'
    i_dieresi = u'ï'
    o_dieresi = u'ö'
    u_dieresi = u'ü'

    a_accent = u'á'
    e_accent = u'é'
    i_accent = u'í'
    o_accent = u'ó'
    u_accent = u'ú'

    guionet = '_'
    dar = 'dar_'
    hacer = 'hacer_'
    poner = 'poner_'
    tener = 'tener_'
    atenerse = 'atener_se'
    sacar = 'sacar_'

    # print name_verb
    n = name_verb.find(ntilde)
    a = name_verb.find(a_dieresi)
    e = name_verb.find(e_dieresi)
    i = name_verb.find(i_dieresi)
    o = name_verb.find(o_dieresi)
    u = name_verb.find(u_dieresi)

    a_ac = name_verb.find(a_accent)
    e_ac = name_verb.find(e_accent)
    i_ac = name_verb.find(i_accent)
    o_ac = name_verb.find(o_accent)
    u_ac = name_verb.find(u_accent)

    g = name_verb.find(guionet)
    d = name_verb.find(dar)
    h = name_verb.find(hacer)
    p = name_verb.find(poner)
    t = name_verb.find(tener)
    s = name_verb.find(sacar)
    # at = name_verb.find(atenerse)

    # print u
    list_name = list(name_verb)
    # print list_name
    # print(n)
    if n != -1:
        list_name[n] = 'n'
        # list_name[n + 1] = ''
    if a != -1:
        list_name[a] = 'a'
    if e != -1:
        list_name[e] = 'e'
    if i != -1:
        list_name[i] = 'i'
    if o != -1:
        list_name[o] = 'o'
    if u != -1:
        list_name[u] = u'u'

    if a_ac != -1:
        list_name[a_ac] = u'a'
    if e_ac != -1:
        list_name[e_ac] = u'e'
    if i_ac != -1:
        list_name[i_ac] = u'i'
    if o_ac != -1:
        list_name[o_ac] = u'o'
    if u_ac != -1:
        list_name[u_ac] = u'u'

    if g != -1 and d == -1 and h == -1 and p == -1 and t == -1 and s == -1:
        list_name[g] = u''
    #
    # if at != -1:
    #     list_name[at] = u'atenerse'

    name_verb = ''.join(list_name)

    return name_verb



with codecs.open('../OutputFiles/dictionary.txt','w') as fd:

    for link in root_ancoranet:
        lexid = link.get('ancoralexid')
        VB, name_verb, num, anc_vtype = lexid.split('.')
        # anc_vtype = ('anc_vtype = ' + anc_vtype)'../OriginalFiles/ancora-verb-es/'
        name = (VB + '_' + name_verb + '_' + '0' + num)
        spec = ('_' + VB + '_')

        bankID = link.get('propbankid')
        pbcls, pbID = bankID.split('.')

        try:
            name_file = ('../OriginalFiles/ancora-verb-es/' + name_verb + ".lex.xml")
            parsing = ET.parse(name_file)
            root_verblex = parsing.getroot()

        except:
            name_verb = ParseName(name_verb)
            name_file = ('../OriginalFiles/ancora-verb-es/' + name_verb + ".lex.xml")
            parsing = ET.parse(name_file)
            root_verblex = parsing.getroot()

        ancoranet_entry = Entry(name, spec)
        ancoranet_entry.attrs = {anc_vtype: props[0], pbcls : props[1], pbID: props[2]}

        fd.write(str(ancoranet_entry))

fd.close()

