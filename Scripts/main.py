#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

###### CLASSES ######
#
class verbLex(object):
    def __init__(self, argument, gp):
        self.attrs = []
        self.argument = argument
        self.gp = gp
    def __str__(self):
        output = ""
        for atr in self.attrs:
            output += "%s \n"  %atr
        output += "%s" %self.argument
        output += "%s" % self.gp
        # for arg in self.argument:
        #     output += " \t%s {\n" % arg
        #     for g in self.gp:
        #         output += "\t\t%s {\n" %g
        return output

class arguments(object):
    def __init__(self,gp):
        self.argument = []
        self.gp  = gp
    def __str__(self):
        output = ""
        for arg in self.argument:
            output += " \t%s {\n" % arg
        output += "%s" %self.gp
        return output

class gp(object):
    def __init__(self):
        self.gp = []
    def __str__(self):
        output = ""
        for g in self.gp:
            output += "\t\t%s \n" % g
        return output

## 1. parse file verb.lex:

def parse_index(lex_root):
    output1 = []
    anc_FUNCT = []
    anc_THEME = []
    ### FILE 1
    j = 0
    for sense in lex_root.findall('sense'):

        id = sense.get('id')
        anc_sense = ('anc_sense  = ' + id)
        get_ThFunc = gp()
        get_arguments = arguments(get_ThFunc)
        WriteOutput = verbLex(get_arguments, get_ThFunc)

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

                get_arguments.argument.append(arg)
                # WriteOutput.attrs.append(arg)

                # get_ThFunc.gp[0] = anc_theme
                get_ThFunc.gp.insert(0,anc_theme)
                # anc_THEME.append(anc_theme)

                # get_ThFunc.gp[1] = anc_function
                get_ThFunc.gp.insert(1,anc_function)
                # anc_FUNCT.append(anc_function)


            # print("j = %i" % j)
            #
            # rel_theme = {arg: anc_THEME[j]}
            # rel_funct = {arg: anc_FUNCT[j]}
            # j += 1
            #
            # WriteOutput.gp.append(rel_theme[arg])
            # WriteOutput.gp.append(rel_funct[arg])

            # output1.append(str(WriteOutput))
            # WriteOutput.gp.remove(rel_theme[arg])
            # WriteOutput.gp.remove(rel_funct[arg])

            # print output1[0]
            print WriteOutput

    # Write to file:
    filename = ('OutputFiles/%s.txt' % 'prova2')


if __name__ == "__main__":

    ancoranet_es = ET.parse('OriginalFiles/ancoranet-es_VIVIRexemple.xml')
    verb_lex = ET.parse('OriginalFiles/vivir.lex.xml')

    lex_root = verb_lex.getroot()
    ancoranet_root = ancoranet_es.getroot()

    parse_index(lex_root)

    # generate_mate_dict(root, root2)
    # haz_todo(root, root2)



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
