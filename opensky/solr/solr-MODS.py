"""
experiment with etree parser (vs requests)
"""

import os,sys,re,time,urllib
from xml.sax.saxutils import escape, unescape
from UserList import UserList
# import requests
from lxml import etree
from solr import FieldHelper, SolrRequest, SolrResult


class ModsResponseDoc (UserList):
	"""
	constructor takes the root node of the Response
	"""
	def __init__ (self, root):
		self.root = root
		self.data = []
		
		# m = self.dec_pat.match(xml)
		# if m:
			# #etree does not like the XML declaration
			# # xml = self.dec_pat.sub('', xml, 1)
			# xml = xml.replace(m.group(1),'', 1) # maybe more effecient?
		# 
		# print xml
		# print '-----------'
		# 
		# self.root = etree.fromstring(xml)

		self.data = map (SolrResult, self.root.xpath('/response/result/doc'))
		
class ModsRequest (SolrRequest):
	"""
	implements the etree parse URL method, where as
	SolrRequest uses the requests package. At one time
	I thought requests wasn't parsing the MODS field
	properly, but now I think they're both fine (its
	the indexed data that's bad)
	"""
	result_constructor = ModsResponseDoc
	
	default_paramsOFF = {
		'stream':'True' # 
	}
	
	def get (self):
		url = self.baseUrl + '?' + urllib.urlencode(self.params)
		print 'GET - url:', url
		root = etree.parse(url)
		# print root.xpath('result/doc/arr[@name="ds.MODS"]/str')[0].text
		return self.result_constructor (root)

def requestTester ():
	params = {
		#'q' : 'mods_extension_collectionKey_ms:technotes',
		#'q' : 'Creator_Lastname:"marlino"',
		'q' : 'Creator_Lastname:"ostwald"',
		# 'q' : 'Creator_Lastname:"trenberth"',
		'rows' : '1000',
		'wt': 'xml',
		'indent': 'true'
	}
	request = ModsRequest(params)
	print "\nrequest params"
	request.showParams()
	
	doc = request.responseDoc
	for i, result in enumerate(doc):
		print etree.tostring(result.root)
		
		try:
			# mods = unescape(result.getMods())
			mods = result.getMods().replace("&lt;", "<").replace('&gt;', '>')
			mods_root = etree.fromstring (mods)
			print ' %d - MODS parsed successfully' % i
		except Exception, msg:
			print ' %d - MODS parse ERROR: %s' % (i, msg)
		
		# print "MODS: %s" % mods


def lxmlParseTester():
	params = {
		'q' : 'mods_extension_collectionKey_ms:technotes',
		'q' : 'Creator_Lastname:"ostwald"',
		'rows' : '1',
		'wt': 'xml',
		'indent': 'true'
	}
	
	fl = FieldHelper().getSolrFieldList()
	params.update ({ 'fl' : ','.join(fl)})
	
	# params.update ({ 'fl' : 'ds.MODS'})
	params['fl'] = params['fl'] + ',' + 'ds.MODS'
	
	url = ModsRequest.baseUrl + '?' + urllib.urlencode(params)
	print 'url', url
	
	root = etree.parse(url)
	#print etree.tostring(root)
	
	mods = root.xpath('result/doc/arr[@name="ds.MODS"]/str')[0].text
	print mods
	

if __name__ == '__main__':
	requestTester ()
	#staticDocTester()
	# fieldHelperTester()
	# resultDocTester()
	# lxmlParseTester()


