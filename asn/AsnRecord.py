"""
Reads an ASN standards document file as an XML Record, and provides accessors
for key elements wtihin the XML.

Provides factory to construct standards nodes using specified 
constructor class (AsnStandard by default).

Does not actually create nodes, though, this is left to implementor (e.g., StdDocument.py)
"""

from xml.dom.minidom import parse, parseString
from xml.parsers.expat import ExpatError
import sys
import string
import os
import re
import codecs

if (sys.platform == 'win32'):
	sys.path.append ("H:/python-lib")
else:
	sys.path.append ("/home/ostwald/python-lib")

from JloXml import XmlRecord, XmlUtils
from AsnStandard import AsnStandard
from util import *

class AsnRecord (XmlRecord):

	xpath_delimiter = '/'
	"""
		Helper class to supply methods for reading the xml contained in ASN StandardsDocuments.
		Parses the XML File containing the following top-level elements:
		- StandardDocument - information about this Standards Document
		- Statment(s) - the Standards themselves
	"""
	
	def getStandardDocumentElement (self):
		xpath = "rdf:RDF/asn:StandardDocument"
		return self.selectSingleNode (self.dom, xpath)

	def getStandardsElements (self):
		xpath = "rdf:RDF/asn:Statement"
		return self.selectNodes (self.dom, xpath)

	def getDocTitle (self):
		title = "Document Title"
		root = self.getStandardDocumentElement()
		if root:
			titleElement = self.selectSingleNode (root, "dc:title")
			if titleElement:
				title = self.getText (titleElement)
		return title
		
	def getFileCreated (self):
		created = "File Created"
		root = self.getStandardDocumentElement()
		if root:
			fcElement = self.selectSingleNode (root, "asn:fileCreated")
			if fcElement:
				created = self.getText (fcElement)
		return created
		
	def getCreated (self):
		created = "Created"
		root = self.getStandardDocumentElement()
		if root:
			fcElement = self.selectSingleNode (root, "dcterms:created")
			if fcElement:
				created = self.getText (fcElement)
		return created
		
	def getAuthorPurl (self):
		root = self.getStandardDocumentElement()
		if root:
			return self.getSubElementResource (root, 'asn:jurisdiction')
		
	def getTopicPurl (self):
		root = self.getStandardDocumentElement()
		if root:
			return self.getSubElementResource (root, 'dc:subject')
			
	def getTopic (self):
		purl = self.getTopicPurl()
		if purl:
			return os.path.basename (purl)
		
	def getAuthor (self):
		purl = self.getAuthorPurl()
		if purl:
			return os.path.basename (purl)
			
	def getSubElementText (self, element, tagName):
		subElement = XmlUtils.getChild (tagName, element)
		if subElement:
			return XmlUtils.getText (subElement)
			
	def getSubElementResource (self, element, tagName):
		subElement = XmlUtils.getChild (tagName, element)
		if subElement:
			return subElement.getAttribute ("rdf:resource")	
	
	def makeAsnNode (self, element, stdConstructor=AsnStandard):
		"""
		determine attributes from the provided element and use them to 
		construct a AsnNode of specified class
		"""
		# get id
		id = element.getAttribute ("rdf:about")
		if not id:
			raise Exception, 'id not found'

		# get description
		description = ""
		descriptionElement = self.selectSingleNode (element, "dc:description")
		if descriptionElement:
			description = self.getText (descriptionElement)

		# get children
		children = []
		childNodes = self.selectNodes (element, "gemq:hasChild/rdf:Seq/rdf:li")
		## print "%d children found" % len (childNodes)
		if childNodes:
			for c in childNodes:
				children.append (c.getAttribute ("rdf:resource"))

		# get parent
		parent = None
		isChildOf = self.selectSingleNode (element, "gemq:isChildOf")
		if isChildOf:
			parent = isChildOf.getAttribute ("rdf:resource")
		
		# get gradeRange
		gradeRange = GradeRange (self.selectNodes (element, "dcterms:educationLevel"))
			
		return stdConstructor (id, children, parent, description, gradeRange)

		
if __name__ == "__main__":
	basedir = "/home/ostwald/Documents/ASN/ASN-2010-0903/Math"
	filename = 'Math-2010-CCSS-Common Core Math.xml'
	path = os.path.join (basedir, filename)
	
	rec = AsnRecord (path)
	root = rec.getStandardDocumentElement()
	if not root:
		print "Root not found"
	else:
		print root.toxml()
	stds = rec.getStandardsElements()
	print "%d standards found" % len (stds)
	
