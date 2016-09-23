#!/usr/bin/env python

import sys, os, site
import string
from JloXml import XmlUtils
from catClient import CatClient

server = 'cnlp'

def getAuthors ():
	params = {
		"method": "getAuthors"
		}
	client = CatClient (server)
	request = client.setRequest (params)
	# print request.report()
	response = client.getResponse()
	if response.hasError():
		print response.error
	else:
		# print response.doc
		return parseResponse (response.doc)

def parseResponse (rec):
	rec.xpath_delimiter = "/"
	authorNodes = rec.selectNodes (rec.dom, "CATWebService/Authors/Author")
	print "%d authors found" % len (authorNodes)
	authors = []
	for node in authorNodes:
		authors.append (XmlUtils.getText (node))
	return authors
	
if __name__ == "__main__":

	authors = getAuthors()
	authors.sort()
	for author in authors:
		print author

	
					   

		

	
