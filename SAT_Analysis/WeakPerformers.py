import sys, os, string
from math import modf
from UserDict import UserDict
from SAT_Eval.sat_utils import states, domain_groups_keys
from Analysis import Collector, standardsWithAnyHits, prtln
from HyperText.HTML import *
from HtmlDocument import MyDocument


def noHit (dataSet, threshold=None, state=None, rank=None):
	"""
	this is a DATA SET filter, which returns true if there NO HIT
	in the dataset which above specified rank
	"""
	for std in dataSet.getStandards (state):
		if rank and std.rank > rank:
			continue
		if std.hasHit(): return 0
	return 1

def standardsWithNoHits (collector, **args):
	prtln ( "standardsWithAnyHits")
	if args:
		for key in args.keys():
			prtln ( "\t%s: %s" % (key, args[key]))
	group = args.has_key("group") and args["group"] or None
	state = args.has_key("state") and args["state"] or None
	rank = args.has_key("rank") and args["rank"] and int(args["rank"]) or None
	
	threshold = args.has_key("threshold") and args["threshold"] and int(args["threshold"]) or None
	
	# print "Standards with hits (threshold='%s', state='%s')" % (threshold, state)
	
	filter = lambda dataSet: noHit(dataSet, threshold=threshold, state=state, rank=rank)
	results = collector.select (filter=filter, group=group)
	print "%d found" % len(results)
	return results
		
class WeaklingSet (UserDict):
	
	def __init__ (self, **args):

		self.state = args.has_key("state") and args["state"] or None
		self.rank = args.has_key("rank") and args["rank"] and int(args["rank"]) or None
		weaklings = standardsWithNoHits (Collector(), state=self.state, rank=self.rank)
		UserDict.__init__ (self, weaklings)
		
	def report (self):
		for nsesDataSet in self.values():
			# see SpreadSheetReader.NSESDataSet, NSESStandard
			print "\n*** %s ***" % os.path.basename (nsesDataSet.path)
			print "NSES Standard: " + nsesDataSet.nses_standard.id
			print "\tgroup: " + nsesDataSet.group
			print "\tgradeLevel: " + nsesDataSet.nses_standard.gradeLevel
			print "\ttext: " + nsesDataSet.nses_standard.text
			print "\tbenchmark: " + nsesDataSet.nses_standard.benchmark
			
			print "\n%s suggested standards" % state
			
			for stateStandard in nsesDataSet[state]:
				# see SpreadSheetReader.StateStandard
				print "%s (%d) -> %s" % (stateStandard.id, stateStandard.rank, stateStandard.relevance)
				print "\tgradeLevel: %s" % stateStandard.gradeLevel
				print "\tText: %s" % stateStandard.text
				print "\tBenchmark: %s" % stateStandard.benchmark
				## print "** schema: %s" % string.join (stateStandard.schema, ', ')

class WeaklingSetHtml (WeaklingSet):
				
	default_write_dest = "weak-std-report.html"
	
	def __init__ (self, **args):

		state = args.has_key("state") and args["state"] or None
		rank = args.has_key("rank") and args["rank"] and int(args["rank"]) or None
		# weaklings = standardsWithNoHits (Collector(), state=self.state, rank=self.rank)
		WeaklingSet.__init__ (self, state=state, rank=rank)
		self.documentInit()
	
	def setsAsHtml (self):
		box = DIV()
		for nsesDataSet in self.values():
			box.append (self.nsesStdAsHtml (nsesDataSet))
			box.append (self.stateStdsAsHtml (nsesDataSet [self.state]))
		return box
			
	def nsesStdAsHtml (self, nsesDataSet):
		table = TABLE (klass="nses-std-table")
		header = TR (valign="top", klass="header-row");
		table.append (header)
		fields = ["id", "group", "gradeLevel", "benchmark", "text"]
		for field in fields:
			headerStr = (field == "id" and "NSES id") or field
			header.append (TH (headerStr, klass=field))
		content = TR (valign="top", klass="content-row");
		table.append (content)
		for field in fields:
			val = getattr (nsesDataSet.nses_standard, field) or getattr (nsesDataSet, field)
			content.append (TD (val, klass=field))
		return table
		
	def stateStdsAsHtml (self, stateStandardList):
		table = TABLE (klass="state-std-table")
		header = TR (valign="top", klass="header-row");
		table.append (header)
		fields = ["id", "relevance", "gradeLevel", "benchmark", "text"]
		for field in fields:
			headerStr = (field == "relevance" and "score") or \
						(field == "id" and "state id") or field
			header.append (TH (headerStr, klass=field))
		for stateStandard in stateStandardList:
			content = TR (valign="top", klass="content-row");
			table.append (content)
			for field in fields:
				val = getattr (stateStandard, field) or "none"
				content.append (TD (val, klass=field))
		return table	

	def documentInit(self):
		
		blurb = """NSES Standards having no relevant state standards suggested 
			in the top %d ranks (%d)""" % (self.rank, len (self))
		
		title = "SAT Analysis"
		subtitle = "Poor Performing Standards for %s" % self.state
	
		self.doc = MyDocument (stylesheet="weak-std-report.css",
							   title=title)
		self.doc.body.append (H1 (title))
		self.doc.body.append (H2 (subtitle))
		self.doc.body.append (DIV (blurb, klass="blurb"))
		self.doc.body.append (self.setsAsHtml())
		
	def write (self, path=None):
		out = path or self.default_write_dest
		self.doc.writeto (out)
		print "html written to " + out
		
if __name__ == "__main__":
	state = "Colorado"
	rank = 5
	ws = WeaklingSetHtml (state=state, rank=rank)
	# ws.report()
	
	# nsesDataSet = ws.values()[0]
	# print ws.nsesStdAsHtml (nsesDataSet).__str__()
	## print ws.stateStdsAsHtml (nsesDataSet[state]).__str__()
	ws.write()
	
		

