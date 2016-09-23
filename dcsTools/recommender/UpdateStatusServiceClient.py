import sys, os, string
from ServiceClient import ServiceClient, ResponseError

class UpdateServiceClient (ServiceClient):
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

	if server == ACORN:
		## serverUrl = "http://acorn:8688"
		serverUrl = "http://acorn.dls.ucar.edu:8688"

	if server == LOCALHOST:
		serverUrl = "http://localhost"


		
	
	baseUrl = "%s/%s/services/dcsws1-0.do" % (serverUrl, context)


	print baseUrl

	params = {
		'id' : 'ANOTHER-000-000-000-001',
		# 'id' : 'MSP2-B-000-000-000-001',
		'dcsStatus' : 'mystatus',
		'dcsStatusNote' : 'celtics in 7',
		'dcsStatusEditor' : 'ostwald'
	}

	service = UpdateServiceClient (baseUrl, params=params, verb="UpdateStatus")
	rec = service.post()
	print rec

		
if __name__ == "__main__":
	tester()
