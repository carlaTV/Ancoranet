#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

class MiddleText(object):
    def __init__(self):
        self.attrs = []
        self.arg = []
        self.gp = []
        #self.gp = gp
    def __str__(self):
        output = " {\n"
        for attr in self.attrs:
            output += "%s\n" % attr
        for a in self.arg:
            output += "\t%s {\n" % a
            for g in self.gp:
                output += "\t\t%s\n" % g
        output += "\t\n}\n}"
        return output



ancoranet_es = ET.parse('OriginalFiles/ancoranet-es_VIVIRexemple.xml')
verb_lex = ET.parse('OriginalFiles/vivir.lex.xml')

root = verb_lex.getroot()
root2 = ancoranet_es.getroot()


filename = ('OutputFiles/print.txt')
file = open(filename, 'a')

##### FILE 2: verbnet.lex.xml ####
for sense in root.findall('sense'):
    id = sense.get('id')
    anc_sense = ('anc_sense  = ' + id)


    for frame in sense.iter('frame'):
        # anc_lss.append(frame.get('lss'))
        lss = frame.get('lss')
        anc_lss = ('anc_lss = ' + lss)

        WriteOutput = MiddleText()
        WriteOutput.attrs.append(anc_sense)
        print("{")
        file.write("{\n")
        print(anc_sense)
        file.write(anc_sense+ "\n")
        WriteOutput.attrs.append(anc_lss)
        file.write(anc_lss+ "\n")
        print(anc_lss)



        for argument in frame.iter('argument'):
            arg = argument.get('argument')
            #gp.argument.append(arg)
            thematicrole = argument.get('thematicrole')
            anc_theme = ('anc_theme= ' + thematicrole)
            funct = argument.get('function')
            anc_function = ('anc_function = ' + funct)


            #gp.attrs.append(anc_theme)
            #gp.attrs.append(anc_function)
            #print gp
            #file.write(str(gp))

            # WriteOutput = MiddleText()
            # WriteOutput.attrs.append(anc_sense)
            # print("Writing %s to file" %anc_sense)
            # WriteOutput.attrs.append(anc_lss)
            # print("Writing %s to file" % anc_lss)
            WriteOutput.arg.append(arg)
            print("\t" + arg + "{")
            file.write(("\t" + arg + "{" + "\n"))
            WriteOutput.gp.append(anc_theme)
            print("\t\t" + anc_theme)
            file.write("\t\t" + anc_theme + "\n")
            WriteOutput.gp.append(anc_function)
            print("\t\t"+anc_function)
            file.write("\t\t"+anc_function+ "\n")
            print("\t\t}\n\t}\n}")
            file.write("\t\t}\n\t}\n}")


        #file.write(str(WriteOutput))

file.close()





