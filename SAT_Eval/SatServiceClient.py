#!/usr/bin/env python
usage = """
DCS utility script usage:
   arg0 is dcs - the command you typed to get here
   arg1 is command:
       start_jvm
       stop_jvm
       deploy
       tail
       bounce
       update
       check
       config_info
   arg2 is dcs instance name

"""
import sys, os, site
import string
import time

import urllib
from urlparse import urlsplit, urljoin
from cgi import parse_qs
from JloXml import XmlRecord
from HyperText.HTML40 import *
from SATServiceRecord import SATServiceRecord

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
	
	def __init__ (self, url):
		self.url = url
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
		
	def _normalize_response (self, data):
		if not data:
			return
		xml = data.read()
		
		if xml.upper().strip().startswith ("<HTML>"):
			raise  ResponseError (Response, "SAT Service response is HTML (XML expected)")
			
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
		# try:
			# return XmlRecord (xml=xml)
		# except:
			# print "error", sys.exc_info()[0], sys.exc_info()[1]
			# self.error = ResponseError (sys.exc_info()[0], sys.exc_info()[1])
		
	def hasError (self):
		return self.error != None

class Request:
	
	def __init__ (self, baseUrl, params):
		self.baseUrl = baseUrl
		self.params = params
		self.url = "%s?%s" % (baseUrl, urllib.urlencode (params))
		print "Request: ",self.url
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
		
		return Response (self.url)._submit()

		
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
		

class SATClient:
	# original location of SAT server
	## baseUrl = "http://lehnert.syr.edu:8080/casaa-rest/service.do"

	# new location
	baseUrl = "http://sat.nsdl.org:8380/casaa-sat/service.do"
	username = "test"
	password = "p"
	topic = "Science"
	maxResults = "5"
	
	baseParams = {
			"username"   : username,
			"password"   : password,
			"topic"      : topic,
			"maxResults" : maxResults
			}
	
	def doSuggestStandards (self, purlId, state, gradeRange=None):
		params = self.baseParams

		startGrade = "-1"
		endGrade   = "-1"
		
		if gradeRange:
			startGrade = gradeRange[0]
			if startGrade.upper() == "K":
				startGrade = "0"
			endGrade = gradeRange[2:]
			
		
		params.update ({
			"method"     : "suggestStandards",
			"query"      : purlId,
			"author"     : state,
			"startGrade" : startGrade,
			"endGrade"   : endGrade
			})

		request = Request (self.baseUrl, params)
		# print "request: " + request.url
		response = request.submit ()
		if response.hasError():
			# print response.error
			raise response.error
		else:
			rec = self.parseResponse(response.content)
			return rec
		

	def parseResponse (self, xml):
		"""
		returns (subject, msg) response
		
		look for "DCSWebService/ExportCollection/result"
		"""
		## print "\n***********************\n%s\n********************" % xml
		rec = SATServiceRecord (xml = xml)
		return rec

def tester ():
	purlId = "http://purl.org/ASN/resources/S101EF6F"
	state = 'Massachusetts'
	gradeRange = "5-8"

	try:
		rec = SATClient().doSuggestStandards (purlId, state, gradeRange)
		rec.showRequestInfo()
		stds = rec.getSuggestedStandards()
		print "%d standards suggested" % len (stds)
		for std in stds:
			print "\n%s  -- %s" % (std.purlId, std.benchmark)
	except ResponseError, msg:
		print "ResponseError: %s" % msg
	except:
		print sys.exc_info()[0], sys.exc_info()[1]
	
if __name__ == "__main__":

	tester()

					   

		

	
