"""
Reads a tab-delimited file that is created from an excel
"""

import os, sys, codecs
from string import split, join, strip
from UserDict import UserDict
from UserList import UserList
from TabDelimitedRecord import TabDelimitedRecord

class FieldList (UserList):
	"""
	Represents a Schema as a list of named fields
	"""
	def __init__ (self, list=[]):
		# remove quote wraps, if present, from field names
		# print list
		list = filter (lambda x: x.strip(), map (self.unquote, list))
		UserList.__init__ (self, list)

	def unquote (self, value):
		if value is None or not (type(value) == type("") or type(value) == type(u'')):
			return ''
			
		value = value.strip()
		if len(value) < 3:
			return value
		first = value[0]
		try:
			last = value[-1]
		except Exception, msg:
			print 'Error: %s' % msg
			return value

		if first == last == "'" or first == last == '"':
			value = value[1:-1]
		return value
		
	def getIndex (self, field):
		"""
		returns the index of the named field, or -1 if the field is not contained
		in the list of fields
		"""
		if field in self.data:
			return self.data.index (field)
		else:
			return -1
			
	def asTabDelimitedListing (self):
		return string.join (self.data, '\t')
		
	def __repr__ (self):
		s=[];add=s.append
		for i, field in enumerate(self.data):
			add ("%d. %s" % (i+1, field))
		return '\n'.join (s)
		
class ColumnFieldList (FieldList):
	"""
	to be used in tables that don't have a header.
	in this case we need to refer to fields by their
	column letter
	
	we create a 20 coluumn field list by default
	"""
	
	default_size = 20
	
	def __init__ (self, size=None):
		if size is None:
			size = self.default_size
		n = 65
		fields = [];add=fields.append
		while n < (65 + size):
			# print chr (n)
			add (chr(n))
			n = n + 1
		# print fields
		FieldList.__init__(self, fields)

class TabDelimitedFile (UserList):
	"""
	a list of Records, which are read from a tab-delimited file.
	entries in the source file can be filtered using the "accept" method.
	The entries are subclasses of TabDelimitedFileEntry
	"""
	verbose = 0
	linesep = os.linesep
	max_to_read = None
	# how files are read and written (prefer utf-8, but sometimes only ISO-8859-1 works)
	encoding = 'ISO-8859-1' # utf-8
	
	def __init__ (self, data=[], entry_class=TabDelimitedRecord):
		self.data = data
		self.schema = None
		self.entry_class = entry_class

## 	def __getitem__ (self, index):
## 		return self.data[index]

	def add (self, item):
		"""
		overide this to create other structurs, such as maps, e.g.,
			self.itemMap[item.key] = item
		"""
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
		Initialize the TabDelimitedFile by reading from a tab-delimitted file 
		(whose first line is schema, i.e., list of fields) and creating
		entries by instantiating the TabDelimitedFileEntry class specified by the 'address_class'
		attribute.
		"""
		# print 'READING', path
		# sys.exit()
		self.data = []
		# print "*** path: %s***" % path
		dir, filename = os.path.split (path)
		root, ext = os.path.splitext (filename)
		# encoding = 'ISO-8859-1' # utf-8
		s = codecs.open(path,'r', self.encoding).read()
		## s = unicode(f.read(),'utf-8')
		s = self.preprocess (s)

		lines = split (s, self.linesep)
		# print '%d lines' % len(lines)
		firstLine = self.splitline(lines[0])
		# print 'lines[0]: ', lines[0]
		self.schema = self.makeSchema(firstLine)

		## print "** %s **" % os.path.splitext(filename)[0]
		if self.verbose:
			print "read %d lines from %s" % (len(lines), path)
		for i in range(1,len(lines)):
			if not lines[i].strip(): 
				# print 'skipping line (%d)' % i
				continue
			fields = self.splitline(lines[i])
			# print '%s' % self.entry_class.__name__
			item = self.entry_class (fields, self)
			if self.accept (item):
				self.add (item)
				
				# print '%d / %s' % (len(self), self.max_to_read)
				# print 'about to inc (', self.max_to_read, ') ', self.max_to_read.__class__.__name__
				
				if self.max_to_read is not None and len(self) >= self.max_to_read:
					print 'READ TRUNCATED after %d records' % self.max_to_read
					return
					
				# if self.max_to_read is None:
					# print 'MAX TO READ IS None'
					# return
		
		# self.data.sort (lastNameCmp)
		
	def makeSchema (self, data):
		"""
		override for CVS, etc
		"""
		# print 'schema line: ', data
		return FieldList(data)

	def __repr__ (self):
		"""
		Creates a string representation of the TabDelimitedFile
		"""
		s=[];add=s.append
		for item in self.data:
			add (str(item))
		return join (s, '\n')

		
	def showSchema (self):
		"""
		the schema is a simple list of field names.
		"""
		# s=[];add=s.append
		# for i in range(len(self.schema)):
			# add ("%d. %s" % (i+1, self.schema[i]))
		# return join (s, '\n')
		print str(self.schema)
			
	def len (self):
		"""
		the number of entries in this TabDelimitedFile
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

	def addField (self, field):
		if field in self.schema:
			raise KeyError, 'field (%s) already exists in schema' % field
		self.schema.append(field)
		
	def getUniqueValues (self, field=None, fn=None):
		if field is None and fn is None:
			raise Exception, "getUniqueValues requires either a field or a function"
		values = []
		for item in self.data:
			if field:
				value = item[field]
			elif fn:
				value = fn(item)
			if not value in values:
				values.append(value)
		return values
		
	def getAllValues (self, field=None, fn=None):
		if field is None and fn is None:
			raise Exception, "getUniqueValues requires either a field or a function"
		values = []
		for item in self.data:
			if field:
				value = item[field]
			elif fn:
				value = fn(item)
			values.append(value)
		return values

def getFieldValues (path, field):
	"""
	returns a list of values from specified field
	"""
	tdfile = TabDelimitedFile()
	tdfile.read(path)
	return map(lambda x:x[field], tdfile.data)
		
		
if __name__ == "__main__":

	path = '/home/ostwald/python-lib/ncar_lib/osm/wos/real_data/wos_ncar-ucar_fy11.txt'
	field = 'wos id'
	values = getFieldValues(path, field)
	for v in values:
		print v


