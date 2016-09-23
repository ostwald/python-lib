import os, sys
from JloXml import XmlUtils

XSD_PREFIX = None
XSD_NAMESPACE_URI = 'http://www.w3.org/2001/XMLSchema'

def qualify (s): 
	if s == '' or isqualified(s):
		return s
	else:
		return "%s:%s" % (XSD_PREFIX, s)

def isqualified (s): return ':' in s

def qualifyPath (xpath):
	"""
	set during init of XSD classes (first XSD_PREFIX) must be set
	by XSD after reading xsd doc and determining prefix
	"""
	if XSD_PREFIX is None:
		raise Exception, "qualifyPath called before XSD_PREFIX is known" 
	return '/'.join( map (lambda x:qualify(x), xpath.split("/")) )
	
"""
shortcut to qualifyPath function
"""
qp = qualifyPath

def createSchemaElement (name):
	"""
	names the element with the correct XSD_PREFIX and sends namespace
	returns an element
	"""
	return XmlUtils.createElement (qp(name), XSD_NAMESPACE_URI)

