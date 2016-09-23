#!/usr/bin/env python

import sys, os, site
import string
from JloXml import XmlUtils
from catClient import CatClient

server = "cnlp"

def getTopics ():
	params = {
		"method": "getTopics"
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
	topicNodes = rec.selectNodes (rec.dom, "CATWebService/Topics/Topic")
	print "%d topics found" % len (topicNodes)
	topics = []
	for node in topicNodes:
		topics.append (XmlUtils.getText (node))
	return topics
	

if __name__ == "__main__":

	for topic in getTopics():
		print topic

	
					   

		

	
