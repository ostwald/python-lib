"""
query for any user saves by a given userId

when we "save" a resource, two things happen:

	note: paths below are relative to the base_dir of the UserContent repository 
	(which is a vanilla DDS repository file structure)

1 - a "CCS-Saved-DL-RESOURCE" record is created
	xmlFormat: ccs_saved_resource
	path e.g. -  /ccs_saved_resource/ccsselecteddlresources/CCS-SAVED-DL-RESOURCE-${recordId}
	collection: ccsselecteddlresources
	
2 - a "UserSave" record is created
	path: dlese_anno/ccsprivateannos/CCS-ANNO-RESOURCE-${userId}-CCS-SAVED-DL-RESOURCE-${resourceId} 
	xmlFormat: dlese_anno
	collection: ccsprivateannos
	
	
-----

In the context of the BSCS Merge - why bother with saved-resources? They are
independent of the user saves. Sure the userId is in the filename. Does this
matter?

	- use case: user has ccsUserId in CCS and bscsUserId in BSCS. We go with
	ccsUserId in the merge, and copy any user saves to CCS. The we have to move
	the saved-resource, too!
	
	- but as far as COUNTING - we only need count UserSaves
	
API
- getUserSaves (userId=None)
	if userId is None:
		return all userSaveRecords
	else:
		return all records for specified user
		
IMPLEMENTATiON
Extend Repository Searcher 

"""
import os, sys, re
from bscs import *
from repo import RepositorySearcher, SearchResult

class UserSaveSearcher (RepositorySearcher):
	
	verbose=0
	
	def __init__ (self, collection=None, userId=None, baseUrl=None):
		self.userId = userId
		RepositorySearcher.__init__(self, collection=collection, baseUrl=baseUrl)
	
	def get_params (self, collection, framework):
		"""
		define the params used to query the search service
		"""
		if self.verbose:
			print 'get_params'
			print '- collection:', collection
			print '- userId:', self.userId
		if self.userId:
			q = '/key//annotationRecord/moreInfo/userSelection/user/userId:%s' % self.userId
		else:
			q = None
		
		return {
			"verb": "Search",
			"ky": collection,
			"q" : q,
			"relation" : 'isAnnotatedBy'
			}

def TallyUserSaves (repoInfo):
	"""
	displays the userSave counts for the bscs_ccs_dup_users. these are saves that can potentially be messed up
	by merge. only if the index is counting on the userId to match that of the recordId...
	"""
	for userInfo in bscs_ccs_dup_users:
		searcher = UserSaveSearcher(baseUrl=repoInfo.baseUrl, collection="ccsprivateannos", userId=userInfo.id)
		print '%s (%s) - %d saves' % (userInfo.name, userInfo.id, len(searcher))


if __name__ == '__main__':
	ostwaldBSCS = "1311287237585"
	ostwaldCCS = "1247065132457"
	repoInfo = bscs_user_content
	if 1:
		searcher = UserSaveSearcher(baseUrl=repoInfo.baseUrl, collection="ccsprivateannos", userId=None)
		print '%d results' % len(searcher)
		print searcher.service_client.request.getUrl()
		for result in searcher:
			print ' - ', result.xmlFormat
	if 0:
		TallyUserSaves(repoInfo)
