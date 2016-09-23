import sys, os, string
from SpreadSheetReader import NSESDataSet
from UserDict import UserDict
from SAT_Eval.sat_utils import states

class Collector (UserDict):
	
	txtFileDir = "txtFiles"
	
	def __init__ (self, band=None, group=None, filter=None):
		UserDict.__init__(self)
		
		
		for filename in os.listdir (self.txtFileDir):
			path = os.path.join (self.txtFileDir, filename)
			r = NSESDataSet (path)
			
			if band and r.band != band: continue
				
			if group and r.group != group: continue
			
			if filter and not filter(r): continue
				
			self[r.nses_standard.id] = r
	
	def list (self):
		for reader in self.values():
			reader.report()
				
def noHitsFilter (reader):
	for state in reader.values():
		for standard in state:
			if standard.hasHit(): return 0
	return 1
			
			
def hasHit (reader, threshold=None, state=None):
	
	for std in reader.getStandards (state):
		if std.hasHit(threshold): return 1
	# for state in reader.keys():
		# for standard in reader[state]:
			# if standard.hasHit(threshold): return 1
	
def standardsWithAnyHits (**args):
	group = args.has_key("group") and args["group"] or None
	state = args.has_key("state") and args["state"] or None
	threshold = args.has_key("threshold") and args["threshold"] or None
	print "Standards with hits (threshold='%s', state='%s')" % (threshold, state)
	filter = lambda reader: hasHit(reader, threshold=threshold, state=state)
	c = Collector (filter=filter, group=group)
	print "%d found" % len(c)
	# c.list()
	return len(c)
	
def standardsWithNoHits ():
	print "Standards with no hits"
	filter = noHitsFilter
	c = Collector (filter=filter)
	print "%d found" % len(c)
	# c.list()
	
def allStandards ():
	c = Collector ()
	print "%d found" % len(c)
	# c.list()
		
def stateTable ():
	m = {}
	for state in states:
		m[state] = {}
		for t in range (1, 4):
			c = standardsWithAnyHits(threshold=t, state=state)
			m[state].update({t:c})
			
	print string.join (["state", "1", "2", "3"], "\t")
	for state in m.keys():
		print "%s\t%d\t%d\t%d" %(state, m[state][1], m[state][2], m[state][3])
if __name__ == "__main__":
	for t in range (1, 4):
		c = standardsWithAnyHits(threshold=t)
	

