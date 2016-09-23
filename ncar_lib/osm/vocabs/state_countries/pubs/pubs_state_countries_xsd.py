import os, sys
from UserDict import UserDict
from JloXml import XmlUtils
from xsd_globals import qp, XSD_PREFIX, XSD_NAMESPACE_URI, createSchemaElement
from annotated_xsd import AnnotatedVocabXSD, AnnotatedEnumerationType, AnnotatedVocabTerm
from pubs_state_countries_data import PubsStateCodes
	
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
		

class PubsStateContriesXSDWriter (AnnotatedVocabXSD):
	
	def __init__ (self):
		AnnotatedVocabXSD.__init__ (self)
		self.removeEnumerationTypes()
		self.stateVocabs = PubsStateCodes ()
		self.countryCodeMap = self.stateVocabs.countryCodeMap
		
		# self.doc.appendChild (self.createCountriesTypeXml())
		
		self.addEnumerationType (self.makeCountriesEnumerationType())
		
		stateVocabs = self.getStateVocabs()
		print "%s stateVocabs found" % len(stateVocabs)
		
		# for stateVocab in stateVocabs:
			# self.addEnumerationType (stateVocab)

		map (self.addEnumerationType, stateVocabs)
			
	def getStateVocabs (self):
		"""
		build a list of EnumerationTypes, one for each country
		"""
		state_vocabs = []
		current_cntry = None
		current_vocab = None

		for termData in self.stateVocabs.getDataList():
		
			# termData[0] is state code, which as form "%s %s % (country_code, state_code)
			country_code = termData[0].split("-")[0]
			
			if not self.countryCodeMap.has_key (country_code):
				raise KeyError, "no country code map entry for '%s'" % counry_code
				
			country = self.countryCodeMap[country_code]
				
			if country_code != current_cntry:
				typeName = self.makeTypeName (country.name)
				current_cntry = country_code
				current_vocab = self.createEnumerationType (typeName)
				state_vocabs.append (current_vocab)

			current_vocab.addValue (termData)
		return state_vocabs

		
	def makeCountriesEnumerationType (self):
		"""
		create an EnuerationType for "countriesType"
		- populate it with info from the countryCodeMap
		"""
		# stub = getEnumerationTypeXmlStub ("countriesType")
		# countriesVocab = AnnotatedEnumerationType (stub)
		countriesVocab = self.createEnumerationType ("countriesType");
		country_codes = self.countryCodeMap.keys()
		country_codes.sort()
		dataList = map (lambda key: (key, self.countryCodeMap[key].name), country_codes)
		countriesVocab.setValues (dataList)
		return countriesVocab
		
	def makeTypeName (self, country_name):
		"""
		derive a type name from provided country_name
		- e.g., "United States" -> "unitedStatesType"
		"""
		#capitalize the segments (but leave first segment lowercase)
		segments = map (lambda x: x.capitalize(), country_name.split(" "))
		segments[0] = segments[0].lower()
		name = "".join(segments) + "Type"
		return unicode(name)

	
if __name__ == '__main__':

	outpath = "xsd/TEST-NEW-STATE-COUNTRY.xsd"
	xsd = PubsStateContriesXSDWriter()
	xsd.showValues()
	# print xsd
	xsd.write (outpath, verbose=True)

