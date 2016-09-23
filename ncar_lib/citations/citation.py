"""
Citation is the XML format for the combined WOS and PUBsDB data.
"""

from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils

# fields that are commented out are not available (or derivable) from WOS

required_fields = [  # NOT required in the "schema-valid" sense !!!
	# "pub_id",
	"title",
	"year",
	"pubname",
	# "publisher"
	"editor",
	"volume",
	"pages",
	# "doi",
	# "url",
	"pubstatus",
	"statusdate",
	# "meetstartdate",
	# "meetenddate",
	# "class",
	"type",
	# "meetcity",
	# "meetstateprov",
	# "meetcountrycode",
	# "collaboration",
	# "meetdate",
	"authors" # list of authors in some normalized form
	]
	
other_fields = [
	"pub_id",
	"wos_id",
	"publisher",
	"doi",
	"url",
	"meetstartdate",
	"meetenddate",
	"class",
	"meetcity",
	"meetstateprov",
	"meetcountrycode",
	"collaboration",
	"meetdate"
	]
	
class Citation (XmlRecord):
	
	schemaURI = 'http://nldr.library.ucar.edu/metadata/citation/0.3/citation.xsd'
	targetNamespace = 'http://nldr.library.ucar.edu/metadata/citation'
	
	def __init__ (self, data, id):
		self.data = data
		self._validate()
		self.id = id
		XmlRecord.__init__ (self, xml="<record />")
		self.setSchemaNamespace ()
		self.setSchemaLocation (self.schemaURI, self.targetNamespace)
		self.setDefaultNamespace (self.targetNamespace)
		# self.setNoNamespaceSchemaLocation (self.schemaURI)
		self.addChild ("recordId", id)
		self.populate ()
			
	def _validate (self):
		for field in required_fields:
			if not self.data.has_key(field):
				raise KeyError, "data does not contain '%s' field" %  field
				
	def populate (self):
		for field in required_fields:
			if field == 'authors':
				continue
			self.addChild (field, self.data[field])
			
		# process authors
		authorsElement = self.addElement (self.doc, "authors")
		for author in self.data['authors']:
			authorElement = self.addElement (authorsElement, "author")
			
			## attributes
			if author.authororder:
				authorElement.setAttribute ("author_order", str(author.authororder))
			if author.person_id:
				authorElement.setAttribute ("person_id", str(author.person_id))
			if author.upid:
				authorElement.setAttribute ("upid", str(author.upid))
				
			# self.setText (authorElement, author)
			for attr in ['lastName', 'firstName', 'middleName', 'suffix']:
				if getattr (author, attr):
					XmlUtils.addChild (self.dom, attr, getattr (author, attr), authorElement)
				
		for field in other_fields:
			if field in self.data.keys():
				self.addChild (field, self.data[field])
				
	def addChild (self, tag, value):
		
		if value:
			element = self.addElement (self.doc, tag)
			self.setText (element, value and str(value) or "")
				

