import sys, os, string
from ServiceClient import ServiceClient, ResponseError

class RecServiceClient (ServiceClient):
	pass

def tester ():

	ACORN = "acorn"
	LOCALHOST = "localhost"
	PREVIEW = "preview"

	server = LOCALHOST

	if server == PREVIEW:
		serverUrl = "http://preview.dpc.ucar.edu"
		collection = "ncc"
	if server == ACORN:
		## serverUrl = "http://acorn:8688"
		serverUrl = "http://acorn.dls.ucar.edu:8688"
		collection = "xncc"
	if server == LOCALHOST:
		serverUrl = "http://localhost"
		collection = "1201216476279"
	
	baseUrl = serverUrl + "/schemedit/services/recommend.do"


	print baseUrl

	params = {}
	params["recordXml"] = open ("ncs_item.xml",'r').read()

	params["collection"] = collection

	service = RecServiceClient (baseUrl, params=params, verb="RecommendResource")
	rec = service.post()
	print rec

		
if __name__ == "__main__":
	tester()
