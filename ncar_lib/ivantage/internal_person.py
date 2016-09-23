import sys, os, re, time
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from UserDict import UserDict

default_data = "data/internal_person.txt"

class IdMapRecord (TabDelimitedRecord):
	
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.upid = self.getInt('upid')
		self.peid = self.getInt('peid')
		self.active = self.getInt('active')
		self.purged = self.getInt('purged_by_hr')
		if self.purged:
			# print '... self is purged (peid is %s)' % self.peid
			self.peid = None
			
	def getInt (self, attr):
		try:
			return int(self[attr])
		except:
			return 0
			
	def report (self):
		print 'upid: %s, peid: %s' % (self.upid, self.peid)
		
class UpidLookup (UserDict):
	"""
	provides a dict-like lookup interface for mappings from peid to upid
	
	self[peid] -> upid
	"""
	
	def __init__ (self):
		self.data = {}
	
	def __setitem__ (self, peid, value):
		# print 'setitem'
		if peid is None or peid == 0: # this is the case when person has been purged by hr
			print 'peid is None or 0'
			return
		if self.data.has_key(peid):
			raise KeyError, "%s is a duplicate peid" % peid
		# print '%d: %d' % (peid, value)
		self.data[peid] = value
		
	def __getitem__ (self, peid):

		if not self.data.has_key(peid):
			raise KeyError, "peopleDBv1 has no upid for peid: %s" % peid
		return self.data[peid]
	
class IdMapTable (TabDelimitedFile):
	verbose = 0
	linesep = "\n"
	# how files are read and written (prefer utf-8, but sometimes only ISO-8859-1 works)
	encoding = 'ISO-8859-1' # utf-8
	
	def __init__ (self, path=None):
		self.path = path or default_data;
		print 'self.path: %s ' % self.path
		TabDelimitedFile.__init__ (self, entry_class=IdMapRecord)
		self.read(self.path)
		self.lookup = self.makeUpidLookup ()
		
	def accept (self, record):
		return record.purged == "0" or record.purged == 0

	def makeUpidLookup (self):
		tics = time.time()
		print 'tics: %f' % tics
		lookup = UpidLookup()
		for rec in self:
			lookup[rec.peid] = rec.upid
		print 'idMap (%d) created in %f secs' % (len(self), 
									float(time.time() - tics))
		return lookup
		
	def getUpid (self, peid):
		return self.lookup[peid]
		
if __name__ == '__main__':
	table = IdMapTable()

	# for rec in table:
		# print rec.upid, rec.peid
	
	if 1:
		lookup = table.lookup
		
		print '\nLookup has %d items' % len(lookup)
#		for peid in lookup.keys():
#			print peid, type(peid)
			# print "%s (%s): %s (%s)" % (key, type(key), lookup[key], type(lookup[key]))
		
		print "%d records read" % len(table)
		peids = [10005, 18080, 16010]
		for peid in peids:
			try:
				print "peid: %s, upid: %s" % (peid, table.getUpid(peid))
			except KeyError, msg:
				print 'ERROR: could not get upid for peid: %s: %s' %  (peid, msg)
				
		peid = lookup.keys()[3]
		print 'peid: ', peid
		
