import sys, os, string
from UserList import UserList
from UserDict import UserDict

from SAT_Eval.SpreadSheetBuilder import SuggestionSetRecord
from SAT_Eval.sat_utils import getNumId, makeFullId
from config import analysis_data_dir, mass_analysis_data_dir, suggestionSet_dir

# txtDir = "txtFiles"
txtDir = "/home/ostwald/Documents/Syracuse/SAT-analysis/data/txtFiles"
txtFile = "Applied_5-8_S101EF6F_done.txt"

path = os.path.join (txtDir, txtFile)

class Schema (UserList):
	def __init__ (self, line):
		splits = line.split('\t')
		self.data = map (string.strip, splits)

	def index_debug (self, field):
		try:
			return self.data.index(field)
		except:
			print "index for %s not found" % field
			return None
		
	def report (self):
		print "Schema"
		for i in range (len (self.data)):
			print "\t%d: '%s'" % (i, self[i])

class Record:
	def __init__ (self, line, schema):
		self.data = line.split ('\t')
		self.schema = schema

	def __getitem__ (self, field):

		index = self.schema.index (field)
		if (index is not None):
			return self.data[index]

	def __setitem__ (self, field, value):
		try:
			index = self.schema.index (field)
			self.data[index] = value
		except:
			print "tried to find field: " + field
			

class Standard (Record):
	def __init__ (self, data, schema):
		Record.__init__ (self, data, schema)
		self.doc = self['Standards Doc']
		self.id = self['id']
		self.text = self['text']
		self.benchmark = self['benchmark']
		self.gradeLevel = self['gradeLevel']
		
	def setDoc (self, doc):
		self.doc = doc

class NSESStandard (Standard):
	def __init__ (self, data, schema):
		Standard.__init__ (self, data, schema)
		self.band = None
		self.group = None

class StateStandard (Standard):
	def __init__ (self, data, schema):
		Standard.__init__ (self, data, schema)
		self.relevance = self._normalize_relevance()
		self.rank = None

	def _normalize_relevance (self):
		"""
		relevance is None, 1,2, or 3
		1 is MORE relevant than 3
		None is not relevant at all
		"""
		no_relevance = "" # None looks ugly when printed ...
		r = self['relevant']
		try:
			r = int(r)
		except:
			return no_relevance
		if r == 0: return no_relevance
		return r
		
	def hasHit (self, threshold=None):
		"""
		"""
		if not threshold:
			return self.relevance
		else:
			return self.relevance and threshold >= self.relevance
		
	def setRank (self, rank):
		self.rank = rank
		
class NSESDataSet (UserDict):
	"""
	NSESDataSet encapsulates all the SAT data associated with a given NSES Standard
	into the following data structures:
		- NSESStandard (NSES standard info)
		- For each of 5 STATES:
			- 5 StateStandard instances (the SAT-suggested Standards)
			
	NSESDataSet is a dict structure keyed by states. Each State key provides acess to the
	ordered list of StateStandard instances for that state.
	
	stores standards sets keyed by "standards_doc", e.g. NSES, Colorado, etc
	"""

	# suggestionSetDir =  "/home/ostwald/Documents/Syracuse/SAT-eval/data/suggestionSets"
	
	def __init__ (self, path):
		if not os.path.exists (path):
			print "data file does not exist at " + path
			sys.exit()
	
		UserDict.__init__ (self, {})
		self.path = path
		s = open (path,"r").read()
		

		lines = s.split ('\n')
		# print "%d lines read" % len (lines)

		self.schema = Schema (lines[0])
		## self.schema.report()
		
		# find the NSES standard for this spreadsheet
		line_counter = 1
		while (1):
			line = lines[line_counter]
			line_counter = line_counter + 1
			if not line.strip():
				continue
			splits = line.split('\t')
			if splits[0] == 'NSES':
				## extract band and group info from the SuggestionSet (for convenience)
				self.nses_standard = NSESStandard (line, self.schema)
				ss = self.getSuggestionSet()
				self.band = ss._get_band()
				self.group = ss._get_group()
				break
			
		# process the (suggested) state standards 
		# - instantiate suggested standards as StateStandards
		# - only the first std for each state has "doc" field. add "doc" to subsequent stds
		# - rank is also not represented explicitly, so we keep a 
		# - add to NSESDataSet map - keyed by doc (state) field.
		current_set = None
		rank_counter = 1
		for line in lines[line_counter:]:
			if not line.strip():
				continue
			rec = StateStandard (line, self.schema)
			if not rec.doc:
				rec.setDoc (current_set)
				rank_counter = rank_counter + 1
			else:
				current_set = rec.doc
				rank_counter = 1
			rec.setRank (rank_counter)
			self._add_state_standard (rec)
			
	def __getitem__ (self, key):
		if not self.has_key(key):
			return []
		else:
			return self.data[key]
			
	def getSuggestionSet (self):
		"""
		retrieve suggestionSetRecord from SAT_Eval suggestSet data. This data structuure
		holds all the info in the spreadsheet (except the relevance), but we only grab
		the "group" and "band" info ...
		"""
		
		filename = os.path.basename (self.path)
		x = filename.find ("_done.txt")
		if x == -1:
			raise "BOGUS_FILENAME", filename
		base = filename [:x]
		# print "'%s'" % base
		path = os.path.join (suggestionSet_dir, base+".xml")
		return SuggestionSetRecord (path)
			
	def _add_state_standard (self, rec):
		set = rec.doc
		if not self.has_key(set):
			self[set] = []
		items = self[set]
		items.append (rec)
		self[set] = items
		
	def getStandards (self, state=None):
		if state:
			return self[state]
		else:
			stds = []
			for state in self.keys():
				stds = stds + self[state]
			return stds
		
	def _make_rec (self, line):
		return Standard (line, self.schema)
		
	def report (self):
		print "\n*** %s ***" % os.path.basename (self.path)
		print "NSES Standard: " + self.nses_standard.id
		print "\tband: " + self.band
		print "\tgroup: " + self.group
		for set in self.keys():
			print "\n** %s **" % set
			for s in self[set]:
				print "\t%s (%d) -> %s" % (s.id, s.rank, s.relevance)


	
if __name__ == "__main__":
	
	r = NSESDataSet (path)
	r.report()
		

	
