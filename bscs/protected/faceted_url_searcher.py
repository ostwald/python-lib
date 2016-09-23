"""
http://localhost:8080/schemedit/services/ddsws1-1?field=$facets&verb=ListTerms

"""
import os, sys, re
from url_searcher import URLSearcher
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import base_protected_url, getAssetPath

baseUrl = 'http://dls-pyramid.dls.ucar.edu:8080/schemedit/services/ddsws1-1' # BSCS Merge DCS

host = os.environ['HOST']
# print 'host:', host

if host == 'purg.local':
	baseUrl = 'http://localhost:8070/curricula/services/ddsws1-1' # BSCS Merge DCS

class FacetedURLSearcher (URLSearcher):
	
	numToFetch = 2
	verbose = True

	def get_params(self, collection, xmlFormat):
		params = URLSearcher.get_params(self, collection, xmlFormat)
		
		params.update ( {
				'facet' : 'on',
				'facet.category' : 'CCSAssetUrl',
				'facet.maxResults' : 1000
		});
		
		return params

if __name__ == '__main__':
	
	assetCollections = ['comment_bscs', 'pbis-tips']
	assetXmlFormats = ['adn', 'dlese_anno', 'ncs_item', 'assessments']

	searcher = FacetedURLSearcher(collection=assetCollections)
	searcher.reportFormatTally()
	print searcher.service_client.request.getUrl()



