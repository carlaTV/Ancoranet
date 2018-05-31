#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET

parsing = ET.parse('/home/carlatv/Documents/AncoraNET/ancoranet/OriginalFiles/ancora-verb-es/abanderar.lex.xml')

root = parsing.getroot()

class WrapFeatures(object):
    def __init__(self):
        self.attrs = {}
        self.mid = {}
        self.otherstuff = []
    def __str__(self):
        output = "{"
        for oth in self.otherstuff:
            output += "%s \n" %self.otherstuff
        for attr in self.attrs:
            output += "%s = %s\n" %(attr, self.attrs.get(attr))
        for m in self.mid:
            output += "%s" %self.mid.get(m)
        output += "}\n"

        return output

names = ['anc_sense', 'lss', 'type','argument', 'theme', 'function']


def ParseFile(root):
        res = []
        for sense in root.findall('sense'):
            wrapping = WrapFeatures()
            id = sense.get('id')
            # anc_sense = ('anc_sense  = ' + id)
            wrapping.attrs = {names[0]:id}
            for frame in sense.iter('frame'):
                lss = frame.get('lss')
                type = frame.get('type')
                wrapping.attrs.update({names[1]:lss, names[2]:type})
                # wrapping.otherstuff.append(wrapping.attrs)
                res.append(str(wrapping))

        return res


res = ParseFile(root)
#
with open('OutputFiles/parse_lex.txt','w') as fd:
     for i in range(0, len(res)):
        fd.write(res[i])



