import os, sys
from JloXml import XmlRecord, XmlUtils

# metadataDir = 'H:/python-lib/ncar_lib/citations/wos/WOS_metadata'
metadataDir = '/home/ostwald/python-lib/ncar_lib/citations/wos/WOS_metadata'

recordPath = os.path.join (metadataDir,'WOS-000-000-000-002.xml')

class CitationReader (XmlRecord):
	xpath_delimiter = '/'

	def __init__ (self, path):
		XmlRecord.__init__ (self, path=path)

	def _get (self, field):
		return self.getTextAtPath ("record/"+field)

	def getPubname (self):
		return self._get("pubname")

	def getEditor (self):
		return self._get("editor")
		
	def getId (self):
		return self._get("recordId");

def getUniqueValues (field):
	vals = []
	filenames = os.listdir (metadataDir)
	print "reading %d files" % len (filenames)
	for i, filename in enumerate (filenames):
		if i % 100 == 0:
			print i
		path = os.path.join (metadataDir, filename)
		rec = CitationReader (path)
		val = rec._get(field)
		if val and not val in vals:
			vals.append (val)
	return vals


if __name__ == '__main__':
	field = 'editor'
	vals = getUniqueValues (field)
	print "%d unique values for '%s'" % (len(vals), field)
	for val in vals:
		print val
	
