#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs
import glob


class Sense(object):
    def __init__(self):
        self.lemma = None
        self.id = None
        self.type = None
        self.frames = []
        self.map_propbank = {}

    def __str__(self):
        title = "%s_VB_0%s" % (self.lemma, self.id)
        try:
            if self.map_propbank[str(title)] is True:
                parent = "VerbExtrArg"
            else:
                parent = "verb_else"
        except:
            parent = "verb"
        output = "\"%s_%s_%s\":_%s_{\n" %(self.lemma, self.id, self.type, parent)
        output += "\tanc_sense = %s\n" % self.id
        output += "\tlemma = %s\n" % self.lemma
        output += "\tanc_vtype = %s\n" % self.type
        for frame in self.frames:
            output += "%s\n" % frame

        return output.encode("utf8")

class Frame(object):
    def __init__(self, lss, type):
        self.lss = lss
        self.type = type
        self.arguments = []

    def __str__(self):
        output = "\tlss = %s\n" % self.lss
        output += "\ttype = %s\n" % self.type
        for argument in self.arguments:
            output += "%s\n" % argument
        output += "\t}\n"

        return output

class Argument(object):
    def __init__(self, arg, role, funct):
        self.arg = arg
        self.role = role
        self.funct = funct
        self.constituents = []
        self.count = 0

    def __str__(self):
        arg_map = {"arg0": "I", "arg1": "II", "arg2": "III", "arg3": "IV", "arg4": "V", "argM": "M%d", "arrgM": "M%d",
                   "arm": "M%d", "argL": "argL", "aer2": "aer2", "arg": "arg"}

        arg_name = arg_map[self.arg]
        if arg_name.startswith("M"):
            arg_name = arg_name % self.count
            self.count += 1

        output = "\t\targ = %s{\n" % arg_name
        output += "\t\t\tanc_theme = %s\n" % self.role
        output += "\t\t\tanc_funct = %s\n" % self.funct

        for constituent in self.constituents:
            output += "\t\t\tanc_prep  = %s\n" % constituent

        output += "\t\t{\n"
        return output

class Constituent(object):
    def __init__(self, prep):
        self.prep = prep
    def __str__(self):
        output = "%s" % self.prep

        return output

def getRoot():
    path = '../OriginalFiles/ancora-verb-es/*.lex.xml'
    files = glob.glob(path)
    root_lex = []
    for name in files:
        verb_lex = ET.parse(name)
        root_lex.append(verb_lex.getroot())
    return root_lex

def getSenses(root_lex):

    # unaxifra = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    lemma = root_lex.get('lemma')
    type = root_lex.get('type')
    senses = []
    for sense_node in root_lex.findall('sense'):
        id = sense_node.get('id')
        sense_obj = Sense()
        sense_obj.lemma = lemma
        sense_obj.type = type
        sense_obj.id = id

        for frame_node in sense_node.iter('frame'):
            lss = frame_node.get('lss')
            frame_type = frame_node.get('type')
            frame_obj = Frame(lss, frame_type)

            if frame_type == 'default':
                for argument_node in frame_node:
                    arg = argument_node.get('argument')
                    role = argument_node.get('thematicrole')
                    funct = argument_node.get('function')

                    if arg is not None:
                        argument_obj = Argument(arg, role, funct)

                        frame_obj.arguments.append(argument_obj)

                        for constituent_node in argument_node.iter('constituent'):
                            prep = constituent_node.get('preposition')
                            constituent_obj = Constituent(prep)

                            argument_obj.constituents.append(constituent_obj)

                sense_obj.frames.append(frame_obj)

        senses.append(sense_obj)

    return senses

def writeOpening():
    with codecs.open("../OutputFiles/test.dic", 'w', encoding="utf8") as fd:
        fd.write("lexiconAncora{\n")
    fd.close()

def writeEnding():
    with codecs.open("../OutputFiles/test.dic", 'a', encoding="utf8") as fd:
        fd.write("}\n")
    fd.close()

def writeSenses(senses):
    with codecs.open("../OutputFiles/test.dic", 'a', encoding="utf8") as fd:
        for sense in senses:
            try:
                fd.write(str(sense))
            except:
                print sense.lemma
    fd.close()

def getPropbankarg(root_ancoranet):
    iszero = False
    sense_obj = Sense()
    map_propbankarg = sense_obj.map_propbank
    for link in root_ancoranet.findall('link'):
        ancoralex_item = link.get('ancoralexid')
        verb_, lemma, sense, type = ancoralex_item.split('.')
        if type == 'default':
            for arglink in link:
                propbankarg = arglink.get('propbankarg')
                if propbankarg == "0":
                    iszero = True
                    break
                else:
                    iszero = False
        map_info = lemma + "_VB_0" + sense
        dict1 = {map_info: iszero}
        if map_info not in map_propbankarg.keys() and iszero == True:
            map_propbankarg.update(dict1)
        map_info = None
        iszero = False
    return map_propbankarg

def main():
    ancoranet = ET.parse("../OriginalFiles/ancoranet-es.xml")
    root_ancoranet = ancoranet.getroot()
    getPropbankarg(root_ancoranet)
    writeOpening()
    root_lex = getRoot()
    for root in root_lex:
        senses = getSenses(root)
        writeSenses(senses)
    writeEnding()
main()