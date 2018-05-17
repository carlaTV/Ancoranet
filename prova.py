#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

## define classes:

class MakeTitle(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def __str__(self):
        output = "%s:%s {\n" % (self.name, self.parent)
        return output

class EndText(object):
    def __str__(self):
        output = "}"
        return output


class ExternText(object):
    def __init__(self,obj):
        self.attrs = []
        self.obj = obj
    def __str__(self):
        output = ""
        for atr in self.attrs:
            output += "%s \n" %atr
        output += "%s\n" % self.obj
        return output

class InternText(object):
    def __init__(self):
        self.arg = []
    def __str__(self):
        output = "{\n"
        for arg in self.arg:
            output += "\t%s \n" %arg
        output += "}\n"
        return output

## define function to Write the file

def WriteFile(name, parent, filename, arguments, objects):
    filename = ('OutputFiles/%s.txt'%filename)
    file = open(filename, 'a')
    title = MakeTitle(name, parent)
    file.write(str(title))

    intern = InternText()
    for arg in arguments:
        intern.arg.append(arg)
    text = ExternText(intern)
    for obj in objects:
        text.attrs.append(obj)
    file.write(str(text))
    end = EndText
    file.write(str(end))

# def WriteFile(**kwargs):
#         if ('name' in kwargs and 'parent' in kwargs and 'filename' in kwargs)
#             kwargs['filename'] = (kwargs['filename'] + '.txt')
#             file = open(kwargs['filename'], 'a')
#             title = MakeTitle(kwargs['name'], kwargs['parent'])
#             print title
#             file.write(str(title))
#
#         if ('objects' in kwargs):
#             text = ExternText()
#             for obj in kwargs['objects']:
#                 text.attrs.append(obj)
#             print text
#             file.write(str(text))
#         if ('arguments' in kwargs)
#             intern = InternText()
#             for arg in kwargs['arguments']:
#                 intern.arg.append(arg)
#             print intern
#             file.write(str(intern))
#
#             end = EndText()
#             print end
#             file.write(str(end))


ancoranet_es = ET.parse('files/ancoranet-es_VIVIRexemple.xml')
verb_lex = ET.parse('files/vivir.lex.xml')

root = verb_lex.getroot()
root2 = ancoranet_es.getroot()

objects = []
arguments = []

## define vectors to save the searchs:
for link in root2:

    lexid = link.get('ancoralexid')
    VB, name_verb, num, anc_vtype = lexid.split('.')
    anc_vtype = ('anc_vtype = ' + anc_vtype)
    name = (VB + '_' + name_verb + '_' + '0' + num)
    spec = ('_' + VB + '_')
    #WriteFile(name = name, parent = spec, filename = 'testsupertest')

    bankID = link.get('propbankid')
    pbcls, pbID = bankID.split('.')

    pbcls = ('pbcls =' + pbcls)
    pbID = ('pbID = ' + pbID)

    objects.append(anc_vtype)
    objects.append(pbcls)
    objects.append(pbID)

    #WriteFile(objects = objects)
    # WriteOutput = Entry(name, spec)
    # #GP = getGP()
    # WriteOutput.attrs.append(anc_vtype)
    # WriteOutput.attrs.append(pbcls)
    # WriteOutput.attrs.append(pbID)

    for verbnet in link:
        fil = verbnet.get('file')
        classe = verbnet.get('class')

        if fil is not None:
            vncls, _number = fil.split('-')
            vncls = ('vncls = ' + vncls)

            objects.append(vncls)  # WriteOutput.attrs.append(vncls)

        if classe is not None:
            classe = ('class = ' + classe)
            objects.append(classe)  # WriteOutput.attrs.append(classe)

        for framenet in verbnet.iter('framenet'):
            fn = framenet.text
            fn = ('fn = ' + fn)
            objects.append(fn)  # WriteOutput.attrs.append(fn

    #WriteFile(objects = objects)

            ##### FILE 2: verbnet.lex.xml ####
            for sense in root.findall('sense'):
                id = sense.get('id')
                anc_sense = ('anc_sense  = ' + id)


                for frame in sense.iter('frame'):
                    # anc_lss.append(frame.get('lss'))
                    lss = frame.get('lss')
                    anc_lss = ('anc_lss = ' + lss)


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

                        objects.append(anc_sense)
                        objects.append(anc_lss)
                        arguments.append(arg)
                        arguments.append(anc_theme)
                        arguments.append(anc_function)

                        # WriteOutput = MiddleText()
                        # WriteOutput.attrs.append(anc_sense)
                        # WriteOutput.attrs.append(anc_lss)
                        # WriteOutput.arg.append(arg)
                        # WriteOutput.gp.append(anc_theme)
                        # WriteOutput.gp.append(anc_function)
            #
                    #WriteFile('vivir','VB',arguments, 'verblex',objects)
                    #file.write(str(WriteOutput))
                    WriteFile(name, spec, 'prova',arguments, objects)



#WriteFile(name,spec, 'prova.txt', arguments, objects)

#WriteFile(nom, par)

