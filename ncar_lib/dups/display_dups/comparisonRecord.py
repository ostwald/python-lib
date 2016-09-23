"""
produces ComparisonTable, which places two XML documents side-by-side

does so by instantiating a ComparisonRecord for each,
and then embedding the comparisonRecords into a table
"""

import os, sys
from JloXml import XmlUtils
from UserList import UserList
from HyperText.HTML40 import *
from termCompareGroup import getTermCompareGroup

top_level_elements = ['general', 'resources', 'contributors', 'classify', 'coverage', 'rights']

class ComparisonRecord:
	"""
	produce an HTML view of an XML record, stripping out the 
	XML brackets and such
	"""
	
	
	def __init__ (self, search_result):
		self.result = search_result # an OsmSearchResult instance
		self.collectionName = self.result.collectionName
		self.rec = self.result.payload # a OsmRecord instance
		
		self.html = DIV(klass='cmp-record')
		for tag in top_level_elements:
			element = XmlUtils.getChild(tag, self.rec.doc)
			if not element:
				setattr (self, tag, None)
			else:
				setattr (self, tag, self.getTopLevelElement (element, 2))
				
			if tag == 'resources':
				print "%s - %s (%s)" % (self.result.recId, self.resources, type(self.resources))
			
	def getTopLevelElement (self, element, level):
		children = XmlUtils.getChildElements(element)
		if not children:
			return None;
		
		html = DIV(klass="element")
			
		for child in children:
			html.append(self.getElementHtml (child, level+1))
		return html
			
	def getElementHtml (self, element, level):
		klass = 'level-%d' % level
		tagName = element.tagName
		text = XmlUtils.getText (element)
		children = XmlUtils.getChildElements(element)
		attributes = element.attributes
		
		if not (text or attributes or children):
			return ""
		
		html = DIV(klass="element")	
			
		if text:
			html.append (DIV('%s: %s' % (tagName, text), klass=klass))
			if attributes:
				html.append(self.getAttributesHtml(attributes, level))
			
		else:
			html.append (DIV(tagName, klass=klass))
			if attributes:
				html.append(self.getAttributesHtml(attributes, level))
			if children:
				for child in children:
					html.append(self.getElementHtml (child, level+1))
		return html
	
	def getAttributesHtml (self, attributes, level):
		klass = 'level-%d' % (level+1)
		s=[];add=s.append
		# for key in attributes.keys():
			# add ("%s: %s" % (key, attributes[key].name))
		for attr in attributes.values():
			name = attr.name
			value = attr.value
			add ("%s: %s" % (name, value))
		return DIV(', '.join(s), klass=klass + ' attr')
		
class ComparisonTable(UserList):
	
	def __init__ (self, search_results):
		UserList.__init__ (self, map (ComparisonRecord, search_results))
		self.html = TABLE()
		hdr = TR();self.html.append(hdr)
		for cmpRecord in self:
			hdr.append (TD (cmpRecord.collectionName, klass='collection-name'))
		
		
		for tag in top_level_elements:
			if not self.anyResultHasSection (tag):
				print ("skipping: " + tag)
				continue
			tagRow = TR();self.html.append(tagRow)
			tagRow.append(TD (tag, colspan=len(search_results), klass='tag-row'))
			row = TR(valign='top');self.html.append(row)
			for comRecord in self:
				contents = getattr (comRecord, tag)
				row.append (TD (contents or 'nbsp;'))
				
			
	def anyResultHasSection (self, tag):
		for result in self:
			html = getattr (result, tag)
			if html is not None:
				return 1
		return 0
		
		
if __name__ == '__main__':
	
	search_result = getTermCompareGroup()[0]
	osmRecord = search_result.payload
	cmpRec = ComparisonRecord(osmRecord)
	print cmpRec.html
