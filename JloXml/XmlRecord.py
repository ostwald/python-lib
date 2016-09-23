from xml.dom import DOMException, Node
from xml.dom.minidom import parse, parseString
from xml.parsers.expat import ExpatError
import sys
import string
import os
import re
import codecs
import XmlUtils
from prettyPrinter import XmlFormatter  
from xml_declaration_fixer import DeclarationFixer

class JloXmlException (Exception):
	pass

class XmlRecord:

	SCHEMA_INSTANCE_URI = "http://www.w3.org/2001/XMLSchema-instance"
	xpath_delimiter = ":"
	schema_instance_namespace = "xsi"
	default_encoding = 'utf-8'
	debug = 0
	
	def __init__ (self, path=None, xml=None, encoding=None):
		"""
		XmlRecord should be called with EITHER "xml" or "path" params
		"""

		if xml and path:
			raise JloXmlException, "either but not both of 'xml' and 'path' allowed"
		
		self.dom = None
		self.doc = None
		self.recordXml = None
		self.path = path
		self.encoding = encoding or self.default_encoding

		# print "new xmlRec with encoding='%s'" % self.encoding
		
		if xml is not None:
			self.recordXml = xml
			
			## experimental - the following worked for eaditem2xml.py ...\
			# print 'type of recordXml: ', type(self.recordXml)
			if type(self.recordXml) == type(u""):
				# print 'encoding as utf-8'
				## self.recordXml = self.recordXml.encode("utf8", "strict")
				pass

			elif type(self.recordXml) == type(""):
				# print "okay", type(self.recordXml)
				self.recordXml = unicode(self.recordXml)
				

			try:
				self.dom = parseString (self.recordXml.encode (self.encoding))
			except ExpatError, e:
				print sys.exc_info()[1], e
				
				# print "self.recordXml going into parseString: ", type(self.recordXml)
				# print self.recordXml
				
				# print 'self.debug is: ', self.debug
				
				if self.debug:
					bogout = "UNPARSEABLE.xml"
					fp = codecs.open (bogout, 'w', self.encoding)
					fp.write(self.recordXml)
					fp.close()
					print 'Wrote bogus response to %s' % bogout
				
				raise Exception, "XmlRecord couldn't parse as XML: %s" % e
				
		if path is not None:
			self.filename = os.path.split(self.path)[1]
			
			if not os.path.exists (path):
				errorMsg = "file does not exist at %s" % path
				raise IOError, errorMsg
			else:
				f = codecs.open(path, 'r', self.encoding)
				# print 'opened file'
				self.recordXml = f.read()
				f.close()
	
				try:
					# print 'parsing record'
					self.dom = parse (path)
	
				except ExpatError, exp:
					# raise DOMException, "%s\n\t(%s)" % (sys.exc_value, self.path)
					raise Exception, "%s\n\t(%s)" % (exp, self.path)
					
		self.root_name_space_prefix = None
		if self.dom is not None:
			self.doc = self.dom.documentElement
			self.root_name_space_prefix = self._getPrefix (self.doc.tagName)
			
	def _getPrefix (self, name):
		splits=name.split(':')
		if len(splits) == 2:
			return splits[0].strip()

	def qualify (self, name):
		return "%s:%s" % (self.schema_instance_namespace, name)
			
	def setSchemaNamespace (self, prefix=None):
		prefix = prefix or self.schema_instance_namespace
		self.doc.setAttribute ("xmlns:"+prefix, self.SCHEMA_INSTANCE_URI)
		
	def setDefaultNamespace (self, defaultNamespace):
		self.doc.setAttribute ("xmlns", defaultNamespace)
		
	def getSchemaLocation (self):
		return self.doc.getAttribute (self.qualify ("schemaLocation"))

	def setSchemaLocation (self, schemaUri, nameSpaceUri):
		data = "%s %s" % (nameSpaceUri, schemaUri)
		self.doc.setAttribute (self.qualify ("schemaLocation"), data)
			
	def getNoNamespaceSchemaLocation (self):
		return self.doc.getAttribute (self.qualify ("noNamespaceSchemaLocation"))

	def setNoNamespaceSchemaLocation (self, schemaUri):
		self.doc.setAttribute (self.qualify ("noNamespaceSchemaLocation"), schemaUri)

	def __repr__ (self):
