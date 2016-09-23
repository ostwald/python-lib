import sys
import string
import os
import re
import codecs
import time

from JloXml import XmlRecord
from JloXml.XmlUtils import createDocument, getChild, getText, getChildText, addChild

class SATServiceRecord (XmlRecord):
	
	def getRequestInfo (self):
		return self.selectSingleNode (self.dom, "SATWebService:SuggestedStandards:RequestInfo")
		
	def showRequestInfo (self):
		info = self.getRequestInfo ()
		print "RequestInfo"
		if info:
			for e in self.getElements (info):
				print "\t%s: %s" % (e.tagName, self.getText(e))
		else:
			print "\tRequestInfo not found"
		
	def getSuggestedStandards (self):
		nodes = self.selectNodes (self.dom, "SATWebService:SuggestedStandards:Results:Result:Standard")
		# print "%d nodes found" % len (nodes)
		nodes = nodes or []
		# stds = []
		# for node in nodes:
			# stds.append (Standard (node))
		return map (StateStandard, nodes)
		
class StateStandard:
	"""
	representation of StateStandards returned by the SAT Rest service within the SATServiceRecord
	"""
	
	def __init__ (self, element):
		self.element = element
		self.purlId = getChildText (element, "Identifier")
		self.state = getChildText (element, "Author")
		self.gradeLevels = getChildText (element, "GradeLevels")
		self.text = getChildText (element, "Text")
		self.benchmark = getChildText (element, "Benchmark")

		self.doc = createDocument ("StateStandard")
		
	def display (self):
		
		print self.purlId
		print "\t state: %s" % self.state
		print "\t benchmark: %s" % self.benchmark
		
	
		
	def toXML (self, tags=None):
		tags = tags or ["purlId", "state", "gradeLevels", "text", "benchmark"]
		for tagName in tags:
			if hasattr (self, tagName):
				addChild (self.doc, tagName, getattr (self, tagName))
		
		return self.doc.documentElement.cloneNode (1)
		
		
if __name__ == "__main__":
	path = "fake-response.xml"
	rec = SATServiceRecord (path=path)
	rec.showRequestInfo()
	for std in rec.getSuggestedStandards():
		std.display()
		print std.toXML().toprettyxml("  ","\n")
	

			
