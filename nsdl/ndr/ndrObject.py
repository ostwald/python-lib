import os, sys
from JloXml import XmlRecord, XmlUtils

class NdrObject (XmlRecord):

	xpath_delimiter = '/'

	properties_path = 'NDRObject/properties'
	
	def __init__ (self, getResponse):
		XmlRecord.__init__ (self, xml=getResponse)
		self.uniqueID = self.getUniqueID()
		
	def getUniqueID (self):
		return self.getProperty('nsdl:uniqueID')
		
	def getProperty(self, prop):
		return self.getTextAtPath (os.path.join (self.properties_path, prop))
