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

class AsnUriResolver (ServiceClient):

	url_opener = urllib.FancyURLopener()	#needed because URI resolver redirects
	
	def __init__ (self, purl):
		self.baseUrl = purl
		self.setRequest(purl)
		self.success = 0
		response = self.getResponse ()
		if response.hasError():
			print response.error
		else:
			self.response = ResolverResponse (xml=response.doc.recordXml)

class StdNode:

	"""
	Works on a Status entry as an element
	"""
	
	def __init__ (self, element):
		self.element = element
		self.id = self.element.getAttribute ("rdf:about")
		typepurl = self.getSubElementResource ("rdf:type")
		if typepurl:
			self.stdtype = os.path.basename (typepurl)
		else:
			raise Exception, "stdtype not found"
		# print self.id, self.stdtype
		
	def isDocNode (self):
		return self.stdtype == "StandardDocument"

	def getSubElementText (self, tagName):
		subElement = XmlUtils.getChild (tagName, self.element)
		if subElement:
			return XmlUtils.getText (subElement)
			
	def getSubElementResource (self, tagName):
		subElement = XmlUtils.getChild (tagName, self.element)
		if subElement:
			return subElement.getAttribute ("rdf:resource")
		
class ResolverResponse (XmlRecord):
	xpath_delimiter = "/"
	nodes_path = "rdf:RDF/rdf:Description"
	
	def __init__ (self, path=None, xml=None):
		XmlRecord.__init__ (self, path, xml)
		self.docNode = None
		self.nodeMap = self.getNodeMap()

	def getNodeMap (self):
		elements = self.getElementsByXpath (self.dom, self.nodes_path)
		# print "%d elements read" % len(elements)
		nodeMap = UserDict()
		for element in elements:
			stdNode = StdNode (element)
			if stdNode.isDocNode():
				self.docNode = stdNode
			nodeMap[stdNode.id] = stdNode
		return nodeMap
		
	def getTopic (self):
		purl = self.docNode.getSubElementResource ("dc:subject")
		if purl:
			return os.path.basename (purl)
			
	def getAuthor (self):
		purl = self.docNode.getSubElementResource ("asn:jurisdiction")
		if purl:
			return os.path.basename (purl)	
			
	def getCreated (self):
		return self.docNode.getSubElementText ("j.0:created")
			
def getDocInfo (purl):
	resolver = AsnUriResolver (purl)
	response = resolver.response
	## print "docNode", response.docNode.id
	print "\t author", response.getAuthor()
	print "\t topic", response.getTopic()
	print "\t created", response.getCreated()	
	
if __name__ == '__main__':
	
	purl = "http://purl.org/ASN/resources/S103E250"
	resolver = AsnUriResolver (purl)
	response = resolver.response
	print "docNode", response.docNode.id
	print "author", response.getAuthor()
	print "topic", response.getTopic()
	print "created", response.getCreated()

