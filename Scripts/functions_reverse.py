#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs
import sys
import glob
import errno

class Entry(object):
    def __init__(self):
        self.ancoralex_item = None
        self.pbcls = None
        self.pbId = None
        self.name = None
        self.sense = None
    def __str__(self):
        output = "%s" %self.pbcls
        output += "%s" % self.pbId

        return output


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
        output = "%s\n" % self.prep

        return output

def getSenses(root_lex):
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

def parseAncoranet(root_ancoranet):

    mapping = {}
    for link in root_ancoranet.findall('link'):
        entry = Entry()
        ancoralex_item = link.get('ancoralexid')
        entry.ancoralex_item = ancoralex_item
        verb_,lemma, sense, type = ancoralex_item.split('.')
        entry.name = lemma
        entry.sense = sense

        map_info = lemma+"_VB_0"+sense

        if type != 'passive':
            propbankid = link.get('propbankid')
            pblcs, pbId = propbankid.split('.')

            entry.pbcls = pblcs
            entry.pbId = pbId

            dict1 = {map_info:[entry.pbcls, entry.pbId] }
            mapping.update(dict1)

    return mapping




def mergeFiles(root_ancoranet):
    path = '../OriginalFiles/ancora-verb-es/*.lex.xml'

    files = glob.glob(path)
    for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.
        # try:
        verb_lex = ET.parse(name)
        root_lex = verb_lex.getroot()

        senses = getSenses(root_lex)

        with codecs.open("../OutputFiles/ReverseDict.txt",'a', encoding="utf8") as fd:
           for sense in senses:
               if sense.type != "passive":
                   if sense.type == "verb":
                       abbrv = "VB"
                   # if sense.type == "noun":
                   #     abbrv = "NN"
                   else:
                       abbrv = "VB"

                   title = "%s_%s_0%s" % (sense.lemma, abbrv, sense.id)
                   print "\"%s_%s_0%s\":_%s_ {\n" % (sense.lemma, abbrv, sense.id, abbrv)
                   fd.write("\"%s_%s_0%s\":_%s_ {\n" % (sense.lemma, abbrv, sense.id, abbrv))

                   print "\tentryId = \"%s\"\n" % '?'
                   fd.write("\tentryId = \"%s\"\n" % '?')
                   print "\tlemma = \"%s\"\n" % sense.lemma
                   fd.write("\tlemma = \"%s\"\n" % sense.lemma)
                   print "\tanc_sense = \"%s\"\n" % sense.id
                   fd.write("\tanc_sense = \"%s\"\n" % sense.id)

                   if sense.type == "verb":
                       anc_vtype = "default"
                   else:
                       anc_vtype = sense.type

                   print"\tanc_vtype = \"%s\"\n" % anc_vtype
                   fd.write("\tanc_vtype = \"%s\"\n" % anc_vtype)

                   mapping = parseAncoranet(root_ancoranet)

                   try:
                       pb = mapping[title]
                       pbcls = pb[0]
                       pbId = pb[1]
                       print "\t %s_VB_%s{\n" %(pbcls, pbId)
                       print "\t\t pbcls = %s \n" %pbcls
                       print "\t\t pbId = %s \n" %pbId

                       fd.write("\t %s_VB_%s{\n" %(pbcls, pbId))
                       fd.write("\t\t pbcls = %s \n" %pbcls)
                       fd.write("\t\t pbId = %s \n" %pbId)
                       fd.write("\t}\n")
                   except:
                       print None

                   for frame in sense.frames:

                        print "\tanc_lss = \"%s\"\n" % frame.lss
                        fd.write("\tanc_lss = \"%s\"\n" % frame.lss)



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




def main():
    ancoranet = ET.parse("../OriginalFiles/ancoranet-es.xml")
    root_ancoranet = ancoranet.getroot()
    mergeFiles(root_ancoranet)

main()
