import os, sys
from JloXml import XmlRecord, XmlUtils
from frameworks import NCARRec
import library_dc_v1_1_globals
globals_1_1 = library_dc_v1_1_globals
del library_dc_v1_1_globals

class LibraryDCRec (NCARRec):
	
	"""
	version 1.1 - single namespace
	"""
	field_specs = globals_1_1.field_specs
	rootElementName = "record"
	schemaUri = "http://nldr.library.ucar.edu/metadata/library_dc/1.1/schemas/library_dc.xsd"
	nameSpaceUri = "http://nldr.library.ucar.edu/metadata/library_dc"
	
	id_field = "recordID"
	url_field = "URL"
	description_field = "description"
	altTitle_field = "altTitle"
	instName_field = "instName"
	instDivision_field = "instDivision"
	rights_field = "rights"
	
	def __init__ (self, path=None, xml=None):
		self.fields_list = self.field_specs.keys()
		if path or xml:
			XmlRecord.__init__ (self, path=path, xml=xml)
			## NCARRec.__init__ (self, path=path)s
		else:
			self.makeRecord ()
		
	def makeRecord (self):
		xml = "<%s />" % self.rootElementName
		NCARRec.__init__ (self, xml=xml)
		self.doc.setAttribute ("xmlns:"+self.schema_instance_namespace, \
								self.SCHEMA_INSTANCE_URI)
		self.doc.setAttribute ("xmlns", self.nameSpaceUri);
		self.setSchemaLocation (self.schemaUri, self.nameSpaceUri)
		
	def isRepeatingField (self, field):
		return self.field_specs[field]
		
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
		
	def getRights (self):
		return self.getFieldValues (self.rights_field)
		
	def setRights (self, value):
		self.setFieldValues (self.rights_field, value)
		
	def getTitle (self):
		return self.getFieldValue ("title")
		
	def getIssue (self):
		return self.getFieldValue ("issue")
		
	def setIssue (self, val):
		return self.setFieldValue ("issue", val)
		
	def getContributors (self):
		return self.getFieldValues ("contributor")
		
	def getCreators (self):
		return self.getFieldValues ("creator")
		
	def getRelations (self):
		return self.getFieldValues ("relation")
		
	def fixRelations (self):
		"""
		get relation elements and then fix each in turn
		-- if href:
			url = value
			type = Has part
		-- else
			label = value
			type = Is related
		"""
		nodes  = self.getFieldElements ("relation")
		if not nodes: return
		
		print "\n%s" % self.getId()
		for r in nodes:
			value = XmlUtils.getText(r)
			if not value: return
			XmlUtils.setText (r,"")
			if value.startswith ("http://"):
				r.setAttribute ("type", "Has part")
				r.setAttribute ("url", value)
			else:
				r.setAttribute ("type", "Is related")
				r.setAttribute ("title", value)
			print r.toxml()
		if 0:
			self.write()
			print "wrote record"
			
		
if __name__ == '__main__':
	# rec = LibraryDCRec (globals_1_1.rec_path)
	rec = LibraryDCRec (os.path.join (globals_1_1.technotes_path, "TECH-NOTE-000-000-000-664.xml"))
	rec.fixRelations()
		

