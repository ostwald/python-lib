"""
WOS-TALLY - get all values for given field in given spreadsheet
"""
from UserDict import UserDict
from WOS_reader import WOSXlsReader

class WOSTally:
	
	def __init__ (self, path):
		self.wos = WOSXlsReader(path)
		tally = UserDict ()
		for rec in self.wos:
			for field in rec.keys():
				val = rec[field]
				if tally.has_key(field):
					tally_val = tally[field]
				else:
					tally_val = 0
				if val:
					tally_val = tally_val + 1
				tally[field] = tally_val
		self.tally = tally
			
	def report (self):
		fields = self.tally.keys()
		fields.sort()
		for field in fields:
			print '%s -> %d' % (field, self.tally[field])
			
class WOSFieldTally:
	
	def __init__ (self, path, field):
		self.wos = WOSXlsReader(path)
		self.field = field
		tally = UserDict ()
		for rec in self.wos:
			val = rec[field]
			if not val: continue
			if tally.has_key(val):
				tally_val = tally[val]
			else:
				tally_val = 0
			if val:
				tally_val = tally_val + 1
			tally[val] = tally_val
		self.tally = tally
			
	def report (self):
		print "value tally for * %s * field" % self.field
		vals = self.tally.keys()
		vals.sort()
		for val in vals:
			print '%s (%d)' % (val, self.tally[val])
	
class WOSPubnameTally:
	
	def __init__ (self, path):
		self.wos = WOSXlsReader(path)
		self.field = "pubname"
		tally = UserDict ()
		for rec in self.wos:
			val = rec._getPubname()
			if not val: continue
			if tally.has_key(val):
				tally_val = tally[val]
			else:
				tally_val = 0
			if val:
				tally_val = tally_val + 1
			tally[val] = tally_val
		self.tally = tally
			
	def report (self):
		print "value tally for * %s * field" % self.field
		vals = self.tally.keys()
		vals.sort()
		for val in vals:
			print '%s (%d)' % (val, self.tally[val])
			
class WOSAuthorNameTally:
	
	def __init__ (self, path):
		self.wos = WOSXlsReader(path)
		tally = UserDict ()
		for rec in self.wos:
			for author in rec._getAuthors():
				val = author
				if not val: continue
				if tally.has_key(val):
					tally_val = tally[val]
				else:
					tally_val = 0
				if val:
					tally_val = tally_val + 1
				tally[val] = tally_val
		self.tally = tally
			
	def report (self):
		print "author tally"
		vals = self.tally.keys()
		vals.sort()
		for val in vals:
			print '%s (%d)' % (val, self.tally[val])
			
def fieldTally():
	path = "WOS_4501-5000.txt"
	fields = ["Volume"]
	for field in fields:
		WOSFieldTally (path, field).report()
		
if __name__ == '__main__':
		
	path = "WOS_4501-5000.txt"
	# WOSAuthorNameTally (path).report()
	# WOSPubnameTally(path).report()
	fieldTally()
