import os, sys
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
from citation_reader import CitationReader 

class UniqueValues (UserDict):
	"""
	traverse all metadata records under startDir 
	and collect unique values for specified field
	"""
	
	def __init__ (self, startDir, field):
		if not os.path.exists (startDir):
			raise Exception, "directory does not exist at " % startDir
		UserDict.__init__ (self)
		self.startDir = startDir
		self.field = field
		self.process()
		self.values = self.keys()

	def process (self):
		"""
		populate self.tally with dict of unique term to occurrence map
		"""
		vals = []
		filenames = os.listdir (self.startDir)
		print "reading %d files" % len (filenames)
		for i, filename in enumerate (filenames):
			if i % 100 == 0:
				print i
			path = os.path.join (self.startDir, filename)
			rec = CitationReader (path)
			term = rec._get(self.field)
			if not term: continue
			if self.has_key(term):
				self[term] = self[term] + 1
			else:
				self[term] = 1
		
	def keys (self):
		ordered = self.data.keys()
		ordered.sort()
		return ordered
					
	def report (self):
		print "unique values for '%s'" % (field)
		for term in self.keys():
			print "%s (%d)" % (term, self[term])


if __name__ == '__main__':
	field = 'publisher'
	startDir = "/home/ostwald/python-lib/ncar_lib/citations/pubs/PUBS_other_metadata"
	vals = UniqueValues (startDir, field)
	vals.report()
	
