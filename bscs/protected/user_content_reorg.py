"""
Update protected URLs in UserContent records.

uses webservice to find protected urls in a User_Content repository, and
specifically in ccs_saved_resource records for:
- supplementary info such as Tips and Comments.
- curricular resources (i.e., Tasks)
- assessments

UserContentURLSearcher supports following actions:
- None or 'report' - populate self.protected with unique protectedUrls found and list them
- 'verify' - test each protectedUrl to see if the protectedAsset exists
- 'update' - update the protectedUrls and update metadata in user_content repo

"""
import os, sys, re
from repo import RepositorySearcher
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import *
from saved_resource_url_rewriting_records import savedResourceUrlRewritingClasses

import bscs.protected
bscs.protected.curriculum_view = "reorg"

class UserContentURLSearcher (RepositorySearcher):
	"""
	A RepositorySearcher for User_Content records having a protected Url
	
	This searcher only looks for ccs_saved_resources for dlese_anno curriculum
	resources, e.g., Tips.
	
	"""
	if os.environ['HOST'] == 'acornvm':
		default_baseUrl = 'http://acornvm.dls.ucar.edu:17248/dds/services/ddsws1-1' # ccs-test user content
		default_baseRepoUrl = 'http://acornvm.dls.ucar.edu:17248/dds/services/ddsupdatews1-1' # ccs-test user content repo update API
	elif os.environ['HOST'] == 'purg.local':
		default_baseUrl = 'http://localhost:8070/dds/services/ddsws1-1' # purg user content
		default_baseRepoUrl = 'http://localhost:8070/dds/services/ddsupdatews1-1' # purg user content repo update API
	
	batchSize = 200
	dowrites = 0
	numToFetch = 20000
	
	# url_path = '/savedResource/record/annotationRecord/annotation/content/url'
	# url_select_path = url_path
	xmlFormat = 'ccs_saved_resource'

	def __init__ (self, collection=None, baseUrl=None, action=None):
		self.protected = []
		self.action = action or 'report'
		print 'ACTION:', self.action
		print 'default_baseUrl:', self.default_baseUrl
		print 'default_baseRepoUrl:', self.default_baseRepoUrl
		xmlFormat = self.xmlFormat
		self.curriculumColl_path = '/savedResource/ddsRepoInfo/collectionKey'
		self.seenFormats = []
		RepositorySearcher.__init__(self, collection, xmlFormat, baseUrl)
		
		if self.action == 'report':
			self.reportUrls()

	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		
		sample records:
		saved nsdl_dc: CCS-SAVED-DL-RESOURCE-2200/20111120201316303T
		"""
		
		pathsToSearch = [
			'/savedResource/record/annotationRecord/annotation/content/url', # dlese_anno working
			'/savedResource/record/nsdl_dc/identifier', # nsdl_dc working
			'/savedResource/record/assessment/question/outline/@url', # assess_1
			'/savedResource/record/assessment/answer/outline/@url', # assess_2
		]
		
		query = '  OR '.join(map (lambda x:'indexedXpaths:%s' % x, pathsToSearch))
		print query
		return {
			"q": query,
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky" : collection
			}
			
	def processResults(self):
		"""
		what happens depends on value of self.action:
		- None or 'report' - populate self.protected with unique protectedUrls found
		- 'verify' - test each protectedUrl to see if the protectedAsset exists
		- 'update' - update the protectedUrls and update metadata in user_content repo
		"""
		print 'processResults ...'
		self.protected = []
		
		# look in each search result for protectedUrls
		for result in self:
			recId = result.recId
			coll = result.collection
			# savedXmlFormat = result.payload.getTextAtPath('savedResource/savedXmlFormat')
			savedXmlFormat = result.payload.getTextAtPath('savedResource:savedXmlFormat')
				
			if (savedXmlFormat in savedResourceUrlRewritingClasses.keys()):
				# xml = str(result.payload).encode('utf-8')
				recordXml = unicode (str(result.payload).decode('utf-8'))
				savedRecord = savedResourceUrlRewritingClasses[savedXmlFormat](recordXml)
			else:
				raise KeyError, 'unknown savedXmlFormat: %s' % savedXmlFormat
			
			if self.action == None or self.action == 'report':
				for url in savedRecord.getProtectedUrls():
					if not url in self.protected:
						self.protected.append(url)
			elif self.action == 'verify':
				# verify assets
				try:
					savedRecord.verifyAssets()
				except Exception, msg:
					print 'could not verify %s: %s' % (recId, msg)	
			elif self.action == 'update':
				if savedRecord.rewriteProtectedUrls():
					self.updateRecord (savedRecord)
			else:
				raise Exception, 'Process Results got unknown action: %s' % self.action
		
	def reportUrls(self):
		self.protected.sort()
		print '\n%d protected Urls' % len(self.protected)
		for url in self.protected:
			print '- %s' % (url)		

	def updateRecord (self, record):
		"""
		update the metadata record via DDSUpdateClient

		NOTE: should have exception handling
		"""
		if not self.dowrites:
			print 'would have updated', record.getId()
			return
			
		params = {
			'verb' : 'PutRecord',
			'id' : record.getId(),
			'collectionKey' : 'ccsselecteddlresources',
			'xmlFormat' : 'ccs_saved_resource',
			'recordXml' : str(record)
		}

		client = DDSUpdateClient(self.default_baseRepoUrl)
		response = client.getResponseDoc(params=params)
		# print 'RESPONSE for %s' % entry.id
		# print response
		print '- updated', record.getId()
	
	
def updateTester ():
	repoUpdateBaseUrl = 'http://localhost:8070/dds/services/ddsupdatews1-1' # purg user content repo update API
	recordXml = "<record><child>child text</child></record>"
	
	params = {
		'verb' : 'PutRecord',
		'id' : 'FAKE',
		'xmlFormat' : 'emaildata',
		'collectionKey' : 'ccsemails',
		'recordXml' : recordXml
	}
	client = DDSUpdateClient(repoUpdateBaseUrl)
	response = client.getResponseDoc(params=params)
	print 'RESPONSE:'
	print response

if __name__ == '__main__':
	# NOTE: you must reindex before verify will give meaningful results
	action =  'verify'  ## report, update, verify
	searcher = UserContentURLSearcher(action=action)


