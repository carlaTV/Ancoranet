#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs
import glob
import string


class Sense(object):
    def __init__(self):
        self.lemma = None
        self.id = None
        self.cousin = None
        self.denotation = None
        self.lexicalized = None
        self.verb_lemma = None
        self.verb_sense = None
        self.synset = None
        self.frames = []
        self.unaxifra = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.examples = []
        self.extArg = None
        self.lextype = None
        self.collocation = None
        self.framenumber = None

    def __str__(self):
        if self.framenumber:
            if self.id in self.unaxifra:
                if self.extArg == True:
                    output = "\"%s_NN_0%s_%s\":_nounExtArg_{\n" % (self.lemma, self.id, self.framenumber)
                else:
                    output = "\"%s_NN_0%s_%s\":_noun_{\n" % (self.lemma, self.id, self.framenumber)
            else:
                if self.extArg == True:
                    output = "\"%s_NN_%s_%s\":_nounExtArg_{\n" % (self.lemma, self.id)
                else:
                    output = "\"%s_NN_%s_%s\":_noun_{\n" % (self.lemma, self.id)
        else:
            if self.id in self.unaxifra:
                if self.extArg == True:
                    output = "\"%s_NN_0%s\":_nounExtArg_{\n" % (self.lemma, self.id)
                else:
                    output = "\"%s_NN_0%s\":_noun_{\n" % (self.lemma, self.id)
            else:
                if self.extArg == True:
                    output = "\"%s_NN_%s\":_nounExtArg_{\n" % (self.lemma, self.id)
                else:
                    output = "\"%s_NN_%s\":_noun_{\n" % (self.lemma, self.id)
        output += "\tanc_sense = \"%s\"\n" % self.id
        output += "\tanc_cousin = \"%s\"\n" % self.cousin
        output += "\tlemma = \"%s\"\n" % self.lemma
        # output += "\tanc_type = \"%s\"\n" % self.type
        output += "\tanc_denotation = \"%s\"\n" % self.denotation
        output += "\tanc_lexicalized = \"%s\"\n" % self.lexicalized
        if self.collocation:
            output += "\tanc_lextype = \"%s\"\n" % self.lextype
            output += "\tanc_alternativelemma = \"%s\"\n" % self.collocation
        output += "\tanc_originalVerb = \"%s_VB_0%s\"\n" % (self.verb_lemma, self.verb_sense)
        if '+' in self.synset:
            synsets = self.synset.split('+')
            for syn in synsets:
                output += "\twnet = \"%s\"\n" % syn
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
        self.plural = None
        self.arguments = []
        self.specifiers = []

    def __str__(self):
        output = "\tanc_diathesis = \"%s\"\n" % self.type
        output += "\tanc_plural = \"%s\"\n" % self.plural
        if self.arguments:
            output += "\tgp = { \n"
            for argument in self.arguments:
                output += "%s" % argument
            if self.specifiers:
                for specifier in self.specifiers:
                    output += "%s" % specifier
                output += "\t} \n"
            else:
                output += "\t} \n"
        else:
            if self.specifiers:
                for specifier in self.specifiers:
                    output += "%s" % specifier
            else:
                output += ""
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


class Constituent_Argument(object):
    def __init__(self, prep):
        self.prep = prep

    def __str__(self):
        output = "\t\t\tprep = \"%s\"\n" % self.prep
        return output


class Specifiers(object):
    def __init__(self):
        self.constituents = []

    def __str__(self):
        output = ""
        if self.constituents:
            for constituent in self.constituents:
                output += "%s" % constituent
            # output += "\t\t}\n"
        return output


class Constituents_Specifiers(object):
    def __init__(self, postype, type):
        self.postype = postype
        self.type = type

    def __str__(self):
        if self.postype is not None:
            output = "\t\tspecifiers = \"%s(%s)\" \n" % (self.type, self.postype)
        else:
            output = "\t\tspecifiers = \"%s\" \n" % self.type
        return output


class Examples(object):
    def __init__(self):
        self.examples = []

    def __str__(self):
        output = "\texamples = {\n"
        for ex in self.examples:
            output += "\t\texample = \"%s\"\n" % ex
        output += '\t}\n'
        return output


