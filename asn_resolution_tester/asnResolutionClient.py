"""
AsnResolutionClient
"""
import os, sys
from serviceclient import SimpleClient

class AsnResolutionClient (SimpleClient):
	verbose = False
	
	def __init__ (self):
		baseUrl = "http://localhost:8080/asn/service.do";
		SimpleClient.__init__(self, baseUrl)
		
	def getStandard (self, id):
		return self.getData ({
			'verb' : "GetStandard",
			'id' : id
		})
		
if __name__ == '__main__':
	client = AsnResolutionClient()
	client.getStandard("http://asn.jesandco.org/resources/S1000296")
