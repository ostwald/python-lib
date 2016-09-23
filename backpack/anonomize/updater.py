"""
updater - for each user, find and update all records to anonymize
"""
import sys, os
from UserList import UserList
from ncar_lib.repository import RepositorySearcher, SearchResult
from recordsForUser import RecordsForUserSearcher
from dlese_anno_record import DleseAnnoRecord
from users import UserSearcher, UserInfo, makeUserInfo

class AnnoSearcherResult(SearchResult):
	"""
		in addition to fields exposed by SearchResult, exposes:
		payload is a DleseAnnoRecord instance
	"""
	default_payload_constructor = DleseAnnoRecord

	def __init__ (self, element, payload_constructor=None):
		SearchResult.__init__ (self, element, payload_constructor)

class UserAnnoSearcher (RepositorySearcher):

	default_baseUrl = "http://localhost:7248/dds/services/ddsws1-1"
	searchResult_constructor = AnnoSearcherResult
	filter_predicate = None
	verbose = False
	
	def __init__ (self, userInfo):
		RepositorySearcher.__init__ (self)
	
			
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		q = ''
		baseIndexField = '/key//annotationRecord/annotation/contributors/contributor/person'
		if self.userInfo.lastName:
			q = '%s/nameLast:"%s"' % (baseIndexField, self.userInfo.lastName)
		if self.userInfo.firstName:
			firstNameClause = '%s/nameFirst:"%s"' % (baseIndexField, self.userInfo.firstName)
			if q:
				q = '%s AND %s' % (q, firstNameClause)
			else:
				q = firstNameClause
		
		return {
			"verb": "Search",
			"format" : 'dlese_anno',
			'q' : q
			}

class Updater (UserList):
	"""
	create a mapping of userInfos (from existing to anonymized form)
	for each STUDENT user:
		anonymize names in user record
		anonymize names in annotation records
	"""
		
	def __init__ (self):
		self.data = [] # used to keep track of users searched
		self.users = UserSearcher()
		self.userInfos = map(makeUserInfo, map (lambda x:x.payload, self.users))
		self.userInfos.sort()
		
	def updateUsers(self):
		for user in self.users:
			# username = user.username
			username = user.lastName
			if username in unique_users:
				continue
			unique_users.append(username)
			results = RecordsForUserSearcher(username)
			if len(results) > 1:
				print '\n%s - %d results' % (username, len(results))
				for result in results:
					print '- %s (%s)' % (result.xmlFormat, result.recId)
					person = result.payload.getPerson(lastName='username')
					print person
			
	def updateUser(self, userInfo):
		
					
if __name__ == '__main__':
	updater = Updater()
	for user in updater.userInfos:
		print user
