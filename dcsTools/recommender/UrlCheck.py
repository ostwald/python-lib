import sys, os, string
from ServiceClient import ServiceClient, ResponseError

class UrlCheckClient (ServiceClient):
	pass

def tester ():

	ACORN = "acorn"
	LOCALHOST = "localhost"
	PREVIEW = "preview"

	server = PREVIEW
	collection = ""
	url = ""

	if server == PREVIEW:
		serverUrl = "http://preview.dpc.ucar.edu"
		collection = ["ncr", "ncc"]
		url = "http://www.mydomain.org"
		
	if server == ACORN:
		## serverUrl = "http://acorn:8688"
		serverUrl = "http://acorn.dls.ucar.edu:8688"
		collection = "ncr"
		url = ""
		
	if server == LOCALHOST:
		serverUrl = "http://localhost"
		##collection = ("1181941677361", "1176742803770")
		collection = "1181941677361"
		url = "http://www.techquila.com/topicmaps/xmlschema/"
	
	baseUrl = serverUrl + "/schemedit/services/dcsws1-0.do"


	print baseUrl

	params = {}

	params["collection"] = collection
	params["url"] = url

	service = UrlCheckClient (baseUrl, params=params, verb="UrlCheck")
	rec = service.post()
	print rec

		
if __name__ == "__main__":
	tester()
