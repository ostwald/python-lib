__author__ = 'ostwald'
"""
http://cypressvm.dls.ucar.edu:8788/osws/search/v1?q=upid:"2775"&start=0&rows=10&output=json&sort=date desc&facet=true
"""

import os, sys
from serviceclient import RequestsClient
from lxml import etree
from mods_model import ModsRecord
from osws_result import OSWSResult
from osws_response import OSWSResponse


class OSWSClient (RequestsClient):

	verbose = 0
	default_baseUrl = 'http://cypressvm.dls.ucar.edu:8788/osws/search/v1'

	def __init__ (self, baseUrl=None):
		baseUrl = baseUrl or self.default_baseUrl
		RequestsClient.__init__(self, baseUrl)


	def getResults(self, params):
		try:
			data = self.getData(params=params)
		except:
			print 'ERROR: %s' % sys.exc_info()[1]
			return

		self.response = OSWSResponse (data)
		return self.response

		# # print 'DATA: %s' % data
		# response = XmlRecord(xml=data)
		#
		# error = response.selectNodes(response.dom, 'OpenSkyWebService:error')
		# if error:
		# 	raise Exception, response.getTextAtPath('OpenSkyWebService:error')
		#
		# # Here's where we could ceck for error and raise Exception ..
		#
		# results_path = 'OpenSkyWebService:Search:results:result'
		# results_els = response.selectNodes(response.dom, results_path)
		# print '%d result elements found' % len(results_els)
		#
		# def getResult(node):
		# 	return ModsRecord(xml=node.toxml())
		#
		# return map(OSWSResult, results_els)


if __name__ == '__main__':

	upids = [
		2275,
		24793
	]

	query = ' OR '.join(map (lambda x:'upid:'+str(x), upids))
	query = '(%s) AND genre:"article"' % query

	# query = 'upid:2775'

	params = {
		'start' : '0',
		'rows' : '1000',
		'output' : 'xml',
		'q' : query
	}

	client = OSWSClient ()
	results = client.getResults(params)


	print '%d results instantiated' % len(results)

	tester = results[0]
	# print tester
	tester.report()
	print tester.toCsv()