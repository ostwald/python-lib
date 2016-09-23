import os, sys, codecs
from simple_client import SimpleClient
from ServiceClient import ServiceClient
from urllib import urlencode
from JloXml import XmlRecord

class OaiClient:
	
	def __init__ (self, baseUrl):
		self.baseUrl = baseUrl
		
	def getRecord (self, identifier, xmlFormat):
		params = {
			'verb'  : 'GetRecord',
			'identifier' : identifier,
			'metadataPrefix' : xmlFormat
		 }
		data = self.getData(params)
		return XmlRecord(xml=data)
		
	def getData (self, params):
		query = urlencode (params)
		# print query
		url = '%s?%s' % (self.baseUrl, query)
		print '\n--------------------\n%s\n-------------------------\n' % url 
		client = SimpleClient(url)
		data = client.getData()
		print 'data chars: %d' % len(data)
		print 'data is type: %s' % type(data)
		return data

class MATDL (OaiClient):
	
	baseUrl = 'http://matdl.org/ncs/services/oai2-0'
	
	def __init__ (self):
		OaiClient.__init__ (self, self.baseUrl)
		
def matdlProbe():
	client = MATDL()
	xmlFormt = 'ncs_data'
	rec = client.getRecord ('MATDL-000-000-000-354', 'nsdl_dc')
	print rec
	
def ncsProbe():
	baseUrl = 'http://ncs.nsdl.org/mgr/services/oai2-0'
	client = OaiClient (baseUrl)
	xmlFormt = 'ncs_data'
	rec = client.getRecord ('MATH-PATH-000-000-000-558', xmlFormt)
	print rec
	
def localProbe():
	baseUrl = 'http://dls-sanluis.dls.ucar.edu/schemedit/services/oai2-0'
	client = OaiClient (baseUrl)
	badRecord = 'MP-000-000-000-007'
	goodRecord = 'MP-000-000-000-008'
	rec = client.getRecord (badRecord, 'math_path')
	# print rec
	
def matdlListRecords():
	client = MATDL()
	params = {
		'verb' : 'ListRecords',
		'metadataPrefix' : 'nsdl_dc',
		'set' : '1314817648524'
		}
	data = client.getData (params)
	
	
if __name__ == '__main__':
	localProbe()
	# ncsProbe()
	# matdlProbe()
	# matdlListRecords()
