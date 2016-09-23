"""
Converting processor
"""

import os, sys
import globals
from ncar_lib.lib_dc_message import utils
from webcatframework import WebcatRec

from convertingProcessor import RecordProcessor, CollectionProcessor, MetadataProcessor

from ncar_lib.lib_dc_message import unchangedRecordsProcessor
from ncar_lib.lib_dc_message.tally import TallyRunner, Tally
from converter import Converter
import mapping.mapper
from mapping.mapper import Mapper

	
class IdListProcessor (unchangedRecordsProcessor.IdListProcessor):
	rpClass = RecordProcessor

	
class VocabTally (TallyRunner):
	"""
	Tally the unique values for instName and instDivision from
	converted recs
	"""
	header = "Vocab Tally"
	verbose = False
	idListProcessor = IdListProcessor

	def __init__ (self):
		self.mapper = Mapper()
		self.instNameTally = Tally ('instName')
		self.instDivTally = Tally ('instDiv')
		self.run()
		self.report()
	
	def myRecordProcessor (self, rp):
		"""
		for each record processed, tallies the following fields
		"""
		rec = Converter (rp.webcat_rec).dest
		instNames = rec.getFieldValues ('library_dc:instName')
		self.instNameTally.tally (instNames)
		instDivs = rec.getFieldValues ('library_dc:instDivision')
		self.instDivTally.tally (instDivs)
		
	def run (self):
		# self.idListProcessor (self.myRecordProcessor)
		MetadataProcessor (self.myRecordProcessor)
		
	def report (self):
		print "unmapped instNames"
		for name in self.instNameTally.keys():
			if not self.mapper.getMapping (name):
				print "\t'%s'" % name

		print "unmapped instDivisions"
		for name in self.instDivTally.keys():
			if not self.mapper.getMapping (name):
				print "\t'%s'" % name
	
if __name__ == "__main__":
	# recordProcessorTester ("TECH-NOTE-000-000-000-357")
	VocabTally()


