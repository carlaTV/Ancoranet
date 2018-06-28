#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs
import glob


def getTitle(link):
    verb_info = []
    ancoralexid = link.get('ancoralexid')
    verb, lemma, id, type = ancoralexid.split('.')
    title = "%s_VB_0%s" %(lemma,id)
    verb_info.append(title)
    verb_info.append(type)
    return verb_info

def getEnglishSenses(root):
    english_senses = []
    wrapping = []
    map = {}
    key = ""
    for link in root:
        wrapping = []
        verb_info = getTitle(link)
        title = verb_info[0]
        type = verb_info[1]
        if type == "default":

            if key != title:
                english_senses = []
                wrapping = []
            key = title

            propbankid  = link.get('propbankid')
            english_senses.append(propbankid)
            arguments = getAncoraArguments(link)
            wrapping.append(english_senses)
            if arguments:
                wrapping.append(arguments)
            dict1  = {title:wrapping}
            map.update(dict1)

    return map

def getAncoraArguments(link):
    arguments = {}
    for arglink in link:
        ancoralexarg = arglink.get('ancoralexarg')
        propbankarg = arglink.get('propbankarg')

        if ancoralexarg:
            dict_arguments = {ancoralexarg:propbankarg}
            arguments.update(dict_arguments)

    return arguments




def main():
    ancoranet = ET.parse("../OriginalFiles/ancoranet-es_sufrir.xml")
    root_ancoranet = ancoranet.getroot()
    mappings = getEnglishSenses(root_ancoranet)



if __name__== "__main__":
    main()