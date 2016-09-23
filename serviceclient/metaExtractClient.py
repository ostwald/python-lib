from ServiceClient import *

verbose = 1

baseUrl = 'http://ada.syr.edu:8080/mast/service.do'

paramsMap = {
	'method' : 'collect',
	'query' : 'http://www.sedl.org/scimath/pasopartners/pdfs/dinosaurs.pdf',
	'queryType' : 'URL'
}
	
# set the params_obj pased to ServiceRequest
params = paramsMap

def tester ():
	client = ServiceClient (baseUrl)
	request = client.setRequest (params)
	if verbose:
		print request.getUrl()
		print ""
		print request.report()
		
	if 1:
		response = client.getResponse()
		if response.hasError():
			print response.error
	
		if response.doc:
			print response.doc


if __name__ == "__main__":
	tester()
