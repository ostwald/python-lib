"""
encapsulates the ASN URI Resolver service.

given an asn identifier (purl) returns information about that standard and it's document
"""

import sys, os, site, urllib
import string
import time
import exceptions

from serviceclient import ServiceClient
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
from asnUriResolver import AsnUriResolver

class AsnHelperService (ServiceClient):

	url_opener = urllib.FancyURLopener()	#needed because URI resolver redirects
	
	def __init__ (self, purl):
		self.baseUrl = purl
		self.setRequest(purl)
		self.success = 0
		self.error = None
		response = self.getResponse ()
		if response.hasError():
			print response.error
			self.error = response.error
		else:
			# self.response = ResolverResponse (xml=response.doc.recordXml)
			pass
		XmlRecord.xpath_delimiter = "/"
		self.response = response.doc

class HelperResponse (UserDict):
	
	url = None
	kludge_mappings = None
	
	def __init__ (self):
		UserDict.__init__ (self, self.kludge_mappings)
		self.rec = AsnHelperService(self.url).response
		self.root = self.rec.doc
		self.processRec ()
		
	def processRec (self):
		self.root.toxml()
		concepts = self.rec.selectNodes (self.rec.dom, "rdf:RDF/skos:Concept")
		# print "%d concepts" % len (concepts)
		for concept in concepts:
			purl = concept.getAttribute ("rdf:about")
			key = os.path.basename (purl)
			label = self.getSubElementText ("skos:prefLabel", concept)
			self[key] = label
			
	def getValue (self, key):
		return self[key]
	
	def getSubElementText (self, tagName, element=None):
		element = element or self.root
		subElement = XmlUtils.getChild (tagName, element)
		if subElement:
			return XmlUtils.getText (subElement)
			
	def getSubElementResource (self, tagName, element=None):
		element = element or self.root
		subElement = XmlUtils.getChild (tagName, element)
		if subElement:
			return subElement.getAttribute ("rdf:resource")
			
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
			
	def report (self):
		for key in self.keys():
			print "%s: %s" % (key, self[key])
			
class TopicHelper  (HelperResponse):
	
	url = "http://purl.org/ASN/scheme/ASNTopic/#"
	
class AuthorHelper  (HelperResponse):
	
	url = "http://purl.org/ASN/scheme/ASNJurisdiction/#"
	
	kludge_mappings = {
		'NAEP':'NAEP'
		}
	
class AsnHelperException (Exception):
	pass
	
class AsnHelper:
	
	def __init__ (self):
		self.topics = TopicHelper()
		self.authors = AuthorHelper()
		
	def getAuthor (self, key):
		if not self.authors.has_key (key):
			# print "COULD NOT find topic for '%s'" % key
			raise AsnHelperException, "Author '%s' could not be resolved" % key
		return self.authors[key]
		
	def getTopic (self, key):
		if not self.topics.has_key (key):
			self.topics.report()
			raise AsnHelperException, "Topic '%s' could not be resolved" % key
		return self.topics[key]
	
def AsnHelperTester ():
	# TopicHelper().report()
	helper = AsnHelper()

	print "\nAUTHORS"
	helper.authors.report()

	print "\nTOPICS"
	helper.topics.report()
	
#	author = "NSES"
#	print "%s: %s" % (author, helper.getAuthor(author))
	topic = "socialStudies"
	print "%s: %s" % (topic, helper.getTopic(topic))	

if __name__ == '__main__':
	
	AuthorHelper().report()


