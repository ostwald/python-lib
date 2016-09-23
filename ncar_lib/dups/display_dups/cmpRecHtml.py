"""
simple display of an xml record.
refined display can be found in comparisonDocument module
"""

import os, sys
from JloXml import XmlUtils
from ncar_lib import OsmRecord
from HyperText.HTML40 import *
from termCompareGroup import getTermCompareGroup

class CmpRecord:
	"""
	produce an HTML view of an XML record, stripping out the 
	XML brackets and such
	"""
	def __init__ (self, rec):
		self.rec = rec
		
		self.html = DIV(klass='cmp-record')
		for element in XmlUtils.getChildElements(self.rec.doc):
			self.getElementHtml (element, 2)
			
	def getElementHtml (self, element, level):
		klass = 'level-%d' % level
		tagName = element.tagName
		text = XmlUtils.getText (element)
		children = XmlUtils.getChildElements(element)
		attributes = element.attributes
		
		if not (text or attributes or children):
			return
		
		if text:
			self.html.append (DIV('%s: %s' % (tagName, text), klass=klass))
			if attributes:
				self.getAttributesHtml(attributes, level)
			
		else:
			self.html.append (DIV(tagName, klass=klass))
			if attributes:
				self.getAttributesHtml(attributes, level)
			if children:
				for child in children:
					self.getElementHtml (child, level+1)
	
	def getAttributesHtml (self, attributes, level):
		klass = 'level-%d' % (level+1)
		s=[];add=s.append
		# for key in attributes.keys():
			# add ("%s: %s" % (key, attributes[key].name))
		for attr in attributes.values():
			name = attr.name
			value = attr.value
			add ("%s: %s" % (name, value))
		self.html.append( DIV(', '.join(s), klass=klass + ' attr'))
					
if __name__ == '__main__':
	
	search_result = getTermCompareGroup()[0]
	osmRecord = search_result.payload
	cmpRec = CmpRecord(osmRecord)
	print cmpRec.html
