
"""
Get RecordIDs of searchResults
"""
from ncar_lib.repository import RepositorySearcher
from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

"""
Use search service to retrieve library_dc and perform tallies over them
"""

class IdGetter (RepositorySearcher):

	"""
	optimize RepositorySearcher to collect only RecordIds from search results
	"""
	
	numToFetch = 10000
	batchSize = 200
	
	def __init__ (self, collection=None, xmlFormat=None, baseUrl=default_baseUrl):
		RepositorySearcher.__init__ (self, collection, xmlFormat, baseUrl)
	
	def get_result_batch (self, start, num):
		responseDoc = self.get_response_doc (start, num)
		responseDoc.xpath_delimiter = ":"
		
		idNodes = responseDoc.selectNodes (responseDoc.dom, 'DDSWebService:Search:results:record:head:id')
		return map (lambda x:XmlUtils.getText(x), idNodes)
		
if __name__ == '__main__':

	xmlFormat = 'osm'
	collection = 'osgc'
	getter = IdGetter(collection, xmlFormat)
	print "%d ids gotten" % len(getter)

