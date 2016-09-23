"""
pdf reconciler -

creates new metadata record AND pdf file so that:
1 - pdf file is named after record id,
2 - url field in metadata is updated to reflect
	- record id
	- baseURL for pdfs
3 - normalize against controlled vocabs (TBP)

see wiki page at: https://wiki.ucar.edu//x/GAXYAQ
"""

import os, sys, string
import utils
from ncar_lib.lib import globals, webcatUtils
from JloXml import XmlRecord
from ncar_lib.lib.frameworks import LibraryDCRec
import baseProcessor
import callbackProcessor
from misc.titlecase import titlecase
import messagedRecordCallbacks
from ncar_lib.conversion.mapping.mapper import Mapper

class MassagingRecordProcessor (baseProcessor.RecordProcessor):
	
	preprocess = 0
	
	def __init__ (self, path, preprocess=0):
		self.path = path
		baseProcessor.RecordProcessor.__init__ (self, path)
		
		# preprocessing
		if preprocess or self.preprocess:
			self.mapper = Mapper()
			self.massage()
		
		# self.title = self.lib_dc_rec.getFieldValue ("dc:title")
		# self.description = self.lib_dc_rec.getDescription()
		# self.altTitle = self.lib_dc_rec.getAltTitle()
		# self.issue = self.lib_dc_rec.getFieldValue ("library_dc:issue");
		
	def massage (self):
		self.processDescription()
		
		self.normalizeField ("dc:language", self._language_normalizer)
		self.normalizeField ("dc:rights", self._rights_normalizer)
		self.normalizeField ("dc:subject", self._removeTrailingPeriod_normalizer)
		self.normalizeField ("dc:title", self._removeTrailingPeriod_normalizer)
		self.normalizeField ("library_dc:altTitle", self._removeTrailingPeriod_normalizer)
		self.normalizeField ("library_dc:URL", self._url_normalizer)
		self.normalizeField ("library_dc:libraryType", self._libraryType_normalizer)
		
		self.normalizeDateDigitized ()
		
		self.removeDupValues ("dc:description", "library_dc:altTitle")
		self.removeDupValues ("dc:description", "dc:title")
		self.removeDupValues ("library_dc:altTitle", "dc:title")
		
		self.toTitleCase("dc:title")
		self.toTitleCase("library_dc:altTitle")
		
		self.massageTitleAndAltTitle ()
		
		self.normalizeVocabs()
		
		for field in globals.library_dc_fields:
			# self.dedup (field)
			pass
		
		self.lib_dc_rec.orderFields()
		
	def normalizeDateDigitized (self):
		"""
		Ensure this field has a SINGLE VALUE
		FOR NOW (as of 10/27/08) take LATEST date
		"""

		field = "library_dc:date_digitized"
		rec = self.lib_dc_rec
		utils.validateField (field)
		vals = rec.getFieldValues (field)
		touse = -1
		if vals:
			for val in vals:
				year = int(val)
				touse = max (touse, year)
			rec.removeField (field)
			rec.setFieldValue (field, str(touse))
		
		
	def dedup (self, field):
		"""
		eliminate duplicate values for each field.
		THIS DOES NOT NEED TO BE USED
		"""
		utils.validateField (field)
		nodups = []
		rec = self.lib_dc_rec
		vals = rec.getFieldValues (field)
		for val in vals:
			if not val in nodups:
				nodups.append (val)
		rec.setFieldValues (field, nodups)
		
	def removeDupValues (self, field1, field2):
		"""
		remove values in field1 that are found in field2
		"""
		utils.validateField (field1)
		utils.validateField (field2)
		rec = self.lib_dc_rec
		vals1 = rec.getFieldValues (field1)
		vals2 = map (string.upper, rec.getFieldValues (field2))
		cleaned = []
		for val in vals1:
			if not val.upper() in vals2:
				cleaned.append (val)
		rec.setFieldValues (field1, cleaned)
		
	def _language_normalizer (self, val):
		"""
		replace "en" with 'English'
		remove values other than 'English' or 'Spanish'
		"""
		if val == 'en': val = 'English'
		if not val in ["English", "Spanish"]:
			val = None
		return val
	
	def _libraryType_normalizer (self, val):
		"""
		replace "en" with 'English'
		remove values other than 'English' or 'Spanish'
		"""
		if val == 'DOCUMENT': val = 'REPORT'
		return val
		
	def _rights_normalizer (self, val):
		if val and val.startswith ("All uses of library resources,"):
			val = "All uses of library resources, including the digitized "
			val = val + "collections, should be consistent with U.S. Copyright Law."
		return val
		
	def _removeTrailingPeriod_normalizer (self, val):
		"""
		remove trailing period
		"""
		if val and val[-1] == "." and not val.endswith ('...'):
			val = val[:-1].strip()
		return val
		
	def _url_normalizer (self, val):
		"""
		eventual form: http://nldr.library.ucar.edu/collections/${collection}/${recID}.pdf
		temporary form: http://nldr.library.ucar.edu/collections/${collection}/${accessionNum}.pdf
		"""
		rec = self.lib_dc_rec
		if not val:
			msg = "No url in %s" + self.recId
			raise Exception, msg
		return "http://nldr.library.ucar.edu/collections/%s/%s.pdf" % (self.collection, self.recId)
		
	def normalizeField (self, field, fn):
		"""
		function takes a single value and returns 
		the normalized value for this field
		"""
		rec = self.lib_dc_rec
		utils.validateField(field)
		vals = rec.getFieldValues (field)
		normalized = []
		for val in vals:
			normalized_val = fn(val)
			if normalized_val:
				normalized.append (normalized_val)
		rec.setFieldValues (field, normalized)
		
	def toTitleCase (self, field):
		"""
		put the field into title-case
		"""
		utils.validateField (field)
		values = self.lib_dc_rec.getFieldValues (field)
		newValues = []
		for val in values:
			newValues.append(titlecase (val.strip()))
		if newValues:
			self.lib_dc_rec.setFieldValues (field, newValues)
		
	def processDescription (self):
		"""
		technotes:
			pdf - remove "pdf" but keep rest of description
			jpg - remove entire description
		manuscripts:
			pdf - remove entire description
			jpg - remove entire description
		"""
		rec = self.lib_dc_rec
		desc_field = "dc:description"
		issue_field = "library_dc:issue"
		altTitle_field = "library_dc:altTitle"
		for field in [desc_field, issue_field, altTitle_field]:
			utils.validateField (field)
		vals = rec.getFieldValues (desc_field)
		new_descriptions = []
		for desc in vals:
			if desc is None:
				continue
			desc = desc.strip()
			if desc.lower().endswith ('pdf'):
				desc = desc[:-3]
				if self.collection == 'manuscripts':
					continue
				if self.collection == 'monographs' and 'ASR' in desc:
					self.lib_dc_rec.addFieldValue (altTitle_field, desc.strip());
					continue
			elif desc and desc.lower().endswith ('.jpg'):
				continue
			if desc:
				new_descriptions.append(desc)
		rec.setFieldValues (desc_field, new_descriptions)
		
	def massageTitleAndAltTitle (self):
		"""
		often, we need to swap title and alt title values. but the
		rules for this are different for each framework
		we don't process 'technotes' or 'theses'
		"""
		rec = self.lib_dc_rec
		title_field = 'dc:title'
		altTitle_field = 'library_dc:altTitle'
		utils.validateField (title_field)
		utils.validateField (altTitle_field)
		
		title_vals = rec.getFieldValues (title_field)
		altTitle_vals = rec.getFieldValues (altTitle_field)
		if title_vals and altTitle_vals:
			
			# manuscripts case
			if self.collection == "manuscripts" and len(title_vals) == 1 and len(altTitle_vals) == 1:
				title = title_vals[0]
				alt = altTitle_vals[0]
				if title.startswith (alt[:-1]): # some altTitles end in period, some don't
					rec.setFieldValue (title_field, alt)
					rec.setFieldValue (altTitle_field, title)
	
			if self.collection == "monographs":
				## is there a title element containing 'ASR'?
				ASRTitle = None
				for title in title_vals:
					if "ASR" in title:
						ASRTitle = title
						continue
				## is there an altTitle containing 'Annual Scientific Report'?
				ASRAltTitle = None
				pat = 'Annual Scientific Report'
				for altTitle in altTitle_vals:
					if pat in altTitle:
						ASRAltTitle = altTitle
						continue
				if ASRTitle and ASRAltTitle:
					rec.removeField (altTitle_field)
					rec.setFieldValue (title_field, ASRAltTitle)
					rec.setFieldValue (altTitle_field, ASRTitle)	
					
	def normalizeVocabs (self):
		""" based on converter.Converter 
		
		If there is not a mapping, add nothing
		if the mapping is an identity mapping, add InstName
		else add all instDivs and instNames for that mapping
		
		Dups are removed during setFieldValues call
		"""
		rec = self.lib_dc_rec
		instNameField = "library_dc:instName"
		instDivField = "library_dc:instDivision"
		
		ncarInstNames = rec.getFieldValues (instNameField)
		ncarInstDivs = rec.getFieldValues (instDivField)
		
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
				# raise Exception, msg
				print msg
		rec.setFieldValues (instNameField, normInstNames)
		rec.setFieldValues (instDivField, normInstDivs)
			
	def getPdfPath (self, pdfName=None):
		"""
		get path to the pdf file specified by "pdfName"
		- pdfName defaults to the basename of the library_dc URL
		"""
		if pdfName is None:
			url = self.lib_dc_rec.getUrl()
			if not url:
				return None
			pdfName = os.path.basename (os.path.dirname (url))
		collection = globals.collectionNameMap[self.collection]
		return os.path.join (globals.pdf, collection, self.accessionNum + ".pdf")
		
	def pdfExists (self, pdfName=None):
		"""
		determine if the pdf file specified by "pdfName" exists
		- pdfName defaults to the basename of the library_dc URL
		"""
		return os.path.exists (self.getPdfPath (pdfName))
		
	def write (self, metadata_set):
		path = webcatUtils.getRecordPath (self.recId, metadata_set)
		dir = os.path.dirname (path)
		if not os.path.exists (dir):
			os.makedirs (dir)
		self.lib_dc_rec.write (path=path)
		print "wrote %s (%s)" % (self.recId, metadata_set)

