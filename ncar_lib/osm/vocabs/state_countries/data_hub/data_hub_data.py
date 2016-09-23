"""
read Data Hub data from a spreadsheet - this is at the level
of provItems in state_countries_xsd.py
"""

import os, sys
from xls import WorksheetEntry, XslWorksheet
from UserDict import UserDict
from JloXml import XmlUtils
from ncar_lib.osm import vocabs

from ncar_lib.osm.vocabs.xsd_globals import qp, XSD_PREFIX, XSD_NAMESPACE_URI, createSchemaElement
from ncar_lib.osm.vocabs.annotated_xsd import AnnotatedVocabXSD, AnnotatedEnumerationType, AnnotatedVocabTerm
from ncar_lib.osm.vocabs.state_countries.state_countries_xsd import ProvItemsMgr

# template is "xsd"
from ncar_lib.osm.vocabs import xsd_globals
xsd_globals.XSD_PREFIX = "xsd"
del xsd_globals

class DataHubProvItem (WorksheetEntry):
	"""
	record from the data hub xsl
	codes are of the form "%s-%s" % (countryCode, provCode)
	"""
	def __init__ (self, textline, schema):
		WorksheetEntry.__init__ (self, textline, schema)
		self.countryName = self['Country Name']
		self.provCode = self['ISO 3166-2 Sub-division/State Code']
		self.provName = self['ISO 3166-2 Subdivision/State Name']
		self.countryCode = self.provCode.split('-')[0]
		self.provOnlyCode = self.provCode.split('-')[1]

	def __cmp__ (self, other):
		return cmp(self.provCode, other.provCode)
	
	def __repr__ (self):
		return "%s | %s | %s" % (self.provCode, self.provName, self.countryName)


class DataHubWorksheet (XslWorksheet):
	"""
	list of all the items in the pubs state/prov vocab
	
	uses contryCodeMap to help build the "name" and "description" that are used in the 
	vocab String
	"""
		
	linesep = "\n"
	default_path = '/Users/ostwald/devel/python-lib/ncar_lib/osm/vocabs/state_countries/data_hub/data_hub_data/cdh_download_07_15_2010.txt'
	
	def __init__ (self, path=None):
		path = path or self.default_path
		XslWorksheet.__init__ (self, entry_class=DataHubProvItem)
		self.read (path)
		self.sort()
		
			
class DataHubItemsMgr (ProvItemsMgr):
	"""
	maps provCode to provItem for all items in dataHub worksheet
	- countryMap organizes the provItems by country (contryCode -> [provItems])
	"""
	def __init__ (self):
		"""
		ProItemsMgr calls self.load()
		"""		
		self.xls = DataHubWorksheet()
		self.countryMap = UserDict() # holds all provItems for given country (key is country code)

		ProvItemsMgr.__init__ (self)


	def load(self):
		"""
		obtain items from the data hub xls and
		populate this class's data structures
		"""
		for provItem in self.xls:
			self[provItem.provCode] = provItem
			country_code = provItem.countryCode
			countryProvItems = None
			if self.countryMap.has_key(country_code):
				countryProvItems = self.countryMap[country_code]
			else:
				countryProvItems = UserDict()
				self.countryMap[country_code] = countryProvItems
			countryProvItems[provItem.provCode] = provItem
			
	def getProvItem (self, provCode):
		"""
		get the provItem for specified provCode (e.g. 'US-CO')
		"""
		return self[provCode]
		
	def getProvItems (self, countryCode):
		"""
		get all the provItems having specified country code
		"""
		return self.countryMap[countryCode].values()
			
def stateCodesTester ():
	psp = DataHubWorksheet ()
	print 'read %d entries' % len(psp)
	if 1:
		# print psp.schema
		for entry in psp.data[:10]:
			print "%s | %s | %s" % (entry.provCode, entry.countryCode, entry.provName)

	
if __name__ == '__main__':
	# stateCodesTester()
	provItems = DataHubItemsMgr()
	for provItem in provItems.getProvItems('AF'):
		print provItem

