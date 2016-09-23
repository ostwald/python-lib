#!/usr/bin/env python
"""
service client that expects an XML response
"""
import sys, os, site, re
import string
import time
import exceptions

import urllib
from cgi import parse_qs
from JloXml import XmlRecord, XmlUtils
import URL

class ServiceRequest:
	"""
	Wraps a URL send to a WebService
	"""
	def __init__ (self, baseUrl, params_obj):
		# self.baseUrl = baseUrl
		# self.params = self._makeParams (params_obj)
		self._url = URL.createInstance (baseUrl, params_obj)

	def getQuery (self):
		return self._url.query
		
	def getUrl (self):
		return self._url.getUrl()

	def report (self, indent=""):
		s=[];add=s.append
		add ("\nREQUEST")
		add ("baseUrl: %s" % self._url.getBaseUrl())
		## add ("contextName: %s" % self.getContextName())

		add ("params:")
		qmap = parse_qs(self.getQuery())
		for key in qmap.keys():
			val = qmap[key]
			if len(val) == 1:
				val = val[0]
			add ("\t%s: %s" % (key, val))
				
		## add ("url: " + self.getUrl())

		return indent + string.join (s, "\n" + indent)
		
class ServiceResponse:
	"""
	Contains either an error (ServiceError) or a response doc (as a XmlRecord)
	"""	
	
	def __init__ (self, data, exc_info=None, preprocessor=None):
		self.data = data
		self.error = None
		if exc_info:
			self.error = ServiceError (exc_info)
		self.doc = None
		if not exc_info:
			try:
				# responseText = data.read()
				# responseText = unicode (data.read(), 'iso-8859-1') # universal?
				responseText = unicode (data.read(), 'utf-8') # experimental 12/2/2010
				
				
				# print "serviceClient: reponseText:\n%s" % responseText
				if preprocessor:
					responseText = preprocessor (responseText)
				self.doc = XmlRecord (xml=responseText)
				
				webResponseErrorNode = self.doc.selectSingleNode (self.doc.dom, 'DDSWebService:error')
				if webResponseErrorNode:
					self.error = XmlUtils.getText(webResponseErrorNode)
			except:
				## self.error = ServiceError (sys.exc_info())
				self.error = ServiceError (["ServiceResponse: Could not parse XML", sys.exc_info()[1]])
		
	def hasError (self):
		return self.error
		
class ServiceError:

	def __init__ (self, exc_info):
		self.type = exc_info[0]
		self.value = exc_info[1]

	def __repr__ (self):

		## is it a class and a subclass of IOError?
		if type(self.type) == type(exceptions.IOError) and issubclass (self.type, exceptions.IOError):
			# return str(self.value)
			if self.value[0] == "http error":
				return "%s: %s (%s)" % (self.value[0], self.value[1], self.value[2])
			else:
				return "%s: %s" % (self.value[0], self.value[1])
		else:
			return "%s: %s" % (self.type, self.value)

		
class ServiceClient:
	"""
	URLopener doesn't follow redirects, FancyURLOpener does
	"""
	url_opener = urllib.URLopener()	# create URLopener
	# url_opener = urllib.FancyURLopener()	# create URLopener

	verbose = 0

	def __init__ (self, baseUrl):
		self.baseUrl = baseUrl
		self.request = None
		self.success = 0

	def setRequest (self, params):
		self.request = ServiceRequest (self.baseUrl, params)
		return self.request
		
	def getResponse (self, preprocessor=None):
		"""
		submit service request and return a ServiceResponse instance
		"""
		if not self.request:
			raise UnboundLocalError, "request not initialized"
		url = self.request.getUrl()
		
		data = None
		try:
			data = self.url_opener.open(url)
		except:
			return ServiceResponse (None, exc_info=sys.exc_info())

		return ServiceResponse (data, preprocessor=preprocessor)

					   

		

	
