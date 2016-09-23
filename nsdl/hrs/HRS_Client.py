"""
HRS Client -

see https://wiki.ucar.edu/x/A6erB for HRS docs

two calls we're interested in:

	- GetMetadataHandle (partnerID, setSpec)
	
	- GetResourceHandle (resourceURL)

"""
import os, sys
from serviceclient import SimpleClient
from JloXml import XmlRecord, XmlUtils

class HRSError (Exception):
	pass

class HRSClient (SimpleClient):
	verbose = 0
	baseUrl = "http://nsdldev.org/hrs/service"
	
	def __init__ (self):
		SimpleClient.__init__ (self, self.baseUrl)
		
	def getResponseDoc (self, params=None, opts=None):
		XmlRecord.xpath_delimiter = '/'
		doc = SimpleClient.getResponseDoc (self, params, opts)
		error = doc.selectSingleNode (doc.dom, "HandleResolutionService/error")
		if error:
			raise HRSError, '%s: %s' % (error.getAttribute('code'),
										XmlUtils.getText(error))
		return doc
		
def getMetadataHandle (partnerId, setSpec):
	params = {
		'verb' : 'GetMetadataHandle',
		'partnerId' : partnerId,
		'setSpec'   : setSpec
	}
	client = HRSClient()
	doc = client.getResponseDoc (params)
	xpath = 'HandleResolutionService/GetMetadataHandle/metadataHandle'
	return doc.getTextAtPath (xpath)

def getResourceHandle(resourceUrl):
	params = {
		'verb' : 'GetResourceHandle',
		'resourceUrl' : resourceUrl
	}
	client = HRSClient()
	doc = client.getResponseDoc (params)
	xpath = 'HandleResolutionService/GetResourceHandle/resourceHandle'
	return doc.getTextAtPath (xpath)
	
def getMdHandleTester():
	pid = 'BIL-000-000-000-108'
	ss = 'ncs-NSDL-COLLECTION-000-003-112-044'
	
	handle = getMetadataHandle (pid, ss)
	print "Metadata Handle:", handle
	
def getResHandleTester():
	resUrl = 'http://curvebank.calstatela.edu/arearev/arearev.htm'
	
	handle = getResourceHandle (resUrl)
	print "Resource Handle:", handle	
	
if __name__ == '__main__':
	getResHandleTester()
