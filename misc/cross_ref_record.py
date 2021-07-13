import os, sys, re
import lxml
from lxml import etree as ET

path = '/Users/ostwald/tmp/CROSSREF-old_simple.xml'

doc = ET.parse (path)
# print ET.tostring(doc)

root = doc.getroot()
print root.tag
for child in root:
    print child.tag