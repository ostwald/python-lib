import sys, os, string
from dcsTools.recommender import ServiceClient
from JloXml import XmlRecord, XmlUtils
from globals import baseUrl

class DCSWebServiceClientError (Exception):
	pass

class DCSWebServiceClient (ServiceClient):
	"""
	ServiceClient that knows how to check a xml response from the DCSWebService
	for errors
	"""
	verb = "" # overridden by concrete classes
	required_params = [] # supply to provide pre-request param checking
	verbose = False
	
	def __init__ (self, baseUrl, params):
		params['verb'] = self.verb
		for param in self.required_params:
			if not params.has_key(param):
				raise KeyError, "Missing required param: %s" % param
		ServiceClient.__init__ (self, baseUrl, params)
	
	def parseResponse (self, xml):
		"""
		check for error in response and raise error if found
		otherwise, return response as XmlRecord
		"""
		if self.verbose:
			print "parseResponse"
			print "\n***********************\n%s\n********************" % xml
		rec = XmlRecord (xml = xml)
		# print rec
		errorEl = rec.selectSingleNode (rec.dom, "DCSWebService:error")
		if errorEl:
			if self.verbose:
				print rec
			raise DCSWebServiceClientError, "Service Error: %s" % XmlUtils.getText (errorEl)
		return rec
		
