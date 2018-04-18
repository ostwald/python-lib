# -*- coding: utf-8 -*-

import requests
from UserDict import UserDict
from model import SearchResponse, SearchResult
import json

# baseurl = "http://localhost:4567/repositories/2/search"
# r = requests.get(baseurl, auth=('admin','admin'))

class AspaceProxy:

	baseurl = 'http://localhost:4567'

	def __init__ (self, user='admin', passwd='admin'):
		self.user = user
		self.passwd = passwd
		self._token = None

	def get_token(self):
		if self._token is None:
			endpoint = '%s/users/%s/login' % (self.baseurl, self.user)
			r = requests.post(endpoint, data={'password':self.passwd})
			# print 'status: %s' % r.status_code
			resp_json = r.json()
			# print resp_json
			self._token = resp_json['session']
		return self._token

	def search (self, q='washington'):

		TOKEN = self.get_token()
		print 'TOKEN: %s' % TOKEN
		endpoint = '%s/repositories/2/search' % self.baseurl
		params = {
			'page': '1',
			# 'q':'title:"%s"' % q
			'q':'text:"%s"' % q
		}
		headers = {
			'X-ArchivesSpace-Session': TOKEN
		}
		r = requests.get(endpoint, headers=headers, params=params)
		print 'status: %s' % r.status_code
		resp_json = r.json()
		# print resp_json
		return SearchResponse(resp_json)

if __name__ == "__main__":
	proxy = AspaceProxy()
	response = proxy.search("warren washington")
	for result in response.results:
		print '\n'
		print result.title
		print '(%s)' % result.resource_type
		# print '\n\t', result.summary