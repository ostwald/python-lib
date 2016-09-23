import sys
import string
import os
import re
from UserList import UserList
from JloXml import XmlRecord
from JloXml.XmlUtils import *
from asn import StdDocument
from sat_utils import getNumId, makeFullId

class SpreadSheetBuilder:
	"""
	we need to read the NSES Standards document to obtain the "text" and "benchmarks" information
	for the NSES standards, which is not contained in the "SuggestionSets"
	"""
	asnDocDir = "/home/ostwald/python-lib/asn/standards-documents/localized/"
	outDir = "spreadsheets"
	nsesDoc = "1995-NSES-v1.2.5-012007.xml"
	
	def __init__ (self, dir):
		self.data_dir = dir
		
		NSESDocPath = os.path.join (self.asnDocDir, self.nsesDoc)
		self.NSES = StdDocument (NSESDocPath)
		
	def reportAll (self):
		self.walkSuggestionSets (self.report)
		
	def report (self, filename):
		rec = SuggestionSetRecord (os.path.join (self.data_dir, filename))
		rec.report()
	
	def writeAll (self):
		print "writing stylesheets ..."
		for filename in os.listdir (self.data_dir):
			if filename.endswith (".xml") and filename[0] != '.':
				print "\t" + filename
				self.writeSheet (filename)
		print " .. done"
		
	def walkSuggestionSets (self, callback):
		print "walking sets ..."
		for filename in os.listdir (self.data_dir):
			if filename.endswith (".xml") and filename[0] != '.':
				callback (filename)
		print " .. done"
		
	def writeSheet (self, filename):
		path = os.path.join (self.data_dir, filename)
		root = os.path.splitext (filename)[0]
		rec = SuggestionSetRecord (path, self.NSES)
		ss = rec.toXLS()
		f = open (os.path.join (self.outDir, root + ".txt"), 'w')
		f.write (ss.encode ("utf-8"))
		f.close()
		
class SuggestionSetRecord (XmlRecord):
	"""
	reader for a "SuggestionSet" xml document.
	SuggestionSets correspond to a single NSES stanard, and the set of Suggested Standards
	made by the SAT service for each State.
	"""
	
	def __init__ (self, path, NSES=None):
		self.path = path
		self.NSES = NSES
		XmlRecord.__init__ (self, path=path)
		self.group = self._get_group()
		self.band = self._get_band()
		self.nses_id = self._get_nses_id()
		self.numId = getNumId (self.nses_id)
		
		# print "group: %s, band: %s, id: %s" % (self.group, self.band, self.numId)
	
	def _get_group (self):
		return self.getTextAtPath ("SuggestionSet:SetInfo:group")
		
	def _get_band (self):
		return self.getTextAtPath ("SuggestionSet:SetInfo:band")

	def _get_nses_id (self):
		return self.getTextAtPath ("SuggestionSet:SetInfo:nses_id")
		
	def init_from_path (self):
		self.filename = os.path.split(self.path)[1]
		self.name = os.path.splitext(self.filename)[0]
		self.group, self.band, self.nses_id = self.name.split("_")
	
	def _get_state_suggestions_map (self):
		state_map = {}
		nodes = self.selectNodes (self.dom, "SuggestionSet:Suggestions")
		for node in nodes:
			state_map[node.getAttribute("state")] = SuggestionList (node)
		return state_map
			
		
	def getSuggestionsNode (self, state):
		nodes = self.selectNodes (self.dom, "SuggestionSet:Suggestions")
		for node in nodes:
			if node.getAttribute("state") == state:
				return node
			
	def getNSESText (self, std):
		s=[];add=s.append
		target = self.NSES[std.parent]
		while target:
			add (target.description)
			target = self.NSES[target.parent]
		s.reverse()
		text = string.join (s, ": ")
		
		# add a hyphen to the listItem markup
		li = "<li>"
		pat = re.compile (li)
		text = re.sub (pat, li+" -", text)
		# strip all html markup
		pat = re.compile ("<[^<]*?>")
		while pat.search (text):
			text = re.sub (pat, "", text)
		return text
				
	def toXLS (self):
		s = [];add=s.append
		tabify = lambda l:string.join (l,"\t")
		#header
		nses_benchmark = "benchmark"
		nses_text = "text"
		
		if self.NSES:
			nses_std = self.NSES[self.nses_id]
			if nses_std:
				nses_benchmark = nses_std.description
				nses_text = self.getNSESText (nses_std)
		
		add (tabify (["Standards Doc", "id", "relevant", "gradeLevel", "benchmark", "text"]))
		add ("")
		
		add (tabify (["NSES", self.numId, "", self.band, nses_benchmark, nses_text]))
		
		for sugList in self._get_state_suggestions_map().values():
			add ("")
			for i in range (len(sugList)):
				sugg = sugList[i]
				stateLabel = (i == 0 and sugList.state) or ""
				add (tabify ([stateLabel, getNumId (sugg.purlId), "", sugg.gradeLevels, sugg.benchmark, sugg.text]))
		
		return string.join (s, "\n")

	def report (self):
		"""
		only report abnormal (non-5) counts
		"""
		state_map = self._get_state_suggestions_map()
		s=[];add=s.append
		for state in state_map.keys():
			sugList = state_map[state]
			# only show the states with other than 5 suggestions
##			if (len(sugList) != 5):
##				add ("%s (%d)" % (state, len(sugList)))
			add ("%s (%d)" % (state, len(sugList)))

		if s:
			header = "%s - %s" % (self.numId, self.band)
			s.insert (0, header)
			print string.join (s, "\n\t")
				
class SuggestionList (UserList):
	"""
	reader to extract a list of Suggested State standards from a *StateStandard* element of
	a SuggestionSet instance.
	"""
	def __init__ (self, element):
		self.state = element.getAttribute ("state")
		UserList.__init__ (self)
		for child in getChildElements (element):
			self.append (Suggestion (child))
			
class Suggestion:
	"""
	Holds the attributes from a "StateStandard" element contained in a SuggestSet instance
	"""
	attributes = ["purlId", "text", "gradeLevels", "benchmark"]
	
	def __init__ (self, element):
		for attr in self.attributes:
			setattr(self, attr,  unicode (getChildText (element, attr),"utf-8"))
		
def suggestionSetRecordTester ():
	path = "suggestionSets/Inquiry_K-4_S1017AA1.xml"
	rec = SuggestionSetRecord (path=path)
	ss = rec.getSuggestionsNode ("Colorado")
	print rec.toXLS()	
			
def spreadSheetBuilderTester():
	data_dir = "suggestionSets"
	filename = "Inquiry_K-4_S1017AA1.xml"
	builder =  SpreadSheetBuilder (data_dir)
	builder.writeSheet (filename)
	
def getNSESText (std, NSES):
	s=[];add=s.append
	target = NSES[std.parent]
	while target:
		add (target.description)
		target = NSES[target.parent]
	s.reverse()
	return string.join (s, "\n")
	
def writeSpreadSheets ():
	data_dir = "suggestionSets"
	builder =  SpreadSheetBuilder (data_dir)
	builder.writeAll ()
	
def reportSpreadSheets ():
	data_dir = "suggestionSets"
	builder =  SpreadSheetBuilder (data_dir)
	builder.reportAll ()
	
if __name__ == "__main__":
	writeSpreadSheets()


			
