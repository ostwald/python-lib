"""
classes for reading library_dc and webcat XML records
"""
import os, sys, re, codecs
from JloXml import XmlRecord, XmlUtils

import globals

class NCARRec (XmlRecord):
	"""
	assumes a flat metadata structure (all fields are children of docRoot)
	"""
	
	field_list = None
	id_field = None
	description_field = None
	xpath_delimiter = "/"
	
	def __init__ (self, path=None, xml=None):
		XmlRecord.__init__ (self, path, xml)
		for attr in self.field_list:
			setattr (self, attr, None)
		for element in self.getElements(self.doc):
			setattr (self, element.tagName, self.getText(element))
			print 'set %s to %s' % (element.tagName, self.getText(element))
			
	def getFieldValue (self, field):
		path = "%s/%s" % (self.rootElementName, field)
		value = self.getTextAtPath (path)
		if not value is None:
			value = value.strip()
		return value
		
	def getFieldValues (self, field):
		path = "%s/%s" % (self.rootElementName, field)
		nodes = self.selectNodes (self.dom, path)
		values = []
		for node in nodes:
			value = self.getText (node)
			if value is None:
				continue
			value = value.strip()
			if value:
				values.append (value)
		return values
		
	def getFieldElements (self, field):
		path = "%s/%s" % (self.rootElementName, field)
		return self.selectNodes (self.dom, path)
		
	def numFieldValues (self, field):
		path = "%s/%s" % (self.rootElementName, field)
		nodes = self.selectNodes (self.dom, path)
		return len(nodes)
		
	def addFieldValue (self, field, value):
		"""
		do not add a value if this field already has it
		strip value before adding
		"""
		path = "%s/%s" % (self.rootElementName, field)
		element = self.addElement (self.doc, field)
		if not value is None:
			value = value.strip()
		if not value in self.getFieldValues (field):
			self.setText (element, value)
		
	def setFieldValue (self, field, value):
		"""
		if there are existing values, this will change the first only
		"""
		path = "%s/%s" % (self.rootElementName, field)
		if not value is None:
			value = value.strip()
		element = self.selectSingleNode (self.dom, path)
		if not element:
			element = self.addElement (self.doc, field)
		self.setText (element, value)
		
	def removeField (self, field):
		path = "%s/%s" % (self.rootElementName, field)
		nodes = self.selectNodes (self.dom, path)
		for node in nodes:
			self.deleteElement (node)
			
	def setFieldValues (self, field, values):
		self.removeField (field)
		self.addFieldValues (field, values)

	def addFieldValues (self, field, values):
		for value in values:
			self.addFieldValue (field, value)
			
	def orderFields (self):
		""" based on converter.Converter """
		
		elements = self.doc.childNodes
			
		# print "-------------"
		mycmp = lambda x, y:cmp (self.field_list.index(x.tagName), 
								 self.field_list.index(y.tagName))
		if elements:
			elements.sort(mycmp)

			
	def getId (self):
		return self.getFieldValue (self.id_field)
		
	def setId (self, value):
		self.setFieldValue (self.id_field, value)
		
	def getDescription (self):
		return self.getFieldValue (self.description_field)
		
	def setDescription (self, value):
		self.setFieldValue (self.description_field, value)
			
class WebcatRec (NCARRec):
	
	rootElementName = "record"
	## issue_delimiter = re.compile ("(?P<issue>NCAR.+?) [:-] (?P<title>[a-zA-Z].+)") # - for all but manuscripts, which use :
	issue_delimiter = re.compile ("(?P<issue>NCAR.+?)[\s]+[:-][\s]+(?P<title>.+)") # - for all but manuscripts, which use :
	field_list = globals.webcat_fields
	id_field = "recordID"
	accessionNum_field = "accessionNum"
	description_field = "description"
	
	def __init__ (self, path=None, xml=None):
		NCARRec.__init__ (self, path, xml)
		
	def getAccessionNum (self):
		return self.getFieldValue (accessionNum_field)
		
	def getPublishers (self):
		return self.getFieldValues ("publisher")
		
	def getScientificDivisions (self):
		return self.getFieldValues ("scientificDivision")
			
