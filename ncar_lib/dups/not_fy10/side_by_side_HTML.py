"""
produces SideBySideDisplay, which places two XML documents side-by-side

does so by instantiating a RecordHTMLInfo for each,
and then embedding the comparisonRecords into a table
"""

import os, sys
from JloXml import XmlUtils
from UserList import UserList
from HyperText.HTML40 import *
from ncar_lib.dups.utils import getPrettyTimeStr

top_level_elements = ['general', 'resources', 'contributors', 'classify', 'coverage', 'rights']

class RecordHTMLInfo:
	"""
	Class for displaying RecordInfo, and recordXML
	recordXML is split up by the top-level elements, and these
	are displayed separately to facilitate side-by-side comparison
	"""
	
	def __init__ (self, recInfo, diff=[]):
		self.recInfo = recInfo # a RecordInfo instance
		self.diff = diff
		self.rec = self.recInfo.getOsmRecord() # a OsmRecord instance
		
		self.html = DIV(klass='cmp-record')
		for tag in top_level_elements:
			element = XmlUtils.getChild(tag, self.rec.doc)
			if not element:
				setattr (self, tag, None)
			else:
				setattr (self, tag, self.getTopLevelElement (element, 2))
				
			# if tag == 'resources':
				# print "%s - %s (%s)" % (self.recInfo.recId, self.resources, type(self.resources))
			
	def getTopLevelElement (self, element, level):
		"""
		represents the contents (children) of toplevel elements (but not TAG
		of the element), which is rendered in side-by-side display
		"""
		children = XmlUtils.getChildElements(element)
		if not children:
			return None;
		
		klass = "top-level-element"
		html = DIV(klass=klass)
			
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
			html.append (DIV(SPAN(tagName+': ', klass='el-name'), SPAN (text, klass="el-text"), klass=klass))
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
		"""
		display the attributes and their values as HTML
		"""
		levelklass = 'level-%d' % (level+1)
		s=[];add=s.append
		# for key in attributes.keys():
			# add ("%s: %s" % (key, attributes[key].name))
		for attr in attributes.values():
			name = attr.name
			value = attr.value
			add ("%s: %s" % (SPAN(name, klass='attr-name'), SPAN (value, klass='attr-value')))
		return DIV(', '.join(s), klass=levelklass)
		
	def getRecordHeaderHtml (self):
		"""
		returns a TD element filled with info about this record
		that is not in metadata
		
		ALTERNATIVE: we might use the header to list info that is
		compared across documents (because it is easier this way than
		doing it from within elements
		"""
		cell = TD(klass="recInfo")
		# editButton = INPUT(type='button', value='edit record in DCS', klass="edit-button", id=self.recInfo.recId)
		# cell.append (editButton)
		
		findButton = INPUT(type='button', value='find record in DCS', klass="find-button", id=self.recInfo.recId)
		cell.append (findButton)
		
		status = self.recInfo.status
		statusKlass = status == "Done" and "done-status" or ""
		cell.append (DIV ("status: %s" % SPAN(status, klass=statusKlass)))
		return cell
		
class SideBySideDisplay(UserList):
	"""
	display the recInfos side by side in an HTML Table
	"""
	def __init__ (self, dupGroup):
		self.dupGroup = dupGroup
		self.data = []
		self.diff = []
		
		for recInfo in self.dupGroup:
			self.append (RecordHTMLInfo (recInfo, self.diff))
		
		self.html = TABLE(id="side-by-side-table")
		
		hdr = TR();self.html.append(hdr)
		
		## record Header
		# collection
		# status
		# lastTouch
		for recInfo in self:
			hdr.append (recInfo.getRecordHeaderHtml())
		
		# ensure that cells have equal width by setting width in header cells
		cellwidth = "%d%%" % (100/len(self.dupGroup))
		for hdrCell in hdr.content:
			hdrCell.dict.update({"width":cellwidth})
		
		for tag in top_level_elements:
			if not self.anyResultHasSection (tag):
				# print ("skipping: " + tag)
				continue
			tagRow = TR();self.html.append(tagRow)
			klass='tag-row'
			

			tagRow.append(TD (tag, colspan=len(dupGroup), klass=klass))
			row = TR(valign='top');self.html.append(row)
			for comRecord in self:
				contents = getattr (comRecord, tag)
				row.append (TD (contents or '&nbsp;'))
				
	def anyResultHasSection (self, tag):
		for result in self:
			html = getattr (result, tag)
			if html is not None:
				return 1
		return 0
		
		
if __name__ == '__main__':
	from comparisonManager import ComparisonManager
	cm = ComparisonManager()


