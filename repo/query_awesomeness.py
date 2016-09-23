import os, sys
from repo.dds_client import DDSClient
from repo.search_result import SearchResult

baseUrl = 'http://nldr.library.ucar.edu/schemedit/services/ddsws1-1'

def makequery (term):
	# base = "(title(xkcd)^10 OR titlestems:(xkcd)^5)"
	production_base = "(xkcd OR xkcd) OR ((title:(xkcd)^15 OR title:(xkcd)^10 OR titlestems:(xkcd)^5) OR titlestems:(xkcd)^3)"
	test_base = "xkcd OR ((title:(xkcd)^10 OR titlestems:(xkcd)^5) OR titlestems:(xkcd)^3)"
	
	return production_base.replace('xkcd', term)

def showParams(params):
	for key in params.keys():
		print '- %s: %s' % (key, params[key])

def getParams (term=None):

	params = {
	  "q": "(xkcd OR xkcd) OR ((title:(xkcd)^15 OR title(xkcd)^10 OR titlestems:(xkcd)^5) OR titlestems:(xkcd)^3)", #159
	  # "q": "(xkcd OR xkcd) OR ((title:(xkcd)^15 OR title(xkcd)^10 OR titlestems:(xkcd)^5))", # 159
	  # "q": "(xkcd OR xkcd) OR ((title:(xkcd)^15 OR title(xkcd)^10))", # 0
	  # "q": "(xkcd OR xkcd) OR ((title:(xkcd)^15 OR titlestems:(xkcd)^5))", # 0
	  # "q": "((title:(xkcd)^15 OR title(xkcd)^10 OR titlestems:(xkcd)^5))", # 159
	  # "q": "(title(xkcd)^10 OR titlestems:(xkcd)^5)", # 159
	  # "q": "(titlestems:(xkcd)^5)", #0
	  # "q": "(title(xkcd)^10)", # 0
	  "s": "0",
	  "verb": "Search",
	  "n": "1000",
	}
	
	if term:
		params['q'] = makequery(term)
	return params

def getNumResults(term=None):
		
	client = DDSClient(baseUrl)
	params = getParams(term)
	params['n'] = 1
	showParams(params)
	response = client.getResponseDoc (params)
	if response is None:
		print "response is None"
		return 0
	else:
		return int(response.getTextAtPath ('DDSWebService:Search:resultInfo:totalNumResults'))


def getResults(term=None):
	
	client = DDSClient(baseUrl)
	params = getParams(term)
	showParams(params)
	response = client.getResponseDoc (params)
	if response is None:
		print "response is None"
		result_nodes = []
	else:
		result_nodes = response.selectNodes (response.dom, 'DDSWebService:Search:results:record')
	results = map (SearchResult, result_nodes)
	
	# print response
	print '%d results' % len (results)
	
if __name__ == '__main__':
	term = 'adrd'
	if len(sys.argv) > 1:
		term = sys.argv[1]
	num = getNumResults(term)
	print '%d results found for "%s"' % (num, term)
	
