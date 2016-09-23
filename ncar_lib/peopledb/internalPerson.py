import os, sys, urllib, urllib2, demjson, time
from UserDict import UserDict
from ncar_lib import unionDateToSecs

peopleDB_1 = "https://api.ucar.edu/people/internalPersons/"
peopleDB_2 = 'https://tmerapi.ucar.edu:8203/api/internalPersons/'

class Position (UserDict):

	def __init__ (self, data):
		self.data = data
		self.start = self.getDateStamp (self['startDate'], '1970')
		self.end = self.getDateStamp (self['endDate'])

	def __repr__ (self):
		return "%s (%s - %s)" % (self['organization'], self['startDate'], self['endDate'])
		
	def validOnDate (self, dateStr):
		checkDate = self.getDateStamp(dateStr)
		return self.start <= check and self.end >= check 
		
	def getDateStamp (self, unionDate, default=None):
		if unionDate:
			return unionDateToSecs (unionDate)
		elif default:
			return unionDateToSecs (default)
		else:
			return time.time()

class InternalPerson(UserDict):
	"""
	InteralPerson Response has following keys
	- upid
	- firstName
	- lastName
	- middleName
	- nameSuffix
	- nickname
	- username
	- email
	"""
	verbose=0
	
	def __init__ (self, upid, version=1):
		self.upid = upid
		self.baseUrl = self.getBaseUrl(version)
		self.data = self._get_data()
		self.positions = None
		# print self.data
		if not self.data:
			raise Exception, 'person not found for %s (in peopleDB v_%s)' % (upid, version)
		if version == 1:
			self.positions = map (Position, self['positions'])

	def getBaseUrl (self, version):
		if version == 1:
			return peopleDB_1
		if version == 2:
			return peopleDB_2
		raise Exception, "Could not getBaseUrl for version '%d'" % version
		
	def __getitem__ (self, key):
		if self.data.has_key(key):
			return self.data[key]
		else:
			return ""

	def _get_data(self):
		url = os.path.join (self.baseUrl, self.upid)
		if self.verbose:
			print url
		req = urllib2.Request(url)
		try:
			response = urllib2.urlopen(req)
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print 'we failed to reach the server.'
				print 'Reason:', e.reason
			elif hasattr (e, 'code'):
				print 'the server couldn\'t fulfill the request (%s)' % self.upid
				print 'Error code:', e.code
			# print e.reason
			return
		return demjson.decode (response.read())
		
	def workedFor (self, org):
		for pos in self.positions:
			if pos['organization'] == org:
				return 1
		return 0

	def __repr1__ (self):
		if not self.data:
			return "no data"
		s=[];add= s.append
		attrs = ['upid', 'firstName', 'lastName', 'middleName']
		for attr in attrs:
			add ('%s: %s' % (attr, self[attr]))
		if self.positions:
			for position in self.positions:
				add (' - ' + str(position))
		return '\n'.join (s)


	def __repr__ (self):
		if not self.data:
			return "no data"
		s = self['firstName']
		if self['middleName']: s = '%s %s' % (s, self['middleName'])
		s = "%s %s (%s)" % (s, self['lastName'], self['upid'])
		if self.positions:
			for position in self.positions:
				s = s + "\n - %s" % position
		return s
		
if __name__ == '__main__':
	my_upid = '2775'
	person = InternalPerson (my_upid, 1)
	print person
