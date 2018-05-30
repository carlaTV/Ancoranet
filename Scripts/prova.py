#!/usr/bin/env python
# -*- coding: UTF-8-*-

import xml.etree.ElementTree as ET
import codecs

verb = ET.parse("../OriginalFiles/ancora-verb-es/abalanzar.lex.xml")

root = verb.getroot()

lex = root.get('lemma')
#lemma = lex.get('lemma')

print(lex)