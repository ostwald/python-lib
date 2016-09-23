""" 
getUserInfo - obtain userInfo from a UserContent repository using webservices,
and write the userInfo to disk where it can be processed by other modules
such as user_info_set.py

files to generate:
	BSCS | CCS
		- userInfo

UserInfo is 

User1Id	User1Name
User2Id	User2Name
...
User2Id	User2Name

"""
import os, sys
from repo import *
from bscs import *

from JloXml import XmlUtils
		
class UserInfoSearchResult (SearchResult):
	
	def __init__ (self, element, payload_constructor=None):
		SearchResult.__init__(self, element, payload_constructor)
		self.username = self.getUsername()
		
	def getUsernameWorks(self):
		nodes = self.payload.selectNodes(self.payload.dom, 'java:object:void')
		for node in nodes:
			print 'property: ', node.getAttribute('property')
			if node.getAttribute('property') == 'username':
				print node.toxml()
				username = XmlUtils.getTextAtPath(node, 'string')
				return username
		return 'unknown'
		
	def getUsername(self):
		return self.payload.getTextAtPath("java:object:void[@property='username']:string")
	
	def report(self):
		print self.recId, self.collection, self.xmlFormat

class UserInfoSearcher (RepositorySearcher):
	
	# numToFetch = 10
	searchResult_constructor = UserInfoSearchResult


def getUserInfo (repo):
	"""
	get userInfo defined by repo (ccsusers collection) using
	UserInfoSearcher
	"""
	try:	
		results = UserInfoSearcher(collection="ccsusers", baseUrl=repo.baseUrl)
	except Exception, msg:
		raise Exception, "Error: getUserInfo could not get info from %s: %s" % (repo.baseUrl, msg)
	
	info = map (lambda x:x.recId+'\t'+x.getUsername(), results)
	info.sort()
	return info 

def writeUserInfo (repo, filename, collection=None, xmlFormat=None):
	info = getUserInfo(repo)
	baseCacheDir = os.path.join('id_cache', repo.name.split('_')[0])
	path = os.path.join (baseCacheDir, filename)
	fp = open(path, 'w')
	fp.write ('\n'.join(info))
	fp.close() 
	print 'wrote to', path 
	
def cacheUserInfo (repo):
	"""
	get userInfo defined by repo (ccsusers collection),
	and write data to "id_cache" on disk in ccsusers.text
	"""
	collection = 'ccsusers'
	filename = "userInfo.txt"
	writeUserInfo(repo, filename, collection)	
	
def reportDupUserNames (repo):
	
	print "REPO.baseUrl", repo.baseUrl
	results = UserInfoSearcher(collection="ccsusers", baseUrl=repo.baseUrl)
	print '%d entries found' % len(results)
	
	# find dups within a repo's user
	dups=[]
	usernames=[]
	for result in results:
		username = result.username
		if not username in usernames:
			usernames.append(username)
		else:
			dups.append(username)
			
	print "%d Unique usernames" % len(usernames)
	print "Duplicates (%d)" % len(dups)
	for dup in dups:
		print " - ", dup
	

if __name__ == '__main__':

	repo = bscs_user_content  # remote - bscs server (reqires tunnel)
	# repo = ccs_curriculum # production
	if 0:
		print "REPO.baseUrl", repo.baseUrl
		results = UserInfoSearcher(collection="ccsusers", baseUrl=repo.baseUrl)
		print '%d entries found' % len(results)
		payload = results[0].payload

	if 1:
		reportDupUserNames(repo)
		
	if 0:
		info = getUserInfo(repo)
		print '%d entries found' % len(info)
		for entry in info:
			print '- ' + entry
	if 0:
		cacheUserInfo(repo)

