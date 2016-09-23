from xml.dom.minidom import parse, parseString
from xml.parsers.expat import ExpatError
import sys
import string
import os
import re
import codecs
import time

from JloXml import XmlRecord, XmlUtils

class Standard:

	"""
	Works on a Status entry as an element
	"""
	
	def __init__ (self, element):
		self.element = element
		self.attrs = ("Identifier", "Author", "Topic", "GradeLevels", "Text", "Benchmark")
		for attr in self.attrs:
			setattr (self, attr, self.get(attr))
		
	def get (self, tag):
		return XmlUtils.getChildText (self.element, tag)
		
	def __repr__ (self):
		s=[];add=s.append
		add ("\n" + self.Identifier)
		for attr in self.attrs:
			if attr != "Identifier":
				add ("\t%s: %s" % (attr, self.get(attr)))
		return string.join (s, "\n")

class SuggestStandardsResponse (XmlRecord):

	standards_path = "CATWebService:SuggestedStandards:Results:Result:Standard"
	
	def __init__ (self, path=None, xml=None):
		XmlRecord.__init__ (self, path, xml)
		self.standards = self.getStandards()

	def getStandards (self):
		elements = self.getElementsByXpath (self.dom, self.standards_path)
		standards = [];add=standards.append
		for std in elements:
			add (Standard (std))
		return standards
		
	def getId (self):
		return self.getTextAtPath (self.id_path)
		
	def setId (self, newId):
		self.setTextAtPath (self.id_path, newId)

	def get_sortedEntryList (self):
		status_entries = []
		entries = self.getElementsByXpath (self.doc, "statusEntries:statusEntry")
		## print ("get_statusEntryList: %d entries found" % len (entries))
		for element in entries:
			entry = StatusEntry (element.toxml())
			status_entries.append (entry)
		status_entries.sort (self.statusEntryCmp)
		return status_entries 

def tester():
	path = "response.xml"
	rec = SuggestStandardsResponse (path)
	print rec
	standards = rec.standards
	print "%d standards found" % len(standards)
	for std in standards:
		print std

if __name__ == "__main__":

	tester()

