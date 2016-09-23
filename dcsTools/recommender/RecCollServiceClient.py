import sys, os, string
from ServiceClient import ServiceClient, ResponseError

class RecCollClient (ServiceClient):
	pass

def tester ():

	ACORN = "acorn"
	LOCALHOST = "localhost"
	PREVIEW = "preview"
	NCS = "ncs"

	context = "schemedit"

	server = LOCALHOST

	if server == PREVIEW:
		serverUrl = "http://preview.dpc.ucar.edu"
		collection = "ncr"
	if server == ACORN:
		## serverUrl = "http://acorn:8688"
		serverUrl = "http://acorn.dls.ucar.edu:8688"
		collection = "ncc"
	if server == LOCALHOST:
		serverUrl = "http://localhost"
		ncs_collect = "1209423223569"
		ncs_item = "1181941677361"
		collection = ncs_collect
	if server == NCS:
		serverUrl = "http://ncs.nsdl.org"
		context = "mgr"
		ncs_collect = "1201216476279"
		collection = ncs_collect
		
	## recpath = "C:/tmp/recommender/coll_by_oai.xml"
	recpath = "C:/tmp/recommender/coll_bad_xml.xml"
	## recpath = "C:/tmp/recommender/coll_by_application.xml"
		
	
	baseUrl = "%s/%s/services/recommend.do" % (serverUrl, context)


	print baseUrl

	params = {}
	params["recordXml"] = open (recpath,'r').read()

	params["collection"] = collection
## 	params["width"] = "125px"
## 	params["height"] = "73px"
## 	params["alttext"] = "a groovy collection"

	service = RecCollClient (baseUrl, params=params, verb="RecommendCollection")
	rec = service.post()
	print rec

		
if __name__ == "__main__":
	tester()
