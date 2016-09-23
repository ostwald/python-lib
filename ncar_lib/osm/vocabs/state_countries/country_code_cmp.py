from prov_item_cmp import ProvItemCompareHelper, getPubsItemsMgr, DataHubItemsMgr
from state_countries_xsd_writer import StateCountriesXSDWriter, AnnotatedVocabXSD
from provName_normalizer import normalize
# from state_countries_xsd import getPubsItemsMgr

def firstTry ():
	helper = ProvItemCompareHelper()
	
	xsd = helper.pubsItemsMgr.xsd
	countriesType = xsd.getCountriesType()
	
	print "countriesType contains %d terms" % len(countriesType)
	
class CountryXsdWriter (StateCountriesXSDWriter):
	
	def __init__ (self, countryComparer):
		self.countryComparer = countryComparer
		AnnotatedVocabXSD.__init__ (self)
		self.removeEnumerationTypes()
		
		countriesType = self.makeCountriesEnumerationType()
		self.addEnumerationType (countriesType)


	def makeCountriesEnumerationType (self):
		"""
		create an EnuerationType for "countriesType"
		- populate it with info from the countryCodeMap
		"""
		# stub = getEnumerationTypeXmlStub ("countriesType")
		# countriesVocab = AnnotatedEnumerationType (stub)
		countriesType = self.createEnumerationType ("countriesType");
		
		self.setDataHubValues (countriesType)
		
		self.setPubsValues (countriesType)
			
		return countriesType

		
	def setDataHubValues (self, countriesType):
		hubCountryMap = self.countryComparer.hubMgr.countryMap
		print "%d unique hubs country codes" % len(hubCountryMap)
		
		dataList = [];add=dataList.append
		
		keys = hubCountryMap.keys()
		keys.sort()
		for hubCountry in keys:
			# hubCountry = hubCountry.encode()
			
			countryItem = self.countryComparer.getDataHubItem (hubCountry)
			# print countryItem.__class__.__name__
			
			code = normalize(countryItem.countryCode)
			name = normalize(countryItem.countryName)
			
			# add ((code, name))
			countriesType.addValue ((code, name))
			
			print "%s - %s" % (code, name)
		
	def setPubsValues (self, countriesType):
		"""
		we add the pubs that are not found in dataHub
		"""
		print "\nsetting hubs values"
		countryTerms = self.countryComparer.getCountriesType().getValues()
		countryTerms.sort(lambda a, b:cmp(a.countryCode, b.countryCode))
		for countryTerm in countryTerms:
			# print "\ncountry term: %s" % countryTerm
			code = normalize(countryTerm.countryCode)
			name = normalize(countryTerm.countryName)
			try :
				hubItem = self.countryComparer.getDataHubItem (code)
			except KeyError:
				countriesType.addValue ((code, name))
				print "%s - %s" % (code, name)
				
			
	def bogusSetCountryType (self):
		dataList = map (lambda a: (a.countryCode, a.countryName), countryTerms)
		xsdWriter.addCountriesEnumerationType (dataList)
		return xsdWriter
	
class CountryComparer:
	xsd_path = "merged/merged-state-countries.xsd"
	
	def __init__ (self):
		self.hubMgr = DataHubItemsMgr()
		self.xsdMgr = getPubsItemsMgr (self.xsd_path)
		self.xsdWriter = CountryXsdWriter (self)
	
	def getCountriesType (self):
		xsd_path = "merged/merged-state-countries.xsd"
		countriesType = self.xsdMgr.xsd.getCountriesType()
		# print "countriesType contains %d terms" % len(countriesType)
		return countriesType
		
	def getDataHubItem (self,countryCode):
		return self.hubMgr.getProvItems (countryCode)[0]

		
	def isMatch (self, vocabTerm, dataHubItem):
		
		codeMatch = vocabTerm.countryCode == dataHubItem.countryCode
		nameMatch = vocabTerm.countryName == dataHubItem.countryName
		
		return  codeMatch and nameMatch

	def comparePubs2Hubs (self):
		"""
		try to find a hubs entry for each pubs entry
		- notfound - pubs items that could not be found in dataHub countries
		- mismatches - pairs of pubs, hub items where the code is the same, but the
			countryName appears not to be the same). 
		NOTE: 
		- mismatch looks for exact matches, so these will have to be examined by hand
		- WRONG! mismatches are overridden by hub data, the "countryName of which 
		  then will have to be edited by hand"
		"""
		tries = 0
		notfound = []
		mismatches = []
		for countryTerm in self.getCountriesType().getValues():
			tries += 1
			# print "\ncountry term: %s" % countryTerm
			countryCode = countryTerm.countryCode
			
			try :
				hubItem = self.getDataHubItem (countryCode)
			except KeyError:
				notfound.append (countryTerm)
				continue
			
			hubName = hubItem.countryName
			termName = countryTerm.countryName
			
			if hubName != termName:
				mismatches.append ((countryTerm, hubItem))
				
		# Report
		if notfound or mismatches:
			 
			if notfound:
				print "\n%d pubs country codes were not found in data hub" % len (notfound)
				for item in notfound:
					print "- %s (%s)" % (item.countryCode, item.countryName)
					
			if mismatches and 0: 
				print "\n%d pubs country codes did not match their counterpart in data hub" % len (mismatches)
				for pair in mismatches:
					# print "- '%s\n  pubs - '%s'\n   hub - '%s'" % \
					print "- %s\n  pubs - %s\n   hub - %s" % \
						(pair[0].countryCode, pair[0].countryName, pair[1].countryName)
						
	def compareHubs2Pubs  (self):
		"""
		tries to match each hub item to a pubs item
		- notfound - hub items that had no counterpart in pubs
		NOTE: our policy is to use the hubs as authority, so we don't take
			action on "notfound"
		"""
		pubsCountryCodes = map (lambda x:x.countryCode, self.getCountriesType().getValues())
		print "%d pubs codes" % len(pubsCountryCodes)
		
		hubCountryMap = self.hubMgr.countryMap
		print "%d unique hubs country codes" % len(hubCountryMap)
		
		notfound = []
		
		keys = hubCountryMap.keys()
		keys.sort()
		for hubCountry in keys:
			hubCountry = hubCountry.encode()
			
			self.getDataHubItem (hubCountry)
			
			if hubCountry not in pubsCountryCodes:
				notfound.append(hubCountry)
				
		# report
		print ""
		if notfound:
			print "%d hubs country codes were not found in pubs countries" % len (notfound)
			for hubCountry in notfound:
				print "%s - %s" % \
				    (hubCountry, self.getDataHubItem (hubCountry).countryName)
		else:
			print "all hubs countries were found in pubs countries"
	
if __name__ == '__main__':
	cc = CountryComparer()
	# cc.comparePubs2Hubs ()
	## cc.compareHubs2Pubs ()
	# print cc.xsdWriter
	cc.xsdWriter.write ("xsd/merged-countries.xsd")
