# -*- coding: utf-8 -*-

import requests
from UserDict import UserDict
from model import SearchResponse, SearchResult, ArchivalObject, TopContainer
import json

# baseurl = "http://localhost:4567/repositories/2/search"
# r = requests.get(baseurl, auth=('admin','admin'))

class AspaceProxy:

	baseurl = 'http://localhost:4567'
	default_user = 'admin'
	default_passwd = 'admin'

	def __init__ (self, user=None, passwd=None):
		self.user = user or self.default_user
		self.passwd = passwd or self.default_passwd
		# print 'PROXY: %s - %s' % (self.user, self.passwd)
		self._token = None

	def get_token(self):
		if self._token is None:
			endpoint = '%s/users/%s/login' % (self.baseurl, self.user)
			r = requests.post(endpoint, data={'password':self.passwd})
			# print 'status: %s' % r.status_code
			resp_json = r.json()
			# print resp_json
			self._token = resp_json['session']
		# print 'TOKEN:', self._token
		return self._token

	def get_headers (self):
		return {
			'X-ArchivesSpace-Session': self.get_token()
		}

	def search (self, q='washington'):

		endpoint = '%s/repositories/2/search' % self.baseurl
		params = {
			'page': '1',
			# 'q':'title:"%s"' % q
			'q':'text:"%s"' % q
		}

		r = requests.get(endpoint, headers=self.get_headers(), params=params)
		# print 'status: %s' % r.status_code
		resp_json = r.json()
		# print resp_json
		return SearchResponse(resp_json)

	def get_archival_object(self, id):
		endpoint = '%s/repositories/2/archival_objects/%s' % (self.baseurl, id)

		r = requests.get(endpoint, headers=self.get_headers())
		# print 'GET status: %s' % r.status_code
		resp_json = r.json()
		# print json.dumps(resp_json, indent=4)
		return ArchivalObject(resp_json)

	def get_top_container (self, id):
		endpoint = '%s/repositories/2/top_containers/%s' % (self.baseurl, id)


		r = requests.get(endpoint, headers=self.get_headers())
		# print 'GET status: %s' % r.status_code
		resp_json = r.json()
		# print json.dumps(resp_json, indent=4)
		return TopContainer(resp_json)

	def update_archival_object(self, id, post_data):

		endpoint = '%s/repositories/2/archival_objects/%s' % (self.baseurl, id)

		r = requests.post(endpoint, headers=self.get_headers(), data=json.dumps(post_data))
		return r.json()

	def delete_top_container (self, id):
		endpoint = '%s/repositories/2/top_containers/%s' % (self.baseurl, id)
		r = requests.delete(endpoint, headers=self.get_headers())
		return r.json()

if __name__ == "__main__":
	proxy = AspaceProxy()
	# response = proxy.search("warren washington")
	# for result in response.results:
	# 	print '\n'
	# 	print result.title
	# 	print '(%s)' % result.resource_type
	# 	# print '\n\t', result.summary

