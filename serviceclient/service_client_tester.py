from ServiceClient import *

verbose = 0

baseUrl = "http://cat.nsdl.org:8280/casaa/service.do"

## different forms of params to test ServiceRequest ...
paramsMap = {
	"username": "dlese",
	"password": "p",
	"method": "suggestStandards",
	"endGrade": "12",
	"query": "http://ga.water.usgs.gov/edu/earthrivers.html",
	"topic": ["Science", "Math"],
	"startGrade": "1",
	"maxResults": "2",
	"author": "National Science Education Standards (NSES)"
	}
	
paramsList = [ ("foo", "1"), ("farb", "2"), ("foo", "3") ]
paramsSeq = ( ("foo", "1"), ("farb", "2"), ("foo", "3") )

paramsStr = "foo=1&foo=2&farb=barf"
	
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
