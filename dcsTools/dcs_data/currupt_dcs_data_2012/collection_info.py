"""
compiles a mapping from collectionKey to collectionInfo for all collections
represented in a repostorie's collectionOfCollection records
"""
import os, sys, time, re
from JloXml import XmlUtils
from UserDict import UserDict
from ncar_lib import RepositorySearcher, SearchResult

class CollectionInfo (UserDict):
	"""
	cache a collection record and expose
	- title
	- key
	"""
	title_path = None
	key_path = None
	
	def __init__ (self, result):
		collectionRecord = result.payload
		self.title = XmlUtils.getTextAtPath (collectionRecord.dom, self.title_path);
		self.key = XmlUtils.getTextAtPath (collectionRecord.dom, self.key_path);
	
class NcarLibCollectionInfo (CollectionInfo):
	"""
	expose collectionInfo for NCAR Lib collection
	"""
	title_path = "collectionRecord/shortTitle"
	key_path = "collectionRecord/key"
	 
class NSDLCollectionInfo (CollectionInfo):
	"""
	expose collectionInfo for NSDL collection
	"""
	title_path = "record/general/title"
	key_path = "record/collection/ingest/oai/set/@setSpec"

class DleseCollectionInfo (CollectionInfo):
	"""
	expose collectionInfo for DLESE collection
	"""	
	title_path = "collectionRecord/general/shortTitle"
	key_path = "collectionRecord/access/key"
	 
class CollectionInfoSearcher (RepositorySearcher):
	"""
	Searches the collection of collection records and exposes
	"collections" as a mapping from collection id to collectionInfo
	"""
	batchSize = 500
	verbose = True
	collection_info_constructor = DleseCollectionInfo
	
	def __init__ (self, collection, xmlFormat, baseUrl):
		self.collections = UserDict()
		RepositorySearcher.__init__ (self, collection=collection, xmlFormat=xmlFormat, baseUrl=baseUrl)
		
	def get_paramsOFF(self, collection, xmlFormat):
		params = RepositorySearcher.get_params(self, collection, xmlFormat)
		for p in params:
			print '- %s: %s' % (p, params[p])
		return params
		
	def processResults (self):
		"""
		concrete classes should override this method to do some real processing
		"""
		for result in self:
			# print result
			# sys.exit()
			info = self.collection_info_constructor (result)
			self.collections[info.key] = info
			# print '- %s (%s)' % (info.title, info.key)
			# sys.exit()
			
	def getCollectionInfo (self, key):
		"""
		return collection info for specified collection
		"""
		print 'lookinfo for key:"%s"' % key
		if not self.collections.has_key(key):
			for key in self.collections.keys():
				print '- ', key
			return None
		return self.collections[key]
		
if __name__ == '__main__':
	baseUrl = "http://dcs.dlese.org/schemedit/services/ddsws1-1"
	CollectionInfoSearcher.collection_info_constructor = DleseCollectionInfo
	searcher = CollectionInfoSearcher("dcr", "", baseUrl)
	print "%d collections found" % len(searcher.collections)
