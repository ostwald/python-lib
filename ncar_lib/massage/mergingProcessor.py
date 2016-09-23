"""
Merging Processor

- apply merging rules to all CHANGED records - merging data from the
  ncar_rec into the (working) lib_dc_rec

"""

import os, sys
import globals, utils
from JloXml import XmlRecord
from frameworks import LibraryDCRec
import baseProcessor
from recordIdListProcessor import ChangedRecordsProcessor
# import ncar_lib.conversion.mapping
from ncar_lib.conversion.mapping.mapper import Mapper

class MergingRecordProcessor (baseProcessor.RecordProcessor):
	preprocess = 1
	
	rule1_fields = [
		'library_dc:issue',
		'dc:source',
		'dc:date',
		'library_dc:date_digitized',
		'library_dc:libraryType',
		'dc:language',   # normalize at massage time
		'dc:relation',
		'dc:rights'
		]
		
	# fields to retain in merged record
	ncar_keep_fields = [
		'dc:title',
		'library_dc:altTitle',
		'dc:description'
	]
	
	def __init__ (self, path, preprocess=None):
		self.path = path
		baseProcessor.RecordProcessor.__init__ (self, path)
		
		# preprocessing
		if preprocess or self.preprocess:
			self.mapper = Mapper()
			self.doMerge()

	def doMerge (self):
		# merge selected fields from ncar_rec into lib_dc_rec
		for field in self.rule1_fields:
			self.applyRule1 (field)
			
		# self.normalizeLanguage()
			
		self.normalizeVocabs()
		self.mergeNcarFields()
		self.lib_dc_rec.orderFields()
		
	def applyRule1 (self, field):
		if not field in globals.library_dc_fields:
			msg = "applyRule1 got bogus field: '%s'" % field
			raise Exception, msg
		ncar_vals = self.ncar_rec.getFieldValues (field)
		working_vals = self.lib_dc_rec.getFieldValues (field)
		
		# sort lists so we can compare them
		ncar_vals.sort()
		working_vals.sort()
		
		if ncar_vals and (ncar_vals != working_vals):
			self.lib_dc_rec.setFieldValues (field, ncar_vals)
			
	def mergeNcarFields (self):
		for field in self.ncar_keep_fields:
			if not field in globals.library_dc_fields:
				msg = "mergeNcarFields got bogus field: '%s'" % field
				raise Exception, msg
			vals = self.ncar_rec.getFieldValues (field)
			self.lib_dc_rec.setFieldValues (field, vals)
			
	def normalizeLanguage (self):
		rec = self.lib_dc_rec
		field = "dc:language"
		vals = rec.getFieldValues (field)
		normalized = []
		for val in vals:
			if val == 'en': val = 'English'
			if not val in ["English", "Spanish"]:
				val = None
			if val:
				normalized.append (val)
		rec.setFieldValues (field, normalized)
			
	def normalizeVocabs (self):
		""" based on converter.Converter 
		
		If there is not a mapping, add nothing
		if the mapping is an identity mapping, add InstName
		else add all instDivs and instNames for that mapping
		
		Dups are removed during setFieldValues call
		"""
		
		instNameField = "library_dc:instName"
		instDivField = "library_dc:instDivision"
		
		ncarInstNames = self.ncar_rec.getFieldValues (instNameField)
		ncarInstDivs = self.ncar_rec.getFieldValues (instDivField)
		
		normInstNames = []
		normInstDivs = []
		
		for vocab in ncarInstNames + ncarInstDivs:
			# print "*** %s ***" % vocab
			if self.mapper.has_key (vocab):
				mapping = self.mapper.getMapping (vocab)
				# print mapping
				if mapping.isIdentity:
					# print "IDENTITY: " + vocab
					if not vocab in normInstNames:
						normInstNames.append (vocab)
					continue
				for instName in mapping.instNames:
					if not instName in normInstNames:
						normInstNames.append (instName)
				for instDiv in mapping.instDivs:
					if not instDiv in normInstDivs:
						normInstDivs.append (instDiv)	
			else:
				msg = "No mapping found for " + vocab
				raise Exception, msg
		self.lib_dc_rec.setFieldValues (instNameField, normInstNames)
		self.lib_dc_rec.setFieldValues (instDivField, normInstDivs)
		
			
class MergingRecordsProcessor (ChangedRecordsProcessor):
	rpClass = MergingRecordProcessor
	rpClass.preprocess = 1
		
def recordProcessorTester (recId):
	print "\n-------------------------------------"
	verbose = 1
	path = utils.getRecordPath (recId)
	rp = MergingRecordProcessor (path, 1)
	callback (rp)
	# print rp.lib_dc_rec

def writing_callback (rp):
	merged = rp.lib_dc_rec
	path = utils.getRecordPath (rp.recId, "merged")
	dir = os.path.dirname (path)
	if not os.path.exists (dir):
		os.makedirs (dir)
	merged.write (path=path)
	print "wrote %s" % rp.recId
	
def diff_callback (rp):
	# field_list = MergingRecordProcessor.rule1_fields
	# field_list = ['library_dc:instName', 'library_dc:instDivision']
	field_list = MergingRecordProcessor.ncar_keep_fields
	utils.library_dc_diff (rp.lib_dc_rec, rp.ncar_rec, "working", "ncar", field_list)
			
callback = writing_callback
	
if __name__ == "__main__":

	id = 'THESES-000-000-000-786'
	# recordProcessorTester (id)
	MergingRecordsProcessor(callback)

	

