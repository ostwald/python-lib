"""
Figure out how to update the urls for bscs curriculum records using
the BSCS webservce.

But ACTUALLY do the update on the bscs repo on disk.

The records we are looking for only exist for certain frameworks
We only want to process certain collection (all that don't contain 'hsbio' in key)

ToDO: define acceptXmlFormat and acceptCollectionKey, then use them
from both webservice (to construct url) and repo approach (as filter)

xmlFormats = ['adn', 'nsdl_dc', 'dlese_anno', 'comm_anno']

BUT FIRST: see if all bscs urls are also protected. If this is the case
then we can wrap the url rewrite into the reorg code ...

"""
import os, sys, re
from UserDict import UserDict
from repo import RepositorySearcher
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from protected.url_records import urlRecordClasses, urlRewritingRecordFromSearchResult

class URLSearcher (RepositorySearcher):
	"""
	A searcher for records having a protected Url
	"""
	
	default_baseUrl = 'http://localhost:7148/dcs/services/ddsws1-1' # BSCS Merge DCS
	numToFetch = 10000
	batchSize = 200

	def __init__ (self, collection=None, xmlFormat=None, baseUrl=None):
		self.formatTally = {}
		self.records = {}
		self.bscs_urls = []
		RepositorySearcher.__init__(self, collection, xmlFormat, baseUrl)

	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		
		note: storedContent only gets first url
		"""
		return {
			"q":'url:h*bscs.dls.ucar.edu*',
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky" : collection,
			"storedContent" : "url"
			}
			
	def processResults(self):
		print 'processResults ...'
		formats = UserDict()
		records = UserDict()
		bscs_urls = []
		for result in self:
			xmlFormat = result.xmlFormat
			num = formats.has_key(xmlFormat) and formats[xmlFormat] or 0
			formats[xmlFormat] = num + 1
			record = urlRewritingRecordFromSearchResult(result)
			records[result.recId] = record
			for url in record.getProtectedUrls():
				if url not in bscs_urls:
					bscs_urls.append(url)
			
		self.formatTally = formats
		self.records = records
		self.bscs_urls = bscs_urls
		
	def reportFormatTally(self):
		keys = self.formatTally.keys()
		keys.sort()
		for key in keys:
			print '- %s - %d' % (key, self.formatTally[key])


if __name__ == '__main__':
	xmlFormat = "assessments"
	searcher = URLSearcher(xmlFormat=xmlFormat)
	# searcher.reportFormatTally()
	# print searcher[0].payload
	for record in searcher.records.values():

		print ' - %d protectedUrls' % len(record.getProtectedUrls())
		if len(record.getProtectedUrls()) > 1: break
	
	print 'NON-protected bscs_urls'
	for url in searcher.bscs_urls:
		if url.find('protected') == -1:
			print url
		
	print '%d records' % len(searcher.records.values())
	print '%d bscs_urls' % len(searcher.bscs_urls)


