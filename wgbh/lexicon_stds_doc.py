"""
Represent WGBH Lexicon as XML document that can be processed by schemedit's standards machinery,
which provides tree "browse/select" and "selected" views - the suggestion stuff only without suggestions

This is done by reading in the lexicon_tree XML and converting to a standards
Document form (see common_core/comm_core_doc.py and resulting "converted" xml form)

<td-lexicon>
    <Document>
        <version>
        <topic>
        <author>
        <title>
        <id>
        <fileCreated>July 6 2010
        <description>
        <children>
            <child>childID
			 ... 
        </children>
    </Document>
    <Standard>
        <id>
        <itemText>
        <startGradeLevel>
        <endGradeLevel>
        <parent>parentID
        <children>
            <child>childID
            ...
    </Standard>
	...

"""
import os, sys
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
from lexicon_tree import LexiconTree
from lexicon import LexiconWorkSheet, lexicon_set_map

class LexNode:
	
	def __init__ (self, text, id=None):
		self.text = text
		self.id = id or text
		self.children = []
		self.parent = ""
		
		# if this node is a "category", use the pretty form for the text ...
		if self.id in lexicon_set_map.keys():
			self.text = lexicon_set_map[self.id]
		
	def getItemText (self):
		"""
		return the last segment
		"""
		return self.text.split("::")[-1].strip()
		
	def addChild (self, child):
		if not child in self.children:
			self.children.append (child)
		
	def __repr__ (self):
		s=[];add=s.append
		if self.text == self.id:
			add ("%s" % self.text)
		else:
			add ("%s (%s)" % (self.text, self.id))
		for child in self.children:
			# add (" - %s" % child)
			pass
		return '\n'.join (s)

class NodeMap (UserDict):
	
	def __init__ (self):
		UserDict.__init__ (self)
		
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def __getitem__ (self, key):
		if not self.data.has_key(key):
			return None
		return self.data[key]
		
	def __setitem__ (self, key, value):
		if self.data.has_key (key):
			# raise KeyError, "Attempting to overwrite existing value for '%s'" % key
			print "overwrite existing value for '%s'" % key
		self.data[key] = value
		
	def __repr__ (self):
		s = [];add=s.append
		for key in self.keys():
			add ("[%s] - %s" % (key, self[key]))
		return '\n\n'.join (s)
		
class LexiconStdDocument (XmlRecord):
	
	def __init__ (self):
		self.docId = "td-lexicon"
		XmlRecord.__init__ (self, xml="<%s/>" % self.docId)
		self.lexiconData = LexiconWorkSheet ()
		self.termMap, self.idMap = self.makeTermAndIdMap()
		self.nodeMap = NodeMap()
		self.processNodes()
		self.makeDoc()
		
	def makeDoc (self):
		self.doc.appendChild(self.getDocElement())
		for key in self.nodeMap.keys():
			self.doc.appendChild(self.getStandardElement (key))
		
	def getDocElement (self):
		docEl = self.dom.createElement ("Document")
		XmlUtils.addChild (self.dom, "version", "0.0.1", docEl)
		XmlUtils.addChild (self.dom, "topic", "all", docEl)
		XmlUtils.addChild (self.dom, "author", "WGBH-Teachers Domain", docEl)
		XmlUtils.addChild (self.dom, "title", "Teachers Domain Lexicon", docEl)
		XmlUtils.addChild (self.dom, "id", self.docId, docEl)
		XmlUtils.addChild (self.dom, "fileCreated", "Aug 5 2010", docEl)
		XmlUtils.addChild (self.dom, "description", "This is a test document", docEl)
		childrenEl = self.addElement (docEl, "children")
		for childKey in self.nodeMap[self.docId].children:
			XmlUtils.addChild (self.dom, "child", self.getNodeId(childKey), childrenEl)
		return docEl
		
	def makeTermAndIdMap (self):
		termMap = UserDict()
		idMap = UserDict()
		for term in self.lexiconData:
			termKey = term.prettyTerm
			idKey = term.id
			if termMap.has_key(termKey):
				print "dup term: " + termKey
				continue
			if idMap.has_key(idKey):
				print "dup id: " + idKey
				continue
			termMap[termKey] = term
			idMap[idKey] = term
		return termMap, idMap
			
		
	def processNodes (self):
		"""
		populate the nodeMap with 
		"""
		
		self.nodeMap[self.docId] = LexNode (self.docId)
		
		for term in self.lexiconData.data:
			# take care of the anscestors, 
			parts = term.raw_xpath.split ("/")
			for i, segment in enumerate (parts[:-1]):
				# key = " :: ".join (parts[:i+1])
				key = self.makeTermKey (parts[:i+1])
				# print "node: %s*" % key
				if not self.nodeMap.has_key (key):
					self.nodeMap[key] = LexNode(key)
				if i > 0:
					parent = self.makeTermKey (parts[:i])
				else:
					parent = self.docId
				# print "  parent: %s" % parent
				self.nodeMap[key].parent = parent
				self.nodeMap[parent].addChild(key)
					
			## now we deal with the term itself
			# key = " :: ".join(parts)
			key = self.makeTermKey (parts)
			self.nodeMap[key] = LexNode (key, term.id)
			# parent = " :: ".join (parts[:-1])
			parent = self.makeTermKey (parts[:-1])
			self.nodeMap[key].parent = parent
			self.nodeMap[parent].addChild(key)
			
	def makeTermKey (self, parts):
		# return " :: ".join(parts)
		return "::".join(parts)
			
	def showHierarchy (self):
		print "\n\n-- Hierarchy --"
		for category in lexicon_set_map.keys():
			node = self.nodeMap[category]
			if not node:
				continue
			print node
			for child in node.children:
				self.showNode (child)
			
	def showNode (self, key):
		level = len(key.split("::")) -1
		node = self.nodeMap[key]
		print "%s%s" % (level*'   ', node)
		for child in node.children:
			self.showNode (child)
			
	def getNodeId (self, key):
		return self.nodeMap[key].id
			
	def getStandardElement (self, key):
		node = self.nodeMap[key]
		nodeEl = self.dom.createElement ("Standard")
		XmlUtils.addChild (self.dom, "id", node.id, nodeEl)
		XmlUtils.addChild (self.dom, "itemText", node.getItemText(), nodeEl)
		XmlUtils.addChild (self.dom, "parent", node.parent, nodeEl)
		childrenEl = self.addElement (nodeEl, "children")
		for childKey in node.children:
			XmlUtils.addChild (self.dom, "child", self.getNodeId(childKey), childrenEl)
		return nodeEl
	
			
if __name__ == '__main__':
	doc = LexiconStdDocument()
	# print doc
	# print "lexiconData has %d entries" % len (doc.lexiconData)
	# print "termMap has %d entries" % len (doc.termMap)
	# print "idMap has %d entries" % len (doc.idMap)
	# print "nodeMap has %d entries" % len (doc.nodeMap)
	# print "\nNodeMap\n%s" % doc.nodeMap
	# doc.showHierarchy()
	
	# print doc.getStandardElement("language_arts::Writing::Grammar").toprettyxml()
	doc.write ("LEXICON_STANDARDS.xml", pretty=True)
	
