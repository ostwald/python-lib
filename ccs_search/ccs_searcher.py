"""
ccs-test searcher
"""
import sys, os, re
from ncar_lib import RepositorySearcher, SearchResult
from JloXml import XmlUtils

class PlaylistSearcher (RepositorySearcher):
	""" 
	find all playlists for given userId
	"""
	default_baseUrl = "http://acornvm.dls.ucar.edu:17248/dds/services/ddsws1-1"
	verbose = False

	def __init__ (self, userId):
		self.userId = userId;
		RepositorySearcher.__init__ (self)
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"xmlFormat": 'playlist',
			'q':'/key//playList/userID:"%s"' % self.userId
		}
	
class ResourceSearcher (RepositorySearcher):
	""" 
	find all resources with given resourceId
	"""
	default_baseUrl = "http://acornvm.dls.ucar.edu:17248/dds/services/ddsws1-1"
	verbose = False

	def __init__ (self, resourceIds):
		self.resourceIds = resourceIds;
		RepositorySearcher.__init__ (self)
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		
		query = " OR ".join (map (lambda x:'id:'+x, self.resourceIds))
		# query = 'idvalue:"%s"' % self.resourceIds[0]
		
		return {
			"verb": "Search",
			# "xmlFormat": 'dlese_anno',
			'q': query,
			'relation':'isAnnotatedBy'
		}
		
# http://acornvm.dls.ucar.edu:17248/dds/services/ddsws1-1?verb=Search&q=idvalue:%221332131902694%22&relation=isAnnotatedBy&s=0&n=10
# http://acornvm.dls.ucar.edu:17248/dds/services/ddsws1-1?q=idvalue:"1358749956407"&s=0&verb=Search&relation=isAnnotatedBy&xmlFormat=dlese_anno&n=1		
def getPlaylistIds (userId):
	results = PlaylistSearcher(userId)
	return map (lambda x:x.recId, results)
	
def getPlaylistResources (userId):
	"""
	return list of all resources found on playlists owned by userId
	"""
	results = PlaylistSearcher(userId)
	resourceIds = [];add=resourceIds.append
	for result in results:
		ids = result.payload.getValuesAtPath ("playList:items:item[@type='ccs_saved_resource']:id");
		for id in ids:
			if id not in resourceIds:
				add (id)
	return resourceIds
	
def getPlaylistResourceAnnotations (userId):
	"""
	returns the ids of annotations by user that annotate resources found on playlists
	"""
	resourceIds = getPlaylistResources (userId)
	resourceResults = ResourceSearcher (resourceIds)
	#print "%d resources found" % len (resourceResults)
	## print resourceResults[0]
	anno_ids = [];add=anno_ids.append
	for result in resourceResults:
		result.xpath_delimiter = '/'
		#print result.recId
		relations = result.selectNodes(result.dom, 'record/relations/relation/record')
		#print ' %d relations found' % len(relations)
		
		# now find the relation that is a annotationRecord and is contributed by our user
		for rel in relations:
			idPath = "metadata/annotationRecord/moreInfo/userSelection/user/userId"
			if XmlUtils.getTextAtPath (rel, idPath) == userId:
				anno_id = XmlUtils.getTextAtPath(rel, 'head/id')
				if not anno_id in anno_ids:
					add (anno_id)
	return anno_ids
			
if __name__ == '__main__':
	userId = '1288102553915'
	
	resourceIds = getPlaylistResources (userId)
	print "Resource Ids (%d)" % len(resourceIds)
	for id in resourceIds:
		print '- ', id
		
	annoIds = getPlaylistResourceAnnotations (userId)
	print "Annotation Ids (%d)" % len(annoIds)
	for id in annoIds:
		print '- ', id 
