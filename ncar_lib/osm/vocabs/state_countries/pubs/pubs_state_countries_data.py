import os, sys
from xls import WorksheetEntry, XslWorksheet
from UserDict import UserDict
from JloXml import XmlUtils
from xsd_globals import qp, XSD_PREFIX, XSD_NAMESPACE_URI, createSchemaElement
from annotated_xsd import AnnotatedVocabXSD, AnnotatedEnumerationType, AnnotatedVocabTerm

# template is "xsd"
import xsd_globals
xsd_globals.XSD_PREFIX = "xsd"
del xsd_globals

# ------- country codes -------------


class PubsCountry (WorksheetEntry):
	"""
	record from the country xsl
	"""
	def __init__ (self, textline, schema):
		WorksheetEntry.__init__ (self, textline, schema)
		self.code = self['Value']
		self.uiLabel = self['UI Label']
		
		# due to an error in creating the country-codes data, the 'Place Name' field is corrupt
		# and we must derive the place name from the uiLable field
		## self.name = self['Place Name']
		self.name = self.deriveName()
		
	def deriveName (self):
		"""
		uiLable has form "%s - %s" % (code, placename) 
		- NOTE: placename may also have hyphens!
		"""
		
		x = self.uiLabel.find('-')
		return self.uiLabel[x+1:].strip()

	def __cmp__ (self, other):
		return cmp(self.name, other.name)
		
class PubsCountryCodes (XslWorksheet):
	"""
	manages data from the country-codes spreadsheet
	"""
	linesep = "\n"
	default_path = 'pubs-data/country-codes.txt'
	
	def __init__ (self, path=None):
		path = path or self.default_path
		XslWorksheet.__init__ (self, entry_class=PubsCountry)
		self.read(path)
		self.sort()
		
	def getDataList (self):
		"""
		make data suitable for use by AnnotatedEnumerationType
		"""
		return map(lambda x: (x.code, x.name), self)
		

class CountryCodeMap (UserDict):
	"""
	provides indexing (by country code) into the pubs country code table
	"""
	
	def __init__ (self):
		UserDict.__init__ (self)
		country_codes_xsl = PubsCountryCodes()
		for entry in country_codes_xsl:
			self[entry.code] = entry
			
			
# ------- state prov stuff -------------
			
class PubsState (WorksheetEntry):
	"""
	One entry of the pubs state/prov vocab
	"""
	def __init__ (self, textline, schema):
		WorksheetEntry.__init__ (self, textline, schema)
		self.code = self['Value']
		self.uiLabel = self['UI Label']
		self.country_code = self.uiLabel.split('-')[0].strip()
		self.name = self['Place Name']
		
	def __cmp__ (self, other):
		return cmp(self.uiLabel, other.uiLabel)

class PubsStateCodes (PubsCountryCodes):
	"""
	list of all the items in the pubs state/prov vocab
	
	uses contryCodeMap to help build the "name" and "description" that are used in the 
	vocab String
	"""
		
	linesep = "\n"
	default_path = 'pubs-data/state-prov.txt'
	
	def __init__ (self, path=None):
		path = path or self.default_path
		XslWorksheet.__init__ (self, entry_class=PubsState)
		self.read (path)
		self.sort()
		
		self.countryCodeMap = CountryCodeMap()
		
	def report (self):
		"""
		run down the state/prov vocab items and print a string
		showing the "resolved" code and description for each
		"""
		current_cntry = None
		
		for entry in self:
			country_code = entry.country_code
			
			if not self.countryCodeMap.has_key (country_code):
				raise KeyError, "no country code map entry for '%s'" % counry_code
				
			country = self.countryCodeMap[country_code]
			
			if country_code != current_cntry:
				# print "** %s **" % self.makeTypeName (country.name)
				current_cntry = country_code
			
			# due to an error in creating the country-codes data, the "name" field is not reliable
			description = "%s, %s" % (entry.name, country.name)
			code = "%s-%s" % (country.code, entry.code)
		
	# def makeTypeName (self, country_name):
		# #capitalize the segments (but leave first segment lowercase)
		# segments = map (lambda x: x.capitalize(), country_name.split(" "))
		# segments[0] = segments[0].lower()
		# return "".join(segments) + "Type"
			
	def getDataList (self):
		"""
		make data suitable for use by AnnotatedEnumerationType
		"""
		dataList = []
		for entry in self:
			country_code = entry.country_code
			if not self.countryCodeMap.has_key (country_code):
				raise KeyError, "no country code map entry for '%s'" % counry_code
				
			country = self.countryCodeMap[country_code]
				
			# if country_code != current_cntry:
				# typeName = self.makeTypeName (country.name)
				# current_cntry = country_code
				# current_enum = getEnumerationTypeXml (typeName)
				# xsd.doc.appendChild (current_enum)
				
			description = "%s, %s" % (entry.name, country.name)
			code = "%s-%s" % (country.code, entry.code)
			
			dataList.append ([code, description])
			
		return dataList

def countryCodesTester ():
	pcc = PubsCountryCodes ()
	print 'read %d entries' % len(pcc)
	# print pcc.schema
	for entry in pcc.data:
		print "%s | %s | %s" % (entry.code, entry.uiLabel, entry.name)

		
def stateCodesTester ():
	psp = PubsStateCodes ()
	print 'read %d entries' % len(psp)
	if 1:
		print psp.schema
		for entry in psp.data[:10]:
			print "%s | %s | %s" % (entry.code, entry.country_code, entry.name)

	
if __name__ == '__main__':
	# stateCodesTester()
	countryCodesTester()
	# PubsStateCodes().report()

