"""
Converting processor
"""

import os, sys
import globals
from ncar_lib.lib_dc_message import utils
from ncar_lib.lib_dc_message.frameworks import LibraryDCRec
from webcatframework import WebcatRec
from ncar_lib.lib_dc_message import callbackProcessor, unchangedRecordsProcessor
from converter import Converter

class RecordProcessor (callbackProcessor.RecordProcessor):
	preprocess = 0

	def _getWebcatRec (self, recId):
		"""
		get webcat record with id=recId
		"""
		path = utils.getRecordPath (recId, "webcat")
		return WebcatRec (path=path)
	
class CollectionProcessor (callbackProcessor.CollectionProcessor):
	rpClass = RecordProcessor
	
class MetadataProcessor (callbackProcessor.MetadataProcessor):
	cpClass = CollectionProcessor
	
class IdListProcessor (unchangedRecordsProcessor.IdListProcessor):
	rpClass = RecordProcessor

	
def recordProcessorTester (id):
	rp = RecordProcessor (utils.getRecordPath (id))
	callback (rp)

def batchProcessor ():
	"""
	test the converted on all the unchanged records. we should see differences
	in multivalue fields ...
	"""
	# IdListProcessor (callback)
	MetadataProcessor (callback)
	
def diff_callback (rp):
	c = Converter(rp.webcat_rec)
	## field_list = ['library_dc:instName', 'library_dc:instDivision']
	# field_list = ['dc:description']
	# field_list = ['dc:title', 'library_dc:altTitle' ]
	# field_list = ['dc:description', 'dc:title', 'library_dc:altTitle' ]
	# field_list = ['library_dc:dateCataloged' ]
		
	if utils.rec_cmp (rp.lib_dc_rec, c.dest):
		utils.library_dc_diff (rp.lib_dc_rec, c.dest, "old", "new", makeFieldList())
		# utils.conversion_diff (rp, c.dest)	
	
def writing_callback (rp):
	converted = Converter(rp.webcat_rec).dest
	path = utils.getRecordPath (rp.recId, "converted")
	dir = os.path.dirname (path)
	if not os.path.exists (dir):
		os.makedirs (dir)
	converted.write (path=path)
	print "wrote %s" % rp.recId
		
callback = writing_callback
		
def makeFieldList():
	return [
	#'library_dc:recordID',
	'library_dc:dateCataloged',
	#'library_dc:URL',
	'library_dc:issue',
	'dc:source',
	'dc:title',
	'library_dc:altTitle',
	#'dc:creator',
	#'dc:contributor',
	'dc:description',
	'dc:date',
	'library_dc:date_digitized',
	#'dc:subject',
	#'library_dc:instName',  # vocab 
	#'library_dc:instDivision', # vocab
	'library_dc:libraryType', #vocab
	'dc:type',
	'dc:format',
	'dc:identifier',
	'dc:language',
	'dc:relation',
	'dc:coverage',
	'dc:rights',
	'dc:publisher'
	]
		
def getDestPath (rp):
	return 
		
if __name__ == "__main__":
	# recordProcessorTester ("TECH-NOTE-000-000-000-153")
	batchProcessor ()


