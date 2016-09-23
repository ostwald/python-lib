"""
Meta_meta data Scanner - scans an NFR Repository, visiting each collection and each MmdRecord

if supplied, an operation is called for each meta-metadata record
"""
import os, sys
from JloXml import MetaDataRecord, XmlUtils

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
		self.resourceMappings = map (ResourceMapping, self.selectNodes (self.dom, "metaMetadata/resources/resource"))
		
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
