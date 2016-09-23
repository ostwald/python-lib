## XML Utils
import re, sys
import xml.dom.minidom
dom = xml.dom.minidom
from xml.dom import DOMException, Node
domImpl = dom.getDOMImplementation()

indexPat = re.compile("(.*?)\[([\d]*?)\]")

def createDocument (rootTagName, namespaceUri=None):
	"""
	Create and return a document having root element named from provided
	rootTagName (and namespace if provided)
	"""
	return domImpl.createDocument (namespaceUri, rootTagName, None)

def createElement (tagName, namespaceUri=None):
	"""
	Returns unattacted element with provided tagName and namespace (if any)
	"""
	doc = createDocument(tagName, namespaceUri)
	root = doc.removeChild (doc.documentElement)
	return root
	
def selectSingleNode (element, xpath, xpath_delimiter="/"):
	nodes = _getNodesByXpath (element, xpath, xpath_delimiter)
	if nodes:
		return nodes[0]
	else:
		return None

def selectNodes (element, xpath, xpath_delimiter="/"):
	return _getNodesByXpath (element, xpath, xpath_delimiter)
		
	
def getChild (tagName, element):
	children = element.getElementsByTagName (tagName)
	if children:
		return children.item(0)
		
def getChildElements (element, childTag=None):
	els = []
	if not element:
		return els
	children = element.childNodes
	for i in range (children.length):
		child = children.item(i)
		if child.nodeType == child.ELEMENT_NODE:
			if childTag is None or child.nodeName == childTag:
				els.append (child)
	return els
		
	
def orderElements(parent, field_order_list):
	"""
	enforce schema-ordering of child elements.
	does this depend on a certain version of python??
	
	side effect is that parent's elements are reordered.
	"""
	children = getChildElements(parent)
	if not children:
		print 'orderElements given NO children'
		return
		
		
	# for child in children:
		# print child.tagName
	# 
	# print '\nfield_order_list'
	# print '  - %s' % ('\n  - '.join(field_order_list))
		

	## prior to version 2.4, the sort function must take
	## two args and return an int
	if sys.version_info < (2, 4):
		def keyFn (e1, e2):
			i1 = field_order_list.index(e1.tagName)
			i2 = field_order_list.index(e2.tagName)
			return cmp(i1, i2)
	
		children.sort(keyFn)
	else:
		keyFn = lambda x:field_order_list.index(x.tagName)
		children.sort(key=keyFn)
			
	for el in children:
		parent.appendChild(el)
	
def getValuesAtPath (element, path, delimiter="/"):
	"""
	return list of values for all nodes at specified path
	"""
	nodes = selectNodes (element, path, delimiter)
	if nodes:
		return map (lambda e: getText(e), nodes)
	else:
		return []
	
def getTextAtPath (element, path, delimiter="/"):
	"""
	NOTE: works most gracefully when default delimiter ('/') is used
	"""
	node = selectSingleNode (element, path, delimiter)
	return node and getText (node)
	
def getText (node):
	"""
	returns text value of either attribute or element
	"""
	if node.nodeType == node.ATTRIBUTE_NODE:
		return node.nodeValue
	
	element = node
	rc = ""
	# accomodate rdf:parseType="Literal"
	parseLiteral =  element.getAttribute ("parseType") == "Literal"
	
	for node in element.childNodes:
		if node.nodeType == node.TEXT_NODE:
			rc = rc + node.data
		elif node.nodeType == node.ELEMENT_NODE and parseLiteral:
			rc = rc + node.toxml()
	# return string.strip(rc).encode ("utf8")
	return rc.strip()
	
def setText (element, value):
	"""
	sets text of provided element with provided value
	"""
	
	# duh - this is confusing because i'm calling an attribute an element
	if element.nodeType == Node.ATTRIBUTE_NODE:
		element.value = value
		return
	
	element.normalize ()
	for node in element.childNodes:
		if node.nodeType == node.TEXT_NODE:
			node.data = value
			return
	text = domImpl.createDocument (None, None, None).createTextNode (value)
	element.appendChild (text)
	return element
	
def getChildText (element, tagName):
	"""
	Gets text of first (tagName) child provided element
	"""
	child = getChild (tagName, element)
	if child:
		return getText (child)
		
def addChild (doc, tagName, text, parent=None):
	"""
	add a child to "parent" with specified tagName and text/content
	- parent is optional (defaults to documentElement)
	RETURNS child
	"""
	parent = parent or doc.documentElement
	## child = root.appendChild (doc.createElement (tagName))
	child = addElement (doc, parent, tagName)
	child.appendChild (doc.createTextNode (text))
	return child
	
