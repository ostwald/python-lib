import sys, os, time
from JloXml import XmlUtils
from serviceClient import SimpleClient
from nsdl.nfr import MmdScanner, MmdRecord

baseUrl = "http://nsdldev.org/hrs/service"

class HrsClient (SimpleClient):
	
	verbose = 0
	
	def getResponseDoc (self, params=None, opts=None):
		doc = SimpleClient.getResponseDoc (self, params, opts)
		doc.xpath_delimiter = '/'
		error = self.getResponseError(doc)
		if error:
			raise Exception, "Service Error: %s" % error
		return doc
			
	def getResponseError (self, doc):
		errorElement = doc.selectSingleNode (doc.dom, 'HandleResolutionService/error')
		if errorElement:
			return "%s: %s" % (errorElement.getAttribute('code'), XmlUtils.getText(errorElement))

def getMetadataMapping (partnerId, setSpec):
	client = HrsClient (baseUrl)
	params = {
		'verb' : 'GetMetadataHandle',
		'partnerId' : partnerId,
		'setSpec' : setSpec
	}
	
	responseDoc = client.getResponseDoc (params)
	
	print responseDoc
	
def mappingOperation (mmd):
	print mmd.partnerId, mmd.setSpec
	getMetadataMapping (mmd.partnerId, mmd.setSpec)
	sys.exit()
	
class Loader:
	
	def __init__ (self, repoBase):
		self.hits = 0
		self.scanner = MmdScanner (repoBase, self.hitDB)
		self.start = time.time()
		self.scanner.scan()
		print 'total elapsed: %f secs' % (time.time() - self.start)
		
	def hitDB (self, mmd):
		tics = time.time()
		getMetadataMapping (mmd.partnerId, mmd.setSpec)
		elapsed = time.time() - tics
		print elapsed
		self.hits = self.hits + 1
		if self.hits >= 10:
			self.scanner.halt()
	
def doHit (mmd):
	tics = time.time()
	getMetadataMapping (mmd.partnerId, mmd.setSpec)
	elapsed = time.time() - tics
	print elapsed	
	
def doHits (n):
	hits = 0
	start_tics = time.time()
	repoBase = "/home/ostwald/python-lib/nsdl/nfr/NFR-10-deep"
	scanner = MmdScanner(repoBase, mappingOperation)
	scanner.scan()
	
if __name__ == '__main__':
	repoBase = "/home/ostwald/python-lib/nsdl/nfr/NFR-10-deep"
	Loader(repoBase)
	if 0:
		
		scanner = MmdScanner(repoBase, mappingOperation)
		scanner.scan()
	if 0:
		partnerId = 'MSP2-000-190-144-955'
		setSpec = '1007936'
		tics = time.time()
		getMetadataMapping (partnerId, setSpec)
		time.sleep(1)
		elapsed = time.time() - tics
		print 'elapased tics: %f' % elapsed
