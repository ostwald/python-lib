#!/usr/bin/env python

"""
/devel/ostwald/records/adn/serceet/SERC-EET-000-000-000-031.xml
"""

import sys, os, site
import string
import time

if (sys.platform == 'win32'):
	sys.path.append ("H:\\python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")

from HyperText.HTML40 import *
from JloXml import XmlRecord
from UserDict import UserDict

CMtemplate = """<?xml version="1.0" encoding="UTF-8"?>
<collectionMetadata>
	<header>
		<collectionPid/>
	</header>
	<content />
</collectionMetadata>
"""
	
def getRootElement (path):
	"""
	return the root element of the XML doc at path
	"""
	return XmlRecord (path=path).doc
	
class CMO (XmlRecord):
	def __init__ (self, recordsDir, xmlFormat, collection, collectionName, configDir):
		XmlRecord.__init__ (self, xml=CMtemplate)
		self.pidCounter = 0
		self.xpath_delimiter = "/"
		self.recordsDir = recordsDir
		self.xmlFormat = xmlFormat
		self.collection = collection
		self.collectionName = collectionName
		self.itemDir = os.path.join (recordsDir, xmlFormat, collection)
		self.dcsDataDir = os.path.join (recordsDir, "dcs_data", xmlFormat, collection)
		self.configDir = configDir
		
		if not os.path.isdir (self.itemDir):
			raise "NotDirectoryError", "itemDir (%s)" % itemDir
			
		if not os.path.isdir (self.dcsDataDir):
			raise "NotDirectoryError", "dcsDataDir (%s)" % dcsDataDir

	def populate (self):
		self.addCollectionData ()
		self.addItemLevelMetdata ()
			
	def addCollectionData (self):
		header = self.selectSingleNode (self.dom, "collectionMetadata/header")
		collectionPid = self.collection + "pid"
		self.setTextAtPath ("collectionMetadata/header/collectionPid", collectionPid)
		
		xmlFormat = self.addElement (header, "xmlFormat")
		self.setText (xmlFormat, self.xmlFormat)
		
		collectionName = self.addElement (header, "collectionName")
		self.setText (collectionName, self.collectionName)
		
		collectionConfig = self.addElement (header, "collection_config")
		configRecord = getRootElement (os.path.join (self.configDir, self.collection+".xml"))
		collectionConfig.appendChild (configRecord)
		
	def addItemLevelMetdata (self):
		for fileName in os.listdir (self.itemDir):
			root, ext = os.path.splitext(fileName)
			if ext.upper() == ".XML":
				 self.addMetadataWrapper (fileName)
				 
	def getPidVal (self):
		self.pidCounter = self.pidCounter + 1
		return "pid-%03d-%03d" % ( (self.pidCounter / 1000), (self.pidCounter % 1000))	
		

		
	def addMetadataWrapper (self, fileName):
		content = self.selectSingleNode (self.dom, "collectionMetadata/content")
		if content is None:
			raise "NodeNotFound", "content"
		metadataWrapper = self.addElement(content, "metadataWrapper")
		
		meta = self.addElement (metadataWrapper, "meta")
		itemRecord = getRootElement (os.path.join (self.itemDir, fileName))
		meta.appendChild (itemRecord)
		
		dcs_data = self.addElement (metadataWrapper, "dcs_data")
		dcsDataRecord = getRootElement (os.path.join (self.dcsDataDir, fileName))
		self.removeAttributes (dcsDataRecord)
		dcs_data.appendChild (dcsDataRecord)
		
		pid = self.addElement (metadataWrapper, "pid")
		self.setText (pid, self.getPidVal())
		return metadataWrapper
		
	def write (self, path=None):
		XmlRecord.write (self, path)
		writePath = None
		if path is not None:
			writePath = path
		elif self.path is not None:
			writePath = self.path
		if writePath is not None:
			print "xml written to %s" % writePath

def testGetRootElement ():
	recordsDir = "/devel/ostwald/records"
	xmlFormat = "adn"
	collection = "serceet"
	path = os.path.join (recordsDir, xmlFormat, collection, "SERC-EET-000-000-000-031.xml")
	root = getRootElement (path)
	print root.toxml().encode('utf8')
	
		
if __name__ == "__main__":
	recordsDir = "/devel/ostwald/records"
	xmlFormat = "oai_dc"
	collection = "1159995857662"
	collectionName = "Oai dc tester"
	configDir = "/devel/ostwald/tomcat/tomcat/dcs_conf/collection_config"
	cm = CMO (recordsDir, xmlFormat, collection, collectionName, configDir)
	
	if 0:
		cm.addMetadataWrapper ("SERC-EET-000-000-000-031.xml")
		print cm
	else:
		cm.populate()
		cm.write ("CMO-%s.xml" % collection)
	

