from UserDict import UserDict
from callbackProcessor import CallbackMetadataProcessor

class Tally (UserDict):
	
	def __init__ (self, name):
		self.name = name
		UserDict.__init__ (self)
	
	def tally (self, values):
		if not values: return
		if type(values) == type(""):
			values = [values]
		count = 0
		for val in values:
			if self.has_key(val):
				count = self[val]
			self[val] = count + 1
		
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def report (self):
		header = "\nUnique values (%d) for %s" % (len (self), self.name)
		print "%s\n%s" % (header, '-'*len(header))
		for key in self.keys():
			print "\t%s (%d)" % (key, self[key])
			
class TallyRunner:
	mp = CallbackMetadataProcessor
	verbose = False
	header = "tally header not provided"

	def __init__ (self):
		self.myTally = Tally (self.header)
		self.run()
		self.report()
	
	def myRecordProcessor (self, rp):
		"""
		for each record processed, tallies a value
		"""
		self.myTally.tally ("recordProcessor not initialized!")
	
	def run (self):
		self.mp(self.myRecordProcessor)
		
	def report (self):
		self.myTally.report()
