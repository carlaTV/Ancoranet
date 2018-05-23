#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs

## funcio que pilli els verbs d'acoranet_es

def getNames(root):
    names = []
    for link in root:
        lexid = link.get('ancoralexid')
        VB, name_verb, num, anc_vtype = lexid.split('.')
        name = (VB + '_' + name_verb + '_' + '0' + num)
        spec = ('_' + VB + '_')

        names.append(name_verb)
    return names

def getAtrs(root):
    attributes = []
    for link in root:
        bankID = link.get('propbankid')
        pbcls, pbID = bankID.split('.')

        attributes.append(pbcls)
        attributes.append(pbID)
    return attributes
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
    echar = 'echar_'
    encontrar = 'encontrar_'
    estar = 'estar_'
    ir = 'ir_'
    llevar = 'llevar_'
    querer = 'querer_'
    valer = 'valer_'
    caer = 'caer_'

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
    ech = name_verb.find(echar)
    enc = name_verb.find(encontrar)
    est = name_verb.find(estar)
    ir_ = name_verb.find(ir)
    # at = name_verb.find(atenerse)
    ll = name_verb.find(llevar)
    q = name_verb.find(querer)
    v = name_verb.find(valer)
    c = name_verb.find(caer)

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

    if g != -1 and d == -1 and h == -1 \
        and p == -1 and t == -1 and s == -1 \
        and ech == -1 and enc == -1 and est == -1 \
        and ir_ == -1 and ll == -1 and q== -1 and v==-1\
        and c==-1:
        list_name[g] = u''
    #
    # if at != -1:
    #     list_name[at] = u'atenerse'

    name_verb = ''.join(list_name)

    return name_verb

def OpenFiles(names):
    name_files = []
    for name in range(0, len(names)):
        names[name] = ParseName(names[name])
        name_file = ('../OriginalFiles/ancora-verb-es/' + names[name] + ".lex.xml")
        name_files.append(name_file)
    return name_files

def Senses(names_files):
    senses = []
    for f in names_files:
        file_lex = ET.parse(f)
        root_lex = file_lex.getroot()
        for sense in root_lex:
            id = sense.get('id')
            senses.append(id)
    return senses



def main():
    ancoranet = ET.parse(codecs.open('../OriginalFiles/ancoranet-es.xml', encoding="utf8"))
    root_ancoranet = ancoranet.getroot()
    names = getNames(root_ancoranet)
    attrs = getAtrs(root_ancoranet)
    names_files = OpenFiles(names)
    senses = Senses(names_files)
    for i in range(0, len(senses)):
        print("sense = "+ senses[i])


main()