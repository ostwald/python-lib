"""
reorg shared
"""
import os, sys, re, time
from serviceclient import SimpleClient, SimpleClientError
from JloXml import XmlUtils

def subDirNames (path):
	"""
	return the list of subdir names for given path
	"""
	return filter (lambda x:os.path.isdir(os.path.join(path, x)), os.listdir(path))	

class ProtectedUrlEntry:
	"""
	attributes: 
	- id
	- currColl - curriculumCollection - the collection of the saved resource in the curriculum repo
	- coll - collection of the saved record in the userContent repo
	- url - protected url
	- filename - derived from url
	- record - metadata for a resource that	contains the protectedUrl.
	"""
	def __init__ (self, id, currColl, coll, url, record):
		self.id = id
		self.coll = coll
		self.currColl = currColl
		self.url = url
		self.record = record
		self.filename = os.path.basename(url)
		
	def __repr__ (self):
		return '%s\n %s - %s' % (self.url, self.id, self.coll)


class DDSUpdateClient(SimpleClient):
	
	def getResponseDoc (self, params=None, opts=None):
		doc = SimpleClient.getResponseDoc(self, params, opts)
		error = doc.selectSingleNode(doc.dom,'DDSRepositoryUpdateService:error')
		if error:
			raise SimpleClientError, 'ERROR %s' % XmlUtils.getText(error)
		# print ' - updated %s' % params['id']
		# id = doc.getTextAtPath('DDSRepositoryUpdateService:PutRecord:recordInfo:recordId')
		# print ' - updated', id
		return doc
