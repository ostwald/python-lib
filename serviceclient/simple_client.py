"""
SimpleClient - uses urllib2

example useage:
	
baseUrl = "http://asn.jesandco.org/api/1/jurisdictions"
params = {}
postData = {}
client = SimpleClient (baseUrl)
data = client.getData(params, postData) # returns response as string
responseDoc = client.getResponseDoc(params, postData) # returns response as JloXml.XmlRecord
	
"""
import os, sys, urllib, urllib2, json, time, codecs
import ssl
from urlparse import urljoin
from JloXml import XmlRecord

def paramsToQueryString (paramMap):
	"""
	util - not currently used
	"""
	params=[];add=params.append
	for key in paramMap:
		val = paramMap[key]
		if type(val) in [type(""), type(u"")]:
			add ("%s=%s" % (key, val))
		if type(val) == type([]):
			for v in val:
				add ("%s=%s" % (key, urllib.quote(v)))
	return '&'.join (params)


class SimpleClientError (Exception):
	pass

class SimpleClient:

	action = None
	verbose = 0
	ignore_certs = 1
	
	def __init__ (self, baseUrl):
		self.baseUrl = baseUrl
		self.responseCode = None

	def paramsToQueryString (self, paramMap):
		"""
		not used
		"""
		raise Exception, "paramsToQueryString is now a static function"
	
	def getResponseDoc (self, params=None, opts=None):
		"""
		returns response as XmlRecord
		"""
		# print 'params: %s' % params
		return XmlRecord(xml=self.getData(params, opts))
		
	def getRequest(self, params=None, opts=None):
		"""
		opts are params that are passed via POST method
		"""
		if params:
			url = "%s?%s" % (self.baseUrl, urllib.urlencode(params))
		else:
			url = self.baseUrl
		
		# build request
		if opts is not None:
			# do not encode strings (e.g., JSON)
			if not type(opts) in [type(''), type(u'')]:
				data = urllib.urlencode(opts)
			else:
				data = opts
			req = urllib2.Request(url, data)
		else:
			req = urllib2.Request(url)
		return req

		
	def getData(self, params=None, opts=None):
		"""
		returns response data as a string
		or, if there is an error, raises SimpleClientError
		"""
			
		req = self.getRequest(params, opts)
		# print "full_url: %s" % req.get_full_url()
		
		# prior to 2.7.9 certs were ignored ...
		# the following does not work in purg 2.7
		# but there is no problem with python26-apple
		# get response
		try:
			ctx = None
			if hasattr(ssl, 'ssl._create_unverified_context'):
				ctx = self.ignore_certs and None or ssl._create_unverified_context()
				print "ssl has attribute ssl._create_unverified_context"
				response = urllib2.urlopen(req, context=ctx)
			elif self.ignore_certs:
				# kluge used for post 2.7.9 - bypass verification
				# see http://stackoverflow.com/questions/27835619/ssl-certificate-verify-failed-error
				context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
				response = urllib2.urlopen(req, context=context)
			else:
				response = urllib2.urlopen(req)
				
		except urllib2.URLError, e:
			errMsg = "unknown error getting data"
			if hasattr(e, 'reason'):
				errMsg = 'we failed to reach the server: %s' % e.reason
			elif hasattr (e, 'code'):
				errMsg = 'the server couldn\'t fulfill the request (%s)' % e
			# print e.reason
			if self.verbose:
				print "%s: %s" % (errMsg, req.get_full_url())
			raise SimpleClientError (errMsg)
			
		self.responseCode = response.getcode()
			
		raw = response.read()
		encoding = 'ISO-8859-1' # 'utf=8'
		if response.headers.has_key('content-type') and 'charset=' in response.headers['content-type']:
			encoding=response.headers['content-type'].split('charset=')[-1]
		raw = unicode(raw, encoding)

		if self.verbose:
			print "\nHEADERS" # same as response.info()
			for key in response.headers.keys():
				print '%s: %s' % (key, response.headers[key])
			print '===== end headers ========\n'
		
		lenBytes = len(raw.encode(encoding))
		
		if response.headers.has_key ('content-length'):
			try:
				if lenBytes != int(response.headers['content-length']):
					print 'WARNING: response length error'
			except:
				pass
		
		if 0:
			response_file = 'current-obtain-response.txt'
			fp = codecs.open (response_file, 'w', 'utf-8')
			fp.write (raw)
			fp.close()
			print "wrote to ", response_file
		# print raw
		# return unicode(raw, 'utf-8')
		return raw
		
if __name__ == '__main__':
	# baseUrl = 'http://nldr.library.ucar.edu/metadata/osm/1.1/schemas/vocabs/instName.xsd'
	baseUrl = 'http://ncs.nsdl.org/mgr/services/ddsws1-1?verb=Search&s=0&n=50&ky=1290084883129&q=algebra&output=json'
	baseUrl = 'http://ncs.nsdl.org/mgr/services/ddsws1-1?verb=Search&s=0&n=50&ky=1290084883129&q=algebra'
	
	baseUrl = 'http://asn.jesandco.org/resources/D2454348.json'
	
	# baseUrl = 'http://ncs.nsdl.org'
	client = SimpleClient(baseUrl)
	client.getData()
	print 'responseCode: ', client.responseCode
	# print 
