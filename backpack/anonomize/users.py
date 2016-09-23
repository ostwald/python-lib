"""
Work with UserRecords on the Backpack DDS

User records are stored in the 'ccsusers' collection
"""
import sys, os
from ncar_lib.repository import RepositorySearcher, SearchResult
from JloXml import MetaDataRecord, XmlUtils

class UserInfo:
	
	def __init__ (self, firstName, lastName, username=None):
		self.firstName = firstName
		self.lastName = lastName
		self.username = username
		
	def __repr__ (self):
		return "%s %s (%s)" % (self.firstName, self.lastName, self.username)
		
	def __cmp__ (self, other):
		for attr in ['lastName', 'firstName', 'username']:
			c = cmp(getattr(self, attr), getattr(other, attr))
			if c != 0:
				return c
		return 0
		
def makeUserInfo (userDataRecord):
	rec = userDataRecord
	return UserInfo (rec.getFirstName(), rec.getLastName(), rec.getUsername())

class UserDataRecord (MetaDataRecord):
	"""
	the xmlFormat used to represent users in the CCS
	"""
	xpaths = {
		'id' : "java/object/void[@property='userId']/string",
		'firstName' : "java/object/void[@property='firstName']/string",
		'lastName' : "java/object/void[@property='lastName']/string",
		'username' : "java/object/void[@property='username']/string",
		'role' : "java/object/void[@property='roles']/array/void/string",
		'password' : "java/object/void[@property='password']/string"
	}
	
	xpath_delimiter = '/'
	id_path = "java/object/void[@property='userId']/string"
	
	def getFirstName(self):
		return self.get('firstName')
		
	def setFirstName(self, value):
		self.set('firstName', value)
		
	def getLastName(self):
		return self.get('lastName')
		
	def setLastName(self, value):
		self.set('lastName', value)
		
	def getUsername(self):
		return self.get('username')
		
	def setUsername(self, value):
		self.set('username', value)
		
	def report (self):
		rpt = '%s %s (%s) - %s' % (self.getFirstName(), self.getLastName(), self.getUsername(), self.getId())
		return '%s %s' % (rpt, self.getRoles())
		
	def getRoles (self):
		return XmlUtils.getValuesAtPath(self.dom, self.xpaths['role'])
		
	def getPassword (self):
		return self.get('password')
		
	def setPassword (self, value):
		self.set ('password', value)
		
class UserSearcherResult(SearchResult):
	"""
		in addition to fields exposed by SearchResult, exposes:
		- firstName
		- lastName
		- username
		- roles
		
		payload is a UserDataRecord instance
	"""
	default_payload_constructor = UserDataRecord

	def __init__ (self, element, payload_constructor=None):
		SearchResult.__init__ (self, element, payload_constructor)
		self.firstName = self.payload.getFirstName()
		self.lastName = self.payload.getLastName()
		self.username = self.payload.getUsername()
		self.roles = self.payload.getRoles()
		
	def __cmp__ (self, other):
		for attr in ['lastName', 'firstName', 'username']:
			c = cmp(getattr(self, attr), getattr(other, attr))
			if c != 0:
				return c
		return 0
	
class UserSearcher (RepositorySearcher):

	default_baseUrl = "http://localhost:7248/dds/services/ddsws1-1"
	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = UserSearcherResult
	filter_predicate = None
	# filter_predicate = lambda self, x:'teacher' in x.roles
	verbose = False
	
	def __init__ (self):
		# self.filter_predicate = self.isStudent
		# self.filter_predicate = self.isAdministrator
		RepositorySearcher.__init__ (self)
		self.data.sort()
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"ky" : 'ccsusers'
			}
			
	def isStudent (self, result):
		"""
		in backback, students have role of 'teacher'
		"""
		return 'teacher' in result.roles
		
	def isAdministrator (self, result):
		return 'administrator' in result.roles
		
class StudentSearcher (UserSearcher):
	filter_predicate = lambda self,result: 'teacher' in result.roles
			
def userDataRecordTester ():
	path = "/Users/ostwald/devel/python/python-lib/backpack/anonomize/user-record.xml"
	rec = UserDataRecord(path=path)
	# print rec.getId()
	# print rec.getTextAtPath("java/object/void[@property='email']/string")
	rec.setLastName ("myLASTname")
	rec.setFirstName ("myFOISTname")
	rec.setUsername ("myUSERNAME")
	print rec
	
def userSearcherTester ():
	searcher = StudentSearcher()
	for result in searcher:
		print result.payload.report()
	
if __name__ == '__main__':
	userDataRecordTester()
	# userSearcherTester()


