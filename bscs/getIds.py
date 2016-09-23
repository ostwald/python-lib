""" 
getIds - obtain Ids from a UserContent repository using webservices,
and write the Ids to disk where they can be processed by other modules
such as idSet.py

files to generate:
	BSCS | CCS
		- userIds
		- playlistIds
		- resourceIds (we are only interested in user-contributed)

"""
import os, sys
from repo import *
from bscs import *

class IDSearchResult (SearchResult):
	
	def report(self):
		print self.recId, self.collection, self.xmlFormat

class IDSearcher (RepositorySearcher):
	
	searchResult_constructor = IDSearchResult
	# numToFetch = 50
	

def getIds (repo, collection=None, xmlFormat=None):
	"""
	return the Ids defined in the specified repo for specified
	collection and xmlFormat. If collection and xmlFormat are not specified,
	all Ids are returned
	"""
	results = IDSearcher(collection, xmlFormat, repo.baseUrl)
	ids = map (lambda x:x.recId, results)
	ids.sort()
	return ids

def cacheIds (repo, filename, collection=None, xmlFormat=None):
	"""
	getIds defined by repo for specified collection and xmlFormat,
	and write Id data to "id_cache" on disk in specified filename
	"""
	ids = getIds(repo, collection, xmlFormat)
	baseCacheDir = os.path.join('id_cache', repo.name.split('_')[0])
	path = os.path.join (baseCacheDir, filename)
	fp = open(path, 'w')
	fp.write ('\n'.join(ids))
	fp.close()
	print 'wrote to', path
	
def cacheUserIds (repo):
	"""
	cache Ids in the specified repo for the ccsusers collection
	"""
	xmlFormat = 'userdata'
	collection = 'ccsusers'
	filename = "userIds.txt"
	cacheIds(repo, filename, collection, xmlFormat)	
	
def cacheResourceIds (repo):
	"""
	cache Ids in the specified repo for the ccsusersubmittedresources collection
	"""
	collection = 'ccsusersubmittedresources'
	filename = "submittedResourceIds.txt"
	cacheIds(repo, filename, collection=collection)	
	
def cachePlaylistIds (repo):
	"""
	cache Ids in the specified repo for the ccsplaylists collection
	"""
	collection = 'ccsplaylists'
	filename = "playlistIds.txt"
	cacheIds(repo, filename, collection=collection)	
	
def cacheEmailds (repo):
	"""
	cache Ids in the specified repo for the ccsemails collection
	"""	
	collection = ' ccsemails '
	filename = "emailIds.txt"
	cacheIds(repo, filename, collection=collection)	

if __name__ == '__main__':
	# repo(s) defined in __init__.py
	repo = bscs_user_content
	# repo = ccs_curriculum
	
	if 0:
		cacheUserIds(repo)
	if 0:
		cacheResourceIds(repo)
	if 0:
		cachePlaylistIds(repo)
	if 0:
		cacheEmailds(repo)		
	if 1:
		collection = 'ccsusersubmittedresources'
		ids = getIds(repo, collection=collection)
		print 'there are %d ids for %s' % (len(ids), collection)

