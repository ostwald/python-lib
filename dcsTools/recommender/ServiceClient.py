"""
Generic WebServiceClient classes

"""
import sys, os, site
import string
import time

import urllib
from urlparse import urlsplit, urljoin
from cgi import parse_qs
from JloXml import XmlRecord
from HyperText.HTML40 import *

def showArgs ():
	for i in range(len (sys.argv)):
		print "arg[%d]: %s" % (i, sys.argv[i])
	print ("\n")

class ResponseError (Exception):
	def __init__ (self, exc_type, message):
		try:
			self.exc_type = exc_type.__class__.__name__
		except:
			self.exc_type = exc_type
		self.message = message
	def __str__ (self):
		return "ResponseError: %s, %s" % (self.exc_type, self.message)

class Response:
	"""
	response does not try to parse response as xml, it simply stores the string as
	content.
	"""
	url_opener = urllib.URLopener()	# create URLopener
	
	def __init__ (self, url, data=None):
		self.url = url
		self.data = data
		self.error = None
		self.content = None
		
	def _submit (self):
		url = self.url
		# print "submitting: %s" % url
		data = None
		try:
			data = self.url_opener.open(url)
		except IOError, error_code :		# catch the error
			if error_code[0] == "http error" :
				print "error_code ", error_code
				self.error = ResponseError (error_code[0], error_code[1])
				return self	
		except:
			print "error", sys.exc_type, sys.exc_value
			self.error = ResponseError (sys.exc_info()[0], sys.exc_info()[1])
			return self

		self.content = self._normalize_response (data)
		return self

	def _post (self):
		url = self.url
		# print "submitting: %s" % url
		post_data = self.data
		response_data = ""
		try:
			# data = self.url_opener.open(url, post_data)
			response_data = urllib.urlopen(url, post_data)

		except IOError, error_code :		# catch the error
			if error_code[0] == "http error" :
				print "error_code ", error_code
				self.error = ResponseError (error_code[0], error_code[1])
				return self	
		except:
			print "error", sys.exc_type, sys.exc_value
			self.error = ResponseError (sys.exc_info()[0], sys.exc_info()[1])
			return self

		self.content = self._normalize_response (response_data)
		return self
		
	def _normalize_response (self, data):
		if not data:
			return
		xml = data.read()
		## print "\n----- data.read():--------\n%s" % xml
		if xml.upper().strip().startswith ("<HTML>"):
			print "--------------------------\n%s-----------------------\n" % xml
			raise  ResponseError (Response, "Service response is HTML (XML expected)")
			
		if 1:
			xml = xml.replace (chr(13), '')
			s=[];add=s.append
			for line in xml.split('\n'):
				if line.strip() != "":
					add (line)
			xml = string.join (s, '\n')
		# print xml
		xml = unicode (xml, "utf8")
		return xml

		
	def hasError (self):
		return self.error != None

class Request:
	
	def __init__ (self, baseUrl, params):
		self.baseUrl = baseUrl
		self.params = params
		self.url = "%s?%s" % (baseUrl, urllib.urlencode (params, doseq=1))
		# print self.url
		self.urlTuple = urlsplit(self.url)

	def getContextName (self):
		path = self.urlTuple[2]
		return path.split("/")[1]

	def getQuery (self):
		return self.urlTuple[3]

	def getParams (self):
		return parse_qs (self.getQuery())

	def submit (self):
		"""
		submit request and return a DOM containing response from service

		returns None in case of http error, but we can do better ... 
		"""		
		url = "%s?%s" % (self.baseUrl, urllib.urlencode (self.params, 1))
		return Response (url)._submit()

	def post (self):
		return Response (self.baseUrl, urllib.urlencode (self.params, 1))._post()
		
	def display (self, indent=""):
		s=[];add=s.append

		add ("baseUrl: %s" % self.baseUrl)
		add ("contextName: %s" % self.getContextName())

		add ("params:")
		params = self.getParams()
		for p in params.keys():
			val = params[p]
			if len (val) > 1:
				add ("\t%s:" % p)
				for v in val:
					add ("\t\t%s" % v)
			else:
				add ("\t%s: %s" % (p, val[0]))

		return indent + string.join (s, "\n" + indent)
		

class ServiceClient:

	"""
		build params dict and then submit a request
	"""
	
	def __init__ (self, baseUrl, params={}, **args):
		self.baseUrl = baseUrl
		self.params = params
		if args:
			self.params.update (args)

		# print "---------\nServiceClient params\n-----------"
		# for name in params.keys():
			# print "\n%s: %s" % (name, params[name])

		
	def _build_params (self):
		return {}

	def post (self):
		"""
		submits a POST request and returns result of calling 'handleResponse'
		"""
		request = Request (self.baseUrl, self.params)
		# print "request: " + request.url
		response = request.post ()
		return self.handleResponse (response)
		
	def submit (self):
		"""
		submits GET request and returns result of calling 'handleResonse'
		"""

		request = Request (self.baseUrl, self.params)
		# print "request: " + request.url
		response = request.submit ()
		return self.handleResponse (response)
		
	def handleResponse (self, response):
		"""
		raise error if the response has an error from http
		self.parseResponse can also raise an error if the
		xml response indicates an error
		"""
		if response.hasError():
			# print response.error
			raise response.error
		else:
			rec = self.parseResponse(response.content)
			return rec
		
	def parseResponse (self, xml):
		"""
		simply returns an XmlRecord instance created from xml
		more sophisticated clients might perform side effect e.g.
		extract specific values from the response and
		store as attributes, etc
		"""
		print "\n***********************\n%s\n********************" % xml
		rec = XmlRecord (xml = xml)
		return rec

def tester ():
	purlId = baseUrl = "http://localhost/schemedit/services/recommend.do"


	try:
		rec = ServiceClient (baseUrl).submit()
		print rec
	except ResponseError, msg:
		print "ResponseError: %s" % msg
	except:
		print sys.exc_info()[0], sys.exc_info()[1]
	
if __name__ == "__main__":

	tester()

					   

		

	
