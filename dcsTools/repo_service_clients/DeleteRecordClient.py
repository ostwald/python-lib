import sys, os, string, time
from JloXml import XmlRecord, XmlUtils
from globals import baseUrl
from dcsWebServiceClient import DCSWebServiceClient
from GetIdClient import getId
from dcsTools.xmlFormats import MSP2Record


class DeleteRecordClient (DCSWebServiceClient):
	verb = "DeleteRecord"
	


def putRecord ():
	pass

def makeTimeString ():
	return time.strftime("%H:%M:%S, %m/%d/%Y ", time.localtime())
		
	
if __name__ == "__main__":
	
	recId = 'MSP2-000-000-000-019'

	
	params = {
		'id' : recId,
		}
		
	client = DeleteRecordClient (baseUrl, params)
	rec = client.post()
	print rec
