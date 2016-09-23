"""
Tool for working out the different domains that work with different authors in asn service
"""

import sys, os, site, re, urllib
import string
import time
import exceptions

from UserDict import UserDict
from serviceclient import SimpleClient, SimpleClientError
import verifier_data

class ASNVerifier:
	
	def __init__ (self, url):
		self.url = url
		pat = re.compile ("http://(.*)/resources/([SD0-9]*)(.*)")
		m = pat.match (url)
		if not m:
			raise Exception, 'could not parse provided url: "%s"' % url
		else:
			
			self.domain = m.group(1)
			self.id = m.group(2)
			self.suffix = m.group(3)
			
		# print 'circle - url: http://%s/resources/%s%s' % (self.domain, self.id, self.suffix)
			
	def verify (self):
		valid = False
		try:
			client = SimpleClient(self.url)
			client.getData()
			responseCode = client.responseCode
			# print 'responseCode: ', client.responseCode
			if responseCode == 200:
				valid = True
		except Exception, msg:
			# print msg
			pass # valid remains False

			
		# print '%s - %s' % (valid, self.url)
		
		return valid

def tester ():
	# http://asn.jesandco.org/resources/D2454348.xml
	domain = 'asn.jesandco.org'
	id = 'D2454348'
	suffix = "" # '.xml'
	url = "http://%s/resources/%s%s" % (domain, id, suffix)
	# print 'url:', url
	verifier = ASNVerifier (url)
	verifier.verify()
	
class Spec (UserDict):
	def __init__ (self, data={}):
		self.data = data
		for attr in self.data.keys():
			setattr(self, attr, self.data[attr])
			
	def toUrl (self):
		return "http://%s/resources/%s%s" % (self.domain, self.id, self.suffix)

class SpecObj:
	def __init__ (self, name, domain, id, suffix):
		self.name = name
		self.domain = domain
		self.id = id
		self.suffix = suffix
		
	def toUrl (self):
		return "http://%s/resources/%s%s" % (self.domain, self.id, self.suffix)

def verifyAuthors(idmap, suffix=''):
	print "verifying Authors"
	print "  suffix: " + suffix
	keys = idmap.keys()
	keys.sort()
	for author in keys:
		verifyId (idmap, author, suffix)

def verifyId (idmap, author, suffix=""):
	print '\nverifying %s' % author
	id = idmap[author]
	for domain in verifier_data.domains:
		spec = SpecObj(author, domain, id, suffix)
		url = spec.toUrl()
		verifier = ASNVerifier (url)
		found = verifier.verify()
		print '- %s - %s - %s' % (found, spec.domain, url)
		
		
	
def verifyFromSpec (spec_data):
	url = Spec(spec_data).toUrl()
	verifier = ASNVerifier (url)
	verifier.verify()
	
	
if __name__ == '__main__':
	
	# verifyId ('Alaska')
	# idmap = verifier_data.idmap_stds
	idmap = verifier_data.idmap_docs
	suffix = '_full.xml' #'# '.xml'
	verifyAuthors (idmap, suffix)
		
