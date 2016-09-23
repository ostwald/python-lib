import sys, os, string
from SpreadSheetReader import NSESDataSet
from UserDict import UserDict
from SAT_Eval.sat_utils import state_list, domain_groups_keys
from config import analysis_data_dir, mass_analysis_data_dir, suggestionSet_dir

verbose=0

class Collector (UserDict):
	
	
	def __init__ (self):
		UserDict.__init__(self)
		
		"""
		build dict of all NSESDataSet, keyed by NSES id
		"""
		for filename in os.listdir (analysis_data_dir):
			path = os.path.join (analysis_data_dir, filename)
			r = NSESDataSet (path)		
			self[r.nses_standard.id] = r
	
	def select (self, band=None, group=None, filter=None):
		"""
		select NSESDataSet by group and band
		then filter by DataSetFilter
		
		Return map of selected NSESDataSets, keyed by ID
		"""
		
		groupSet = None
		if not group: groupSet = []
		elif type (group) == type (""): groupSet = [group]
		elif type (group) == type ([]): groupSet = group
		
		
		selected = {}
		for nses in self.keys():
			dataSet = self[nses]
			if band and dataSet.band != band: continue
			if group and dataSet.group not in groupSet: continue
			if filter and not filter(dataSet): continue
			
			selected[nses] = dataSet
			
		return selected
		
			
	def list (self, dataSet_map):
		for dataSet in dataSet_map.values():
			dataSet.report()

class MASSGraftCollector (Collector):
	
	def __init__ (self,):
		UserDict.__init__(self)
		
		"""
		build dict of all NSESDataSet, keyed by NSES id
		"""
		for filename in os.listdir (analysis_data_dir):
			path = os.path.join (analysis_data_dir, filename)
			dataset = NSESDataSet (path)
			
			masspath = os.path.join (mass_analysis_data_dir, filename)
			massdataset = NSESDataSet (masspath)
			
			dataset["Massachusetts"] = massdataset["Massachusetts"]
			
			self[dataset.nses_standard.id] = dataset
			
def prtln (s):
	if (verbose):
		sys.stdout.write(s + "\n")
				
def noHitsFilter (dataSet):
	for state in dataSet.values():
		for standard in state:
			if standard.hasHit(): return 0
	return 1
			
			
def hasHit (dataSet, threshold=None, state=None, rank=None):
	"""
	this is a DATA SET filter, which returns true if there is a
	standard in the dataset which satisfies the critieria
	"""
	for std in dataSet.getStandards (state):
		if rank and std.rank > rank:
			continue
		if std.hasHit(threshold): return 1
	# for state in dataSet.keys():
		# for standard in dataSet[state]:
			# if standard.hasHit(threshold): return 1
	
def standardsWithAnyHits (collector, **args):
	prtln ( "standardsWithAnyHits")
	if args:
		for key in args.keys():
			prtln ( "\t%s: %s" % (key, args[key]))
	group = args.has_key("group") and args["group"] or None
	state = args.has_key("state") and args["state"] or None
	rank = args.has_key("rank") and args["rank"] and int(args["rank"]) or None
	threshold = args.has_key("threshold") and args["threshold"] and int(args["threshold"]) or None
	# print "Standards with hits (threshold='%s', state='%s')" % (threshold, state)
	filter = lambda dataSet: hasHit(dataSet, threshold=threshold, state=state, rank=rank)
	results = collector.select (filter=filter, group=group)
	# print "%d found" % len(results)
	# collector.list(results)
	return len(results)
	
def standardsWithNoHits (collector):
	prtln ( "Standards with no hits" )
	filter = noHitsFilter
	results = collector.select (filter=filter)
	prtln ( "%d found" % len(results))
	# collector.list(results)
	
def allStandards ():
	c = Collector().select()
	print "%d found" % len(c)
	# c.list()
		
def stateTable ():
	collector = Collector()
	m = {}
	for state in state_list + [""]:
		m[state] = {}
		for t in range (1, 4):
			c = standardsWithAnyHits(collector, threshold=t, state=state, rank=1)
			m[state].update({t:c})
			
	print string.join (["state", "1", "2", "3"], "\t")
	for state in m.keys():
		print "%s\t%d\t%d\t%d" %(state, m[state][1], m[state][2], m[state][3])

def groupTable (state=None, rank=None):
	collector = Collector()
	m = {}

	print "GroupTable"
	if state: print "\t state: " + state
	if rank: print "\t rank: " + rank
	
	for group in domain_groups_keys + [""]:
		m[group] = {}
		for t in range (1, 4):
			c = standardsWithAnyHits(collector, threshold=t, group=group, rank=rank, state=state)
			m[group].update({t:c})
			
	print string.join (["threshold", "1", "2", "3"], "\t")
	for group in domain_groups_keys:
		print "%s\t%d\t%d\t%d" %(group, m[group][1], m[group][2], m[group][3])
	
def groupSizer ():
	collector = Collector()
	print "Group sizes"
	for group in domain_groups_keys:
		n = collector.select (group=group)
		print "\n%s: %d" % (group, len(n))
		
def hasHitTester ():
	c = Collector()
	dataSet = c["S10245A5"]
	dataSet.report()
	if hasHit(dataSet, threshold=2, state="New York", rank=3):
		print "HIT"
	else:
		print "MISS"	
		
if __name__ == "__main__":
	groupTable (state="Colorado")
	

