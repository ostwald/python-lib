"""
requests_client

leaves simple client alone as much as possible but uses
request to get the data
"""

import os, sys, urllib, urllib2, demjson, time, codecs
import ssl
from urlparse import urljoin
from JloXml import XmlRecord

import requests
from simple_client import SimpleClient, SimpleClientError

class RequestsClient (SimpleClient):
	
	def getData (self, params=None, opts=None):
		"""
		return data as a string
		raises SimpleClientError if request fails
		
		opts - are params that are passed via POST (??)
		"""
		try:
			resp = requests.get(self.baseUrl, params=params, data=opts)

			if resp.status_code == 200:
				return resp.text
				
			print '- status code: %d', resp.status_code
			raise Exception, 'Unhandled status_code: %d (%s)' % (resp.status_code, resp.reason)
		except Exception, errMsg:
			raise SimpleClientError (errMsg) 
