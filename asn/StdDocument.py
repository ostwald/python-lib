"""
Reads an Asn Standards Document file and provides dict interface for accessing individual
standards nodes.

Nodes are instances of AsnStandard by default, but this can be overridden.

"""

import sys
import string
import os
import re
import codecs

from UserDict import UserDict
from AsnRecord import AsnRecord
from AsnStandard import AsnStandard
import util
import AsnGlobals

class StdDocument (UserDict):

	"""
		Provides mapping interface onto an ASN StandardDocument, where the standards nodes are
		accessible by their unique IDs.
	"""
	
	stdConstructor = AsnStandard

	attrMap = {
		"version" : "asn:exportVersion",
		"fileCreated" : "asn:fileCreated",
		"created" : "dcterms:created",
		"title" : "dc:title",
		"description" : "dc:description"
	}
	
	
	def __init__ (self, path):
		"""
		Read a file as an "AsnRecord" object and then create the mapping from ids to standard Node instances.
		The Standards Nodes create a tree, with the root being the "StandardsDocument" Element.
		"""
		UserDict.__init__ (self)
		self.asnRecord = AsnRecord (path)
		self.root = None
		
		docElement = self.asnRecord.getStandardDocumentElement()
		if not docElement:
			raise "docElement not found"
		self.root = self.asnRecord.makeAsnNode (docElement, self.stdConstructor)
		
		self.docId = util.getNumId (self.root.id)
		
		# self.title = self.asnRecord.getDocTitle()
		# self.fileCreated = self.asnRecord.getFileCreated()
		# self.author = self.asnRecord.getAuthor()
		# self.created = self.asnRecord.getCreated()
		# self.topic = self.asnRecord.getTopic()
		
		## print docElement.toxml()
		for attr in self.attrMap.keys():
			tagName = self.attrMap[attr]
			# print "\n", attr
			val = self.asnRecord.getSubElementText (docElement, tagName)
			# print "val: %s" % val
			setattr (self, attr, val)
			# print "%s: %s" % (attr, getattr (self, attr))
			
		self.topic = self.asnRecord.getTopic()
		self.author = self.asnRecord.getAuthor()

		self.add (self.root)
		
		standardsElements = self.asnRecord.getStandardsElements()
		# print "%d standards elements found" % len (standardsElements)
		for e in standardsElements:
			self.add (self.asnRecord.makeAsnNode (e, self.stdConstructor))

		self.levels = self.assignLevels()

	def __getitem__(self, key):
		if self.has_key (key):
			return self.data[key]
		else:
			return None

	def assignLevels (self):
		"""
		assign a "level" to each node, returning max level
		"""
		maxLevel = -1
		for key in self.keys():
			std = self[key]
			if std == self.root: std.level = -1
			else:
				std.level = len (self.ancestorsOf (std))
			maxLevel = max (maxLevel, std.level)
		return maxLevel

	def add (self, standard):
		"""
		add a standard
		"""
		## print ("adding " + standard.id)
		self.update ({standard.id: standard})

	def toString (self):
		s=[];add=s.append
		for key in self.data.keys():
			add (self[key].toString())
		return string.join (s, "\n")

	def parentOf (self, std):
		"""
		find the parent of a given node
		"""
		if std is None:
			raise "Node not found for ", stdId
		return self[std.parent]

	def ancestorsOf (self, std):
		anscestors = []
		ptr = std
		while ptr:
			ptr = self.parentOf (ptr)
			if ptr:
				anscestors.append (ptr)
		return anscestors

	def showOutline (self, baseStd, level=0, maxlevels=4):
		if level > maxlevels:
			return
		indentStr = "  "
		indent = indentStr * level
		lineOut = "%s(%d)- %s - %s" % (indent, level, getNumId (baseStd.id), baseStd.description)
		print lineOut.encode ("utf-8", 'replace')
		if (baseStd.children):
			for std in baseStd.children:
				self.showOutline (self[std], level+1, maxlevels)
				
def showNode (stdDoc, idNum):
	id = makeFullId (idNum)
	std = stdDoc[id]
	print std.toString()
	
def anscestorTest (stdDoc, idNum):
	id = makeFullId (idNum)
	std = stdDoc[id]
	foo = stdDoc.ancestorsOf(std)
	print "%d ancestors found" % len (foo)
	for a in foo:
		print a.toString()
				
if __name__ == "__main__":
	# path = AsnGlobals.coloradoPath
	basedir = "/Users/ostwald/devel/python-lib/common_core/data"
	filename = 'Math-2010-CCSS-Common Core Math.xml'
	path = os.path.join (basedir, filename)
	stdDoc = StdDocument (path)

	# showNode (stdDoc, "S1017304")

	# stdDoc.showOutline (asn[makeFullId("S102A818")], maxlevels=3)

	
	## print asn.toString()

