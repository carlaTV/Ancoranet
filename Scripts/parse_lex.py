#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET

parsing = ET.parse('/home/carlatv/Documents/AncoraNET/ancoranet/OriginalFiles/ancora-verb-es/abanderar.lex.xml')

root = parsing.getroot()

class WrapFeatures(object):
    def __init__(self):
        self.attrs = {}
        # self.otherstuff = otherstuff
    def __str__(self):
        output = "{"
        for attr in self.attrs:
            output += "%s = %s\n" %(attr, self.attrs.get(attr))
        # output += "%s" %self.otherstuff
        output += "}"
        return output

names = ['anc_sense', 'lss', 'type']

def ParseFile(root):
        res = []
        for sense in root.findall('sense'):
            id = sense.get('id')
            # anc_sense = ('anc_sense  = ' + id)
            wrapping = WrapFeatures()
            wrapping.attrs = {names[0]:id}
            for frame in sense.iter('frame'):
                # anc_lss.append(frame.get('lss'))
                lss = frame.get('lss')
                type = frame.get('type')
                wrapping.attrs.update({names[1]:lss, names[2]:type})
                res.append(str(wrapping))
        return res


res = ParseFile(root)
