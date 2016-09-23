import sys, os, site
import string

from urls import *
import CATGlobals
from suggesterClient import SuggesterClient, createUrlInstance
from asnUriService.asnUriResolver import getDocInfo

def getSuggestions (state):
	
	# from 
	
	baseUrl = CATGlobals.baseUrl
	params = {
		"method": "suggestStandards",
		"endGrade": "12",
		"query": "http://ga.water.usgs.gov/edu/earthrivers.html",
		"topic": "Science",
		"startGrade": "1",
		"maxResults": "1",
		"author": state
		}
	url = createUrlInstance (baseUrl, params)
	client = SuggesterClient (baseUrl)
	request = client.setRequest (params)
	# print request.report()
	response = client.getResponse()
	if response.hasError():
		print response.error
	else:
		# print response.doc
		id = client.getIds()[0]
		if id:
			print "\n%s - %s" % (state, id)
			getDocInfo (id)
		# print "%s - %s" % (state, id)
	
if __name__ == "__main__":
	authors = [
		"Colorado", 
		"National Science Education Standards (NSES)",
		"Florida",		
		"New York",
		"Massachusetts"
		]
	
	
	for author in authors:
		getSuggestions(author)

