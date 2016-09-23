#!/usr/bin/env python

import sys, os, site
import string
import time

import urllib
from urlparse import urlsplit, urljoin
from cgi import parse_qs
from ServiceClient import ServiceClient, ServiceRequest
from JloXml.AdnRecord import AdnRecord
from HyperText.HTML40 import *

def showArgs ():
	for i in range(len (sys.argv)):
		print "arg[%d]: %s" % (i, sys.argv[i])
	print ("\n")


class GetRecordClient (ServiceClient):

	def _getRecord (self, params):

		self.request = ServiceRequest (self.baseUrl, params)
				
		print "GetRecordClient - URL: " + self.request.url
		rec, error = self._getResponse ()
		if (rec):
			 return self._parseResponse(rec)
		else:
			print "Error:", error

	def _parseResponse (self, rec):
		"""
		returns XML record if successful, otherwise prints error message and
		returns None
		"""
		# print "parse response with\n", rec.dom.toxml()
		element = rec.selectSingleNode (rec.dom,"DDSWebService:GetRecord:record:metadata:itemRecord")
		if element:
			xml = element.toxml()
			## print "metadata found:\n", xml
			return AdnRecord (xml=xml)
			
		else:
			element = rec.selectSingleNode (rec.dom,"DDSWebService:error")
			print "GetRecordClient error: " + rec.getText(element)
			print "Request:\n%s" % self.request.display("\t")
			return None

def tester ():
	id = "NASA-ESERevProd384"
	baseUrl = "http://www.dlese.org/dds/services/ddsws1-0"
	params = (
		('verb','GetRecord'),
		('id', id))
	client = GetRecordClient (baseUrl)
	adn = client._getRecord (params)
	newId = "CAT-DEMO-000-000-001"
	if adn:
		print "Success!"
		## print adn.dom.toxml()
		print ("id: " + adn.getId())
		adn.setId(newId)
		print ("id: " + adn.getId())

	
	
if __name__ == "__main__":

	tester()

					   

		

	
