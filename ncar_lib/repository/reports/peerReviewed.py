"""
Number of records in OpenSky, having a primaryAsset, status=Done, Refereed

/key//record/classify/classification:Refereed

Same count without asset 
"""
import sys, codecs
from UserList import UserList
from UserDict import UserDict
from JloXml import XmlUtils
from ncar_lib.repository import SummarySearcher

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class PeerReviewCounter (SummarySearcher):

	"""
	17362 osm framework and status=Done
	14415 osm, Done, Refereed
		618 havePrimaryAsset
		13796 do not have PrimaryAsset
	
	for osgc (ky:osgc) 824 (now 825)
		511 havePrimaryAsset
	
	"""
	
	verbose = True
	
	def __init__ (self, collection=None, xmlFormat='osm', baseUrl=default_baseUrl):
		SummarySearcher.__init__ (self, collection, xmlFormat, baseUrl)
	
	def get_params (self, collection, xmlFormat):
		"""
		having a primaryAsset, status=Done, peer-reviewed
		"""
		
		clauses = [
			'/key//record/classify/classification:Refereed',
			'indexedXpaths:"/record/resources/primaryAsset/@url"'
		]
		
		q = ' AND NOT '.join (clauses)
			
		return {
			"verb": "Search",
			'dcsStatus':'Done',
			'q':q,
			'storedContent':['dcsstatus','dcsstatusNote'],
			## 'ky':'osgc',
			"xmlFormat": xmlFormat
		}
		

		
if __name__ == '__main__':
	
	summary = PeerReviewCounter()
	print '%d records found' % summary.numRecords

