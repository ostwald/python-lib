"""
does searches to find urls in the repo

"""
import os, sys, re
from repo import RepositorySearcher
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import base_protected_url, getAssetPath
from url_rewriting_records import urlRewritingRecordClasses

class URLSearcher (RepositorySearcher):
	"""
	A searcher for records having a protected Url
	"""
	
	# default_baseUrl = 'http://localhost:8070/curricula/services/ddsws1-1'
	# default_baseUrl = 'http://acornvm.dls.ucar.edu:27248/dcs/services/ddsws1-1' # CCS Catalog
	default_baseUrl = 'http://acornvm.dls.ucar.edu:8688/schemedit/services/ddsws1-1' # BSCS Merge DCS
	numToFetch = 10
	batchSize = 200

	def __init__ (self, collection=None, xmlFormat=None, baseUrl=None):
		self.formatTally = {}
		RepositorySearcher.__init__(self, collection, xmlFormat, baseUrl)

	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"q":'url:h*ccs.dls.ucar.edu/home/protected/*',
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky" : collection
			}
			
	def processResults(self):
		print 'processResults ...'
		formats = {}
		for result in self:
			xmlFormat = result.xmlFormat
			num = formats.has_key(xmlFormat) and formats[xmlFormat] or 0
			formats[xmlFormat] = num + 1
		self.formatTally = formats
		
	def reportFormatTally(self):
		keys = self.formatTally.keys()
		keys.sort()
		for key in keys:
			print '- %s - %d' % (key, self.formatTally[key])

if __name__ == '__main__':
	searcher = URLSearcher(xmlFormat=None)
	searcher.reportFormatTally()
	# print searcher[0].payload


