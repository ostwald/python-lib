"""
Purpose: Scraping data from webCat
How to use:
	navigate to a WebCat page that contains desired info (starting at http://library.ucar.edu)
	copy and past the url into the "url" varable at the bottom of this page.
	make sure the "collection" parameter matches the desired node title from the html page
	running "getMetadata" will collect all metadata under the starting node and write it to a directory
	named after the "collection"
"""
from JloXml import XmlRecord, XmlUtils
# import re
import sys, os
from UserDict import UserDict
from ArchiveBrowsePage import ArchiveBrowsePage
from WebCatMetadata import WebCatMetadata
import webcatUtils

class WebCatNode:
	def __init__ (self, element):
		"""
		element is a row element containing an unknown number of cells.
		the last cell is where the data is, the others are "indents", which
		determin this node's "level"
		"""
		
		cells = XmlUtils.getChildElements (element, "TD")
		self.level = len(cells) - 1;
		dataCell = cells[-1]
		components = XmlUtils.getChildElements (dataCell, "A")
		icon = components[0]
		img = XmlUtils.getChild ("IMG", icon)
		filename = os.path.split (img.getAttribute ("SRC"))[1]
		self.type = filename.split(".")[0]
		self.metadatapath = webcatUtils.webcatDomain + icon.getAttribute ("HREF")
		
		linkElement = components[1]
		url = linkElement.getAttribute ("HREF")
		label = XmlUtils.getText (linkElement)
		self.link = webcatUtils.WebCatLink ((url, label))
		self.title = self.link.label
		self.parent = None
		self.children = None
		
	def getMetadata (self, prefix):
		return WebCatMetadata (self.metadatapath, prefix)
		
	def addChild (self, node):
		if self.children is None:
			self.children = []
		if not node in self.children:
			self.children.append (node)
			# print "%s added child: %s" % (self.title, node.title)
		
	def getGliph (self):
		if self.type == "ISSUE": return "*"
		if self.children is None: return "-"
		return "+"
			
	def __repr__ (self):
		indent = self.level * '   '
		# return "%s%s (%d)" % (indent, self.link.label, self.level)
		return "%s %s %s" % (indent, self.getGliph(), self.link.label)
		
	def hierarchy (self):
		print self
		if self.children:
			for child in self.children:
				child.hierarchy()

class WebCat (UserDict):
	"""
	we treate the browse hierarchy table as an xml record...
	"""
	
	def __init__ (self, url):
		UserDict.__init__ (self)
		self.root = None
		self.nodes = []
		
		self.importPage (url)
		
	def getChildren (self, title):
		node = self.getNode (title)
		if not node:
			msg = 'getChildren can find starting node ("%s")' % title
			raise Exception, msg
		if node.children is None:
			self.importPage (node.link.url)
		return node.children
		
	def importPage (self, url):
		page = ArchiveBrowsePage (url)
		lastnode = None
		for nodeElement in page.nodeElements:
			node = self.findOrMakeNode (nodeElement)
			if lastnode == None:
				if not self.root: # we may already have imported the root
					self.root = node
			elif lastnode.level < node.level:
				if not node.parent:
					node.parent = lastnode
				lastnode.addChild (node)
			else:
				if not node.parent:
					node.parent = lastnode.parent
				lastnode.parent.addChild (node)
			lastnode = node

	def findOrMakeNode (self, nodeElement):
		newNode = WebCatNode (nodeElement)
		oldNode = self.getNode (newNode.title)
		if oldNode:
			return oldNode
		else:
			self.addNode (newNode)
			return newNode
		
	def getNode (self, title):
		if self.has_key (title):
			return self[title]
		else:
			return None
			
	def hasNode (self, title):
		return self.has_key(title)
		
	def addNode (self, node):
		if (self.hasNode (node.title)):
			msg = "duplicate title (%s)" % node.title
			raise Exception, msg
		self.nodes.append (node)
		self[node.title] = node
		
	def getLeaves (self, node, leaves=[]):
		"""
		traverses subtree under "node" until there are no more
		FOLDERS remaining
		"""
		if not node:
			raise Exception, "getLeaves called with no node!"
		children = self.getChildren (node.title)
		for child in children:
			if child.type == "FOLDER" and child.children is None:
				try:
					self.getLeaves (child, leaves)
				except:
					print "Exception: %s for '%s'" % (sys.exc_info()[1], child.title)
			elif child.type == "ISSUE":
				leaves.append (child)
		return leaves
				
	def getComposites (self, node, composites=[]):
		"""
		traverses subtree under "node" until there are no more
		FOLDERS remaining
		"""
		if not node:
			raise Exception, "getComposites called with no node!"
		children = self.getChildren (node.title)
		allLeaves = True
		for child in children:
			if child.type == "FOLDER":
				# print "not adding: " + node.title
				try:
					self.getComposites (child, composites)
				except:
					print "Exception: %s for '%s'" % (sys.exc_info()[1], child.title)
				allLeaves = False

		if allLeaves:
			composites.append (node)
			# print "added ", node.title
			
		return composites
		
	def toString (self):
		s=[];add=s.append
		for node in self.nodes:
			add (node.__repr__())
		return "\n".join (s)
		
	def hierarchy (self):
		self.root.hierarchy()
	
