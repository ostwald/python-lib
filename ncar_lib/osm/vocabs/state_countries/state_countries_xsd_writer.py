import os, sys
from UserDict import UserDict
from JloXml import XmlUtils, PrettyPrinter
from ncar_lib.osm.vocabs.xsd_globals import qp, XSD_PREFIX, XSD_NAMESPACE_URI, createSchemaElement
from ncar_lib.osm.vocabs.annotated_xsd import AnnotatedVocabXSD, AnnotatedEnumerationType, AnnotatedVocabTerm
	
def getEnumerationTypeXmlStub (typeName):
	"""
	create a new enumerationType definition (named for typeName)
	enum is NOT populated with values at this time
	""" 
	simpleType = createSchemaElement("simpleType")
	simpleType.setAttribute ("name",typeName)
	restriction = createSchemaElement("restriction")
	restriction.setAttribute ("base", qp("token"))
	simpleType.appendChild (restriction)
	return simpleType
		

class StateCountriesXSDWriter (AnnotatedVocabXSD):
	
	def __init__ (self):
		AnnotatedVocabXSD.__init__ (self)
		self.removeEnumerationTypes()
		
	def addCountryType (self, typeName, dataList):
		countryEnumType = self.createEnumerationType (typeName);
		for item in dataList:
			countryEnumType.addValue (item)
		self.addEnumerationType (countryEnumType)
		
	def addCountriesEnumerationType (self, dataList):
		"""
		create an EnuerationType for "countriesType"
		- populate it from the dataList
		"""
		# stub = getEnumerationTypeXmlStub ("countriesType")
		# countriesVocab = AnnotatedEnumerationType (stub)
		countriesVocab = self.createEnumerationType ("countriesType");
		# country_codes = self.countryCodeMap.keys()
		# country_codes.sort()
		# dataList = map (lambda key: (key, self.countryCodeMap[key].name), country_codes)
		countriesVocab.setValues (dataList)
		self.addEnumerationType (countriesVocab)
		return countriesVocab

	def write (self, path):
		f = open(path, 'w') # don't mess with encoding here
		try:
			f.write (self.__repr__())
			## self.dom.writexml (f, encoding="UTF-8")
			print "wrote to " + path
		except:
			print "XmlRecord write error: %s \n\t(%s)" % (sys.exc_info()[1],
														  path)
		f.close()
		pp = PrettyPrinter (path)
		pp.write(path)
	
if __name__ == '__main__':

	outpath = "xsd/TEST-MERGED-STATE-COUNTRY.xsd"
	xsd = StateCountriesXSDWriter()
	xsd.showValues()
	# print xsd
	xsd.write (outpath)

