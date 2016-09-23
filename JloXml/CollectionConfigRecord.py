import sys
import string
import os
import re
import codecs
import time


from JloXml import MetaDataRecord

class CollectionConfigRecord (MetaDataRecord):

	id_path = "collectionConfigRecord:collectionId"
	
	xpaths = {
		'id' : "collectionConfigRecord:collectionId",
		'idPrefix' : "collectionConfigRecord:idPrefix",
		'xmlFormat' : "collectionConfigRecord:xmlFormat",
		'statusFlags' : "collectionConfigRecord:statusFlags",
		'exportDir' : "collectionConfigRecord:exportDirectory"		
	}
	def __init__ (self, path=None, xml=None):
		MetaDataRecord.__init__ (self, path, xml)

	def getId (self):
		return self.getTextAtPath (self.id_path)
	
	def getKey(self):
		return self.getId()
		
	def setKey(self, new_key):
		self.setId(new_key)
	
	def getIdPrefix (self):
		# return self.getTextAtPath (self.idPrefix_path)
		return self.get('idPrefix')
		
	def setIdPrefix (self, new_prefix):
		"""
		if idPrefix element does not exist, create it before "statusFlags"
		"""
		if not self.selectSingleNode (self.dom, self.xpaths['idPrefix']):
			idPrefix = self.dom.createElement ("idPrefix")
			statusFlags = self.getStatusFlagsElement()
			self.doc.insertBefore (idPrefix, statusFlags)
		self.set('idPrefix', new_prefix)
		
	def getXmlFormat (self):
		return self.get('xmlFormat')
		
	def setXmlFormat (self, new_xmlFormat):
		self.set('xmlFormat', new_xmlFormat)

	def getStatusFlagsElement (self):
		return self.selectSingleNode (self.dom, self.xpaths['statusFlags'])
		
	def getExportDir (self):
		return self.get('exportDir')
		
	def setExportDir (self, newExportDir):
		self.set('exportDir', newExportDir)
		
def showElementSequence (nodeList):
	for i in range (nodeList.length):
		print "%d - '%s'" % (i, nodeList.item(i).nodeName)
		
if __name__ == "__main__":
	path = "/home/ostwald/python-lib/dcsTools/prefixer/collection-config.xml"	
	rec = CollectionConfigRecord (path=path)
	print "prefix before: %s" % rec.getPrefix()
	rec.setPrefix("yabadaba")
	print "prefix after: %s" % rec.getPrefix()
	print rec
