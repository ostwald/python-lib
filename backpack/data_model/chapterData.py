"""
Chapters are represented by an HTML file that contains a Table of Contents for the chapter Topics.

the 'htm' files saved by Ecel for each CHAPTER contain an xml structure (see TabData)
that is used to construct a list of TOPICS (key concepts) for that chapter.

example chapter htm containing the TOC
	/Documents/Work/NSDL/BackPack/html/Pathways & Advance Engineering/Physics 2.6.0 Part 1.htm

	Each topic corresponds to a TAB in the original chapter spreadsheet, and also with an 'htm' file that was
created when the chapter spreadsheet was saved as HTML. 
"""

import os, sys, re, codecs, urllib
from JloXml import XmlRecord, XmlUtils, RegExUtils
from UserList import UserList
import utils

utils.linesep = '\r'

class TabData:
	"""
	<x:ExcelWorksheet>
    <x:Name>Archimedes</x:Name>
    <x:WorksheetSource HRef="Physics%202.6.0%20Part%201_files/sheet002.htm"/>
   </x:ExcelWorksheet>
   
    self.unit - name of unit to which this topic belongs
   	self.name - used for topic (key concept) name
	self.data_path - absolute path to spreadsheet for this TAB (topic)
	"""
	def __init__ (self, element, unit):
		self.unit = unit
		self.num = None
		self.name = urllib.unquote(XmlUtils.getChildText (element, 'Name')) # take the %20s out
		source = XmlUtils.getChild ('WorksheetSource', element)
		self.href = urllib.unquote(source.getAttribute('HRef')) # take the %20s out
		self.data_path = os.path.join (utils.ingest_data_dir, self.unit, self.href)
		
	def __repr__ (self):
		return '%s - %s (%d)' % (self.name, self.href, self.num)

class ChapterData(UserList):
	"""
	Chapter HTML contains the "table of contents" for the tabs in the Chapter Spreadsheet file.
	This class reads the html and produces a list of TabData instances
	
	path specifies the html file, named for the chapter (e.g., Physics 2.6.0 Part 1.htm)
	
	After instantiating the Key Concept objects, it can create a
	chapter record, and populate the relations fields with pointers
	to the tabs.
	
	"""
		
	def __init__ (self, path):
		"""
		self.unit - the unit to which this Chapter belongs (e.g., 'Pathways & Advance Engineering')
		self.data - TabData instances for each topic
		"""
		self.data = []
		s = utils.getHtml(path)
		
		filename = os.path.basename(path)
		self.unit = os.path.basename(os.path.dirname(path))
		self.num, self.chapter = self.getChapterInfo(filename)
		tagPat = RegExUtils.getTagPattern ('x:ExcelWorkbook')
		m = tagPat.search (s)
		if not m:
			raise Exception, "could not get TABS data from file (%s)" % path
		print 'found data'
		xml = m.group(0).replace('x:', '') # strip x prefix from all elements
		
		rec = XmlRecord (xml=xml)
		rec.xpath_delimiter = '/'
		tabNodes = rec.selectNodes (rec.dom, "ExcelWorkbook/ExcelWorksheets/ExcelWorksheet")
		
		# we ignore the 'Cover sheet'
		print 'creating %d tabs' % len(tabNodes)
		for tabElement in tabNodes:
			tabData = TabData (tabElement, self.unit)
			if tabData.name.lower() != 'cover sheet':
				tabData.num = len(self)+1
				self.append(tabData)

	def getChapterInfo (self, filename):
		"""
		ASSUMES chapter filenames are of the form:
			n_chapter name_vj
		n specifies the order num of this chapter
		'vj' specifies the version of this file (NO LONGER PRESENT)
		"""
		root, ext = os.path.splitext(filename)
		pat = re.compile ('([\d]+)_(.*)')
				
		m = pat.match (root)
		if not m:
			raise Exception, 'could not parse chapter name ("%s")' % filename
		print 'num: %d, name: %s' % (int(m.group(1)), m.group(2))
		
		return int(m.group(1)), m.group(2)
		
	def report (self):
		print '%s (%s)' % (self.chapter, self.unit)
		print '%d tabs found' % len(self)
		for tab in self:
			print tab
	
if __name__ == '__main__':
	# unit = 'Pathways & Advanced Engineering'
	# unit = 'Aerospace Technology Class'
	# filename = '2_Physics 2.6.0 Part 1_v2.htm'
	# filename = '2_Rocketry & Space.htm'
	filename = '2_Rocketry & Space.htm'
	unit = 'Engineering Class'
	filename = '14_Engineering Bridges.htm'
	data_path = os.path.join (utils.ingest_data_dir, unit, filename)
	chapterData = ChapterData(data_path)
	chapterData.report()
