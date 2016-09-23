

"""
traverse all the metadata and make a report of what fields there are, and how
many times each field occurs per record
"""


import os
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict

webCatDataDir = "/Documents/Work/DLS/NCAR Lib/WebCatMetadata/"
technotesDir = os.path.join (webCatDataDir, "NCAR Technical Notes");

techNote = os.path.join (technotesDir, "TECH-NOTE-000-000-000-001.xml")

# for filename in os.listdir (technotesDir):
	# print filename
	
class AllWebCat:
	
	def __init__ (self, baseDir):
		self.baseDir = baseDir
		self.types = []
		for dirName in os.listdir (baseDir):
			path = os.path.join (baseDir, dirName)
			
			if not os.path.isdir(path):
				continue
			
			self.addTypes (WebCatDir(path).types)
		
	def addTypes (self, types):
		for type in types:
			if not type in self.types:
				self.types.append (type)
				
class WebCatDir:
	
	def __init__ (self, dir):
		self.dir = dir
		self.types = []
		self.process()
		
	def process (self):
		for filename in os.listdir (self.dir):
			if not filename.endswith (".xml"): continue
			path = os.path.join (self.dir, filename)
			rec = WebCatRecord (path)
			for type in rec.types:
				self.addType (type)
				
	def addType (self, type):
		if type not in self.types:
			self.types.append (type)


class WebCatRecord (XmlRecord):
	
	def __init__ (self, path):
		self.path = path
		XmlRecord.__init__ (self, path=path)
		self.types = self.getTypes()
		
	def getTypes (self):
		xpath = "record:itemType"
		types = []
		nodes = self.selectNodes (self.dom, xpath)
		if nodes:
			for node in nodes:
				types.append (XmlUtils.getText(node))
		print "%s %s" % (types, os.path.basename(self.path))
		return types


if __name__ == "__main__":
	# obj = WebCatRecord (techNote)
	# obj = WebCatDir (technotesDir)
	obj = AllWebCat (webCatDataDir)

	types = obj.types;
	print "%d types found" % len(types)
	for type in types:
		print "\t%s"  % type

