import sys, os, string
from SpreadSheetReader import NSESDataSet
from UserDict import UserDict
from Analysis import Collector
from SAT_Eval.sat_utils import domain_groups_keys

class Minn:
	def __init__ (self):
		c = Collector()
		readerList = c.values()
		readerList.sort (self._cmp)
		self.s = []
		self.add=self.s.append
		
		self.addLine (["Standard", "id", "relevance", "benchmark", "text"])
		
		for reader in readerList:
			self.addNSESDataSet (reader)
			
	def _cmp (self, r1, r2):
		band_cmp = lambda b: (b[0] == "K" and "0") or str(b[0])
		group_cmp = lambda g: str(domain_groups_keys.index(g))
		
		return cmp (group_cmp(r1.group) + band_cmp(r1.band), group_cmp(r2.group) + band_cmp (r2.band))
		
	def addNSESDataSet (self, reader):
		nses = reader.nses_standard
		self.addLine()
		band_group = "%s / %s" % (reader.group, reader.band)
		self.addLine ([nses.doc, nses.id, band_group.encode("utf-8"), nses.benchmark, nses.text])
		self.addLine ()

		for std in reader["Minnesota"]:
			self.addLine (["", std.id, str(std.relevance), std.benchmark, std.text])

	def addLine (self, item_list=None):
		if not item_list: 
			self.add ("")
		else: 
			self.add (string.join (item_list,'\t'))

	def __repr__ (self):
		return string.join (self.s, "\n")

	
if __name__ == "__main__":
	
	m = Minn ()
	f = open ("Minnesota.txt", 'w')
	f.write (str(m))
	f.close()
