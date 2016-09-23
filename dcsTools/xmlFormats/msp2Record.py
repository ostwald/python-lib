
from JloXml import MetaDataRecord, XmlUtils

class MSP2Record (MetaDataRecord):

	id_path = "record:general:recordID"
	description_path = "record:general:description"
	title_path = "record:general:title"
	
	
	def __init__ (self, path=None, xml=None):
		MetaDataRecord.__init__ (self, path=path, xml=xml)
		
	def getDescription (self):
		return self.getTextAtPath (self.description_path)
		
	def setDescription (self, text):
		return self.setTextAtPath (self.description_path, text)
		
	def getTitle (self):
		return self.getTextAtPath (self.title_path)
		
	def setTitle (self, text):
		return self.setTextAtPath (self.title_path, text)
