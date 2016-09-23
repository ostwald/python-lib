"""
a status aware query is one that specifies a set of dcs_status values
and expects only results that match one of the status values

The StatusAwareClient is used to test URLs against a DDS. We want to
- restrict by status
- require dcsisValid
- include the record's status and validity in the webservice response

"""
import os, sys, re
from repo import RepositorySearcher

class StatusAwareClient (RepositorySearcher):

	default_baseUrl = 'http://localhost:8070/curricula/services/ddsws1-1'

	def __init__ (self, status=None, collection=None, xmlFormat=None, baseUrl=None):
		if status is None:
			status = []
		elif type(status) == type(''):
			status = [status]
		elif type(status) != type([]):
			raise Exception, 'unknown status type: %s' % type(status)
		self.status = status

		RepositorySearcher.__init__(self, collection, xmlFormat, baseUrl)

	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"q":'dcsisValid:true',
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky": collection,
			"dcsStatus": self.status,
			"storedContent":['dcsstatusLabel', 'dcsisValid']
			}

if __name__ == '__main__':
	status = ['Done', 'In Progress']
	searcher = StatusAwareClient(status=status, xmlFormat='concepts')
	print '%d concepts found' % len(searcher)
	print searcher.service_client.request.getUrl()
		
		
