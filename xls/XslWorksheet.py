"""
Reads a tab-delimited file that is created from an excel
"""

import os, sys, codecs
from string import split, join, strip
from UserDict import UserDict
from UserList import UserList
from WorksheetEntry import WorksheetEntry

class XslWorksheet (UserList):
	"""
	a list of Records, which are read from a tab-delimited file.
	entries in the source file can be filtered using the "accept" method.
	The entries are subclasses of XslWorksheetEntry
	"""
	verbose = 0
	linesep = "\n"
	# how files are read and written (prefer utf-8, but sometimes only ISO-8859-1 works)
	encoding = 'ISO-8859-1' # utf-8
	
	def __init__ (self, data=[], entry_class=WorksheetEntry):
		self.data = data
		self.schema = None
		self.entry_class = entry_class

## 	def __getitem__ (self, index):
## 		return self.data[index]

	def add (self, item):
		self.append(item)

	def accept (self, item):
		"""
		subclasses may specialize this method to filter addresses
		"""
		return 1

	def splitline (self, line):
		"""
		split the line of data into fields.
		override for csv, etc
		"""
		return line.split('\t')
		
	def preprocess (self, filecontents):
		"""
		hook to do some preprocessing to the entire data file
		before parsing into records
		"""
		return filecontents
		
	def read (self, path):
		"""
		Initialize the XslWorksheet by reading from a tab-delimitted file 
		(whose first line is schema, i.e., list of fields) and creating
		entries by instantiating the XslWorksheetEntry class specified by the 'address_class'
		attribute.
		"""

		self.data = []
		# print "*** path: %s***" % path
		dir, filename = os.path.split (path)
		root, ext = os.path.splitext (filename)
		# encoding = 'ISO-8859-1' # utf-8
		s = codecs.open(path,'r', self.encoding).read()
		## s = unicode(f.read(),'utf-8')
		s = self.preprocess (s)
		lines = split (s, self.linesep)
		schema = self.splitline(lines[0])

		## print "** %s **" % os.path.splitext(filename)[0]
		if self.verbose:
			print "read %d lines from %s" % (len(lines), path)

		for i in range(1,len(lines)):
			if not lines[i].strip(): 
				# print 'skipping line (%d)' % i
				continue
			fields = self.splitline(lines[i])
			item = self.entry_class (fields, schema)
			if self.accept (item):
				self.add (item)

		self.schema = schema
		# self.data.sort (lastNameCmp)
		

	def __repr__ (self):
		"""
		Creates a string representation of the XslWorksheet
		"""
		s=[];add=s.append
		for item in self.data:
			add (str(item))
		return join (s, '\n')

		
	def showSchema (self):
		"""
		the schema is a simple list of field names.
		"""
		s=[];add=s.append
		for i in range(len(self.schema)):
			add ("%d. %s" % (i+1, self.schema[i]))
		return join (s, '\n')
			
	def len (self):
		"""
		the number of entries in this XslWorksheet
		"""
		return len (self.data)
		
	def write (self, path):
		"""
		writes the Worksheet to a tab delimited file
		- used to update a data file
		"""
		s=[]; add=s.append
		add ('\t'.join (self.schema))
		for record in self.data:
			add (record.asTabDelimitedRecord())
		
		# f = open (path, 'w')
		f = codecs.open(path, 'w', 'utf-8')
		f.write (self.linesep.join (s))
		f.close()
		print ("data written to " + path)


if __name__ == "__main__":
	path = "Roster.txt"

   	ab = XslWorksheet ()
	ab.read (path)
	print "There are %s items" % ab.len()
	print ab
	## print ab.showSchema()


