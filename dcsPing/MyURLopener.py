import sys, os, site
import string
import urllib
from urllib import *
from urllib import toBytes
import socket


class MyURLopener (urllib.FancyURLopener):

	def __init__ (self, username, password):
		urllib.FancyURLopener.__init__(self)
		self.maxtries = 3
		self.username = username
		self.password = password
		self.tempcache = None
	
	def prompt_user_passwd (self, host, realm):
		return self.username, self.password

	def open(self, fullurl, data=None):

		if self.tries > self.maxtries:
			# print 'bailing after %d tries (check username and password)' % (self.tries -1)
			self.tries = 0
			raise IOError, ('too many tries - bailing')
		
		fullurl = unwrap(toBytes(fullurl))
		if self.tempcache and fullurl in self.tempcache:
			filename, headers = self.tempcache[fullurl]
			fp = open(filename, 'rb')
			return addinfourl(fp, headers, fullurl)
		urltype, url = splittype(fullurl)
		if not urltype:
			urltype = 'file'
		if urltype in self.proxies:
			proxy = self.proxies[urltype]
			urltype, proxyhost = splittype(proxy)
			host, selector = splithost(proxyhost)
			url = (host, fullurl) # Signal special case to open_*()
		else:
			proxy = None
		name = 'open_' + urltype
		self.type = urltype
		if '-' in name:
			# replace - with _
			name = '_'.join(name.split('-'))
		if not hasattr(self, name):
			if proxy:
				return self.open_unknown_proxy(proxy, fullurl, data)
			else:
				return self.open_unknown(fullurl, data)
		try:
			if data is None:
				return getattr(self, name)(url)
			else:
				return getattr(self, name)(url, data)
		except socket.error, msg:
			raise IOError, ('socket error', msg), sys.exc_info()[2]

	def http_error_default(self, url, fp, errcode, errmsg, headers):
		"""Default error handler: close the connection and raise IOError."""
		void = fp.read()
		fp.close()
		raise IOError, ('http error', errcode, errmsg, headers)

