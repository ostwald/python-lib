from UserDict import UserDict
from position_history_data import position_data

print "data has %d items" % len (position_data)

class Position(UserDict):
	def __init__ (self, data):
		self.data = data
		print data

	def __getitem__ (self, key):
		if self.data.has_key(key):
			return self.data[key]
		else:
			return ""
		
	def __repr__ (self):
		s = '%s %s - %s' % (self['organization'], self['startDate'], self['endDate'])
		if self['type'] == 'Visitor':
			s = s + " Visitor"
		return s
		
	def __cmp__ (self, other):
		return cmp (self['startDate'], other['startDate'])
		
class PositionData (UserDict):
	"""
	keyed by upid
	"""
	def __init__ (self):
		self.data = {}
		for item in position_data:
			upid = item['upid']
			positions = map (Position, item['positions'])
			positions.sort()
			self[upid] = positions



if __name__ == '__main__':
	pData = PositionData()
	for key in pData.keys():
		print key
		for pos in pData[key]:
			print ' - ', pos
				
		   