def getMetadata (url, collection, prefix):
	destDir = "WebCatMetadata/%s" % collection
	if not os.path.exists (destDir):
		os.makedirs(destDir)
	cat = WebCat (url)
	node = cat.getNode (collection)
	leaves = cat.getLeaves (node)
	cat.hierarchy()
	count = len (leaves)
	errors = []
	for i, l in enumerate (leaves):
		try:
			md = l.getMetadata(prefix)
			## md.write(destDir)
			msg = "%d/%d" % (i, count)
			print (msg)
		except:
			errors.append ( "%d/%d: couldn't write to %s: %s" % (i, count, md.url, sys.exc_info()[1]))
	if errors:
		print "\nERRORS:\n" + "\n".join (errors)
	
	
def processCompositeRecords (url, collection, prefix="FOO"):
	cat = WebCat (url)
	node = cat.getNode (collection)
	composites = cat.getComposites (node)
	for comp in composites:
		print comp.title
	count = len (composites)
	errors = []
	for i, comp in enumerate (composites):
		try:
			md = comp.getMetadata(prefix)
			print md
			sys.exit()
			## md.write(destDir)
			msg = "%d/%d" % (i, count)
			print (msg)
		except:
			errors.append ( "%d/%d: couldn't write to %s: %s" % (i, count, md.url, sys.exc_info()[1]))
	if errors:
		print "\nERRORS:\n" + "\n".join (errors)
		
def getMonographs():
	url = "http://www.library.ucar.edu/uhtbin/cgisirsi/DLNyXHQdFY/SIRSI/310750009/503/6862"
	collection = "Monographs"
	prefix = "MONOGRAPH"
	getMetadata (url, collection, prefix)	
	
def getManuscripts():
	url = "http://www.library.ucar.edu/uhtbin/cgisirsi/0xDXBgD2CU/SIRSI/310750009/503/991"
	collection = "NCAR Manuscripts"
	prefix = "MANUSCRIPT"
	getMetadata (url, collection, prefix)	
	
def getTheses():
	url = "http://library.ucar.edu/uhtbin/cgisirsi/iSpEBmOWtw/SIRSI/44010022/503/996"
	collection = "Cooperative Theses"
	prefix = "THESES"
	getMetadata (url, collection, prefix)
	
def compositeTester():
	url = "http://www.library.ucar.edu/uhtbin/cgisirsi/OykNJYO0RB/SIRSI/310750009/503/993"
	collection = "NCAR Technical Notes 21-40"
	processCompositeRecords (url, collection)
	
if __name__ == "__main__":
 	compositeTester ()
