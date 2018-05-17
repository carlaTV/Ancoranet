#!/usr/bin/env python
# -*- coding: utf-8 -*-

### 1r pas: replicar l'exemple de vivir fet a mà.

#### class to write the txt file

class Entry(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.attrs = []

    def __str__(self):
        output = "%s:%s {\n" % (self.name, self.parent)
        for attr in self.attrs:
            output += "%s\n" % attr
        output += "\n}"
        return output


class getGP(object):
    def __init__(self):
        self.attrs = []

    def __str__(self):
        output = "gp  {\n I {\n"
        for attr in self.attrs:
            output += "%s\n" % attr
        output += "\n}\n}"
        return output


WriteOutput = Entry("vivir_VB", "_verb_")
GP = getGP()

# 1.1. de vivir.lex.xml a vivir_carla.txt

import xml.etree.ElementTree as ET

tree = ET.parse('files/vivir.lex.xml')

root = tree.getroot()



for sense in root.findall('sense'):
    id = sense.get('id')
    anc_sense = ('anc_sense  = ' + id)
    WriteOutput.attrs.append(anc_sense)
    for frame in root.iter('frame'):
        # anc_lss.append(frame.get('lss'))
        lss = frame.get('lss')
        anc_lss = ('anc_lss = ' + lss)
        WriteOutput.attrs.append(anc_lss)
        for argument in root.iter('argument'):
            thematicrole = argument.get('thematicrole')
            anc_theme = ('anc_theme= ' + thematicrole)
            WriteOutput.attrs.append(anc_theme)

            funct = argument.get('function')
            anc_function = ('anc_function = ' + funct)
            WriteOutput.attrs.append(anc_function)

print(WriteOutput)
print(GP)