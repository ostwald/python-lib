"""
Number of records in OpenSky, having a primaryAsset, status=Done, Refereed

/key//record/classify/classification:Refereed

Same count without asset 
"""
import sys, codecs
from UserList import UserList
from UserDict import UserDict
from JloXml import XmlUtils
from ncar_lib.repository import RepositorySearcher, OsmSearchResult

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class PeerReviewSearcher (RepositorySearcher):

	"""
	17362 osm framework and status=Done
	14415 osm, Done, Refereed
	
	for osgc (ky:osgc) 824 (now 825)
	
	"""
	
	numToFetch = 20
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	verbose = True
	
	def __init__ (self, collection=None, xmlFormat='osm', baseUrl=default_baseUrl):
		unique_titles = []
		RepositorySearcher.__init__ (self, collection, xmlFormat, baseUrl)
	
	def get_params (self, collection, xmlFormat):
		"""
		having a primaryAsset, status=Done, peer-reviewed
		"""
		q = '/key//record/classify/classification:Refereed'
		return {
			"verb": "Search",
			'dcsStatus':'Done',
			'q':q,
			'storedContent':['dcsstatus','dcsstatusNote'],
			'ky':'osgc',
			"xmlFormat": xmlFormat
		}
		
	def filter_predicate(self, result): 
		osm = result.payload
		hasAsset = False
		assetEl = osm.selectSingleNode (osm.dom, 'record/resources/primaryAsset')
		if assetEl:
			url = assetEl.getAttribute('url')
			hasAsset = url is not None and url.strip() != ""
		# print 'predicate returning %s' % (hasAsset)
		return hasAsset
		
	def processResults(self):
		pass
		

		
if __name__ == '__main__':
	
	searcher = PeerReviewSearcher()
	print '%d records found' % len(searcher)

