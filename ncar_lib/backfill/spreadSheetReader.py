"""

"""

import sys, os, time, math
from ncar_lib.lib import globals
from UserDict import UserDict

delimiter = "\t"

class Entry:
	"""
	records a payment (amount, date)
	"""
	
	def __init__ (self, line, schema):
		self.line = line
		self.schema = schema
		self.fields = line.split(delimiter)

	def getFieldValue (self, field):
		i = self.schema.index(field)
		val = self.fields[i]
		if val:
			if val[0] in ['"', "'"] and val[0] == val[-1]:
				val = val[1:-1]
			if val: val = val.strip()
		return val
		
	def setFieldValue (self, field, value):
		if value:
			value = value.strip()
		if value is None:
			value = ""
		i = self.schema.index (field)
		self.fields[i] = value
		
	def __repr__ (self):
		s=[];add=s.append
		for field in self.schema:
			add (self.getFieldValue (field))
		return "\t".join(s)
		
class SpreadSheetReader (UserDict):
	
	"""
	processes a file one line at a time
	each line becomes an Entry
	"""
	
	key_field = "DR Number"
	errorOnDups = True
	
	def __init__ (self, path, name="Report"):
		self.name = name
		self.path = path
		UserDict.__init__(self)
		s = open (path).read()
		lines = s.splitlines()
		self.schema = lines.pop(0).split (delimiter)
		self.processLines (lines)

	def processLines (self, lines):
		"""
		each successfully processed line is a Payment (if a date cannot be parsed,
		an Exception is raised and that line is not processed)
		"""
		for line in lines:
			try:
				entry = Entry (line, self.schema)
				key = entry.getFieldValue (self.key_field)
				if self.has_key (key):
					msg = "duplicate key (%s)" % key
					if self.errorOnDups:
						raise Exception, msg
					else:
						print "WARNING: %s" % msg
				self[key] = entry

			except "ValueError":
				# print sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
				print sys.exc_info()[0], sys.exc_info()[1]
				print line
				pass

			
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
			
	def report (self):
		s=[];add=s.append
		for entry in self.values():
			add (entry.__str__())
		return '\n'.join (s)

	def write (self):
		out = self.getReportPath()
		fp = open (out, 'w')
		fp.write ('\t'.join(reader.schema))
		fp.write (self.report())
		fp.close()
		print "wrote to ", out
		
def entryTest ():
	l = "4/25/03\t-600.0"
	e = Payment (l)
	print e
	
if __name__ == "__main__":
	
	path = os.path.join (globals.docBase, "backfill/DR numbers for TN parts.txt")
	reader = SpreadSheetReader (path)

