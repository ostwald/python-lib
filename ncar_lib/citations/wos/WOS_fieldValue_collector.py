import sys, os, re
from WOS_Processor import WOSProcessor
from WOS_Batch_Processor import WOS_Batch_Processor
from UserDict import UserDict

class CountingUserDict (UserDict):
	
	def __init__ (self):
		UserDict.__init__ (self)
	
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def count (self, key):
		if self.has_key (key):
			self[key] = self[key] + 1
		else:
			self[key] = 1
			
	def merge (self, other):
		for key in other.keys():
			if self.has_key (key):
				self[key] = self[key] + other[key]
			else:
				self[key] = other[key]
				
	def report (self):
		for key in self.keys():
			print "%s\t%d" % (key, self[key])

class FieldValueWOSProcessor (WOSProcessor):
	"""
	processes a single WOS file. collects the unique values for specified field from the
	raw data in the spreadsheet, and makes it available in "unique_values"
	
	accessorFn is a function, that, when present, is used to obtain the field value
	"""
	
	id_prefix = "NOT USED"
	
	def __init__ (self, path, field, limit=None, accessorFn=None):
		self.unique_values = CountingUserDict()
		self.field = field
		self.accessorFn = accessorFn
		WOSProcessor.__init__ (self, path, startid=1, limit=limit, write=0)
	
	def processRecords (self):
		"""
		self.records is a list of WOSRecord instances
		"""
		print "process Records: field is %s" % self.field
		for rec in self.records:

			if self.accessorFn:
				try:
					value = self.accessorFn(rec)
				except:
					raise Exception, "AccessorFunction error: %s" % sys.exc_info()[1]
					
			else:
			
				# data = self.makeDataDict (rec)
				try:
					value = rec[self.field]
				except KeyError:
					raise KeyError, "WOSRecord does not have field: '%s'" % self.field
				
			self.unique_values.count (value)
				
			# print "%d - %s" % (self.reccounter+1, rec['pubname'])

			self.reccounter = self.reccounter + 1
			if self.reccounter >= self.limit: break
		
class WOSFieldValueCollector (WOS_Batch_Processor):
	"""
	subclass of pubname collector that maintains a list of unique field values
	accross all spreadsheets processed
	
	accessorFn - when present, is used to calculate unique values (rather than simply
		plucking the provided field. In this case, the report is written using the 
		provided "field", but the values are calcuated using accessorFn
	"""
	
	
	def __init__ (self, field, accessorFn=None):
		self.unique_values = CountingUserDict()
		self.field = field
		self.accessorFn = accessorFn
		filenames = os.listdir(self.dataDir)
		filenames.sort()
		for filename in filenames:
			root, ext = os.path.splitext (filename)
			if not (root.startswith ('WOS') and ext == '.txt'):
				print "skipping %s" % filename
			print filename
			path = os.path.join (self.dataDir, filename)
			self.processFile (path)
			
	def processFile (self, path):
		pnp = FieldValueWOSProcessor (path, self.field, accessorFn=self.accessorFn)
		
		self.unique_values.merge (pnp.unique_values)
		
	def write (self):
		
		# sorted_values = self.unique_values.keys()
		vals = self.unique_values
		content = [];add=content.append
		for key in vals.keys():
			add ("%s\t%d" % (key, vals[key]))
		
		filename = "term_reports/uniqueWOSvalues_" + self.field + ".txt"
		fp = open (filename, 'w')
		fp.write ("\n".join (content))
		fp.close()
		print "wrote %d unique values for '%s' to %s" % (len (vals), self.field, filename)
		
	def report (self, showCount=True):
		print "unique values for %s field" % self.field
		for val in self.unique_values.keys():
			if showCount:
				print "\t%s (%d)" % (val, self.unique_values[val])
			else:
				print "\t%s" % val 
		
def FieldValueWOSProcessorTester():
	datafile1 = "WOS_data_files/WOS_1-500.txt"
	datafile2 = "WOS_data_files/WOS_11001-11500.txt"
	field = 'Year'
	accessorFunction = lambda rec:rec._getYear()	
	
	uvs = []
	for datafile in [datafile1, datafile2]:
		pnp = FieldValueWOSProcessor (datafile, field,accessorFn=accessorFunction)
		uv = pnp.unique_values
		print "\n%s" % datafile
		# uv.report()
		uvs.append(uv)
		
	uvs[0].merge(uvs[1])
	print "\nMERGED"
	uvs[0].report()

	
def collectUniqueFieldValues (field, accessorFn=None, write=0):
	accessorFunction = accessorFn
	collector = WOSFieldValueCollector (field, accessorFunction)
	if write:
		collector.write()
	else:
		collector.report()	
	
def collectUniqueYearValues():
	accessorFunction = lambda rec:rec._getYear()
	collectUniqueFieldValues ('year', accessorFunction, 1)
	
def collectPubDateValues():
	accessorFunction = lambda rec:rec._getPubDate()
	collectUniqueFieldValues ('PubDate', accessorFunction, 1)	
	
def collectPubNameValues():
	accessorFunction = None # lambda rec:rec._getPubName()
	collectUniqueFieldValues ('pubname', accessorFunction, 1)
	
def collectTitleValues():
	accessorFunction = None # lambda rec:rec._getPubName()
	collectUniqueFieldValues ('Title', accessorFunction, 1)
	
def collectPublisherValues():
	accessorFunction = None # lambda rec:rec._getPubName()
	collectUniqueFieldValues ('Publisher', accessorFunction, 1)
	
if __name__ == '__main__':
	# collectUniqueYearValues()
	# collectPubDateValues()
	# FieldValueWOSProcessorTester()
	# collectPubNameValues()
	# collectTitleValues()
	collectPublisherValues()
