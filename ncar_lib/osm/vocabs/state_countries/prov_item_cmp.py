from state_countries_xsd import PubsItemsMgr, getPubsItemsMgr
from data_hub import DataHubItemsMgr
from provName_normalizer import normalizeProvItem
from UserList import UserList
from state_countries_xsd_writer import StateCountriesXSDWriter

verbose = 0

class ProvItemCompareHelper:
	
	def __init__ (self):
		self.pubsItemsMgr = getPubsItemsMgr()
		print 'pubsItemsMgr has %d provItems' % len(self.pubsItemsMgr)
		
		self.dataHubItemsMgr = DataHubItemsMgr()
		print 'dataHubItemsMgr has %d provItems' % len(self.dataHubItemsMgr)
			
		self.xsdWriter = self.getXsdWriter()
		
	def getXsdWriter (self):
		xsdWriter = StateCountriesXSDWriter()
		
		# set CountriesType
		countryTerms = self.pubsItemsMgr.countryCodes.values()
		
		print "setXsdCountriesType: countriesTerms are of type %s" % \
			countryTerms[0].__class__.__name__
		
		dataList = map (lambda a: (a.countryCode, a.countryName), countryTerms)
		xsdWriter.addCountriesEnumerationType (dataList)
		return xsdWriter
		
	def getXsdItem (self, provCode):
		if self.pubsItemsMgr.has_key (provCode):
			return self.pubsItemsMgr[provCode]

	def getXsdProvTypes (self):
		return self.pubsItemsMgr.xsd.getProvTypes()
		
	def getXsdProvType (self, provTypeName):
		return self.pubsItemsMgr.xsd.getEnumerationType (provTypeName)
			
	def getDataHubItem (self, provCode):
		if self.dataHubItemsMgr.has_key (provCode):
			return self.dataHubItemsMgr[provCode]
	
	def getDataHubItems (self, countryCode):
		return self.dataHubItemsMgr.getProvItems(countryCode)
			
	def scanXsdItems (self, xsdItems, callback):
		print 'scanXsdItems (%s) got %d items' % (type (xsdItems), len(xsdItems))
		for xsdItem in xsdItems:
			callback(xsdItem, self)
			
class ComparisonList (UserList):
	"""
	items are "provItems" having
		 - provName, provCode, countryName, countryCode
	provide mapping for addressing:
	     - getItemByProvName, getItemByProvCode
	"""
	def __init__ (self, data=None):
		"""
		init is handed a list of provItems (obtained from either 
			- data_hub_item_mgr or
			- state_countries_xsd
		"""
		UserList.__init__ (self, data)
		self.provNameMap = {}
		self.provCodeMap = {}
			
		for provItem in self:
			old = provItem.provName
			provItem = normalizeProvItem (provItem)
			if old != provItem.provName:
				# print "%s was normalized" % provItem.provName
				pass
			self.provNameMap[provItem.provName.lower()] = provItem
			self.provCodeMap[provItem.provCode] = provItem
			
		self.sort (lambda a, b: cmp(a.provCode, b.provCode))
		
	def report (self):
		for item in self:
			print item
			
	def getItemByProvName (self, provName):
		key = provName.lower()
		if self.provNameMap.has_key(key):
			return self.provNameMap[key]
			
	def getItemByProvCode (self, provCode):
		if self.provCodeMap.has_key(provCode):
			return self.provCodeMap[provCode]		
	
	def getMatch (self, item, other):
		
		provCodeMatch = other.getItemByProvCode (item.provCode)
		provNameMatch = other.getItemByProvName (item.provName.lower())
		
		return provCodeMatch or provNameMatch
			
	def compare (self, other):
		print "comparing self (%s) against %s" % (self.__class__.__name__,
												  other.__class__.__name__)
	def getDataList (self):
		return map (lambda item: (item.provCode, "%s, %s" % (item.provName, item.countryName)), self)
												  
												  
class DataHubItems (ComparisonList):
	def compare (self, other):
		print "comparing dataHubs to pubs"
		tries = 0
		matches = 0
		for item in self:
			tries += 1
			if self.getMatch (item, other):
				matches += 1
		print " ... %d/%d matches - %d items would be added to pubs" % (matches, tries, tries-matches)
		
	def merge (self, other):
		"""
		nothing done here. pubs injects its non-matching items into this list
		"""
		pass
				

