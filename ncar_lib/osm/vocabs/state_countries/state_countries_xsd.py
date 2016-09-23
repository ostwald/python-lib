from ncar_lib.osm.vocabs.annotated_xsd import AnnotatedVocabXSD, AnnotatedVocabTerm, AnnotatedEnumerationType
from UserDict import UserDict

class ProvItemsMgr (UserDict):
	"""
	class to provide uniform access to lists from different sources
	(from xsd and from a xls)
	provides mapping from provCode to provItem
	- getProvItems (countryCode)
	- getProvItem (provCode)
	"""
	def __init__ (self):
		UserDict.__init__ (self)
		self.load()
		
	def load(self):
		"""
		populate the data structures
		"""
		raise NotImplementedError, "load"
		
	def getProvItems (self, country):
		"""
		getsProvItems for a specified country
		"""
		raise NotImplementedError, "getProvItems"
		
	def getProvItem (self, provCode):
		"""
		obtain the provItem for the specified provCode (e.g., 'US-CO')
		"""
		raise NotImplementedError, "getProvItem"
		
	def report (self):
		print "%s contains %d items" % (self.__class__.__name__,
										len(self))
		
class PubsItemsMgr (ProvItemsMgr):
	"""
	build mapping from provCode to provItem: self[provCode] = provItem
	also 
	 - contry code to vocabValue
	 - provTypeName to provItems
	"""
	def __init__ (self, xsd):		
		"""
		- xsd is a StateCountryVocabXSD instance which provides the items
		
		- provItemsMdr calls load()
		"""
		self.countryCodes = UserDict()
		self.provTypes = UserDict()
		self.xsd = xsd		
		ProvItemsMgr.__init__ (self)

		
	def load (self):
		"""
		obtain items from the pubs xsd file, and
		populate this class's data structures
		"""
		for vocab in self.xsd.getCountriesType().getValues():
			self.countryCodes[vocab.value] = vocab
			
		for vocab in self.xsd.getProvTypes():
			prov = ProvItems(vocab)
			self.provTypes[prov.name] = prov
			
			for provItem in prov.values():
				self[provItem.value] = provItem
			
	def getProvItems (self, countryTypeName):
		"""
		gets all items having supplied countryTypeName (e.g., 'austrailiaType'),
		which is how the pubs iems for a country are organized. 
		 
		note: it would be nice to never deal with the typeName - very ugly
		"""
		return self.provTypes[provTypeName].values()
		
	def getProvItem (self, provCode):
		"""
		obtain the provItem for the specified provCode (e.g., 'US-CO')
		"""
		return self[provCode]
				
	def report (self):
		print "%d items were read" % len(self)
		
		if 0:
			print "\nCountryCodes"
		for code in self.countryCodes.keys():
			print self.countryCodes[code]

		for provTypeName in self.provTypes.keys():
			self.provTypes[provTypeName].report()
			

		
class ProvItems (UserDict):
	"""
	convenience holder of a typeDef's items
	- e.g., from 'austaliaType' we would extract the australian provinces
	
	mapping interface: provItems['ER-JW'] -> vocabTerm
	"""
	def __init__ (self, typeDef):
		"""
		populate the data dict with vocabTerms contained by the provided TypeDef
		"""
		UserDict.__init__ (self)
		self.name = typeDef.name
		# print self.name
		for term in typeDef.getValues():
			self[term.value] = term
			
	def report (self):
		print "\n%s" % self.name
		for key in self.keys():
			print self[key]

class StateCountryVocabTerm (AnnotatedVocabTerm):
	"""
	we want to expose:
		provCode, countryCode, code, provName, countryname
	"""
	def __init__ (self, element=None, data=None):
		AnnotatedVocabTerm.__init__ (self, element, data)
		self.provCode = self.value
		self.countryCode = self.value.split('-')[0]
		# print self.description
		if ',' in self.description:
			self.countryName = self.description.split(',')[1].strip()
			self.provName = self.description.split(',')[0].strip()
		else:
			self.countryName = self.description.strip()
			self.provName = None
			
	def __repr__ (self):
		return "%s | %s | %s" % (self.provCode, self.provName, self.countryName)
			
class StateCountryEnumType (AnnotatedEnumerationType):
	"""
	extend AnnotatedEnumerationType to instantiate StateCountryVocabTerm
	instances
	"""
	vocabTerm_constructor = StateCountryVocabTerm
	
	def __init__ (self, element):
		AnnotatedEnumerationType.__init__(self, element)
		try:
			self.countryCode = self.getValues()[0].countryCode
		except:
			print "unable to get countryCode for %s" %  self.name
			self.countryCode = None
		# print "enumType %s has contry code: %s" % (self.name, self.countryCode)
		
class StateCountryVocabXSD (AnnotatedVocabXSD):
	"""
	class for modifying existing state-countries to match with
	the SO 3166-2 State Codes as found at 
	http://www.commondatahub.com/live/geography/state_province_region/iso_3166_2_state_codes
	"""
	xsd_template_path = 'xsd/pubs-state-countries.xsd'
	enumType_constructor = StateCountryEnumType
	dowrites = 0
	
	def __init__ (self, path=None):
		AnnotatedVocabXSD.__init__ (self, path)
		
	def getCountriesType (self):
		return self.getEnumerationType("countriesType")
		
	def getProvTypes (self):
		provs = []
		for typeDef in self.getEnumerationTypes():
			if typeDef.name != "countriesType":
				provs.append (typeDef)
		return provs

def getPubsItemsMgr(path=None):
	return PubsItemsMgr (StateCountryVocabXSD(path))
		
# ---------- TESTERS --------------
def showEnumTypes ():
	"""
	for each typeDef, print the vocab entries
	"""
	print "Showing all Enumeration Types"
	xsd = StateCountryVocabXSD()
	for typeDef in xsd.getEnumerationTypes():
		typeName = typeDef.name
		print '\n', typeName
		for vocab in typeDef.getValues():
			print " - ", vocab
	
def showProvTypes ():
	"""
	for each prof typeDef, print the vocab entries
	"""
	print "Showing all Prov Types"
	xsd = StateCountryVocabXSD()
	for typeDef in xsd.getProvTypes():
		typeName = typeDef.name
		print '\n', typeName
		for vocab in typeDef.getValues():
			# print " - ", vocab
			pass
			
def showCountryTerms ():
	xsd = StateCountryVocabXSD()
	# for vocab in xsd.getCountriesType().getValues():
		# print " - ", vocab
	cc = PubsItemsMgr (xsd)
	cc.report()
			
if __name__ == '__main__':
	# showCountryTerms ()
	# showProvTypes()
	# PubsItemsMgr(StateCountryVocabXSD()).getProvItems('australiaType').report()
	mgr = PubsItemsMgr(StateCountryVocabXSD())
	print 'there are %d provItems' % len(mgr)
