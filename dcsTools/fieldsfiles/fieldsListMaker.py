import os
from JloXml import XmlRecord, XmlUtils

baseDir = "c:/tmp/mets_fields_files"
version = "1.7"

template = "<metadataFieldsInfo><files/></metadataFieldsInfo>"

def getFormats ():
	formats = []
	for filename in os.listdir (baseDir):
		formats.append (filename)
	return formats

class FieldsListMaker:

	def __init__ (self, xmlFormat, version):
		self.xmlFormat = xmlFormat
		self.version = version
		self.fieldsDir = os.path.join (baseDir, self.xmlFormat, self.version, "fields")
		self.rec = XmlRecord (xml=template)
		if not os.path.exists(self.fieldsDir):
			raise "FileDoesNotExist", self.fieldsDir
		self.buildDir = os.path.join (baseDir, self.xmlFormat, self.version, "build")
		if not os.path.exists(self.fieldsDir):
			raise "FileDoesNotExist", self.fieldsDir
		print "fieldsDir: %s\nbuildDir: %s" % (self.fieldsDir, self.buildDir)

		self.addFieldsFiles()

	def addFieldsFiles (self):
		filesElement = self.rec.selectSingleNode (self.rec.doc, "files")
		if not filesElement:
			raise Exception, "Files element not found"
		for fieldsFile in self.getFieldsFileNames():
			text = "/".join ([self.xmlFormat, self.version, "fields", fieldsFile])
			XmlUtils.addChild (self.rec.dom, "file", text, filesElement)

	def getFieldsFileNames (self):
		names = []
		for filename in os.listdir (self.fieldsDir):
			names.append (filename)
		return names

	def write (self):
		path = os.path.join (self.buildDir, "fields-list.xml")
		fp = open (path, 'w')
		fp.write (self.rec.dom.toprettyxml("  "))
		fp.close()
		print "wrote to %s" % path

def makeAllFieldsLists ():
	for format in getFormats():
		flm = FieldsListMaker (format, version)
		# print flm.rec.dom.toprettyxml("  ")
		flm.write()

if __name__ == "__main__":
	
	makeAllFieldsLists()
