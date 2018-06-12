#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs
import glob


class Sense(object):
    def __init__(self):
        self.lemma = None
        self.type = None
        self.id = None
        self.denotation = None
        self.lexicalized = None
        self.origin = None
        self.synset = None
        self.parent = None
        self.frames = []
        self.unaxifra = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def __str__(self):
        if self.id in self.unaxifra:
            output = "\"%s_NN_0%s\":_%s_{\n" %(self.lemma, self.id, self.parent)
        else:
            output = "\"%s_NN_%s\":_%s_{\n" % (self.lemma, self.id, self.parent)

        output += "\tanc_sense = \"%s\"\n" % self.id
        output += "\tlemma = \"%s\"\n" % self.lemma
        output += "\tanc_vtype = \"%s\"\n" % self.type
        output += "\tdenotation = \"%s\"\n" % self.denotation
        output += "\tlexicalized = \"%s\"\n" % self.lexicalized

        verb, verb_lemma, verb_sense = self.origin.split('.')

        output += "\torigin = \"%s_VB_0%s\"\n" % (verb_lemma, verb_sense)
        output += "\tsynset = \"%s\"\n" % self.synset
        for frame in self.frames:
            output += "%s\n" % frame

        return output.encode("utf8")



class Frame(object):
    def __init__(self, appearsinplural, type):
        self.appearsinplural = appearsinplural
        self.type = type
        self.arguments = []
        self.specifiers = []

    def __str__(self):
        output = "\tplural = \"%s\"\n" % self.appearsinplural
        output += "\ttype = \"%s\"\n" % self.type

        for argument in self.arguments:
            output += "%s" %argument
        for specifier in self.specifiers:
            output += "%s" %specifier

        return output

class Argument(object):
    def __init__(self, arg, role):
        self.arg = arg
        self.role = role
        self.constituents = []
        self.count = 0


    def __str__(self):

        output = "\t\targ = \"%s\"{\n" % self.arg
        output += "\t\t\tanc_theme = \"%s\"\n" % self.role

        for constituent in self.constituents:
            output += "%s" % constituent

        output += "\t\t}\n"
        return output

class Constituent(object):
    def __init__(self, prep, type):
        self.prep = prep
        self.type = type
    def __str__(self):
        output = "\t\t\tanc_prep  = \"%s\"\n" % self.prep
        output += "\t\t\tanc_type  = \"%s\"\n" % self.type
        return output

class Specifiers(object):
    def __init__(self):
        self.constituents= []
    def __str__(self):
        output = ""
        for constituent in self.constituents:
            output += "%s" % constituent
        return output

class Constituents_Specifiers(object):
    def __init__(self, postype, type):
        self.postype = postype
        self.type = type
    def __str__(self):
        output = "\t\t\tpostype = %s \n" %self.postype
        output += "\t\t\ttype = %s\n" %self.type
        return output


def getRoot():
    path = '../OriginalFiles/ancora-noun-es/*.lex.xml'
    files = glob.glob(path)
    root_lex = []
    for name in files:
        verb_lex = ET.parse(name)
        root_lex.append(verb_lex.getroot())
    return root_lex


arg_map = {"arg0": "I", "arg1": "I", "arg2": "II", "arg3": "III", "arg4": "IV", "argM": "M%d", "arrgM": "M%d",
           "arm": "M%d", "argL": "argL", "aer2": "aer2", "arg": "arg"}

def getSenses(root_lex):
    lemma = root_lex.get('lemma')
    type = root_lex.get('type')
    senses = []
    for sense_node in root_lex.findall('sense'):
        id = sense_node.get('id')
        sense_obj = Sense()
        sense_obj.lemma = lemma
        sense_obj.type = type
        sense_obj.id = id
        sense_obj.denotation = sense_node.get('denotation')
        sense_obj.lexicalized = sense_node.get('lexicalized')
        sense_obj.origin = sense_node.get('originlink')
        sense_obj.synset = sense_node.get('wordnetsynset')

        for frame_node in sense_node.iter('frame'):
            plural = frame_node.get('appearsinplural')
            frame_type = frame_node.get('type')
            frame_obj = Frame(plural, frame_type)
            count = 0

            if frame_type == 'default':
                for argument_node in frame_node.iter('argument'):
                    arg = argument_node.get('argument')
                    role = argument_node.get('thematicrole')

                    if arg is not None:
                        arg_name = arg_map[arg]
                        if arg_name.startswith("M"):
                            arg_name = arg_name % count
                            count += 1

                        argument_obj = Argument(arg_name, role)

                        frame_obj.arguments.append(argument_obj)

                        for constituent_node in argument_node.iter('constituent'):
                            prep = constituent_node.get('preposition')
                            const_type = constituent_node.get('type')
                            constituent_obj = Constituent(prep, const_type)

                            argument_obj.constituents.append(constituent_obj)
                for specifier_node in frame_node.iter('specifiers'):
                    specifier_obj = Specifiers()
                    for constituent_node in specifier_node.iter('constituent'):
                        postype = constituent_node.get('postype')
                        type_spec = constituent_node.get('type')

                        constituent_spec_obj = Constituents_Specifiers(postype, type_spec)
                        specifier_obj.constituents.append(constituent_spec_obj)
                    frame_obj.specifiers.append(specifier_obj)

                sense_obj.frames.append(frame_obj)

        senses.append(sense_obj)

    return senses

def writeOpening(filename):
    with codecs.open(filename, 'w', encoding="utf8") as fd:
        fd.write("lexiconAncora{\n")
    fd.close()

def writeEnding(filename):
    with codecs.open(filename, 'a', encoding="utf8") as fd:
        fd.write("}\n")
    fd.close()

def writeSenses(filename,senses):
    with codecs.open(filename, 'a', encoding="utf8") as fd:
        for sense in senses:
            sense_str = str(sense)
            fd.write(sense_str.decode("utf8"))
    fd.close()



def main():
    filename = "../OutputFiles/AncoraDict_nouns.dic"
    writeOpening(filename)
    root_lex = getRoot()
    for root in root_lex:
        senses = getSenses(root)
        writeSenses(filename, senses)
    writeEnding(filename)

if __name__ == "__main__":
    main()