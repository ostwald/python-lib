#!/usr/bin/env python

import sys, os, site
import string
from JloXml import XmlUtils
from serviceclient import ServiceRequest, ServiceResponse, ServiceError, ServiceClient, URL
import CATGlobals
from suggestStandardsResponseDoc import Standard

"""
we want to parse the response from the Client to show different things, like
suggested standard ids
"""

class CatResponseError (ServiceError):
	pass

class CatRequest (ServiceRequest):
	
	def report (self):
		"""
		custom request report (showing final url)
		"""
		#return "%s\nrequestURL: %s" % (ServiceRequest.report(self), self.getUrl())
		return ServiceRequest.report(self)
		

class CatClient (ServiceClient):
	
	result = None
	
	def __init__ (self, catServer):
		self.server = CATGlobals.servers[catServer]
		if not self.server:
			raise KeyError, "cat server not found for '%s'" % catServer
		self.credentials = {
			'username': self.server['username'],
			'password': self.server['password']
		}
		# params_obj['username'] = server
		# params_obj['password'] = server['password']
		ServiceClient.__init__ (self, self.server['baseUrl'])
	
	def setRequest (self, params):
		"""
		update provided params with credentials
		"""
		if type(params) == type([]):
			for key in self.credentials:
				params.append ((key, self.credentials[key]))
		elif type(params) == type ({}):
			params.update (self.credentials)
		else:
			raise Exception, "unrecognized params type: %s" % type(params)
		self.request = CatRequest (self.baseUrl, params)
		return self.request
		
	def getResponse (self, preprocessor=None):
		"""
		simply return response from server as an XmlRecord instance
		"""
		response = ServiceClient.getResponse (self, preprocessor)
		if not response.hasError():
			# now test for CAT error
				error = response.doc.selectSingleNode (response.doc.dom, 'CATWebService:Error')
				if error:
					statusMessage = XmlUtils.getChildText (error, "StatusMessage")
					returnCode = XmlUtils.getChildText (error, "ReturnCode")
					response.error = CatResponseError ([statusMessage, returnCode])
			
			
			#self.result = response.doc
		return response
		
	def report (self):
		print "\nCAT CLIENT RESULT"
		print self.result

def tester (url):
	params = url.getParams()
	url.printParams()
	client = CatClient ("cnlp")
	request = client.setRequest (params)
	# print request.report()
	response = client.getResponse()
	if response.hasError():
		print response.error

	else:
		# print response.doc
		client.report()	
	
	
if __name__ == "__main__":
	# url = URL (ssDoc)
	url = URL (latest)
	url.addParam ("author", "Colorado")
	url.replaceParam ("maxResults", "10")
	
	print "CASE 1"
	tester (url)

	
					   

		

	
