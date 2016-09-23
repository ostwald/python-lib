from xml.dom.minidom import parse, parseString
from xml.parsers.expat import ExpatError
import sys
import string
import os
import re
import codecs
import time

from JloXml import XmlRecord

class MetaDataRecord (XmlRecord):

	xpaths = {}
	
	DLESE_NAMESPACE_URI = "http://adn.dlese.org"
	id_path = ""
	
	def setSchemaLocation (self, schemaUri, nameSpaceUri=None):
		if nameSpaceUri is None:
			nameSpaceUri = self.DLESE_NAMESPACE_URI
		# XmlRecord.setSchemaLocation (self, schemaUri, nameSpaceUri)
		XmlRecord.setSchemaLocation (self, schemaUri, nameSpaceUri)

	def makeRecordId (self, prefix, idnum):
		try:
			idnum = int(idnum)
		except:
			raise ValueError, "could not treat idnum (%s) as integer" % idnum
			
		if idnum > 999999:
			raise ValueError, "idnum (%d) exceeds 999999" % idnum
		thousands = idnum / 1000
		ones = idnum % 1000
		return '%s-000-000-%03d-%03d' % (prefix, thousands, ones)
		
	def makeRecordId (self, prefix, idnum):
		"""
		lifted from MetaDataRecord
		"""
		try:
			idnum = int(idnum)
		except:
			raise ValueError, "could not treat idnum (%s) as integer" % idnum
			
		if idnum > 999999999:
			raise ValueError, "idnum (%d) exceeds 999999" % idnum
		hunthousands = idnum / 1000000
		idnum = idnum - (hunthousands * 1000000)
		thousands = idnum / 1000
		# print 'thousands', thousands
		ones = idnum % 1000
		return '%s-000-%03d-%03d-%03d' % (prefix, hunthousands, thousands, ones)
		
	def getXsdDate (self, secs=None):
		"""
		getXsdDate (secs) -> xsdDate
		return a string of the form "YYYY-MM-DD"
		"""
		if secs is None:
			secs = time.time()

		timeTuple = time.localtime(secs)
		return time.strftime ("%Y-%m-%d", timeTuple)
		
	def getId (self):
		return self.getTextAtPath (self.id_path)
		
	def setId (self, text):
		return self.setTextAtPath (self.id_path, text)
		
	def changeId (self, newId):
		self.setId (newId)
		newpath = os.path.join (os.path.dirname (self.path), newId+'.xml')
		print self
		print "about to write to %s" % newpath
		
	def _xpath (self, field):
		"""
		_xpath('id') -> '/record/RecordID'
		lookup for field in self.xpaths
		raises KeyError if an xpath for field is not found
		"""
		try:
			return self.xpaths[field]
		except:
			raise KeyError, "path not defined for '%s'" % field
		
	def get (self, field):
		"""
		general getter - requires 'field' path is defined in self.xpaths
		"""
		return self.getTextAtPath (self._xpath(field))
		
	def set (self, field, value):
		"""
		general-purpose setter - requires 'field' path is defined in self.xpaths
		"""
		self.setTextAtPath (self._xpath(field), str(value))
