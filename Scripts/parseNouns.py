#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs
import glob


class Sense(object):
    def __init__(self):
        self.lemma = None
        # self.type = None
        self.id = None
        self.denotation = None
        self.lexicalized = None
        self.verb_lemma = None
        self.verb_sense = None
        self.synset = None
        self.frames = []
        self.unaxifra = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.examples = []
        self.extArg = None

    def __str__(self):
        if self.id in self.unaxifra:
            if self.extArg == True:
                output = "\"%s_NN_0%s\":_nounExtArg_{\n" %(self.lemma, self.id)
            else:
                output = "\"%s_NN_0%s\":_noun_{\n" %(self.lemma, self.id)
        else:
            if self.extArg == True:
                output = "\"%s_NN_%s\":_nounExtArg_{\n" % (self.lemma, self.id)
            else:
                output = "\"%s_NN_%s\":_noun_{\n" % (self.lemma, self.id)
        output += "\tanc_sense = \"%s\"\n" % self.id
        output += "\tlemma = \"%s\"\n" % self.lemma
        # output += "\tanc_type = \"%s\"\n" % self.type
        output += "\tanc_denotation = \"%s\"\n" % self.denotation
        output += "\tanc_lexicalized = \"%s\"\n" % self.lexicalized

        output += "\tanc_originalVerb = \"%s_VB_0%s\"\n" % (self.verb_lemma, self.verb_sense)
        if '+' in self.synset:
            a = self.synset.replace('+','\"\n\t\t   \"')
            output += "\twnet = \"%s\"\n" % a
        else:
            output += "\twnet = \"%s\"\n" % self.synset
        for frame in self.frames:
            output += "%s\n" % frame
        for example in self.examples:
            output += "%s" % example
        output += "}\n\n"

        return output.encode("utf8")



class Frame(object):
    def __init__(self, type):
        self.type = type
        self.arguments = []
        self.specifiers = []
    def __str__(self):
        # output = "\ttype = \"%s\"\n" % self.type
        if self.arguments:
            output = "\tgp = { \n"
            for argument in self.arguments:
                output += "%s" %argument
        # if self.specifiers:
            for specifier in self.specifiers:
                output += "%s" %specifier
            output += "\t} \n"
        else:
            output = ""
        return output

class Argument(object):
    def __init__(self, arg, role):
        self.arg = arg
        self.role = role
        self.constituents = []
        self.count = 0
    def __str__(self):
        output = "\t\t%s = {\n" % self.arg
        output += "\t\t\tanc_theme = \"%s\"\n" % self.role
        for constituent in self.constituents:
            output += "%s" % constituent
        output += "\t\t}\n"
        return output

class Constituent(object):
    def __init__(self, prep):
        self.prep = prep
        # self.type = type
        # self.postype = postype
    def __str__(self):
        output = "\t\t\tanc_prep = \"%s\"\n" %self.prep
        # if self.postype is not None:
        #     output += "\t\t\tpostype = \" %s \"\n" %self.postype
        return output

class Specifiers(object):
    def __init__(self):
        self.constituents= []
    def __str__(self):
        output = ""
        for constituent in self.constituents:
            output += "%s" % constituent
        output += "\t\t}\n"
        return output

class Constituents_Specifiers(object):
    def __init__(self, postype, type):
        self.postype = postype
        self.type = type
    def __str__(self):
        output = ""
        if self.postype is not None:
            output = "\t\t\tspecifiers = \"%s(%s)\" \n" % (self.type, self.postype)
        return output

class Examples(object):
    def __init__(self):
        self.examples = []
    def __str__(self):
        # if self.examples:
        output = ""
        for ex in self.examples:
            output += "\texample = {\"%s\"}\n" % ex
        return output


def getRoot():
    path = '../OriginalFiles/ancora-noun-es/*.lex.xml'
    files = glob.glob(path)
    root_lex = []
    for name in sorted(files):
        verb_lex = ET.parse(name)
        root_lex.append(verb_lex.getroot())
    return root_lex

