#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET


class Ancoranet(object):
    def __init__(self, name, parent, verb):
        self.name = name
        self.parent = parent
        self.attrs = []
        self.verb = verb

    def __str__(self):
        output = "%s:%s {\n" % (self.name, self.parent)
        for attr in self.attrs:
            output += "%s\n" % attr
        output += "%s\n}" % self.verb
        return output
#
class verbLex(object):
    def __init__(self):
        self.attrs = []
        self.argument = []
        self.gp = []
    def __str__(self):
        output = ""
        for atr in self.attrs:
            output += "%s \n"  %atr
        for arg in self.argument:
            output += " \t%s {\n" % arg
            for g in self.gp:
                output += "\t\t%s {\n" %g
        return output

# class verbLex(object):
#     def __init__(self):
#         self.attrs = []
#     def __str__(self):
#         output = ""
#         for atr in self.attrs:
#             output += "%s \n"  %atr
#         return output

def haz_todo(root, root2):
    output1 = []
    anc_FUNCT = []
    anc_THEME = []
    ### FILE 1
    j = 0
    for sense in root.findall('sense'):


        id = sense.get('id')
        anc_sense = ('anc_sense  = ' + id)
        WriteOutput = verbLex()
        WriteOutput.attrs.append(anc_sense)


        for frame in sense.iter('frame'):

            lss = frame.get('lss')
            anc_lss = ('anc_lss = ' + lss)
            WriteOutput.attrs.append(anc_lss)


            for argument in frame.iter('argument'):
                arg = argument.get('argument')

                thematicrole = argument.get('thematicrole')
                anc_theme = ('anc_theme= ' + thematicrole)

                funct = argument.get('function')
                anc_function = ('anc_function = ' + funct)

                WriteOutput.argument.append(arg)

                # WriteOutput.gp.append(anc_theme)
                anc_THEME.append(anc_theme)

                # WriteOutput.gp.append(anc_function)
                anc_FUNCT.append(anc_function)

                print("j = %i" %j)

                rel_theme = {arg : anc_THEME[j]}
                rel_funct = {arg : anc_FUNCT[j]}
                j += 1

                WriteOutput.gp.append(rel_theme[arg])
                WriteOutput.gp.append(rel_funct[arg])

            output1.append(str(WriteOutput))
                # WriteOutput.gp.remove(rel_theme[arg])
                # WriteOutput.gp.remove(rel_funct[arg])

            #print output1[0]

    # Write to file:
    filename = ('OutputFiles/%s.txt' % 'prova2')

    with open(filename, 'w') as fd:
        i = 0
        for link in root2:

            lexid = link.get('ancoralexid')
            VB, name_verb, num, anc_vtype = lexid.split('.')
            anc_vtype = ('anc_vtype = '+ anc_vtype)
            name = (VB + '_' + name_verb+ '_'+ '0' + num)
            spec = ('_'+VB+'_')
            bankID = link.get('propbankid')
            pbcls, pbID = bankID.split('.')

            pbcls = ('pbcls ='+ pbcls)
            pbID = ('pbID = '+  pbID)

            rel = {name : output1[i]}  #falla quan tenen el mateix nom
            print("i = %i" %i)
            i += 1

            AncDict = Ancoranet(name, spec, rel[name])

            AncDict.attrs.append(anc_vtype)
            AncDict.attrs.append(pbcls)
            AncDict.attrs.append(pbID)


            for verbnet in link:
                fil = verbnet.get('file')
                classe = verbnet.get('class')

                if fil is not None:
                    vncls,_number = fil.split('-')
                    vncls = ('vncls = '+ vncls)

                    AncDict.attrs.append(vncls)

                if classe is not None:
                    classe = ('class = ' + classe)
                    AncDict.attrs.append(classe)

                for framenet in verbnet.iter('framenet'):
                    fn = framenet.text
                    fn = ('fn = '+fn)
                    AncDict.attrs.append(fn)

            fd.write(str(AncDict))



#
# def get_words(index_root):
#
#     for sense in root.findall('sense'):
#
#         id = sense.get('id')
#         anc_sense = ('anc_sense  = ' + id)
#         WriteOutput = verbLex()
#         WriteOutput.attrs.append(anc_sense)
#
#
#         for frame in sense.iter('frame'):
#
#             lss = frame.get('lss')
#             anc_lss = ('anc_lss = ' + lss)
#             WriteOutput.attrs.append(anc_lss)
#
#
#             for argument in frame.iter('argument'):
#                 arg = argument.get('argument')
#
#                 thematicrole = argument.get('thematicrole')
#                 anc_theme = ('anc_theme= ' + thematicrole)
#
#                 funct = argument.get('function')
#                 anc_function = ('anc_function = ' + funct)
#
#                 WriteOutput.argument.append(arg)
#
#                 WriteOutput.gp.append(anc_theme)
#
#                 WriteOutput.gp.append(anc_function)
#
#             output1.append(str(WriteOutput))
#             #print output1[0]
#
#
# def generate_mate_dict(index_root, lex_root):
#
#     lex_infos = get_all_lex(lex_root)
#
#     words = get_words(index_root)
#     for word in index_root:
#
#         merge(word, lex_info)
#
#         add_to_dict()

if __name__ == "__main__":

    ancoranet_es = ET.parse('files/ancoranet-es_VIVIRexemple.xml')
    verb_lex = ET.parse('files/vivir.lex.xml')

    root = verb_lex.getroot()
    root2 = ancoranet_es.getroot()

    # generate_mate_dict(root, root2)
    haz_todo(root, root2)