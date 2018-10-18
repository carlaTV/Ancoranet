#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs
import glob
import os

class Sense(object):
    def __init__(self):
        self.lemma = None
        self.id = None
        self.type = None
        self.parent = None
        self.lightverb = None
        self.frames = []
        self.examples = []
        self.unaxifra = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def __str__(self):
        if self.id in self.unaxifra:
            output = "\"%s_VB_0%s\":_%s_{\n" %(self.lemma, self.id, self.parent)
        else:
            output = "\"%s_VB_%s\":_%s_{\n" % (self.lemma, self.id, self.parent)
        for example in self.examples:
            output += "%s" %example
        output += "\tanc_sense = \"%s\"\n" % self.id
        output += "\tlemma = \"%s\"\n" % self.lemma
        output += "\tanc_type = \"%s\"\n" % self.type
        if self.lightverb:
            output += "\tanc_lightVerb = \"%s\"\n" % self.lightverb
        for frame in self.frames:
            output += "%s\n" % frame

        return output.encode("utf8")

class Frame(object):
    def __init__(self, lss, type):
        self.lss = lss
        self.type = type
        self.arguments = []
        self.pb = []
        self.ancoralexarg = []
        self.propbankarg = []
        # self.examples = []

    def __str__(self):
        output = "\tanc_lss = \"%s\"\n" % self.lss
        output += "\tanc_diathesis = \"%s\"\n" % self.type
        output += "\tgp = { \n"
        if self.pb:
            output += "\t\tpb = { \n"
            for p in self.pb:
                pbcls, pbId = str(p).split('.')
                output += "\t\t\t\"%s_VB_%s\"= {\n" %(pbcls, pbId)
                output += "\t\t\t\tpbcls = \"%s\" \n" %pbcls
                output += "\t\t\t\tpbId = \"%s\" \n" % pbId
                output += "\t\t\t}\n"
            output += "\t\t}\n"
            # output += "\t gp = { \n"
            for i in range(0,len(self.ancoralexarg)):
                if "/" in self.propbankarg[i]:
                    propbank,xxx = self.propbankarg[i].split('/')
                    # output += "\t\t %s = %s \n" %(self.propbankarg[i],self.ancoralexarg[i])
                    output += "\t\t %s = %s \n" %(xxx,self.ancoralexarg[i])
                else:
                    output += "\t\t %s = %s \n" %(self.propbankarg[i],self.ancoralexarg[i])
        for argument in self.arguments:
            output += "%s" % argument
        output += "\t} \n"

        output += "}\n"
        return output

class Examples(object):
    def __init__(self):
        self.examples = []
    def __str__(self):
        # if self.examples:
        output = ""
        for ex in self.examples:
            output += "\texample = \"%s\"\n" % ex
        return output

class Argument(object):
    def __init__(self, arg, role, funct):
        self.arg = arg
        self.role = role
        self.funct = funct
        self.constituents = []
        self.count = 0
    def __str__(self):
        output = "\t\t %s = {\n" % self.arg
        output += "\t\t\tanc_theme = \"%s\"\n" % self.role
        output += "\t\t\tanc_funct = \"%s\"\n" % self.funct
        for constituent in self.constituents:
            output += "\t\t\tprep  = \"%s\"\n" % constituent
        output += "\t\t}\n"
        return output

class Constituent(object):
    def __init__(self, prep):
        self.prep = prep
    def __str__(self):
        output = "%s" % self.prep
        return output


def getTitle(link):
    verb_info = []
    ancoralexid = link.get('ancoralexid')
    verb, lemma, id, type = ancoralexid.split('.')
    title = "%s_VB_0%s" %(lemma,id)
    verb_info.append(title)
    verb_info.append(type)
    return verb_info

