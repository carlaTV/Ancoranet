#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs


class Entry(object):

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.attrs = {}

    def __str__(self):
        output = "%s:%s {\n" % (self.name, self.parent)
        for attr in self.attrs:
            output += "%s = %s\n" % (self.attrs.get(attr), attr)
        output += "\n}"
        return output.encode("utf8")


### Structure:
# 1. treure totes les paraules d'acoranet-es.xml + features
# 2. per cada word obrir el seu fitxer word.lex.xml
# 3. ajuntar cada word.lex amb la seva part de ancoranet

# 1)

# obrim el fitxer ancoranet-es.xml (codificant-lo a UTF8)

# ancoranet_es = ET.parse(unicode('../OriginalFiles/ancoranet-es.xml', errors='replace'))

ancoranet_es = ET.parse(codecs.open('../OriginalFiles/ancoranet-es.xml', encoding="utf8"))


# generem la root:
root_ancoranet = ancoranet_es.getroot()

names = ['anc_vtype', 'pbcls','pbID']

with codecs.open('../OutputFiles/dictionary.txt','w') as fd:

    for link in root_ancoranet:
        lexid = link.get('ancoralexid')
        VB, name_verb, num, anc_vtype = lexid.split('.')
        # anc_vtype = ('anc_vtype = ' + anc_vtype)
        name = (VB + '_' + name_verb + '_' + '0' + num)
        spec = ('_' + VB + '_')

        bankID = link.get('propbankid')
        pbcls, pbID = bankID.split('.')


        ancoranet_entry = Entry(name, spec)
        ancoranet_entry.attrs = {anc_vtype: names[0], pbcls : names[1], pbID: names[2]}

        fd.write(str(ancoranet_entry))
        # print(AncoranetEntry)

fd.close()