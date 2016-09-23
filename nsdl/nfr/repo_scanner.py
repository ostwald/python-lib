"""
repo scanner - answer questions about repo, collections, item, mmd level
"""

import os, sys, re
from JloXml import MetaDataRecord, XmlUtils
from UserList import UserList
from UserDict import UserDict

handlePat = re.compile ("2200/[0-9]*T")

class ResourceMapping:
	"""
	exposes:
		- handle - a resourceHandle
		- url - the mapped resourceUrl
	"""
	def __init__ (self, element):
		self.handle = element.getAttribute("resourceHandle")
		self.url = element.getAttribute("resourceUrl")

class MmdRecord (MetaDataRecord):
	"""
	encapsulates a meta-metaData record
	exposes:
		- handle
		- partnerId
		- resourceMappings (instance of ResourceMapping)
	"""
	xpath_delimiter = '/'
	
	def __init__(self, path, setSpec, repoScanner):
		MetaDataRecord.__init__ (self, path=path)
		self.repoScanner = repoScanner
		self.setSpec = setSpec
		self.handle = self.getTextAtPath ("metaMetadata/metadataHandle")
		self.partnerId = self.getTextAtPath ("metaMetadata/partnerId")
		self.resourceMappings = map (ResourceMapping, self.getResourceNodes())
		
	def getResourceNodes (self):
		return self.selectNodes (self.dom, "metaMetadata/resources/resource")
	
	def removeEmtpyResources (self):
		parent = self.selectSingleNode (self.dom, 'metaMetadata/resources')
		for node in self.getResourceNodes():
			if not node.getAttribute("resourceUrl"):
				parent.removeChild(node)
		
class Item:
	
	nativePat = re.compile ("native_(.*).xml")
	
	def __init__ (self, path, collection):
		self.baseDir = path
		self.collection = collection
		self.setSpec = collection.setSpec
		self.repo = repo
		self.handle = os.path.basename(path).replace ('%2F', '/')
		self.mmd = MmdRecord (os.path.join (self.baseDir, 'meta-meta.xml'), self.setSpec, self.repo)
		self.nativeFormat = self.getNativeFormat()
		
	def getNativeFormat(self):
		for filename in os.listdir(self.baseDir):
			m = self.nativePat.match(filename)
			if m:
				return m.group(1)
				
	def getNativeRecord(self):
		if self.nativeFormat:
			filename = "native_%s.xml" % self.native_format
			return os.path.join (self.baseDir, filename)
		
class CollectionScanner (UserList):
	
	def __init__ (self, path, repo):
		self.data = []
		self.repo = repo
		self.baseDir = path
		self.setSpec = os.path.basename(path)
		self.itemHandles = filter (lambda x:x[0] != '.', os.listdir(self.baseDir))
		
	def scan (self):
		for itemHandle in self.itemHandles:
			item = Item (itemHandle, self)
		
class RepoScanner (UserDict):
	
	def __init__ (self, repoBase):
		self.data = {}
		self.baseDir = repoBase
		self.setSpecs = filter (lambda x:x[0] != '.', os.listdir(self.baseDir))
		
	def scan (self):
		for setSpec in self:
			colScanner = CollectionScanner (os.path.join (self.baseDir, setSpec), self)
			self[setSpec] = colScanner

		
class MmdScanner:
	"""
	Meta-metadata scanner
	"""
	
	def __init__ (self, repoBase, mmdOperation=None):
		"""
		repoBase - NFR directory
		mmdOperation - function to be called on mmdRecords
		"""
		self.halt_execution = False
		self.repoBase = repoBase
		self.mmdOperation = mmdOperation
		self.setSpecs = filter (lambda x:x[0] != '.', os.listdir(self.repoBase))
		print '%d sets found' % len(self.setSpecs)
		
	def halt (self):
		self.halt_execution = True
		
	def scan (self):
		"""
		visit a mmdRecords, calling self.mmdOperation on each
		"""
		for setSpec in self.setSpecs:
			setBase = os.path.join (self.repoBase, setSpec)
			setItems = filter (lambda x:x[0] != '.', os.listdir(setBase))
			
			for handle in setItems:
				if self.halt_execution:
					break
				mmdPath = os.path.join (setBase, handle, "meta_meta.xml")
				if not os.path.exists (mmdPath):
					raise Exception, 'mmd not found for %s' % handle
				mmd = MmdRecord (mmdPath, setSpec, self)
				
				if self.mmdOperation:
					self.mmdOperation (mmd)
					
def mmdOperation (mmd):
	"""
	example that prints handles of mmd records containing more than one resource
	"""
	
	if len(mmd.resourceMappings) > 1:
		print mmd.handle

		
if __name__ == '__main__':
	repoBase = "/home/ostwald/python-lib/nsdl/nfr/NFR-10-deep"
	scanner = MmdScanner(repoBase, mmdOperation)
	scanner.scan()