def getAncoraInfo(root):
    english_senses = []
    wrapping = []
    map = {}
    key = ""
    for link in root:
        wrapping = []
        verb_info = getTitle(link)
        title = verb_info[0]
        type = verb_info[1]
        if type == "default":
            if key != title:
                english_senses = []
                wrapping = []
            key = title
            propbankid  = link.get('propbankid')

            english_senses.append(propbankid)
            arguments = getAncoraArguments(link)
            wrapping.append(english_senses)
            if arguments:
                wrapping.append(arguments)
            dict1  = {title:wrapping}
            map.update(dict1)
    return map

def getAncoraArguments(link):
    arguments = {}
    isZero = True
    map = []
    for arglink in link:
        ancoralexarg = arglink.get('ancoralexarg')
        propbankarg = arglink.get('propbankarg')


        if ancoralexarg:
            dict_arguments = {ancoralexarg:propbankarg}
            arguments.update(dict_arguments)
            if arguments not in map:
                map.append(arguments)
            if propbankarg == "0" and isZero == True:
                isZero = True
                map.append(isZero)

            if propbankarg != "0" and isZero == False:
                isZero = False
                map.append(isZero)


    return map

def getRoot():
    path = '../OriginalFiles/ancora-verb-es/*.lex.xml'
    files = glob.glob(path)
    root_lex = []
    for name in sorted(files):
        verb_lex = ET.parse(name)
        root_lex.append(verb_lex.getroot())
    return root_lex

def getExtArg(verb_class,lss):
    if verb_class == True or lss in lss_list:
        parent = "verbExtArg"
    else:
        parent = "verb"
    return parent

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
            if sense is not None:
                sense_str = str(sense)
                fd.write(sense_str.decode("utf8"))
    fd.close()



lss_list = ["A21.transitive-agentive-patient","A22.transitive-agentive-theme", "A23.transitive-agentive-extension", "A31.ditransitive-patient-locative", "A32.ditransitive-patient-benefactive",
            "A33.ditransitive-theme-locative", "A34.ditransitive-patient-theme", "A35.ditransitive-theme-cotheme", "D11.inergative-agentive", "A11.transitive-causative",
            "A12.ditransitive-causative-state","A13.ditransitive-causative-instrumental","D21.inergative-experiencer","D31.inergative-source"]

romans_zero = {"arg0": "I", "0": "I" , "arg1": "II", "1": "II", "arg2": "III", "2": "III", "arg3": "IV", "3": "IV", "arg4": "V", "argM": "M%d", "arrgM": "M%d",
           "arm": "M%d", "argL": "L", "aer2": "aer2", "arg": "M%d"}

romans_one = {"arg1": "I", "1": "I", "arg2": "II", "2": "II", "arg3": "III", "3": "III", "arg4": "IV", "argM": "M%d", "arrgM": "M%d",
           "arm": "M%d", "argL": "L", "aer2": "aer2", "arg": "M%d"}