class CollectionProcessor(callbackProcessor.CallbackCollectionProcessor):
	"""
	calls process on each of the records in the collection
	"""
	rpClass = MassagingRecordProcessor
	rpClass.preprocess = 1
	

class MetadataProcessor (callbackProcessor.CallbackMetadataProcessor):
	cpClass = CollectionProcessor
			
def recordProcessorTester (recId):
	verbose = 0
	path = webcatUtils.getRecordPath (recId)
	
	rp = MassagingRecordProcessor (path, 0)
	print "\nBEFORE"
	callback (rp)
	
	rp = MassagingRecordProcessor (path, 1)
	print "\nAFTER"
	callback (rp)
	
def recordProcessorFinal (recId):
	verbose = 0
	path = webcatUtils.getRecordPath (recId)
	
	rp = MassagingRecordProcessor (path, 1)
	callback (rp)


def multiCollectionProcessor ():
	print globals.collectionNameMap.keys()
	for collection in globals.collectionNameMap.keys():
		if not collection in ['technotes', 'manuscripts']:
			CollectionProcessor (collection)
	
def writing_callback (rp):
	rp.write ("massaged")
	
def test_writer (rp):
	rp.write ("test")
			
# callback = messagedRecordCallbacks.multiFields
# callback = messagedRecordCallbacks.showTitleStuff
# callback = lambda rp: sys.stdout.write ("url: %s\n" % rp.lib_dc_rec.getFieldValue ("library_dc:URL"))

# callback = messagedRecordCallbacks.accessionNumberMapping
# callback = test_writer
callback = writing_callback
# callback = messagedRecordCallbacks.showVocabs
# callback = messagedRecordCallbacks.showWebcatDates
# callback = messagedRecordCallbacks.dates

if __name__ == "__main__":

	# CollectionProcessor ("monographs", callback)
	MetadataProcessor (callback)
	# recordProcessorTester ("TECH-NOTE-000-000-000-151")
	recordProcessorFinal ("TECH-NOTE-000-000-000-150")

	

