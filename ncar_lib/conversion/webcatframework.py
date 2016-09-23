import os, sys, re
from JloXml import XmlRecord, XmlUtils

import globals
from ncar_lib.lib import webcatUtils
from ncar_lib.lib.frameworks import WebcatRec
BaseWebcatRec = WebcatRec
del WebcatRec

class WebcatRec (BaseWebcatRec):
	"""
	add the methods present in the original "webcat_to_library_dc.frameworks.WebcatRec
	that were not included in "lib_dc_message.WebcatRec"
	
	Assumptions:
		title is a singleton
		issue is a singleton
	
	"""
	
	def __init__ (self, path=None, xml=None):
		BaseWebcatRec.__init__ (self, path, xml)

		self.issue = None
		self.processTitles()
	
	def processTitles (self):
		"""
		during conversion: fullTitle, if present, is mapped to dc:title
				(and then title is mapped to dc:altTitle)
		"""
		if self.recordID.startswith ("MANUSCRIPT"):
			self.processTitlesManuscript()
		else:
			self.processTitlesDefault()
		
	def processTitlesDefault (self):
		"""
		if there is an issue, assign self.issue and then adjust self.title
		when writing Library_dc record:
		if fullTitle
			- fullTitle gets mapped to dc:title, and
			- title gets mapped to library_dc:altTitle
		else
			- title gets mapped to dc:title
		"""
		
		## issue num contained in title takes precidence over "fullTitle"?
		issue, title = self.issueTitleSplit(self.title)
		if issue:
			self.issue = issue
			self.title = title
			
		if self.fullTitle:
			issue, title = self.issueTitleSplit(self.fullTitle)
			if issue:
				self.issue = issue
				self.fullTitle = title 
	
	def processTitlesManuscript (self):
		"""
		if there is an issue, assign self.issue and then adjust self.title
		when writing Library_dc record:
		if fullTitle
			- fullTitle gets mapped to dc:title, and
			- title gets mapped to library_dc:altTitle
		else
			- title gets mapped to dc:title
		"""
		
		## issue num contained in title takes precidence over "fullTitle"?
		issue, title = self.issueTitleSplit(self.fullTitle)
		if issue:
			self.issue = issue
			self.fullTitle = title
			
		if self.title:
			issue, title = self.issueTitleSplit(self.title)
			if issue:
				self.issue = issue
				self.title = title
				
	def issueTitleSplit (self, input):
		# if not hasattr (self, 'fullTitle'): return None
		# print "\n fullTitle: %s" % self.fullTitle
		issue = None
		title = None
		
		if not self.recordID in globals.issueTitleSkipList:
			m = self.issue_delimiter.match (input)
			if m:
				issue = m.group('issue').strip()
				title = m.group('title').strip()

		return issue, title

if __name__ == "__main__":
	# id = "TECH-NOTE-000-000-000-007"
	id = "MANUSCRIPT-000-000-000-805"

	path = webcatUtils.getRecordPath (id, "webcat")
	rec = WebcatRec (path=path)
	# print rec
	print "title: " + rec.title
	print "issue: " + rec.issue
		
