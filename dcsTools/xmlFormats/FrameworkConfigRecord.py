import sys
import string
import os
import re
import codecs
import time

from JloXml import XmlRecord

class FrameworkConfigRecord (XmlRecord):

	xmlFormat_path = "frameworkConfigRecord:xmlFormat"
	schemaURI_path = "frameworkConfigRecord:schemaInfo:schemaURI"
	fieldInfoURI_path = "frameworkConfigRecord:editorInfo:fieldInfoURI"
	version_path = "frameworkConfigRecord:version"
	
	def __init__ (self, path=None, xml=None):
		XmlRecord.__init__ (self, path, xml)
		
	def getXmlFormat (self):
		return self.getTextAtPath (self.xmlFormat_path)
		
	def getSchemaURI (self):
		return self.getTextAtPath (self.schemaURI_path)
		
	def setSchemaURI (self, uri):
		self.setTextAtPath (self.schemaURI_path, uri)
		
	def getFieldInfoURI (self):
		return self.getTextAtPath (self.fieldInfoURI_path)
		
	def getVersion (self):
		return self.getTextAtPath (self.version_path)

		
if __name__ == "__main__":
	path = "/dls/devel/ostwald/tomcat/tomcat/dcs_conf/framework_config/collection_config.xml"	
	rec = FrameworkConfigRecord (path=path)
	print rec
	print "xmlFormat", rec.getXmlFormat()
	print "schemaURI", rec.getSchemaURI()
	rec.setSchemaURI ("http://I.am.just.set/")
	print "schemaURI", rec.getSchemaURI()