class LibraryDCRec_v1_0 (NCARRec):
	
	"""
	made obsolete (~2/09) when framework changed to contain a single namespace!
	
	we are always writing a new rec, not reading an existing one ...
	
	xsi:schemaLocation="http://www.dlsciences.org/frameworks/library_dc 
						http://www.dlsciences.org/frameworks/library_dc/1.0/schemas/library_dc.xsd"
	"""
	rootElementName = "library_dc:record"
	schemaUri = "http://www.dlsciences.org/frameworks/library_dc/1.0/schemas/library_dc.xsd"
	nameSpaceUri = "http://www.dlsciences.org/frameworks/library_dc"
	dcNameSpaceUri = "http://purl.org/dc/elements/1.1/"
	field_list = globals.library_dc_fields
	
	id_field = "library_dc:recordID"
	url_field = "library_dc:URL"
	description_field = "dc:description"
	altTitle_field = "library_dc:altTitle"
	instName_field = "library_dc:instName"
	instDivision_field = "library_dc:instDivision"
	
	def __init__ (self, path=None):
		if path:
			XmlRecord.__init__ (self, path=path)
		else:
			self.makeRecord ()
		
	def makeRecord (self):
		xml = "<%s xmlns:library_dc='%s' />" % (self.rootElementName, self.nameSpaceUri)
		NCARRec.__init__ (self, xml=xml)
		self.doc.setAttribute ("xmlns:library_dc", self.nameSpaceUri)
		self.doc.setAttribute ("xmlns:dc", self.dcNameSpaceUri)
		self.doc.setAttribute ("xmlns:"+self.schema_instance_namespace, \
								self.SCHEMA_INSTANCE_URI)
		self.setSchemaLocation (self.schemaUri, self.nameSpaceUri)
		
	def getUrl (self):
		return self.getFieldValue (self.url_field)
		
	def setUrl (self, value):
		self.setFieldValue (self.url_field, value)
		
	def getAltTitle (self):
		return self.getFieldValue (self.altTitle_field)
		
	def setAltTitle (self, value):
		self.setFieldValue (self.altTitle_field, value)
		
	def getInstName (self):
		return self.getFieldValue (self.instName_field)
		
	def setInstName (self, value):
		self.setFieldValue (self.instName_field, value)
		
	def getInstDivisions (self):
		return self.getFieldValues (self.instDivision_field)
		
	def setInstDivisions (self, value):
		self.setFieldValues (self.instDivision_field, value)
		
	def getTitle (self):
		return self.getFieldValue ("dc:title")
		
	def getIssue (self):
		return self.getFieldValue ("library_dc:issue")
		
	def setIssue (self, val):
		return self.setFieldValue ("library_dc:issue", val)
		
	def getContributors (self):
		return self.getFieldValues ("dc:contributor")
		
	def getCreators (self):
		return self.getFieldValues ("dc:creators")

		
def LibraryDCRecTester ():
	rec = LibraryDCRec_v1_0 ()
	rec.setFieldValue ("library_dc:URL", "http://fooberry/index.html")
	print "URL: %s" % rec.getFieldValue ("library_dc:URL")
	rec.setUrl ("imachanged")
	print "URL: %s" % rec.getUrl()
	
	rec.addFieldValues ("dc:subject", ['sub1', 'sub2'])
	print rec
	
	rec.addFieldValues ("dc:subject", ['sub3', 'sub4'])
	print rec
	print "number of dc:subject fields: %d" % rec.numFieldValues ("dc:subject")
	print "number of dc:Xsubject fields: %d" % rec.numFieldValues ("dc:Xsubject")
	rec.removeField ("dc:subject")
	print rec

	
if __name__ == "__main__":
	LibraryDCRecTester ()


