#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs

class Entry(object):

    def __init__(self, name, parent, num):
        self.name = name
        self.parent = parent
        self.num = num
        self.anc_vtype = None
        self.pbcls = None
        self.pbID = None
        self.propbankarg = None

        self.attrs = {}

    def __str__(self):
        output = "%s:%s {\n" % (self.name, self.parent)

        output += "\tanc_vtype = %s\n" % self.anc_vtype
        output += "\tpbcls = %s\n" % self.pbcls
        output += "\tpbID = %s\n" % self.pbID

        output += "\tpropbankarg = %s\n" % self.propbankarg

        return output.encode("utf8")

class Sense(object):
    def __init__(self, id, lemma):
        self.lemma = lemma
        self.id = id
        self.frames = []

    def __str__(self):
        output = "\tlemma = %s\n" % self.lemma
        output += "\tid = %s\n" % self.id
        output += "\t{\n"
        for frame in self.frames:
            output += "%s\n" % frame
        output += "\t}\n"

        return output

class Frame(object):
    def __init__(self, lss, type):
        self.lss = lss
        self.type = type
        self.arguments = []

    def __str__(self):
        output = "\t\tlss = %s\n" % self.lss
        output += "\t\ttype = %s\n" % self.type
        output += "\t\t{\n"
        for argument in self.arguments:
            output += "%s\n" % argument
        output += "\t}\n"

        return output

class Argument(object):
    def __init__(self, arg, func, role):
        self.arg = arg
        self.func = func
        self.role = role

        self.constituents = []

    def __str__(self):
        output = "\t\t\targ = %s\n" % self.arg
        output += "\t\t\tfunction = %s\n" % self.func
        output += "\t\t\trole = %s\n" % self.role

        for constituent in self.constituents:
            output += "%s\n" % constituent
        return output

class Constituent(object):
    def __init__(self, prep):
        self.prep = prep
    def __str__(self):
        #output = "\t\t\tprep = %s\n" % self.prep
        output = "%s\n" % self.prep

        return output

## funcio que pilli els verbs d'acoranet_es

def getEntries(root):

    entries = []
    for link in root:

        lexid = link.get('ancoralexid')

        parent, name, num, anc_vtype = lexid.split('.')

        entry = Entry(name, parent, num)
        entry.anc_vtype = anc_vtype

        getAttributes(link, entry)

        getArgAncora(link, entry)

        entries.append(entry)

    return entries

def getAttributes(link, entry):

    bankID = link.get('propbankid')
    pbcls, pbID = bankID.split('.')

    entry.pbcls = pbcls
    entry.pbID = pbID

def getArgAncora(link, entry):
    for arglink in link:
        propbankarg = arglink.get('propbankarg')

        entry.propbankarg = propbankarg


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
    #atenerse = 'atener_se'
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

def getSenses(lex_filename):

    file_lex = ET.parse(lex_filename)
    root_lex = file_lex.getroot()

    lemma = root_lex.get('lemma')

    senses = []
    for sense_node in root_lex.findall('sense'):
        id = sense_node.get('id')
        sense_obj = Sense(id, lemma)

        for frame_node in sense_node.iter('frame'):
            lss = frame_node.get('lss')
            type = frame_node.get('type')
            frame_obj = Frame(lss, type)

            for argument_node in frame_node.iter('argument'):
                arg = argument_node.get('argument')
                func = argument_node.get('function')
                role = argument_node.get('thematicrole')
                argument_obj = Argument(arg, func, role)

                frame_obj.arguments.append(argument_obj)

                for constituent_node in argument_node.iter('constituent'):
                    prep = constituent_node.get('preposition')
                    constituent_obj = Constituent(prep)

                    argument_obj.constituents.append(constituent_obj)


            sense_obj.frames.append(frame_obj)

        senses.append(sense_obj)

    return senses

arg_map = {"arg0": "I", "arg1": "II", "arg2": "III", "arg3": "IV", "arg4": "V", "argM": "M%d","arrgM": "M%d" ,"arm": "M%d","argL":"argL", "aer2":"aer2", "arg":"arg"}

def getIndices(entries):

    #with open("../OutputFiles/MateDict.txt",'w') as fd:
    with codecs.open("../OutputFiles/MateDict.txt", 'w', encoding="utf8") as fd:
        for entry in entries:
            lex_name = ParseName(entry.name)
            lex_filename = '../OriginalFiles/ancora-verb-es/' + lex_name + ".lex.xml"

            #sense_count = 1
            senses = getSenses(lex_filename)
            for sense in senses:

                for frame in sense.frames:

                    if entry.parent == 'verb':
                        abbrv = "VB"
                    if entry.parent == 'noun':
                        abbrv = 'NN'

                    if entry.propbankarg == "0":
                        parent = "VerbExtrArg"
                    else:
                        parent = entry.parent


                    print "\"%s_%s_0%s\":_%s_ {\n" % (entry.name, abbrv, sense.id, parent)
                    fd.write("\"%s_%s_0%s\":_%s_ {\n" % (entry.name, abbrv, sense.id, parent))
                    #sense_count += 1

                    print "\tentryId = \"%s\"\n" % '?'
                    fd.write("\tentryId = \"%s\"\n" % '?')
                    print "\tlemma = \"%s\"\n" % sense.lemma
                    fd.write("\tlemma = \"%s\"\n" % sense.lemma)
                    print "\tanc_sense = \"%s\"\n" % sense.id
                    fd.write("\tanc_sense = \"%s\"\n" % sense.id)
                    print "\tanc_vtype = \"%s\"\n" % entry.anc_vtype
                    fd.write("\tanc_vtype = \"%s\"\n" % entry.anc_vtype)
                    print "\tanc_lss = \"%s\"\n" % frame.lss
                    fd.write("\tanc_lss = \"%s\"\n" % frame.lss)
                    print "\tpbcls = \"%s\"\n" % entry.pbcls
                    fd.write("\tpbcls = \"%s\"\n" % entry.pbcls)
                    print "\tpbID = \"%s\"\n" % entry.pbID
                    fd.write("\tpbID = \"%s\"\n" % entry.pbID)
                    #print "\tpropbankarg = \"%s\"" % entry.propbankarg

                    print "\tgp = {\n"
                    fd.write("\tgp = {\n")
                    count = 1
                    for argument in frame.arguments:

                        arg_name = arg_map[argument.arg]
                        if arg_name.startswith("M"):
                            arg_name = arg_name % count
                            count +=  1

                        print "\t\t%s = {\n" % arg_name
                        fd.write("\t\t%s = {\n" % arg_name)
                        print "\t\t\tanc_function = \"%s\"\n" % argument.func
                        fd.write("\t\t\tanc_function = \"%s\"\n" % argument.func)
                        print "\t\t\tanc_theme = \"%s\"\n" % argument.role
                        fd.write("\t\t\tanc_theme = \"%s\"\n" % argument.role)

                        for constituent in argument.constituents:
                            print "\t\t\tanc_prep = \"%s\"\n" % constituent
                            fd.write("\t\t\tanc_prep = \"%s\"\n" % constituent)
                            print "\t\t}\n"
                            fd.write("\t\t}\n")

                    print "\t}\n"
                    fd.write("\t}\n")

                    print "}\n"
                    fd.write("}\n")
    fd.close()

def main():

   # ancoranet = ET.parse(codecs.open('../OriginalFiles/ancoranet-es.xml', encoding="utf8"))
    ancoranet = ET.parse('../OriginalFiles/ancoranet-es.xml')
    root_ancoranet = ancoranet.getroot()

    entries = getEntries(root_ancoranet)
    getIndices(entries)



main()