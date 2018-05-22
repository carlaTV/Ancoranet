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

class GetTheMiddle(object):
    def __init__(self):
        self.attrs = {}
    def __str__(self):
        output = ""
        for attr in self.attrs:
            output += "\t%s = %s\n" %(attr, self.attrs.get(attr))
        return output



names = ['anc_sense', 'lss', 'type', 'argument', 'thematicrole', 'function', 'constituent', 'preposition']
result = []

def ParseFile(root):
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
                result.append(str(wrapping))
        # print("result inside function")
        # print(result)
        return result


res = ParseFile(root)
middle = GetTheMiddle()
mid_res = []
def Arguments(root):
    for arguments in root.iter('argument'):
        arg = arguments.get('argument')
        themrole = arguments.get('thematicrole')
        funct = arguments.get('function')

        middle.attrs = {names[3]:arg, names[4]:themrole, names[5]:funct}
        mid_res.append(str(middle))

    return mid_res


# coses = ['casa','cosa']
mid_res = Arguments(root)
#
# for j in range(0, len(mid_res)):
#     print mid_res[j]

# print mid_res

for j in range(0, len(res)):
    total  = res[j]
    for i in range(0, len(mid_res)):
        total += mid_res[i]
        total += "\n"
    print total
# print "result outside function:"
# print res[0],"\n", res[1]
# print str(result)
