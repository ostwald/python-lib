import os, sys, urllib, urllib2, time, codecs
from urlparse import urljoin
from JloXml import XmlRecord
from ndrObject import NdrObject

ndr_prod_baseUrl = 'http://ndr.nsdl.org/api'

class NdrClientError (Exception):
	pass

class NdrClient:

	action = None
	
	def __init__ (self, baseUrl=ndr_prod_baseUrl):
		self.baseUrl = baseUrl

	def paramsToQueryString (self, paramMap):
		params=[];add=params.append
		for key in paramMap:
			val = paramMap[key]
			if type(val) in [type(""), type(u"")]:
				add ("%s=%s" % (key, val))
			if type(val) == type([]):
				for v in val:
					add ("%s=%s" % (key, urllib.quote(v)))
		return '&'.join (params)
	
	def get (self, handle):
		tries = 0
		maxtries = 2
		
		while tries < maxtries -1:
			try:
				return self.doGet(handle)
			except:
				pass
			tries = tries + 1
		return self.doGet(handle)
		
	def doGet(self, handle):
		url = os.path.join (self.baseUrl, 'get', handle)
		req = urllib2.Request(url)
		try:
			response = urllib2.urlopen(req)
		except urllib2.URLError, e:
			errMsg = "unknown error getting data"
			if hasattr(e, 'reason'):
				errMsg = 'we failed to reach the server: %s' % e.reason
			elif hasattr (e, 'code'):
				errMsg = 'the server couldn\'t fulfill the request (%s)' % e
			# print e.reason
			print "%s: %s" % (errMsg, url)
			raise NdrClientError (errMsg)
			
		try:
			responseDoc = XmlRecord (xml=response.read())
			responseDoc.xpath_delimiter = '/'
		except:
			raise Exception, "response could not be parsed as XML: %s" % sys.exc_info()[1]
			
		#print responseDoc
			
		ndrObject = responseDoc.selectSingleNode (responseDoc.dom, 'NSDLDataRepository/NDRObject')
		if not ndrObject:
			raise Exception, "ndrObject not found in response"
			
		return NdrObject(ndrObject.toxml())
		

		
if __name__ == '__main__':
	baseUrl = 'http://ndr.nsdl.org/api'
	handle = '2200/20110216093718621T'
	client = NDRClient(baseUrl)
	ndrObject = client.get (handle)
	print 'uniqueID: ', ndrObject.uniqueID
