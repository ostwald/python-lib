
import urllib
from urlparse import urlsplit, urljoin, urlunsplit
from cgi import parse_qs, parse_qsl
# from CATGlobals import baseUrl, suggest_standards_params, more_like_these_params
# from urls import *

class URL:
	"""
	
	takes a url and splits it into parts, allowing for manipulation
	(modification) of params and other url parts
	
	"""
	def __init__ (self, urlStr):
		tpl = urlsplit (urlStr)
		self.protocol = tpl[0]
		self.domain = tpl[1]
		self.path = tpl[2]
		self.query = urllib.unquote(tpl[3])
		self.hsh = tpl[4]

	def getTuple (self, encoded=1):
		query = encoded and urllib.urlencode(self.getParams()) or self.query 
		return (self.protocol, self.domain, self.path, query, self.hsh)
		
	def getParamNames (self):
		return self.getParamMap().keys()
					 
	def getParamMap (self):
		return parse_qs (self.query)

	def getParams (self):
		return parse_qsl (self.query)

	def getBaseUrl (self):
		return urlunsplit ((self.protocol, self.domain, self.path, None, None))

	def getUrl (self):
		"""
		returns string representation
		"""
		return urlunsplit (self.getTuple())

	def __repr__ (self):
		return self.getUrl()
		
	def addParam (self, name, value):
		params = self.getParams()
		params.append ((name, value))
		self.query = seq2ParamString (params)

	def delParam (self, name):
		params = self.getParams()
		new = []
		for item in params:
			if not item[0] == name:
				new.append (item)
		self.query = seq2ParamString (new)
		
	def replaceParam (self, name, value):
		self.delParam (name)
		self.addParam (name, value)
		
	def report (self, header=None):
		if header:
			print "\n", header
		print "baseUrl: %s" % self.getBaseUrl()
		self.printParams ("params")
		print "url: %s" % urllib.unquote(self.getUrl())
		
	
	def printParams (self, header=None):
		if header:
			print header
		params = self.getParamMap()
		for p in params.keys():
			val = params[p]
			if len(val) == 1:
				val = val[0]
			print "\t%s: %s" % (p, val)

def createInstance (baseUrl, params_obj, hsh=None):
	urlStr = baseUrl
	if params_obj:
		urlStr = urlStr + "?" + seq2ParamString(_makeParams (params_obj))
	if hsh:
		urlStr = urlStr + "#" + hsh
	return URL (urlStr)
		
def _makeParams (params_obj):
	"""
	given a params_object in an 'acceptable form' return a params sequence
	acceptable forms:
		- queryString
		- map where params are name, value mappings (values may be strings or lists)
		- list of params (each member is a tuple of form (name, value), 
			where value may be a list of values (represented as a tuple)
		- tuples - returned unchanged
	"""
	if type(params_obj) == type (()):
		return params_obj
		
	if type(params_obj) == type([]):
		## cgi.parse_qsl returns a list (with params encoded as tuples)
		return tuple(params_obj)
		
	if type(params_obj) == type({}):
		params = []
		for key in params_obj:
			values = params_obj[key]
			## ensure the param value is a list
			if values is None:
				continue
			if type(values) in [type(""), type(u"")]:
				values = [values]
			for val in values:
				params.append ((key, urllib.quote(val)))
		return tuple(params)
		
	if type(params_obj) == type(""):
		return parse_qsl(params_obj)
	
	msg = "unrecognized params_obj type: %s" % type(params_obj)
	raise ValueError, msg
		
def seq2ParamString (paramSeq):
	"""
	values should be escaped?
	"""
	params = [];add=params.append
	for tup in paramSeq:
		name = tup[0]
		value = tup[1]
		#if type(value) == type("") or type(value) == type(u""):
		if type(value) in [type(""), type(u"")]:
		
			value = [value]
		for val in value:
			add ("%s=%s" % (name, urllib.quote(val)))
	return '&'.join (params)	
		
def map2ParamString (paramMap):
	params = [];add=params.append
	for key in paramMap:
		val = paramMap[key]
		if type(val) in [type(""), type(u"")]:
			add ("%s=%s" % (key, val))
		if type(val) == type([]):
			for v in val:
				add ("%s=%s" % (key, urllib.quote(v)))
	return '&'.join (params)
		
	
def tester (urlStr):
	url = URL (urlStr)
	print "\n----tester ---\n"
	url.report()
	url.printParams()
	return

	url.addParam ('author', ['colorado','mexico'])
	url.delParam ('author')
	url.addParam ('author', 'utah')
	url.replaceParam ('topic', 'math')
	url.printParams()
	
if __name__ == "__main__":
	# tester (latest)
	
	testUrl =       'http://mathdl.maa.org/mathDL/46/?pa=content&sa=viewDocument&nodeId=3362'
	# urllib.quoted: http%3A//mathdl.maa.org/mathDL/46/%3Fpa%3Dcontent%26sa%3DviewDocument%26nodeId%3D3362
	
	params = {
			"verb": "Search",
			'q':'/key//record/general/title:"%s"' % u"hello world",
			# 'storedContent':['dcsstatus','dcsstatusNote'],
			# "xmlFormat": 'osm',
			# "ky": 'osgc',
			# 's': '0',
			# 'n': '100'
			# 'foo': testUrl
		}
		
	_url = createInstance ("http://foo/farb", params)
	_url.addParam('foo', testUrl)
	print _url 
	_url.printParams()

