import sys, os, string
from math import modf
from UserDict import UserDict
from SAT_Eval.sat_utils import state_list, domain_groups_keys
from Analysis import Collector, standardsWithAnyHits, MASSGraftCollector
from HyperText.HTML import *
from HtmlDocument import MyDocument

class GroupSpec:
	def __init__ (self, name, size):
		self.name = name
		self.size = size
		
groupspecs = [
	GroupSpec ("Inquiry", 6),  
	GroupSpec ("Subject", 24), 
	GroupSpec ("Applied", 19),  
	GroupSpec ("All", 49) # all
	]

class GroupRow (UserDict):
	def __init__ (self, name, size):
		UserDict.__init__ (self)
		self.name = name
		self.size = size
		self.groupSet = name
		if name == "All":
			self.groupSet = []


class GroupTable:
	"""
	group table presents the assignments for a specific STATE and RANK
	the rows each present information from this group for a particular GroupSpec
		e.g., "Applied" group spec has 19 members
	the first column basically identifies the groupSpec
	the subsequent columns present the number of "hits" for each relevance/threshold
	
	"""
	def __init__ (self, collector, state=None, rank=None):
		self.state = state
		self.rank = rank
		self.collector = collector
		
		self.groups = []
		
		for groupspec in groupspecs:
			group = groupspec.name
			size = groupspec.size
			row = GroupRow (group, size)
			self.groups.append(row)
			for threshold in [1,2,3]:
				hits = standardsWithAnyHits (self.collector, 
											 threshold=threshold, 
											 group=row.groupSet, 
											 rank=self.rank,
											 state=self.state)
				row[threshold] = hits
				
	def _state (self):
		if self.state: return self.state
		else: return "All"
		
	def _rank (self):
		if self.rank: return self.rank
		else: return "All"
				
	def __repr__(self):
		s=[];add=s.append
		add ("State: " + self._state())
		add ("Rank: " + self._rank())
		add (string.join (["threshold", "1", "2", "3"], "\t"))
		for row in self.groups:
			add ("%s\t%d\t%d\t%d" %(row.name, row[1], row[2], row[3]))
		return string.join (s, "\n")
		
	def ashtml (self):
		maintable = TABLE()
		mainrow = TR()
		maintable.append (mainrow)
		header = TD(klass="main-header")		
		mainrow.append (header)
		## header.append (DIV ("State: " + self._state()))
		header.append (DIV ("Rank: ", B(self._rank())))
		
		datarow = TR()
		maintable.append (datarow)
		datacell = TD()
		datarow.append (datacell)

		datatable = TABLE(klass="datatable")
		datacell.append (datatable)
		
		header = TR (klass="header")
		if self.rank == "1":
			header.append (TD ("relevance"))
		for relevance in range (1,4):
			header.append (TD (relevance))
		datatable.append (header)
		
		for grouprow in self.groups:
			row = TR()
			datatable.append (row)
			## content = "%s (%d)" % (grouprow.name, grouprow.size)
			# only show the group name for the "ALL" case
			if self.rank == "1":
				name = grouprow.name or "Inc & Subj"
				row.append (TD (B(name, style="white-space:nowrap"), DIV (grouprow.size, klass="count")))
			for threshold in [1,2,3]:
				hits = grouprow[threshold]
				f, percent = modf ((float(hits) / grouprow.size) * 100)
				if f > .5: percent = percent + 1
				## content = "%d%s<br/>(%d)" % (percent, "%", hits)
				percentSign = SPAN ("%", klass="percent-sign")
				percentStr = SPAN ("%d" % percent, klass="percent")
				row.append (TD (percentStr, percentSign, DIV (hits, klass="count")))
		
		return maintable
		
class StateReport:
	
	outpath = "state-out.html"
	rank_list = ["", "1", "2", "3"]
	all_rank_list = ["1", "2", "3", "4", "5"]
	interpretation = """<b>Interpretation</b> &mdash;
	Contents of a cell denote the number of NSES standards for the given group
	(e.g., Applied) had a assigned relevance (or less) than the relevance number
	contained in the column header, at the rank specified for the particular table."""
	
	def __init__ (self):
		
		title = "SAT Analysis - Results by State"
	
		self.doc = MyDocument (stylesheet="state-report-styles.css",
							   title=title)
		self.doc.body.append (H1 (title))
		self.doc.body.append (self.data_table())
		
		self.write()
		
	def data_table(self):
		ranklist = self.all_rank_list
		collector = MASSGraftCollector()  ## graft newer Mass results
		## collector = Collector()
		table = TABLE()
		interp = TR (TD (DIV (self.interpretation, klass="interpretation"), colspan=len(ranklist)))
		table.append (interp)
		state_list.sort()
		for state in state_list:
			## if state == "Massachusetts": continue
			table.append (TR (TD (H2 (state), colspan=len(ranklist))))
			row = TR()
			table.append(row)
			for rank in ranklist:
				row.append (TD (GroupTable (collector, state=state, rank=rank).ashtml()))
		return table
		
	def write (self):
		# fp = open (self.outpath, 'w')
		# fp.write (self.html.__str__())
		# fp.close()
		self.doc.writeto (self.outpath)
		
if __name__ == "__main__":
	StateReport()

