#!/usr/bin/env python

import sys, os, string
# from serviceclient import ServiceClient, URL, createInstance
# createUrlInstance = createInstance
# del createInstance

from JloXml import XmlUtils, XmlRecord
from serviceclient import ServiceClient

import CATGlobals
# from suggestStandardsResponseDoc import SuggestStandardsResponse, Standard
from catUtils import stripLearningResourceContent
from catClient import CatClient

class FlatElementObj:
	"""
	Takes a "flat element" - each child contains a value but does not have 
	attributes or child elements - and exposes the child elements as attributes.
	"""
	
	def __init__ (self, element):
		self.element = element
		self.attrs = []
		for child in XmlUtils.getChildElements (element):
			attr = child.tagName
			self.attrs.append (attr)
			setattr (self, attr, XmlUtils.getText (child))
		
	def __repr__ (self):
		s=[];add=s.append
		for attr in self.attrs:
			add ("\t%s: %s" % (attr, getattr (self, attr)))
		return string.join (s, "\n")

class RequestInfo (FlatElementObj):
	"""
	manages information returned from CAT about the request it processed
	"""
	def __repr__ (self):
		return "\nRequestInfo\n%s" % FlatElementObj.__repr__(self)
		
class Standard (FlatElementObj):
	"""
	represents a standard as returned by CAT
	"""
	
	def __repr__ (self):
		s=[];add=s.append
		add ("\n" + self.Identifier)
		attrsToShow = ("Identifier", "StandardDocument", "Author", "Topic", "GradeLevels", "Text", "Benchmark")
		for attr in attrsToShow:
			if attr != "Identifier":
				add ("\t%s: %s" % (attr, getattr(self, attr)))
		return string.join (s, "\n")

class SuggestStandardsResponse (XmlRecord):

	standards_path = "CATWebService:SuggestedStandards:Results:Result:Standard"
	requestInfo_path = "CATWebService:SuggestedStandards:RequestInfo"
	
	def __init__ (self, path=None, xml=None):
		XmlRecord.__init__ (self, path, xml)
		self.results = self.getStandards()
		self.requestInfo = self.getRequestInfo()
		
	def getRequestInfo (self):
		node = self.selectSingleNode (self.dom, self.requestInfo_path)
		return RequestInfo (node)

	def getStandards (self):
		elements = self.getElementsByXpath (self.dom, self.standards_path)
		# standards = [];add=standards.append
		# for std in elements:
			# add (Standard (std))
		# return standards
		return map (Standard, elements)

		
class SuggesterClient (CatClient):
	
	results = None
	
	def __init__ (self, params, server='cnlp' ):
		self.results = []
		self.requestInfo = None
		CatClient.__init__ (self, server)
		request = self.setRequest (params)
		print request.report()
		# print request.getUrl()
		response = self.getResponse(preprocessor=stripLearningResourceContent)
		if response.hasError():
			print "SERVICE ERROR: ", response.error
	
		else:
			# print response.doc
			parsedResponse = SuggestStandardsResponse (xml=response.doc.recordXml)
			self.results = parsedResponse.results
			self.requestInfo = parsedResponse.requestInfo
			
	def getIds(self):
		"""
		returns a list of standards obtained from result doc
		"""
		return map (lambda x: x.Identifier, self.results)
		
	def report (self):
		print "\nResults returned (%d)" % len (self.getIds())
		# for id in self.getIds():
			# print "\t", id
		#for std in self.results.standards:
			# print '--------------------------\n%s' % std
		
		print self.results
			

def variousAuthorTester (params):
	"""
	get suggestions for the given params from various authors
	"""
	for author in ['Colorado', 'National Science Education Standards', 'Texas', 'Florida', 'California', 'Virgina']:
		myParams.update ({'author':author})
		client = SuggesterClient (myParams)
		print '\n%d results' % len(client.results)
		
if __name__ == "__main__":

	aaas1993 = 'http://purl.org/ASN/resources/D1000152'
	aaas2008 = 'http://purl.org/ASN/resources/D10003EA'
	
	myParams = {
		"method": "suggestStandards",
		"query": "http://ga.water.usgs.gov/edu/earthrivers.html",
		"startGrade": "9",
		"endGrade": "12",
		"maxResults": "10",
 		"topic": "Science",
		'standardDocuments' : aaas1993,
		# "author":"National Science Education Standards"
		# "author":"American Association for the Advancement of Science"
		"author":"AAAS"
	}
	
	if 1:
		client = SuggesterClient (myParams)
		for id in client.results:
			print id
	if 0:
		variousAuthorTester (myParams)


	
					   

		

	
