"""
Generate report for:
	records that have status not reflected in date type

ids of these records are listed in ids_of_status_challenged_records.txt
	
"""
import sys, os
from ncar_lib.repository import GetRecord
from UserList import UserList

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

def getIds():
	path = 'ids_of_status_challenged_records.txt'
	return filter (None, map (lambda x:x.strip(), open(path, 'r').read().split('\n')))
	
class Reporter(UserList):
	
	report_freq = 100
	
	def __init__ (self):
		self.data = []
		self.ids = getIds()
		self.processIds()
		
	def getRecord(self, recId):
		return GetRecord(recId).response
	
	def processIds (self):
		num_recs = len(self.ids)
		for i, recId in enumerate(self.ids):
			response = self.getRecord(recId)
			osmStatus = response.payload.getStatus()
			dcsStatus = response.dcsstatus
			# print '%s - %s - %s' % (recId, osmStatus, dcsStatus)
			self.append ('\t'.join ([recId, osmStatus, dcsStatus]))
			if i and i % self.report_freq == 0:
				print '%d/%d' % (i, num_recs)
			
	def writeAsTabDelimited (self, path=None):
		if path is None:
			path = "STATUS_REPORT.txt"
		header = '\t'.join (['recId', 'osmStatus', 'dcsStatus'])
		self.data.insert(0, header)
		fp = open(path, 'w')
		fp.write ('\n'.join(self.data))
		fp.close()
		print 'wrote to', path
		
	
if __name__ == '__main__':

	reporter = Reporter()
	reporter.writeAsTabDelimited()
