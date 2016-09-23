import os, sys
from UserDict import UserDict
from UserList import UserList
from xls import XslWorksheet, WorksheetEntry
from xls.WorksheetEntry import FieldList, scrubQuotes
journals_data = 'data/EOL journal.txt'
# data = 'data/EOL proceedings.txt'

author_fields = ['Author Last', 'Author First', 'Author Middle 1', 'Author Middle 2', 'Institutional Affiliation']

class LineDataReader (UserList):
	"""
	Reads data from a file
	assumes data items are one-per-line
	reads data items into a list
	"""
	def __init__ (self, data_file):
		UserList.__init__ (self)
		self.data_file = data_file
		raw = open(self.data_file, 'r').read()
		lines = raw.split('\n')
		# print len(lines), 'lines read'
		for line in lines:
			if not line.strip(): continue
			if line[0] == '#': continue
			self.append(line)

class Author(WorksheetEntry):
	"""
	we get a line of data but are only interested in the author_fields
	"""
	def __init__ (self, textline, line_schema):
		"""
		only work with author_fields (in data and schema)
		the first field is ignored as well (hence "[1:len(author_fields)]")
		"""
		self.data = map (scrubQuotes, textline.split ('\t'))
		self.data = self.data[1:len(author_fields)+1]
		self.schema = FieldList (line_schema[1:len(author_fields)+1])
	
	def __repr__ (self):
		s=[];add=s.append
		for field in self.schema:
			add ("%s: %s" % (field, self[field]))
		return '\n'.join (s)		

class JournalRecord (WorksheetEntry):
	
	def __init__ (self, textline, line_schema):
		"""
		only work with non_author_fields (in data and schema)
		the first field is ignored as well (hence "[len(author_fields) + 1:]")
		"""
		self.data = map (scrubQuotes, textline.split ('\t'))
		self.data = self.data[len(author_fields) + 1:]
		self.schema = FieldList (line_schema[len(author_fields)+1:])
		self.authors = []

	def addAuthor (self, author):
		self.authors.append(author)
		
	def __repr__ (self):
		s=[];add=s.append
		for field in self.schema:
			add ("%s: %s" % (field, self[field]))
		return '\n'.join (s)
		
	def report (self):
		print self
		for a in self.authors:
			print '  ', a['Author Last']
		
class EolRecords (UserList):
	
	def __init__ (self, data_path):
		UserList.__init__ (self)
		self.lines = LineDataReader (data_path)
		print "%d lines read" % len(self.lines)

		## ignore first 2 lines
		schema = self.lines[2].strip().split('\t')
		print "schema: %s" % schema
		item = None
		for line in self.lines.data[3:]:
			if not line.strip():
				continue
			fields = line.split('\t')
			if (fields[0].strip()):
				item = JournalRecord(line, schema)
				self.append(item)
			item.addAuthor(Author (line, schema))

	def report (self):
		for i, entry in enumerate(self):
			print '\n%d' % (i+1)
			entry.report()
		
def uniqueAuthorValues (recs, fieldname, verbose=1):
	vals = []
	for rec in recs:
		for author in rec.authors:
			val = author[fieldname]
			if not val in vals:
				vals.append(val)
	vals.sort()
	if verbose:
		print "\n- Unique Author Values for '%s' -" % fieldname
		for val in vals:
			print val
	return vals
	
if __name__ == '__main__':
	recs = EolRecords(journals_data)
	print "%d records read" % len(recs)
	# recs.report()
	uniqueAuthorValues (recs, "Institutional Affiliation")
	
