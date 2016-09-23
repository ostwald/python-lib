"""
SEE ncar_lib/repository/put_record.py for a more robust version!!
"""

import sys, os, string, time
from JloXml import XmlRecord, XmlUtils
from globals import baseUrl
from dcsWebServiceClient import DCSWebServiceClient
from ncar_lib.osm import OsmRecord


class OpenSkyPutRecordClient (DCSWebServiceClient):
	verb = "PutRecord"
	


def putRecord (recordXml, collection, baseUrl):
	params = {
		'collection' : collection, # msp2 records
		'recordXml' : osmRec.doc.toxml()
		# 'dcsStatus' : 'Fooberry2',
		# 'dcsStatusNote' : 'I am a new status note'
		}
		
	client = OpenSkyPutRecordClient (baseUrl, params)
	rec = client.post()
	print rec

def makeTimeString ():
	return time.strftime("%H:%M:%S, %m/%d/%Y ", time.localtime())
		
if __name__ == "__main__":

	env = 'ttambora'
	
	if env == 'ttambora':
		collection = 'testosm'
		template = '/home/ostwald/tmp/openSkyPutRecordTemplates/osm-template-1.xml'
		baseUrl = 'http://ttambora.ucar.edu:10160/schemedit/services/opensky.do'
		recId = 'TESTO-000-000-000-031'
		
	elif env == 'sanluis':
		collection = 'osgc'
		template = '/home/ostwald/tmp/openSkyPutRecordTemplates/osm-template-1.xml'
		baseUrl = 'http://dls-sanluis.dls.ucar.edu/schemedit/services/opensky.do'
		recId = 'OSGC-000-000-001-901'
	
	osmRec = OsmRecord (path = template)

	osmRec.setId (recId)
	osmRec.setTitle (makeTimeString())
	
	putRecord (osmRec.doc.toxml(), collection, baseUrl)
		
	# print osmRec
	# sys.exit()
		

