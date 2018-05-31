#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs
import sys
import glob
import errno

class Sense(object):
    def __init__(self, id, lemma, type):
        self.lemma = lemma
        self.id = id
        self.type = type
        self.frames = []

    def __str__(self):
        output = "\tlemma = %s\n" % self.lemma
        output = "\ttype = %s\n" % self.type
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

def getSenses(root_lex):

    # file_lex = ET.parse(lex_filename)
    # root_lex = file_lex.getroot()

    lemma = root_lex.get('lemma')
    type = root_lex.get('type')

    senses = []
    for sense_node in root_lex.findall('sense'):
        id = sense_node.get('id')
        sense_obj = Sense(id, lemma, type)

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

def readFiles():
    path = '../OriginalFiles/ancora-verb-es/*.lex.xml'

    files = glob.glob(path)
    for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        # try:
        verb_lex = ET.parse(name)
        root_lex = verb_lex.getroot()

        senses = getSenses(root_lex)

        # with open("../OutputFiles/ReverseDict.txt",'a') as fd:
        with codecs.open("../OutputFiles/ReverseDict.txt",'a', encoding="utf8") as fd:
           for sense in senses:
               if sense.type != "passive":
                   if sense.type == "verb":
                       abbrv = "VB"
                   # if sense.type == "noun":
                   #     abbrv = "NN"
                   else:
                       abbrv = "VB"

                   print "\"%s_%s_0%s\":_%s_ {\n" % (sense.lemma, abbrv, sense.id, abbrv)
                   fd.write("\"%s_%s_0%s\":_%s_ {\n" % (sense.lemma, abbrv, sense.id, abbrv))

                   print "\tentryId = \"%s\"\n" % '?'
                   fd.write("\tentryId = \"%s\"\n" % '?')
                   print "\tlemma = \"%s\"\n" % sense.lemma
                   fd.write("\tlemma = \"%s\"\n" % sense.lemma)
                   print "\tanc_sense = \"%s\"\n" % sense.id
                   fd.write("\tanc_sense = \"%s\"\n" % sense.id)

                   for frame in sense.frames:

                        # if entry.parent == 'verb':
                        #     abbrv = "VB"
                        # if entry.parent == 'noun':
                        #     abbrv = 'NN'
                        #
                        # if entry.propbankarg == "0":
                        #     parent = "VerbExtrArg"
                        # else:
                        #     parent = entry.parent
                        #
                        # print "\"%s_%s_0%s\":_%s_ {\n" % (entry.name, abbrv, sense.id, parent)
                        # fd.write("\"%s_%s_0%s\":_%s_ {\n" % (entry.name, abbrv, sense.id, parent))
                        # # sense_count += 1

                        # print "\tanc_vtype = \"%s\"\n" % entry.anc_vtype
                        # fd.write("\tanc_vtype = \"%s\"\n" % entry.anc_vtype)
                        print "\tanc_lss = \"%s\"\n" % frame.lss
                        fd.write("\tanc_lss = \"%s\"\n" % frame.lss)

                        # print "\t\"%s_%s_%s\" = {\n" % (entry.pbcls, abbrv, entry.pbID)
                        # fd.write("\"%s_%s_%s\" = {\n" % (entry.pbcls, abbrv, entry.pbID))
                        #
                        # print "\t\tpbcls = \"%s\"\n" % entry.pbcls
                        # fd.write("\t\tpbcls = \"%s\"\n" % entry.pbcls)
                        # print "\t\tpbID = \"%s\"\n" % entry.pbID
                        # fd.write("\t\tpbID = \"%s\"\n" % entry.pbID)
                        # print "\tpropbankarg = \"%s\"" % entry.propbankarg

                        print "\t}\n"
                        fd.write("}\n")

                        print "\tgp = {\n"
                        fd.write("\tgp = {\n")
                        count = 1
                        for argument in frame.arguments:

                            arg_name = arg_map[argument.arg]
                            if arg_name.startswith("M"):
                                arg_name = arg_name % count
                                count += 1

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


        # except IOError as exc:
        #     if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
        #         raise # Propagate other kinds of IOError.








def main():
    readFiles()

main()

#
# verb = ET.parse("../OriginalFiles/ancora-verb-es/abalanzar.lex.xml")
#
# root = verb.getroot()
#
# lex = root.get('lemma')
# #lemma = lex.get('lemma')
#
# print(lex)