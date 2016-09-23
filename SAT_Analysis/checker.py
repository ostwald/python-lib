import sys
from SAT_Analysis.Analysis import Collector, stateTable
from SAT_Analysis.config import analysis_data_dir, \
	               mass_analysis_data_dir, \
				   suggestionSet_dir
from HyperText.HTML import *
class Reporter:

	def __init__ (self, state="Ohio", group="Subject"):
		self.state = state
		self.group = group
		self.results = Collector().select(group=self.group)
		self.report()
		
	def report (self):
		print ( "%d found" % len(self.results))
		for rank in range (1,6):
			self.report_by_rank (rank)
			
	def report_by_rank (self, max_rank=5):
		print "\n-----------------------------------------"
		hdr = "RESULTS of rank < %d" % max_rank
		print "%s\n%s" % (hdr, '-'*len(hdr))
		for dataset in self.results.values():
			print "%s" % dataset.nses_standard.id
			for std in dataset[self.state]:
				if std.rank <= max_rank:
					print "\t%s (%d) -> %s" % (std.id, std.rank, std.relevance)
	
class HtmlReporter (Reporter):

	def report (self):
		table = TABLE (width="100%")
		for rank in range (1, 6):
			table.append (self.makeRow (rank))
## 		f = open ("checker.html", "w")
## 		f.write (table.__str__())
## 		f.close()
		print table.__str__()
	
	def makeRow (self, rank):
		row_klass = rank % 2 == 0 and "even" or "odd"
		row = TR(klass=row_klass)
		row.append (TD (rank, klass="rank"))
		for dataset in self.results.values():
			stds = dataset[self.state]
			id = relevance = "&nbsp"
			if len(stds) >= rank:
				std = stds[rank-1]
				id = std.id
				relevance = std.relevance
			# row.append (TD (id, klass="std-id"))
			row.append (TD (relevance, klass="std-relevance"))
		return row
					
if __name__ == "__main__":
	HtmlReporter()