extarg_map = {"arg0": "I", "arg1": "II", "arg2": "III", "arg3": "IV", "arg4": "V", "argM": "M%d", "arrgM": "M%d",
           "arm": "M%d", "argL": "argL", "aer2": "aer2", "arg": "arg"}
arg_map = {"arg1": "I", "arg2": "II", "arg3": "III", "arg4": "IV", "argM": "M%d", "arrgM": "M%d",
           "arm": "M%d", "argL": "argL", "aer2": "aer2", "arg": "arg"}

def getSenses(root_lex):
    lemma = root_lex.get('lemma')
    type = root_lex.get('type')
    senses = []
    for sense_node in root_lex.findall('sense'):
        count_sense_iter = 0
        id = sense_node.get('id')
        sense_obj = Sense()
        sense_obj.lemma = lemma
        # sense_obj.type = type
        sense_obj.id = id
        sense_obj.denotation = sense_node.get('denotation')
        sense_obj.lexicalized = sense_node.get('lexicalized')
        sense_obj.synset = sense_node.get('wordnetsynset')

        origin = sense_node.get('originlink')

        if origin is not None:
            verb_, sense_obj.verb_lemma, sense_obj.verb_sense = origin.split('.')

        for frame_node in sense_node:
            frame_type = frame_node.get('type')
            frame_obj = Frame(frame_type)
            count = 0

            if frame_type == 'default':
                for argument_node in frame_node:
                    if argument_node.tag == 'argument':
                        arg = argument_node.get('argument')
                        role = argument_node.get('thematicrole')
                        if arg is not None:
                            if count_sense_iter == 0:
                                if arg == 'arg0':
                                    extArg = True
                                    sense_obj.extArg = True
                                else:
                                    extArg = False
                                    sense_obj.extArg = False
                            if count_sense_iter > 1:
                                pass
                            # else:
                            #     if extArg is not True:
                            #         extArg = False
                            #         sense_obj.extArg = False
                            #     else:
                            #         extArg
                            if extArg == True:
                                arg_name = extarg_map[arg]
                            else:
                                arg_name = arg_map[arg]
                            if arg_name.startswith("M"):
                                arg_name = arg_name % count
                                count += 1

                            argument_obj = Argument(arg_name, role)
                            count_sense_iter += 1

                            frame_obj.arguments.append(argument_obj)

                            for constituent_node in argument_node.iter('constituent'):
                                prep = constituent_node.get('preposition')
                                # type = constituent_node.get('type')
                                # postype = constituent_node.get('postype')
                                if prep is not None:
                                    constituent_obj = Constituent(prep)
                                    argument_obj.constituents.append(constituent_obj)

                for specifier_node in frame_node.iter('specifiers'):
                    specifier_obj = Specifiers()
                    frame_obj.specifiers.append(specifier_obj)
                    for constituent_node in specifier_node.iter('constituent'):
                        postype = constituent_node.get('postype')
                        type_spec = constituent_node.get('type')

                        constituent_spec_obj = Constituents_Specifiers(postype, type_spec)
                        specifier_obj.constituents.append(constituent_spec_obj)

                count_ex = 0
                example_obj = Examples()
                for example_node in frame_node.findall('examples'):
                    # if example_node is not None:
                    for ex in example_node.findall('example'):
                        if ex.text is not None:
                            example1 = ex.text.strip()
                            arg = ex.find('argset')
                            try:
                                spec = arg.find('specifier').text
                            except:
                                spec = ''
                            try:
                                head = arg.find('head').text
                            except:
                                head = ''
                            try:
                                argument = arg.find('argument').text
                            except:
                                argument = ''
                            example3 = arg.tail
                            example = example1+" "+spec+" "+head+" "+argument+" "+example3
                            count_ex += 1
                            example_obj.examples.append(example)
                            if count_ex == 10:
                                break

                sense_obj.frames.append(frame_obj)
                sense_obj.examples.append(example_obj)

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