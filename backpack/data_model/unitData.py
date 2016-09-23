"""
Units correspond to a folder containing spreadsheets, each of which represents a chapter

An example unit is "Pathways & Advance Engineering"
"""

import os, sys, re, codecs, urllib
from JloXml import XmlRecord, XmlUtils, RegExUtils
from UserList import UserList
import utils
from backpack_config_data import courses_config

utils.linesep = '\r'

class ChapterInfo:
	"""
	NOT currently used??
	"""
	def __init__ (self, element, unit):
		self.unit = unit
		self.name = urllib.unquote(XmlUtils.getChildText (element, 'Name')) # take the %20s out
		source = XmlUtils.getChild ('WorksheetSource', element)
		self.href = urllib.unquote(source.getAttribute('HRef')) # take the %20s out
		self.data_path = os.path.join (utils.ingest_data_dir, self.unit, self.href)
		
	def __repr__ (self):
		return '%s - %s' % (self.name, self.href)

class UnitData(UserList):
	"""
	Provides Chapters for this unit, each represented as a map:
		- name : chaptername, 
		- data_path : path to the HTML file representing the chapter
	"""
		
	def __init__ (self, path):
		self.data = []
		self.path = path
		self.name = os.path.basename(path)
		self.blurb = courses_config[self.name]['description']
		
		for filename in os.listdir(path):
			root, ext = os.path.splitext(filename)
			if ext != '.htm': continue
			self.append ({
				'data_path' : os.path.join (path, filename),
				'name' : root
			})

	def report (self):
		print 'Unit (%s)' % self.name
		print '%d chapters' % len(self)
		for chapterInfo in self:
			print '- %s (%s)' % (chapterInfo['name'], chapterInfo['data_path'])
	
if __name__ == '__main__':
	data_path = os.path.join (utils.ingest_data_dir, 'Pathways & Advanced Engineering')
	unitData = UnitData(data_path)
	unitData.report()
