"""
The following query finds all the records that are annotated/saved by ostwald. 
The if the relation='isAnnotedBy' params are included in the request url, the results
will include annotations - many annotations to one record.
The current user's annotation will be one of these

/relation.isAnnotatedBy//key//annotationRecord/moreInfo/userSelection/@selectedByUserId:"1247065132457"

Must the results be retreived (using above) and then processed again to find the user's record?
Or does it even matter?

"""
import os, sys, re
from user_content_searcher import DleseAnnoRecord, UserContentResult
from ncar_lib.repository import RepositorySearcher, SearchResult
from JloXml import MetaDataRecord, XmlUtils

ddswsBaseUrlForUserContent = "http://acorn.dls.ucar.edu:17248/dds/services/ddsws1-1"
purgBaseUrlForUserContent = "http://localhost:8070/dds/services/ddsws1-1"
ccsDevDDS = "http://acorn.dls.ucar.edu:17248/dds/services/ddsws1-1"

class UserContentTester (RepositorySearcher):
	
	default_baseUrl = purgBaseUrlForUserContent
	searchResult_constructor = UserContentResult
	
	verbose=True
	numToFetch=10000
	
	def __init__ (self, userId, recordId=None):
		self.userId = userId
		self.recordId = recordId
		collection = 'ccsprivateannos'
		xmlFormat = 'dlese_anno'
		if recordId:
			self.filter_predicate = self.recordId_filter
		self.get_params = self.get_test_params
		RepositorySearcher.__init__ (self, collection=collection, xmlFormat=xmlFormat, baseUrl=self.default_baseUrl)
		# print self.service_client.request.getUrl()
		
	def get_filtered(self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		start = "2012-05-01T00:00:00Z"
		end = "2012-05-20T00:00:00Z"
		query = '/text//annotationRecord/service/date/@modified:[%s TO %s]' % (start, end)
		
		return {
			'q' : query,
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky": collection,
			'sortDescending' : '/text//annotationRecord/service/date/@modified'
			}
			
	def get_test_params(self, collection, xmlFormat):
		
		query = '/relation.isAnnotatedBy//key//annotationRecord/moreInfo/userSelection/@selectedByUserId:"%s"' % self.userId
		
		print 'query: %s' % query
		return {
			'q' : query,
			"verb": "Search",
			# "xmlFormat": xmlFormat,
			# "ky": collection,
			'relation' : 'isAnnotatedBy'
			}		
		
	def recordId_filter (self, result):
		"""
		keep only records that ha
		"""
		selectPath = 'record:relations:relation:record:metadata:annotationRecord:moreInfo:userSelection:originalRecordId'
		originalRecordId = result.getTextAtPath(selectPath)
		# print ' filtering on ', originalRecordId
		return originalRecordId == self.recordId
			
def getSelectedUserResources (userId):
	"""
	returns a UserContentTester instance, which provides list api to results
	"""
	searcher = UserContentTester(userId=userId)
	# print searcher.data[0]
	print '%d results' % len(searcher)
	return searcher
	
def getUserResource (userId, recordId):
	"""
	Gets a resource that the user has saved.
	the provided recordId is for resource, not the userSelectionAnno
	Returns a UserContentResult, which contains a DleseAnnoRecord payload 
	"""
	searcher = UserContentTester(userId=userId, recordId=recordId)
	
	# print searcher.data[0]
	print '%d results' % len(searcher)
	if len(searcher) == 0:
		return None
	if len(searcher) == 1:
		# the result is a resource with annotations
		result = searcher[0]
		# print result
		return result
	raise Exception, "more than 1 result found for '%s'" % recordId
	
def getUserSelectionAnno (userId, recordId):
	result = getUserResource(userId, recordId)
	if result is None:
		raise Exception, "record not found for '%s'" % recordId
	
	# find the anno for this user
	selectPath = 'record:relations:relation:record:metadata:annotationRecord:moreInfo:userSelection:@selectedByUserId'
	relationAnnos = result.selectNodes(result.dom, 'record:relations:relation')
	print '%d relationAnnos' % len(relationAnnos)
	for anno in result.selectNodes(result.dom, 'record:relations:relation:record:metadata:annotationRecord'):
		itemID = XmlUtils.getTextAtPath(anno, 'itemID')
		print 'itemID', itemID
		print result.xpath_delimiter
		if userId == XmlUtils.getTextAtPath(anno, 'moreInfo:userSelection:@selectedByUserId', ':'):
			return DleseAnnoRecord(xml=anno.toxml())


def tester(userId):
	pass

			
if __name__ == '__main__':
	userId = "1247065132457"
	recordId = 'COMMENT-000-000-000-011'
	# getSelectedUserResources(userId)
	
	# result = getUserResource(userId, recordId)
	# print result
	anno = getUserSelectionAnno(userId, recordId)
	print anno
