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
        self.parent = None
        self.frames = []
        self.unaxifra = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def __str__(self):
        if self.id in self.unaxifra:
            output = "\"%s_VB_0%s\":_%s_{\n" %(self.lemma, self.id, self.parent)
        else:
            output = "\"%s_VB_%s\":_%s_{\n" % (self.lemma, self.id, self.parent)
        output += "\tanc_sense = \"%s\"\n" % self.id
        output += "\tlemma = \"%s\"\n" % self.lemma
        output += "\tanc_type = \"%s\"\n" % self.type
        for frame in self.frames:
            output += "%s\n" % frame

        return output.encode("utf8")

class Frame(object):
    def __init__(self, lss, type):
        self.lss = lss
        self.type = type
        self.arguments = []
        self.pb = []

    def __str__(self):
        output = "\tlss = \"%s\"\n" % self.lss
        output += "\ttype = \"%s\"\n" % self.type

        if self.pb:
            for p in self.pb:
                pbcls, pbId = str(p).split('.')
                output += "\t\"%s_VB_%s\"= {\n" %(pbcls, pbId)
                output += "\t\tpbcls = \"%s\" \n" %pbcls
                output += "\t\tpbId = \"%s\" \n" % pbId
                output += "\t}\n"
            output += "\t gp = { \n"
        for argument in self.arguments:
            output += "%s" % argument
        output += "\t } \n"
        output += "}\n"

        return output

class Argument(object):
    def __init__(self, arg, role, funct):
        self.arg = arg
        self.role = role
        self.funct = funct
        self.constituents = []
        self.count = 0
        # self.ancoralexarg = None
        # self.propbankarg = None


    def __str__(self):

        output = "\t\targ = \"%s\"{\n" % self.arg
        output += "\t\t\tanc_theme = \"%s\"\n" % self.role
        output += "\t\t\tanc_funct = \"%s\"\n" % self.funct

        for constituent in self.constituents:
            output += "\t\t\tanc_prep  = \"%s\"\n" % constituent

        output += "\t\t}\n"
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

def getPropbankarg(root_ancoranet):
    iszero = False
    map_propbankarg = {}
    for link in root_ancoranet.findall('link'):
        ancoralex_item = link.get('ancoralexid')
        verb_, lemma, sense, type = ancoralex_item.split('.')
        # if type == 'default':
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

lss_list = ["A21.transitive-agentive-patient","A22.transitive-agentive-theme", "A23.transitive-agentive-extension", "A31.ditransitive-patient-locative", "A32.ditransitive-patient-benefactive",
            "A33.ditransitive-theme-locative", "A34.ditransitive-patient-theme", "A35.ditransitive-theme-cotheme", "D11.inergative-agentive", "A11.transitive-causative",
            "A12.ditransitive-causative-state","A13.ditransitive-causative-instrumental"]

def getPb(root_ancoranet):
    mapping = {}
    propbank = []
    # map = "aclarar_VB_01"
    map = ""
    for link in root_ancoranet.findall('link'):
        ancoralex_item = link.get('ancoralexid')
        verb_, lemma, sense, type = ancoralex_item.split('.')

        map_info = lemma + "_VB_0" + sense
        if map != map_info:
            propbank = []
        map = map_info

        if type == 'default':
            propbankid = link.get('propbankid')
            propbank.append(propbankid)

            dict1 = {map_info: propbank}

            mapping.update(dict1)
    return mapping

def getExtrArg(title, map_propbank, lss):
    try:
        if lss in lss_list:
            parent = "verbExtArg"

        elif map_propbank[str(title)] is True:
            parent = "VerbExtArg"
        else:
            parent = "verb"
    except:
        parent = "verb"

    return parent

def getArgLink(root_ancoranet):
    mapping = {}
    for link in root_ancoranet:
        ancoralexid = link.get('ancoralexid')
        verb, name, identifier, type_verb = ancoralexid.split('.')
        title = "%s_VB_0%s" %(name, identifier)
        arguments = {}
        if type_verb == 'default':
            for arglink in link:
                ancoralexarg = arglink.get('ancoralexarg') #mateix argument que verb.lex.xml
                # arguments.append(ancoralexarg)
                propbankarg = arglink.get('propbankarg')   #s'ha de passar a numeros romans
                # arguments.append(propbankarg)
                if ancoralexarg is not None:
                    dict_arguments = {ancoralexarg:propbankarg}
                    arguments.update(dict_arguments)
            if arguments:
                dict1 = {title:arguments}
                mapping.update(dict1)
    return mapping




arg_map = {"arg0": "I", "arg1": "I", "arg2": "II", "arg3": "III", "arg4": "IV", "argM": "M%d", "arrgM": "M%d",
           "arm": "M%d", "argL": "argL", "aer2": "aer2", "arg": "arg"}

def getSenses(root_lex, map_propbank, map_pb, map_arguments):
    lemma = root_lex.get('lemma')
    type = root_lex.get('type')
    senses = []
    for sense_node in root_lex.findall('sense'):
        # id = sense_node.get('id')
        # sense_obj = Sense()
        # sense_obj.lemma = lemma
        # sense_obj.type = type
        # sense_obj.id = id
        # #
        # title = "%s_VB_0%s" % (lemma, id)
        # sense_obj.parent = getExtrArg(title, map_propbank)

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

                sense_obj.parent = getExtrArg(title, map_propbank, lss)

                frame_obj = Frame(lss, frame_type)
                count = 0


                try:
                    # frame_obj.pb.append(map_pb[title])
                    frame_obj.pb = map_pb[title]
                except:
                    # pass
                    frame_obj.pb = None
                for argument_node in frame_node:
                    arg = argument_node.get('argument')
                    role = argument_node.get('thematicrole')
                    funct = argument_node.get('function')

                    if arg is not None:
                        arg_name = arg_map[arg]
                        if arg_name.startswith("M"):
                            arg_name = arg_name % count
                            count += 1

                        argument_obj = Argument(arg_name, role, funct)

                        frame_obj.arguments.append(argument_obj)

                        for constituent_node in argument_node.iter('constituent'):
                            prep = constituent_node.get('preposition')
                            constituent_obj = Constituent(prep)

                            argument_obj.constituents.append(constituent_obj)

                sense_obj.frames.append(frame_obj)

            senses.append(sense_obj)
            sense_obj = None

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
            if sense is not None:
                sense_str = str(sense)
                fd.write(sense_str.decode("utf8"))
    fd.close()

def main():
    ancoranet = ET.parse("../OriginalFiles/ancoranet-es.xml")
    root_ancoranet = ancoranet.getroot()
    map_propbank = getPropbankarg(root_ancoranet)
    map_pb = getPb(root_ancoranet)
    map_arguments = getArgLink(root_ancoranet)
    print map_arguments
    filename = "../OutputFiles/AncoraDict_verbs_test.dic"
    writeOpening(filename)
    root_lex = getRoot()
    for root in root_lex:
        senses = getSenses(root, map_propbank, map_pb, map_arguments)
        writeSenses(filename, senses)
    writeEnding(filename)

if __name__ == "__main__":
    main()