import os, sys, urllib, urllib2, demjson, time

class PeopleDBClient:

	baseUrl = 'https://api.ucar.edu/people/'
	action = "orgs"
	
	def paramsToQueryString (self, paramMap):
		params=[];add=params.append
		for key in paramMap:
			val = paramMap[key]
			if type(val) in [type(""), type(u"")]:
				add ("%s=%s" % (key, val))
			if type(val) == type([]):
				for v in val:
					add ("%s=%s" % (key, urllib.quote(v)))
		return '&'.join (params)
	
	def getUrl (self, action, params):
		url = self.baseUrl
		if action:
			url = os.path.join (self.baseUrl, action)
		if params:
			url += "?" + self.paramsToQueryString(params)
		return url
		
	def getData(self, action=None, params=None):
		url = self.getUrl(action, params)
		print 'URL: ', url
		req = urllib2.Request(url)
		try:
			response = urllib2.urlopen(req)
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print 'we failed to reach the server.'
				print 'Reason:', e.reason
			elif hasattr (e, 'code'):
				print 'the server couldn\'t fulfill the request (%s)' % url
				print 'Error code:', e.code
			# print e.reason
			return
		return demjson.decode (response.read())
		

		
if __name__ == '__main__':
	client = PeopleDBClient()
	data = client.getData (action='subOrgs', params={'org':'EOL'})
	for item in data:
		print item['acronym']
