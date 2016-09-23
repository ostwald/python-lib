from xml.dom.minidom import parse, parseString
from xml.parsers.expat import ExpatError
import sys
import string
import os
import re
import codecs
import time

if (sys.platform == 'win32'):
	sys.path.append ("H:/python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")

from JloXml import XmlRecord

class IdPrefixesRecord (XmlRecord):

	id_path = "dcsDataRecord:recordID"
	
	def __init__ (self, path=None, xml=None):
		XmlRecord.__init__ (self, path, xml)

	def getPrefixMap (self, key_filter=None):
		prefixes = self.selectNodes (self.dom, "prefixes:prefix")
		# print "there are %d prefixes" % len(prefixes)
		pMap = {}
		for prefix in prefixes:
			key = self.getText (self.selectSingleNode (prefix, "prefix-key"))
			prefix = self.getText (self.selectSingleNode (prefix, "prefix-value"))
			if not key_filter or key in key_filter:
				pMap[key] = prefix
		return pMap
		
	def addPrefix (self, key, value):
		prefix = self.addElement (self.doc, "prefix")
		keyElement = self.addElement (prefix, "prefix-key")
		self.setText (keyElement, key)
		valueElement = self.addElement (prefix, "prefix-value")
		self.setText (valueElement, value)
		return prefix

def test_getPrefixMap (rec=None):
	if not rec:
		path = "/home/ostwald/python-lib/dcsTools/record-consolidator/idPrefixes.xml"
		rec = IdPrefixesRecord (path=path)
	key_filter = None # ['nocc']
	m = rec.getPrefixMap(key_filter)
	print "prefixes"
	for key in m.keys():
		print "\t" + key + ": " + m[key]
		
if __name__ == "__main__":
	xml = "<prefixes/>"
	rec = IdPrefixesRecord (xml=xml)
	rec.addPrefix ("112938", "YADA")
	test_getPrefixMap (rec)
	
