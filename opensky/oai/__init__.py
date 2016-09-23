import sys, requests, re, logging
from lxml import etree

baseUrl = 'http://osstage2.ucar.edu:8080/fedora/oai'
verb = 'ListIdentifiers'
resumptionToken = ''
metadataPrefix = 'oai_dc'

class ParsedResult:
	
	def __init__ (self, doc):
		print 'parse_response'
		ns = {'n' : 'http://www.openarchives.org/OAI/2.0/'}
		self.ids = doc.xpath('//n:header/n:identifier/text()', namespaces=ns)
	
		# if len (self.ids):
			# print '%d found' % len(self.ids)
			# print '\n'.join (self.ids)
		# else:
			# print "nothing found"
			
		resumptionToken = doc.xpath('//n:ListIdentifiers/n:resumptionToken/text()', namespaces=ns)
		self.resumptionToken = len(resumptionToken) and resumptionToken[0] or None
		print 'resumptionToken: %s' % self.resumptionToken      

def getAllIds ():
	all_ids = []
	max = 500
	resp = get_response()
	result = ParsedResult(resp)
	all_ids = all_ids + result.ids
	print 'added %d' % (len (result.ids))
	while result.resumptionToken:
		try:
			resp = get_response(resumptionToken=result.resumptionToken)
			result = ParsedResult(resp)
		except Exception, msg:
			print "ERROR: %s" % msg
			break
		all_ids = all_ids + result.ids
		print 'added %d' % (len (result.ids))
		if len(result.ids) > max:
			break
	return all_ids

def get_response (resumptionToken=None):
	url = "%s?verb=ListIdentifiers" % baseUrl
	if resumptionToken:
		url = "%s&resumptionToken=%s" % (url, resumptionToken)
	else:
		url = "%s&metadataPrefix=%s" % (url, metadataPrefix)
	print url
	r = requests.get(url)
	
	try:
		parser = etree.XMLParser(recover=True,encoding='utf-8')
		document = etree.fromstring(r.text.encode('utf-8'),parser)
		
		# print etree.tostring(document)[-100:]
		return document
		
		# ns = {'m': 'http://www.loc.gov/mods/v3' }
		# 
		# ark  = document.xpath('//m:identifier[@type="ark"]/text()', namespaces=ns)
		# if len(ark) > 1:  
		# pass # there is a problem here - claim it
		# 
		# return ''.join(ark)
	except Exception, msg:
		print 'TROUBLE: %s' % msg
		
def parse_response(doc):
	"""
	return results, resumption_token
	"""

def tester():
	resp = get_response()
	result = ParsedResult(resp)
	
if __name__ == '__main__':

	ids = getAllIds ()
	print '%d ids found' % len(ids)
	print '\n'.join (ids)