def getSenses(root_lex, map):
    lemma = root_lex.get('lemma')
    type = root_lex.get('type')
    senses = []
    ancora_arguments = []
    arg_pointers = {}
    for sense_node in root_lex.findall('sense'):
        for frame_node in sense_node.iter('frame'):
            lss = frame_node.get('lss')
            frame_type = frame_node.get('type')
            if frame_type == 'default':
                id = sense_node.get('id')
                sense_obj = Sense()
                sense_obj.lemma = lemma
                sense_obj.type = type
                sense_obj.id = id

                title = "%s_VB_0%s" % (lemma, id)
                try:
                    slices = map[title]
                    english_senses = slices[0]
                    if len(slices) > 1:
                        other_info = slices[1]
                        ancora_arguments = other_info[0]
                        if len(other_info) > 1:
                            verb_class = other_info[1]
                            sense_obj.parent = getExtArg(verb_class, lss)
                        else:
                            if lss in lss_list:
                                sense_obj.parent = "verbExtArg"
                            else:
                                sense_obj.parent = "verb"
                    else:
                        ancora_arguments = []
                        # verb_class = []
                        if lss in lss_list:
                            sense_obj.parent = "verbExtArg"
                        else:
                            sense_obj.parent = "verb"

                except:
                    english_senses = []
                    if lss in lss_list:
                        sense_obj.parent = "verbExtArg"
                    else:
                        sense_obj.parent = "verb"

                frame_obj = Frame(lss, frame_type)
                i = 0
                try:
                    # frame_obj.pb.append(map_pb[title])
                    frame_obj.pb = english_senses
                except:
                    # pass
                    frame_obj.pb = None
                # i = 0
                counter = 1
                for argument_node in frame_node.findall('argument'):
                    arg = argument_node.get('argument')
                    role = argument_node.get('thematicrole')
                    funct = argument_node.get('function')
                    arg_pointer = "%s/%s" %(arg,role)
                    # arg_pointers.append(arg_pointer)
                    if arg == "arg0" or lemma == 'repatriar':
                        i = 1
                    if arg is not None:
                        if i == 1:
                            arg_name = romans_zero[arg]
                            # if arg_name.startswith("M"):
                            #     arg_name = arg_name %counter
                            #     counter += 1
                        else:
                            arg_name = romans_one[arg]
                    if arg_name.startswith("M"):
                        arg_name = arg_name % counter
                        counter += 1
                        if lemma == 'repatriar':
                            arg_name = 'I'
                    if arg_name == 'argL':
                        sense_obj.lightverb = 'yes'
                    aux_dict = {arg_pointer:arg_name}
                    arg_pointers.update(aux_dict)
                    argument_obj = Argument(arg_name, role, funct)
                    frame_obj.arguments.append(argument_obj)
                    for constituent_node in argument_node.iter('constituent'):
                        prep = constituent_node.get('preposition')
                        constituent_obj = Constituent(prep)
                        argument_obj.constituents.append(constituent_obj)
                if title in map.keys() and ancora_arguments != [] and lemma != 'repatriar':
                    counter = 1
                    for corr in ancora_arguments:
                        if corr == "arg0" and i == 0:
                            i = 1
                        if i == 1:
                            try:
                                corr_name = romans_zero[corr]
                            except:
                                if corr.startswith("argM") and corr in arg_pointers.keys():
                                    # corr_name = "M%d" %counter
                                    corr_name = arg_pointers[corr]
                                    # corr_name = romans_zero[corr]
                                else:
                                    corr_name = corr
                        else:
                            try:
                                corr_name = romans_one[corr]
                            except:

                                if corr.startswith("argM"):
                                    corr_name = "M%d" %counter
                                    # corr_name = romans_zero[corr]
                                else:
                                    corr_name = corr
                        # if corr.startswith("M"):
                        #
                        frame_obj.ancoralexarg.append(corr_name)
                        if ancora_arguments[corr].startswith("M"):
                            prop_num = "arg%s" %ancora_arguments[corr]
                            if prop_num == 'argM/LOC':
                                prop_num = 'LOC'
                        else:
                            prop_num = "A%s" % ancora_arguments[corr]
                        frame_obj.propbankarg.append(prop_num)
                count_ex = 0
                example_obj = Examples()
                for example_node in frame_node.findall('examples'):
                    if example_node is not None:
                        for ex in example_node.findall('example'):
                            example = ex.text.strip()
                            count_ex += 1
                            example_obj.examples.append(example)
                            if count_ex == 10:
                                break

                sense_obj.frames.append(frame_obj)
                sense_obj.examples.append(example_obj)

            senses.append(sense_obj)
            sense_obj = None
    return senses


def main():
    ancoranet = ET.parse("../OriginalFiles/ancoranet-es.xml")
    root_ancoranet = ancoranet.getroot()
    mappings = getAncoraInfo(root_ancoranet)
    root_lex = getRoot()
    filename = "../OutputFiles/AncoraDict_verbs_xxx.dic"
    writeOpening(filename)
    for root in root_lex:
        senses = getSenses(root, mappings)
        writeSenses(filename, senses)
    writeEnding(filename)




if __name__== "__main__":
    main()