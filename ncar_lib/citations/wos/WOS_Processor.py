"""
WOS to XML

read in a WOS spreadsheet and produce xml records for each line.
"""
import os, re
from ncar_lib.citations import Citation, GenericProcessor
from WOS_reader import WOSXlsReader

class WOSProcessor (GenericProcessor):

	id_prefix="WOS"
	
	def __init__ (self, path, startid=None, limit=None, write=1):
		"""
		- path - the data file to be processed
		"""
		GenericProcessor.__init__ (self, startid, limit, write)
		
		self.path = path
		self.records = WOSXlsReader (path)
		self.processRecords()
		
	def makeDataDict (self, rec):
		"""
		make the data structure from which the Citation record will be built
		"""
		data = {}
		data['title'] = rec._getTitle()
		data['year'] = rec._getYear()
		data['pubname'] = rec._getPubName()
		data['editor'] = rec._getEditors()
		data['volume'] = rec._getVolume()
		data['pages'] = rec._getPages()
		data['pubstatus'] = rec._getPubStatus()
		data['statusdate'] = rec._getPubDate()
		data['type'] = rec._getPubType()
		data['authors'] = rec._getAuthors()
		data['wos_id'] = rec['wos_id']
		return data
	
if __name__ == '__main__':
	# datafile = "WOS_4501-5000.txt"
	datafile = "WOS_data_files/WOS_11001-11500.txt"
	# foo = WOSProcessor (datafile, 7695)
	WOSProcessor.destDir = "WOS_metadata_tmp"
	foo = WOSProcessor (datafile, limit=5, write=0)
