#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

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



ancoranet_es = ET.parse('files/ancoranet-es_VIVIRexemple.xml')
verb_lex = ET.parse('files/vivir.lex.xml')

root = verb_lex.getroot()
root2 = ancoranet_es.getroot()

#### FILE 1: ancoranet-es
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

    WriteOutput = Entry(name, spec)
    #GP = getGP()
    WriteOutput.attrs.append(anc_vtype)
    WriteOutput.attrs.append(pbcls)
    WriteOutput.attrs.append(pbID)


    for verbnet in link:
        fil = verbnet.get('file')
        classe = verbnet.get('class')

        if fil is not None:
            vncls,_number = fil.split('-')
            vncls = ('vncls = '+ vncls)

            WriteOutput.attrs.append(vncls)

        if classe is not None:
            classe = ('class = ' + classe)
            WriteOutput.attrs.append(classe)

        for framenet in verbnet.iter('framenet'):
            fn = framenet.text
            fn = ('fn = '+fn)
            WriteOutput.attrs.append(fn)

    #Write to file:
    filename = ('OutputFiles/%s.txt' % name_verb)

    file = open(filename, 'a')
    file.write(str(WriteOutput))
    file.close()