class PubsItems (ComparisonList):
	def compare (self, other):
		print "comparing pubs to dataHub"
		tries = 0
		matches = 0
		misses = []
		for item in self:
			tries += 1
			if self.getMatch (item, other):
				matches += 1
			else:
				misses.append (item)
		print " ... %d/%d matches - %d items need to be checked (and possibly deleted)" % (matches, tries, tries-matches)
		if misses:
			for miss in misses:
				print ' - %s' % miss
			
	def merge (self, other):
		"""
		just add all the pubsItems that can't be matched to this list
		and return a "dataList" that can be fed into the xsd_writer
		"""

		tries = 0
		merges = []
		for item in self:
			tries += 1
			if not self.getMatch (item, other):
				other.append (item)
				merges.append (item)
				
		if verbose:
			if merges:
				print "%d/%d pubs items could not be matched and were merged" % (len (merges), tries)
				for item in merges:
					print item
			else:
				print "all %d pubs items had matches in dataHubList" % tries
		
		
class CountryProvItemsCompare:
	"""
	compares two lists of provItems for a given country, 
	 - lists: pubs and dataHub
	"""
	
	def __init__ (self, countryTypeName, helper=None):
		self.helper = helper or ProvItemCompareHelper()
		self.countryTypeName = countryTypeName
		self.pubsCountryType = self.helper.getXsdProvType(self.countryTypeName)
		self.pubsItems = self.getPubsItemList()
		self.countryCode = self.pubsCountryType.countryCode
		self.dataHubItems = self.getDataHubItemList()
		
		print '\n%s - %d pubs items, %d datahub items' % (self.countryTypeName, len (self.pubsItems), len (self.dataHubItems))
		
		self.execute ()

	def execute(self):
		self.compare()
		
	def compare (self):
		self.pubsItems.compare (self.dataHubItems)
		self.dataHubItems.compare (self.pubsItems)
		
	def getPubsItemList (self):
		# make list to operate over
		items = self.pubsCountryType.getValues()
		items.sort (lambda a, b: cmp(a.provCode, b.provCode))
		
		if verbose:
			print "%d pubs items found (%s)" % (len (items), items[0].__class__.__name__)
			for provItem in items:
				print provItem

		return PubsItems (items)
			
	def getDataHubItemList(self):
		# print "\nprocessing dataHub items for %s" % self.countryCode
		items = self.helper.getDataHubItems (self.countryCode)
		
		# print "%d raw items" % len (items)
		dataHubItems = DataHubItems (items)
		
		if verbose:
			print "%d datahub items found (%s)" % (len (dataHubItems), dataHubItems[0].__class__.__name__)
			for provItem in dataHubItems:
				print provItem
				
		return dataHubItems
		
class CountryProvItemsMerge (CountryProvItemsCompare):
	
	def __init__ (self, countryTypeName, helper=None):
		CountryProvItemsCompare.__init__ (self, countryTypeName, helper)
		
	def execute (self):
		self.merge()
			
	def merge (self):
		# print "\npubsItems before merge"
		# self.pubsItems.report()
		self.pubsItems.merge (self.dataHubItems)
		# print "\nafter merge there are %d dataHubItems" % len (self.dataHubItems)
		# self.dataHubItems.report()
		dataList = self.dataHubItems.getDataList()
		# print "dataList"
		#for item in dataList:
		#	print " %s - %s" % (item[0], item[1])
		
		self.helper.xsdWriter.addCountryType(self.countryTypeName, dataList)
		# print "xsdWriter after adding %s" % (self.countryTypeName)
		# print self.helper.xsdWriter	
		
def compareAll (helper=None):
	helper = helper or ProvItemCompareHelper()
	for provType in helper.getXsdProvTypes():
		CountryProvItemsCompare(provType.name, helper)
		
def mergeAndWrite (helper=None):
	helper = helper or ProvItemCompareHelper()
	for provType in helper.getXsdProvTypes():
		CountryProvItemsMerge(provType.name, helper)
		
	helper.xsdWriter.write ("xsd/TEST-MERGED-STATE-COUNTRY.xsd")
		
if __name__ == '__main__':
	# mergeAndWrite ()
	compareAll()
	
	if 0:
		helper = ProvItemCompareHelper()
		print (helper.xsdWriter)
	# CountryProvItemsCompare("newZealandType")
	# CountryProvItemsMerge("newZealandType")
	

	