def addElement (doc, parent, tagName):
	"""
	creates new element as child of parent and named as provided tagName
	RETURNS newly created element
	"""
	return parent.appendChild (doc.createElement (tagName))
	
def insertAsFirstChild (parent, child):
	"""
	insert child node as the first child of parent
	"""
	children = getChildElements (parent);
	if children:
		parent.insertBefore(child, children[0])
	else:
		parent.appendChild(child)
	
def getPath (node, reference_element=None, xpath_delimeter=":"):
	"""
	WARNING: is not attribute aware!
	"""
	segments = [node.tagName]
	parent = node.parentNode

	while parent:
		segments.append (parent.tagName)
		parent = parent.parentNode
		if parent.__class__.__name__ == "Document":
			break
	segments.reverse()
	return xpath_delimeter.join(segments)
	
class AttributeRestriction:
	
	attrPat = re.compile("(.*?)\[@(.*)=[\'\"](.*)[\'\"]\]")
	
	def __init__ (self, pathSegment):
		self.isRestriction = False
		self.tagName = self.attrName = self.value = None
		
		m = self.attrPat.match(pathSegment)
		if m:
			self.isRestriction = True
			self.tagName = m.group(1)
			self.attrName = m.group(2)
			self.value = m.group(3)
			
	def matchesElement(self, element):
		if element.tagName != self.tagName:
			return False
		if not element.hasAttribute (self.attrName):
			return False
		if element.getAttribute(self.attrName) != self.value:
			return False
		return True
	
def _getNodesByXpath (element, xpath, xpath_delimiter="/"):
		"""
		returns a list of nodes at xpath relative to element
		- handles element indexing and attributes
		- also handles xpath expression containing attribute/values (e.g., /[@someAttr='someValue'/,
		  but this requires an exact match for someValue (no wildcarding)
		"""
		# if xpath_delimiter == '/':
			# raise Exception, 'delimiter is /'
		splits = xpath.split (xpath_delimiter)
		tagName = splits[0]
		
		if not tagName:
			return []
		
		index = None
		m = indexPat.match (splits[0])
		if m:
			tagName = m.group(1)
			index = int(m.group(2))
			if index < 1:
				raise KeyError, "illegal xpath index: %d" % index
		
		
		attrRestriction = AttributeRestriction (splits[0])
		if attrRestriction.isRestriction:
			#filter by attribute restriction
			tagName = attrRestriction.tagName
			children = filter (lambda x: attrRestriction.matchesElement(x), getChildElements(element))
			
		else:
			# contruct list of child elements that match leaf segment of xpath
			children = getChildElements(element,tagName)
		
		if 0:
			print "\nxpath: %s (%d)" % (xpath, len(splits))
			# print element.toxml()
			print "\nCHILDREN (%d)" % len(children)
			print "----------------\n"
		
		# if there is an index, we are effectively reducing the children to a 
		# list containing only the indexed child
		if index is not None:
			# print 'INDEX: %d' % index
			if len(children) > index -1:
				children = [children[index-1]]
			else:
				# this was an out-of-bounds index
				return []
		
		if len(splits) == 1:
			# print 'LENGTH 1!'
			if tagName[0] == '@':
				return [element.getAttributeNode (tagName[1:])]
			return children
		else:
			elements = []
			for child in children:
				elements = elements + _getNodesByXpath (child, xpath_delimiter.join( splits[1:]), xpath_delimiter)
			return filter (None, elements)


	
def pp (element):
	# return element.toprettyxml()
	
	#  prettyxml contains a bunch of blank lines - strip them
	lines = element.toprettyxml(" "*4, "\n").split("\n")
	return '\n'.join (filter (lambda x: x.strip(), lines))
	# stripped = [];add=stripped.append
	# for line in lines:
		# if string.strip(line):
			# add (line)
	# returnstring.join (stripped, "\n")
	
if __name__ == '__main__':
	from XmlRecord import XmlRecord
	rec = XmlRecord (path='/home/ostwald/python-lib/ncar_lib/dups/data/metadata/osgc/OSGC-000-000-001-618.xml')
	
	print rec
		## print osmRecord
	xpath_delimeter = rec.xpath_delimiter
	segs = ['record', 'general', 'pubName', '@type']
	path = xpath_delimeter.join(segs)
	node = rec.selectSingleNode (rec.dom, path)
	if node is None:
		print "node not found at ", path
	else:
		print getPath (node, xpath_delimeter=xpath_delimeter)
