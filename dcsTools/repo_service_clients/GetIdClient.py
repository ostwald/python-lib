import sys, os, string
from JloXml import XmlRecord, XmlUtils
from globals import baseUrl
from dcsWebServiceClient import DCSWebServiceClient

class GetIdClient (DCSWebServiceClient):
	verb = "GetId"
	
	def __init__ (self, baseUrl, params):
		DCSWebServiceClient.__init__ (self, baseUrl, params)
		self.id = None
	
	def getResult (self):
		rec = self.post()
		return self.id
		
	def parseResponse (self, xml):
		rec = DCSWebServiceClient.parseResponse(self, xml)
		print rec
		self.id = rec.getTextAtPath ("DCSWebService:GetId:id")
		return rec
	
def getId (collection):
	params = {
		'collection' : collection
		}
	client = GetIdClient (baseUrl, params=params)
	client.post()
	return client.id

if __name__ == "__main__":
	collection = "1249326574904x" # msp2 records
	# tester(collection)
	print getId(collection)
