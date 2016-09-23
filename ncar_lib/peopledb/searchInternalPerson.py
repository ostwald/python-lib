import os, sys, urllib, urllib2, demjson, time
from UserList import UserList
from ncar_lib import unionDateToSecs
# from json_client import JsonClient  # json_client should power search ...

peopleDB_1 = "https://api.ucar.edu/people/internalPersons"
peopleDB_2 = 'https://tmerapi.ucar.edu:8203/api/persons'

class InternalPersonSearch(UserList):
	"""
	results are a list of json structures for authors found
	"""
	
	verbose = 1
	
	def __init__ (self, params, version=1):
		self.data = []
		self.params = params
		self.baseUrl = self.getBaseUrl(version)
		self.url = self.baseUrl + '?' + urllib.urlencode (self.params)
		self.result = None
		self.data = self._get_data(self.url)
		
		if len(self) == 1:
			self.result = self.data[0]
			if 0 and self.verbose:
				print self.reportItem (self.result)
		else:
			if self.verbose:
				print '%d results found' % len(self)

	def getBaseUrl (self, version):
		if version == 1:
			return peopleDB_1
		if version == 2:
			return peopleDB_2
		raise Exception, "Could not getBaseUrl for version '%d'" % version
				
	def _get_data(self, url):
		req = urllib2.Request(url)
		if self.verbose:
			print url
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
		

	def reportItem2 (self):
		if not self.data:
			return "no data"
		s=[];add= s.append
		attrs = ['upid', 'firstName', 'lastName', 'middleName']
		for attr in attrs:
			add ('%s: %s' % (attr, self[attr]))
		return '\n'.join (s)


	def reportItem (self, data):
		if not data:
			return "no data"
		s = data['firstName']
		if data['middleName']: s = '%s %s' % (s, data['middleName'])
		s = "%s %s (%s)" % (s, data['lastName'], data['upid'])
		return s
		
	def report(self):
		for result in self:
			print self.reportItem (result)
			
			
if __name__ == '__main__':
	params = { 
		'lastName' : 'Sanderson',
		#'firstName' : 'Z'
	}
	results = InternalPersonSearch(params, 2)
	for result in results:
		print "%s, %s (%s)" % (result['lastName'], result['firstName'], result['upid'])
	
