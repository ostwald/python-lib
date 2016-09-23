"""
facet reader
"""
import os, sys, re
from ncar_lib.repository import SummarySearcher


baseUrl = 'http://dls-pyramid.dls.ucar.edu:8080/schemedit/services/ddsws1-1' # BSCS Merge DCS

host = os.environ['HOST']
# print 'host:', host

if host == 'purg.local':
	baseUrl = 'http://localhost:8070/curricula/services/ddsws1-1' # BSCS Merge DCS

class AssetUrlSummarySearcher (SummarySearcher):
	
	verbose = True

	def get_params(self, collection, xmlFormat):

		return {
			"q":'url:h*ccs.dls.ucar.edu/home/protected/*',
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky": collection,
			'facet' : 'on',
			'facet.category' : 'CCSAssetUrl',
			'facet.maxResults' : '10000'
		}


if __name__ == '__main__':
	assetCollections = ['comment_bscs', 'pbis-tips']
	assetCollections = []
	searcher = AssetUrlSummarySearcher (baseUrl=baseUrl, collection=assetCollections)
	faceted_fields = searcher.summary.faceted_fields
	
	print '%d faceted_fields' % len(faceted_fields)
	
	for faceted_field in faceted_fields:
		print '- %s (%d terms)' % (faceted_field.category, len(faceted_field.data))
		
	ccsAssetUrl_field = searcher.summary.getFacetedField("CCSAssetUrl")
	
	if (not ccsAssetUrl_field):
		print 'ccsAssetUrl_field not found'
	else:
		for facet in ccsAssetUrl_field.facets:
			# print facet.term
			pass
		
		
		
	# print searcher.responseDoc.selectSingleNode(searcher.responseDoc.dom, 'DDSWebService/Search/facetResults').toxml()
	# print searcher.responseDoc