##		return "%s\n%s\n%s" % ('-'*70, self.doc.toxml(), '-'*70)
		# print "__repr__ (%s)" % (self.encoding)
		# print "\n%s" % self.doc.toxml().encode(self.encoding)
		lines = self.doc.toprettyxml(" "*4, "\n", encoding=self.encoding).split("\n")
		
		stripped = [];add=stripped.append
		for line in lines:
			if string.strip(line):
				add (line)
		xml = string.join (stripped, "\n")
		
		## xml = "%s\n%s\n%s" % ('-'*70, xml, '-'*70)
		return xml

	def getElements (self, element):
		"""
		return list of child elements for given element
		"""
		els = []
		children = element.childNodes
		for i in range (children.length):
			child = children.item(i)
			if child.nodeType == child.ELEMENT_NODE:
				els.append (child)
		return els

	def addElement (self, element, tagName):
		"""
		returns the added element
		"""
		new = self.dom.createElement (tagName)
		element.appendChild (new)
		return new
		
	def clearElement (self, element):
		"""
		removes all content, attributes and children from element.
		this is done by first deleting the element and then adding a new element with 
		tagname of the deleted element.
		"""
		if not element: return
		parent = element.parentNode
		tagName = element.tagName
		if parent:
			parent.removeChild (element)
			element.unlink()
			return self.addElement (parent, tagName)
		
		
	def removeComments (self, element, recursive=False):
		for child in element.childNodes:
			if child.nodeType == Node.COMMENT_NODE:
				element.removeChild (child)
				child.unlink()
			elif recursive and child.nodeType == Node.ELEMENT_NODE:
				self.removeComments (child, recursive)
			
	def getValuesAtPath (self, xpath):
		"""
		return list of values for all nodes at specified path
		"""
		# nodes = self.selectNodes (self.dom, path)
		# if nodes:
			# return map (lambda e: self.getText(e), nodes)
		# else:
			# return []
		return XmlUtils.getValuesAtPath (self.dom, xpath, self.xpath_delimiter)

	def setRecordXml (self, xml):
		self.recordXml = xml.encode (self.encoding)
		try:
			self.dom = parseString (self.recordXml)
		except ExpatError:
			print "Parse Error: %s \n\t(%s)" % (sys.exc_info()[1], self.path)
			self.doc = None
			return
		self.doc = self.dom.documentElement

	def getTextAtPath (self, path):
		"""
		path is from documentElement down, e.g.,
		<record>
			<general>
				<id>1232</id>
		getTextAtPath("record:general:id") => 1232
		"""
		element = self.selectSingleNode (self.dom, path)
		if element:
			return self.getText (element)

	def setTextAtPath (self, path, text):
		"""
		raises exception if path does not exist
		"""
		node = self.selectSingleNode (self.dom, path)
		if node:
			# self.setText (element, text)
			if node.nodeType == Node.ATTRIBUTE_NODE:
				node.value = text
			else:
				XmlUtils.setText(node, text)
		else:
			raise Exception, "element not found at %s" % path
			
	def getText(self, node):
		"""
		returns text value of either attribute or element
		"""
		return XmlUtils.getText(node)

	def setText (self, element, value):

		return XmlUtils.setText(element, value)

	def selectNodes (self, element, xpath):
		"""
		same as getNodesByXpath
		"""
		return XmlUtils._getNodesByXpath (element, xpath, self.xpath_delimiter)

	def selectSingleNode (self, element, xpath):
		nodeList = XmlUtils._getNodesByXpath (element, xpath, self.xpath_delimiter)
		if nodeList:
			return nodeList[0]

	def write (self, path=None, verbose=False, pretty=False):
		if path is None:
			if self.path is None:
				raise JloXmlException, "XmlRecord has no path and no path was provided to write method" 
			path = self.path
			
		# f = open(path, 'w') # don't mess with encoding here
		f = codecs.open(path, 'w', self.encoding)
		
		if pretty:
			try:
				# f.write (self.pp())
				self.dom.writexml (f, '', " "*4, "\n", encoding=self.encoding)
			except:
				print "prettyPrint formatting error: %s \n\t(%s)" % (sys.exc_info()[1], path)
													
		else:
			try:
				self.dom.writexml (f, encoding=self.encoding)
				##### lines = self.doc.toprettyxml(" "*4, "\n").split("\n")
				if verbose:
					print "wrote to " + path
			except:
				msg = "XmlRecord write error(%s): %s \n\t(%s)" % (self.encoding, sys.exc_info()[1], path)
				#print msg
				raise Exception, msg
		f.close()
		DeclarationFixer (path, encoding=self.encoding)
		try:
			os.chmod(path, 0664)
		except:
			print "unable to chmod on %s" % path
			
	def delete_file (self):
		if self.path:
			os.remove (self.path)
		else:
			raise IOError, "can't delete %s because file does not exist"
			
	def deleteElement(self, element):
		"""
		removes element from dom
		"""
		if not element: return
		parent = element.parentNode
		if parent:
			parent.removeChild (element)
			element.unlink()
			
	def deleteElementsAtPath (self, xpath):
		"""
		removes all elements at specified xpath
			for example, to remove record/rights/access field
		"""
		elements = self.selectNodes (self.dom, xpath)
		if elements:
			# print '%d elements found at %s' % (len(elements), xpath)
			for el in elements:
				self.deleteElement (el)
			# print "updated %s" % self.getId()
			
	def removeAttributes (self, e):
		"""
		remove all attributes from this element (works for namespaces)
		"""
		atts = e.attributes
		if atts is None or atts.length == 0: return

		for i in range (atts.length-1, -1, -1):
			e.removeAttributeNode(e.attributes.item(i))

	def pp (self):
		"""
		returns a pretty-formated version of this record
		"""
		return XmlFormatter (self).pp()
			
if __name__ == "__main__":

	rec = XmlRecord (path="/home/ostwald/python-lib/ncar_lib/citations/pubs/PUBS_2010_metadata/PUBS-000-000-000-004.xml")
	print rec.pp()
	# rec.write()
