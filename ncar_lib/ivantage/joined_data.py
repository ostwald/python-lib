"""
create a map structure representing merged position history

upid is the key --> positions

position
	- upid
	- start
	- end
	- entity
	- org
	- divCode
	- divProg
"""
import sys, os, time
from UserDict import UserDict
from ivantage_data import iVantageDataTable
from internal_person import IdMapTable

class JoinedData (UserDict):
	
	def __init__ (self):
		"""
		upidLookup gets upid for given peid
		"""
		UserDict.__init__(self)
		self.errors = []
		ivantage_data = iVantageDataTable()
		idMap = IdMapTable()
		
		for record in ivantage_data.data:  # careful - must be greater than records read
			try:
				upid = idMap.getUpid (record.peid)
			except KeyError, msg:
				self.errors.append(str(record))
				continue
			self.add (upid, record)
			
	def add (self, upid, position):
		try:
			positions = self.getPositions (upid)
		except KeyError:
			positions = []
		positions.append (position)
		self.data[upid] = positions
		
	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def getPositions (self, upid):
		return self.data[upid]
		
	def showErrors (self):
		if self.errors:
			print "The following peids have no upid (%d)" % len (self.errors)
			for err in self.errors:
				print ' - ', err
		else:
			print 'No errors'
			
	def report (self, upids=None):
		upids = upids or self.keys()
		for upid in upids:
			print '\n %d - % s' % (upid, (self[upid])[0].name)
			for ivRec in self[upid]:
				s = [];add=s.append
				for attr in [ 'start', 'end', 'entity', 'lab', 'org']:
					add (getattr (ivRec, attr))
				print ' - ' + '  -  '.join(s)
			
if __name__ == '__main__':
	ph = JoinedData()
	print "%d unique upids" % len(ph)
	ph.showErrors()
	ph.report()
	
	
