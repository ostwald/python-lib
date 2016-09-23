"""
SEE ncar_lib/repository/put_record.py for a more robust version!!
"""

import sys, os, string, time
from JloXml import XmlRecord, XmlUtils
from globals import baseUrl
from dcsWebServiceClient import DCSWebServiceClient
from GetIdClient import getId
from dcsTools.xmlFormats import MSP2Record


class PutRecordClient (DCSWebServiceClient):
	verb = "PutRecord"
	


def putRecord ():
	pass

def makeTimeString ():
	return time.strftime("%H:%M:%S, %m/%d/%Y ", time.localtime())
		
	
if __name__ == "__main__":
	
	collection = "1249326574904"  ## MSP2 records
	template = "xml/msp2-template-record.xml"

	msp2rec = MSP2Record (path = template)
	if 1:
		recId = getId(collection)
	else:
		recId = 'MSP2-000-000-000-019'
		msp2rec.setTitle (makeTimeString())
	msp2rec.setId (recId)
	# print msp2rec
	
	params = {
		'xmlFormat' : 'msp2',
		'collection' : collection, # msp2 records
		'id' : recId,
		'recordXml' : msp2rec.doc.toxml(),
		# 'dcsStatus' : 'Fooberry2',
		# 'dcsStatusNote' : 'I am a new status note'
		}
		
	client = PutRecordClient (baseUrl, params)
	rec = client.post()
	print rec
