"""
OSWS Response - expose the following based on xml service response

- numFound
- numResults
- start

- results - a list of OSWS Response Instances
"""
import os, sys
from UserList import UserList
from lxml import etree
from osws_result import OSWSResult

__author__ = 'ostwald'

class OSWSResponse(UserList):
	"""
	provides results via List API
	"""

	def __init__(self, xml):
		self.data = []
		xml = self._sanitize_xml(xml)
		self.root = etree.fromstring(xml)

		response_q = self.root.xpath('/OpenSkyWebService/Search/resultInfo/response')
		if len(response_q):
			# print 'RESPONSE_EL found'
			for node in response_q[0]:
				# print '-', node.tag
				setattr (self, node.tag, int(node.text))

		result_nodes = self.root.xpath('/OpenSkyWebService/Search/results/result')
		self.data = map (OSWSResult, map(lambda x:etree.tostring(x), result_nodes))

	def _sanitize_xml(self, raw):
		"""
		strip xml-dec
		"""
		if raw.startswith ("<?"):
			return '\n'.join(raw.split('\n')[1:])
		return raw

	def report (self):
		print '%d found' % response.numFound
		print '%d returned' % response.numResults
		print '%d start' % response.start

if __name__ == '__main__':
	path = 'xml_samples/osws-response-sample.xml'
	response = OSWSResponse(open (path, 'r').read())

	response.report()
	print 'response has %d results' % len(response)
