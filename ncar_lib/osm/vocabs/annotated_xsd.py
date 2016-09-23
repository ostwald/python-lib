"""

Reads and writes XSD files containing enumeration types with annotated values
	(see AnnotatedVocabTerm)

"""
# import xsd_globals
# xsd_globals.XSD_PREFIX = "xsd"

import os, sys
from xsd import VocabXSD, EnumerationType
from xsd_globals import qp, XSD_PREFIX, XSD_NAMESPACE_URI, createSchemaElement
from JloXml import XmlUtils

verbose = False

class AnnotatedVocabTerm:
	"""
	element is an enumeration element. 
	
	<xsd:enumeration value="AD">
		<xsd:annotation>
		<xsd:documentation>Andorra</xsd:documentation>
		</xsd:annotation>
	</xsd:enumeration>
	
	
	exposes two attributes:
		- value
		- description
	"""
	def __init__ (self, element=None, data=None):
		
		self.description_path = qp("annotation/documentation")
		
		if element is not None:
			# print "AnnotatedVocabTerm with element of type %s" % type(element)
			self.value = element.getAttribute("value")
			self.description = XmlUtils.getTextAtPath (element, self.description_path)
		if data is not None:
			self.value = data[0]
			self.description = data[1]

		# print "AnnotatedVocabTerm - value: %s, description: %s" % (self.value, self.description)
			
	def __repr__ (self):
		ret = "%s - %s" % (self.value, self.description)
		return ret.encode("utf-8")
		
	def toXml (self):
		"""
		return an "enumeration" element populated with code and description
		"""
		# enum = XmlUtils.createElement (qp("enumeration"), XSD_NAMESPACE_URI)
		enum = createSchemaElement("enumeration")
		enum.setAttribute ("value", self.value)
		
		anno = enum.appendChild (createSchemaElement("annotation"))
		
		doc = anno.appendChild(createSchemaElement("documentation"))
		## XmlUtils.setText (doc, unicode(self.description, 'utf-8')) # description is already unicode
		XmlUtils.setText (doc, self.description)
		
		return enum
		
class AnnotatedEnumerationType (EnumerationType):
	"""
	Extends EnuemerationType to manage AnnotatedVocabTerm
	as its values
	"""
	vocabTerm_constructor = AnnotatedVocabTerm
	
	def __init__ (self, element):
		EnumerationType.__init__(self, element)
		# print "instantiated AnnotatedEnumerationType for %s (%d items)" % (self.name, self.size())

	def clearValues (self):
		"""
		remove vocabs from this enumeration
		"""
		for child in XmlUtils.getChildElements(self.restriction):
			# self.clearElement (child)
			self.restriction.removeChild (child)
			child.unlink()
		
	def setValues (self, termList):
		"""
		set the vocab values to the provided list of values
		"""
		self.clearValues()
		for termData in termList:
			# term = self.vocabTerm_constructor (data=termData)
			# self.restriction.appendChild (term.toXml())
			self.addValue (termData)
			
	def addValue (self, termData):
		"""
		creates an VocabTerm with provided data (a map?)
		and then adds the avt (as xml) to this EnumerationType's
		restriction element
		"""
		vocabTerm = self.vocabTerm_constructor (data=termData)
		self.restriction.appendChild (vocabTerm.toXml())
			
	def getValues (self):
		"""
		return a list of vocab values (AnnotatedVocabTerms)
		defined in this enumeration
		"""
		# return map (lambda x:x.getAttribute('value'), self.terms)
		
		# we can't use terms, because it is a nodeList
		## - does XmlUtils.getChildElements work better?
		if not self.restriction:
			raise Exception, "self.restriction not found"
		
		# try:
			# print "self.restriction: %s" % XmlUtils.pp (self.restriction)
		# except:
			# print "getValues - self.restriction could not be printed: bailing"
			# sys.exit()
		
		return map (lambda x: self.vocabTerm_constructor(element=x), 
					XmlUtils.getChildElements(self.restriction))
		
class AnnotatedVocabXSD (VocabXSD):
	"""
	class responsible for creating and writing a vocab file in which
	the vocabTerms are annoated (they contain a value and a description).
	- e.g., "state-countries.xsd" 
	
	- reads in an  template file (default to state-countries.xsd)
	- the state-country xsd have two structural enhancements
	  over the vanilla single-enumeration xsd file (such as instDiv)
		1 - there may be several enumerationTypes defined in a single file
		2 - the vocabItems are *annoated* (by a desription) - see AnnotatedVocabTerm
	- writes new xsd to file
	
	"""
	xsd_template_path = '/Users/ostwald/devel/python-lib/ncar_lib/osm/vocabs/state_countries/xsd/state-countries-TEMPLATE.xsd'
	enumType_constructor = AnnotatedEnumerationType
	
	dowrites = 1

	def __init__ (self, path=None):
		path = path or self.xsd_template_path
		VocabXSD.__init__ (self, path)
		
		
# --------- TESTERS------------
def showEnumTypes (path):
	"""
	for each typeDef, print the vocab entries
	"""
	print "Showing all Enumeration Types"
	xsd = AnnotatedVocabXSD(path)
	for typeDef in xsd.getEnumerationTypes():
		typeName = typeDef.name
		print '\n%s (%s)' % (typeName, len (typeDef.getValues()))
		for vocab in typeDef.getValues():
			# print " - ", vocab
			pass

def addAnnotatedTermsTester ():
	"""
	assign a set of values to a enumerationType
	and print the values to confirm
	"""
	xsd = AnnotatedVocabXSD()
	typeName = "canadaType"
	data = [
		('one', 'the first number'), 
		('two', 'always in second place'),
		('three', 'the last one im gunna do')
	]
	
	xsd.setEnumerationValues(typeName, data)
	
	if 1: # confirm new values
		enums = xsd.getEnumerationValues(typeName)
		print "%d terms found" % len(enums)
		for term in enums:
			print term

if __name__ == '__main__':
	for path in [ 'state_countries/xsd/state-countries.xsd',
				  'state_countries/xsd/pubs-state-countries.xsd',
				  'state_countries/xsd/TEST-MERGED-STATE-COUNTRY.xsd']:
		showEnumTypes(path)
	# addAnnotatedTermsTester()

