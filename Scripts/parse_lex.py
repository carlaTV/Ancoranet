#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET

parsing = ET.parse('/home/carlatv/Documents/AncoraNET/ancoranet/OriginalFiles/ancora-verb-es/abanderar.lex.xml')

root = parsing.getroot()

class WrapFeatures(object):
    def __init__(self):
        self.attrs = {}
    def __str__(self):
        output = "{"
        for attr in self.attrs:
            output += "%s = %s\n" %(attr, self.attrs.get(attr))
        output += "}"
        return output

wrapping = WrapFeatures()

names = ['anc_sense', 'lss', 'type', 'argument', 'thematicrole', 'function', 'constituent', 'preposition']


def ParseFile(root):
    for sense in root.findall('sense'):
        id = sense.get('id')
        # anc_sense = ('anc_sense  = ' + id)
        wrapping.attrs = {names[0]:id}
        for frame in sense.iter('frame'):
            # anc_lss.append(frame.get('lss'))
            lss = frame.get('lss')
            type = frame.get('type')
            {names[1]: lss, names[2]: type}
            wrapping.attrs.update({names[1]:lss, names[2]:type})

            for argument in frame.iter('argument'):
                arg = argument.get('argument')
                themrole = argument.get('thematicrole')
                funct = argument.get('function')

                wrapping.attrs.update({names[3]:arg, names[4]:themrole, names[5]:funct})
                print wrapping

    return wrapping

ParseFile(root)
# print str(result)
