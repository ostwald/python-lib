"""
put record - DCS PutRecordClient to write a metadata record to the repository

usage:
	
	def tester ():
		params = {
			'collection' : 'test',
			'xmlFormat' : 'osm',
			'id' : 'TESTO-000-000-000-019',
			'recordXml' : '<record .....>'
		}

		putRecord = PutRecordClient (params)
		print putRecord.id
	
"""
import sys, os, time
from dcsTools.repo_service_clients import DCSWebServiceClient, GetIdClient
from ncar_lib import OsmRecord

ttambora_putBaseUrl = 'http://ttambora.ucar.edu:10160/schemedit/services/dcsws1-0'

class PutRecordClient (DCSWebServiceClient):
	"""
	pass PutRecordClient data in a params dict. required dict keys are:
		- collection, id, xmlFormat, recordXml
		- NOTE: the id in the record must match the id sent!
	"""
	verb = "PutRecord"
	required_params = ['collection', 'id', 'xmlFormat', 'recordXml']
	default_baseUrl = ttambora_putBaseUrl
	
	def __init__ (self, params, baseUrl=None):
		tics = time.time()
		baseUrl = baseUrl or self.default_baseUrl
		DCSWebServiceClient.__init__ (self, baseUrl, params)
		self.collection = params['collection']
		self.result = self.post()
		self.id = self.result.getTextAtPath ('DCSWebService:PutRecord:id')
		self.elapsed = time.time() - tics
		
###############################
# Utilities		

def makeTimeString ():
	return time.strftime("%H:%M:%S, %m/%d/%Y ", time.localtime())
	
def makeOsmRecord (id=None):
	# template = "C:/tmp/osm_put_record_TEMPLATE.xml"
	template = "/home/ostwald/tmp/osm_put_record_TEMPLATE.xml"
	## return codecs.open(template, 'r', 'utf-8').read()
	rec = OsmRecord (path=template)
	rec.setId(id)
	rec.setTitle (makeTimeString())
	return rec.doc.toxml()

def makeAdnRecord (id=None):
	from JloXml import AdnRecord
	# template = "C:/tmp/osm_put_record_TEMPLATE.xml"
	template = "/home/ostwald/tmp/adn_put_record_TEMPLATE.xml"
	if not os.path.exists(template):
		raise Exception, 'ADN template does not exist at %s' % template
	## return codecs.open(template, 'r', 'utf-8').read()
	rec = AdnRecord (path=template)
	rec.setId(id)
	rec.setTitle (makeTimeString())
	return rec.doc.toxml()
	
#############################
# Testers
	
def osmTester ():
	"""
	writes to test library DCS
	"""
	collection = 'testosm'
	recId = 'TESTO-000-000-000-019'
	# recId = _getId(collection)
	params = {
		'collection' : collection,
		'xmlFormat' : 'osm',
		'id' : recId,
		'recordXml' : makeOsmRecord (recId)
	}
	if 1:
		putRecord = PutRecordClient (params)
		print putRecord.id
	else:
		print params['recordXml']
	
def adnTester ():
	putBaseUrl = 'http://dls-sanluis.dls.ucar.edu/dcs/services/dcsws1-0'
	collection = 'test_adn'
	recId = 'TEST-ADN-000-000-000-001'
	# recId = _getId(collection)
	params = {
		'collection' : collection,
		'xmlFormat' : 'adn',
		'id' : recId,
		'recordXml' : makeAdnRecord (recId),
		# 'dcsStatusNote' : 'hello world',
		'dcsStatus' : 'bogosity'
	}
	if 1:
		putRecord = PutRecordClient (params, putBaseUrl)
		print putRecord.id
	else:
		print params['recordXml']
		
if __name__ == '__main__':
	pass
	
