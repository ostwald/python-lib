import os, sys
from JloXml import XmlRecord, XmlUtils
from xsd_globals import qp, XSD_PREFIX, XSD_NAMESPACE_URI, createSchemaElement

class EnumerationType:
	"""
	EnumerationTypes restrict (xsd-speaking) some simple type (e.g., xsd:string) by 
	expressng an eumeration of values
	"""
	def __init__ (self, element):
		self.element = element
		self.name = element.getAttribute ("name")
		self.restriction = XmlUtils.selectSingleNode (element, qp("restriction"))
		self.terms = XmlUtils.selectNodes (self.restriction, qp("enumeration"))
		# print "%d terms read for %s" % (len(self.terms), self.name)
		
	def __len__(self):
		return len(self.terms)
		
	def clearValues (self):
		"""
		remove all vocab terms
		"""
		for child in XmlUtils.getChildElements(self.restriction):
			# self.clearElement (child)
			self.restriction.removeChild (child)
			child.unlink()
		
	def setValues (self, valueList):
		"""
		set the vocab values to the provided list of values
		"""
		self.clearValues()
		for term in valueList:
			# child = XmlUtils.createElement (qp("enumeration"), XSD_NAMESPACE_URI)
			# child.setAttribute ("value", term)
			# self.restriction.appendChild (child)
			self.addValue(term)
			
	def getValues (self):
		"""
		return a list of vocab values defined in this enumeration
		"""
		return map (lambda x:x.getAttribute('value'), self.terms)
		
	def addValue(self, value):
		vocabTerm = XmlUtils.createElement (qp("enumeration"), XSD_NAMESPACE_URI)
		vocabTerm.setAttribute ("value", value)
		self.restriction.appendChild (vocabTerm)

			

class VocabXSD (XmlRecord):
	"""
	WARNING: this class assumes the xsd file constains enumeration definitions.
	- see enumeration_path & restriction_paths
	"""
	xpath_delimiter = "/"
	enumType_constructor = EnumerationType
	dowrites = False
	
	def __init__ (self, path=None, xml=None):
		if path:
			print "reading %s" % path
		XmlRecord.__init__ (self, path=path, xml=xml)

		import xsd_globals
		xsd_globals.XSD_PREFIX = self.root_name_space_prefix
		del xsd_globals
		
		# since these use XSD prefix - we define only after figuring out what it is..
		self.enumeration_path = qp("schema/simpleType/restriction/enumeration")
		self.restriction_path = qp("schema/simpleType/restriction")
		self._enumTypes = None
	
	def _get_typeDefs (self):
		return self.selectNodes (self.dom, qp("schema/simpleType"))
		
	def getEnumerationTypes (self):
		"""
		get the Enumeration Type defs defined in this XSD
		"""
		
		# print "getEnumerationTypes: enumTypes is %s" % type(self._enumTypes)
		
		if self._enumTypes is None:
			self._enumTypes = []
			for typeDef in self._get_typeDefs():
				# print "typeDef (%s) %s" % (type(typeDef), typeDef.getAttribute("name"))
				
				# we don't require any enums to be present
				if XmlUtils.selectSingleNode (typeDef, qp("restriction")):
					self._enumTypes.append (self.enumType_constructor (typeDef))
	
			if len(self._enumTypes) == 0:
				print "WARNING: getEnumerationTypes did not find any"
		return self._enumTypes
		
	def removeEnumerationTypes (self):
		"""
		removes all enumerationType elements from the doc
		"""
		parent = self.doc
		for enum in self.getEnumerationTypes():
			# self.clearElement (child)
			self.doc.removeChild (enum.element)
			enum.element.unlink()
		self._enumTypes = None
			
	def createEnumerationType (self, typeName):
		"""
		create a new EnumerationType instance (named for typeName)
		- enumType is NOT populated with values at this time
		""" 
		simpleType = createSchemaElement("simpleType")
		simpleType.setAttribute ("name",typeName)
		restriction = createSchemaElement("restriction")
		restriction.setAttribute ("base", qp("token"))
		simpleType.appendChild (restriction)
		return self.enumType_constructor (simpleType)
		
	def addEnumerationType (self, enumerationType):
		"""
		add provided EnumerationType 
		- append EnumerationType.element to the doc
		- reset self._enumTypes so they will be recalculated (picking up newly
		added enumType
		"""
		# print "\naddEnumerationType\n%s" % enumerationType.toprettyxml()
		
		# print "\n\nself.doc before adding enum\n%s" % XmlUtils.pp(self.doc) # self.doc.toprettyxml()
		self.doc.appendChild (enumerationType.element)
		# print "\n\nself.doc AFTER adding enum\n%s" % XmlUtils.pp(self.doc)
		self._enumTypes = None
		
	def getEnumerationType (self, typeName):
		"""
		we are looking for a EnumerationType with a 
			name attribute that matches provided typeName
		"""
		# print "\ngetEnumerationType (%s)" % typeName
		
		enumTypes = self.getEnumerationTypes()
		if not enumTypes:
			print "WARNING no enumerationTypes were found"
		for enumType in enumTypes:
			# print "enum: %s" % enumType.name
			if enumType.name == typeName:
				return enumType
	
	def getEnumerationValues (self, typeName):
		"""
		get the values from specified enum
		- finds the enumerationType for specified typeName
		- calls getValues method of enumerationType
		"""
		enum = self.getEnumerationType (typeName)
		if not enum:
			raise KeyError, "typeDef not found for %s" % typeName
			
		return enum.getValues()
				
	def setEnumerationValues (self, typeName, values):
		"""
		set the values of the specified enum
		- finds the enumerationType for specified typeName
		- calls setValues method of enumerationType
		
		-- values - either a flat list of values for simple enums, OR
		          - a list of value, description tuples for annotatedVocabs
		
		
		"""
		enum = self.getEnumerationType (typeName)
		if not enum:
			raise KeyError, "typeDef not found for %s" % typeName
		enum.setValues(values)
	
	def showValues (self, verbose=False):
		"""
		debugging utility
		"""
		for typeDef in self.getEnumerationTypes():
			print '\n** %s (%d terms) *' % (typeDef.name, typeDef.size())
			if verbose:
				for vocab in typeDef.getValues():
					print " - ", vocab
			
	def write (self, path, verbose=False):
		"""
		require a path so we don't tromp the template
		"""
		if self.dowrites:
			XmlRecord.write (self, path, verbose)
		else:
			print "WOULD have written to " + path
			
def getValuesTester (path, verbose=0):
	rec = VocabXSD (path=path)
	values = rec.getEnumerationValues()
	if verbose:
		print '%d instNames found' % len(values)
		for pn in values:
			print pn
	return values
	
def setValuesTester (path, values):
	rec = VocabXSD (path=path)
	rec.setEnumerationValues (values)
	return rec
	
def enumTester (path):
	rec = VocabXSD (path=path)
	enumTypes = rec.getEnumerationTypes()
	print len(enumTypes), ' enumTypes found'
	enumType = enumTypes[0]
	# print enumDef.toxml()
	# enum = EnumerationType (enumDef)
	enumType.setValues(["fee", "fii", "foo"])
	print rec
	
if __name__ == "__main__":
	path = "inst_div/xsd/instDivision.xsd"

	## rec = setInstNames (path, instNames)
	## print rec
	# getValuesTester (path, 1)
	# print setValuesTester (path, ["you", 'me', 'someoneelse'])
	enumTester (path)
	