def getRoot():
    path = 'Resources/OriginalFiles/ancora-noun-es/*.lex.xml'
    # path = '../OriginalFiles/descenso_02.lex.xml'
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

alphabet = list(string.ascii_lowercase)
numbers = range(1, 27)
alpha_numeric = dict(zip(numbers, sorted(alphabet)))


def getSenses(sense_node, lemma):
    id = sense_node.get('id')
    sense_obj = Sense()
    sense_obj.lemma = lemma
    sense_obj.id = id
    sense_obj.cousin = sense_node.get('cousin')
    sense_obj.denotation = sense_node.get('denotation')
    sense_obj.lexicalized = sense_node.get('lexicalized')
    if sense_obj.lexicalized == 'yes':
        sense_obj.lextype = sense_node.get('lexicalizationtype')
        sense_obj.collocation = sense_node.get('alternativelemma')
    sense_obj.synset = sense_node.get('wordnetsynset')
    origin = sense_node.get('originlink')

    if origin is not None:
        verb_, sense_obj.verb_lemma, sense_obj.verb_sense = origin.split('.')

    return sense_obj


def checkFrames(sense_node):
    check = sense_node.get('frame').attrib
    print check


def getFrames(frame_node, count_sense_iter, sense_obj):
    frame_type = frame_node.get('type')
    frame_obj = Frame(frame_type)
    frame_obj.plural = frame_node.get('appearsinplural')
    # if frame_type == 'default':
    for argument_node in frame_node:
        count = 0
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
                    if prep is not None:
                        constituent_obj = Constituent_Argument(prep)
                        argument_obj.constituents.append(constituent_obj)

    for specifier_node in frame_node.iter('specifiers'):
        specifier_obj = Specifiers()
        frame_obj.specifiers.append(specifier_obj)
        for constituent_node in specifier_node.iter('constituent'):
            postype = constituent_node.get('postype')
            type_spec = constituent_node.get('type')

            constituent_spec_obj = Constituents_Specifiers(postype, type_spec)
            specifier_obj.constituents.append(constituent_spec_obj)
    return frame_obj


def getExamples(frame_node):
    example_obj = Examples()
    count_ex = 0
    ex = ''
    for example in frame_node.find('examples'):
        if example.text is not None:
            ex += example.text
        else:
            ex += ''
        argset = example.find('argset')
        for arg in argset:
            if arg.tag == 'argument' and 'thematicrole' in arg.attrib:
                them_role = arg.attrib['thematicrole']
                ex += '[' + arg.text + ']-' + them_role.upper() + ' '
            else:
                ex += arg.text + ' '
                if arg.tail:
                    ex += arg.tail + ''
        ex += argset.tail
        example = ex.replace('"', '\\"')
        count_ex += 1
        example_obj.examples.append(example)
        ex = ''
        if count_ex == 10:
            break
    return example_obj


def parseXML(root_lex):
    lemma = root_lex.get('lemma')
    senses = []
    for sense_node in root_lex.findall('sense'):
        count_sense_iter = 0
        # sense_obj = getSenses(sense_node,lemma)
        frames = sense_node.getchildren()
        if len(frames) > 1:
            countframes = 0
        else:
            countframes = None
        for frame_node in sense_node:
            sense_obj = getSenses(sense_node, lemma)
            frame_obj = getFrames(frame_node, count_sense_iter, sense_obj)
            # print lemma
            example_obj = getExamples(frame_node)
            if countframes is not None:
                countframes += 1
                sense_obj.framenumber = alpha_numeric[countframes]
            sense_obj.frames.append(frame_obj)
            sense_obj.examples.append(example_obj)
            senses.append(sense_obj)
    return senses

# def writeOpening(filename):
#     with codecs.open(filename, 'w', encoding="utf8") as fd:
#         fd.write("lexiconAncora{\n")
#     fd.close()
#
# def writeEnding(filename):
#     with codecs.open(filename, 'a', encoding="utf8") as fd:
#         fd.write("}\n")
#     fd.close()
#
# def writeSenses(filename,senses):
#     with codecs.open(filename, 'a', encoding="utf8") as fd:
#         for sense in senses:
#             sense_str = str(sense)
#             fd.write(sense_str.decode("utf8"))
#     fd.close()
