"""
Vocab Usage Reporter

"""
import os, sys, codecs, time
from vocab_data import collection_params
from faceted_searcher import getFacetedField
from ncar_lib.repository.search_summary import FacetedField, Facet
from ncar_lib.osm.vocabs import VocabXSD
from serviceclient import SimpleClient
from vocab_usage_searcher import VocabUsageSearcher

term_schema = ['term', 'count', 'first_date', 'last_date', 'inSchema']

class TermUsageRecord:
	"""
	represent the rows of the report table
	"""
	def __init__ (self, term, count, reporter):
		# print "type(term): %s" % type(term)
		self.reporter = reporter
		self.term = term
		self.count = count
		self.first_date = ''
		self.last_date = ''
		self.inSchema = ''
		
	def set_dates (self):
		"""
		if this term is not in xsd:
			search for this term in repository
			pluck the recordDates from the results
			if recordsDates:
				self.first_date is the first, and
				self.last_date is the last
		"""
		self.last_date = self.first_date = 'Not Found'
		# print "searching for '%s'" % self.term
		try:
			VocabUsageSearcher.verbose = 0
			searcher = VocabUsageSearcher (self.term, self.reporter.vocabXpath)
			print "%d results found for '%s'" % (len (searcher), searcher.term)

			recordCreatedDates = map (lambda x:x.payload.getRecordDate(), searcher.data)
			recordCreatedDates.sort()
			
			# for recordCreated in recordCreatedDates:
				# print recordCreated
				
			if len(recordCreatedDates) > 0:
				self.first_date = recordCreatedDates[0]
				self.last_date = recordCreatedDates[-1]
				
		except:
			print "error processing %s" % self.term
			self.last_date = self.first_date = "ERROR"

		
	def toTabDelimited (self):
		values = []
		for field in term_schema:
			value = getattr(self, field)
			value = unicode (value)
			values.append(value)
		return '\t'.join (values)

class VocabUsageReporter:
	"""
	builds a tabdelimted report listing all terms defined by the vocab and their occurrences in the metadata.
	
	the occurrence count is obtained using the facet functionality of DDS Search.
	"""
	default_threshold = 1
	
	def __init__ (self, vocabUrl, typeName, vocabXpath, threshold=None):
		"""
		vocabUrl - points to the schema file that defines terms for this vocab
		typeName - a human readable name (e.g., 'eventNameType')
		vocabXpath - the xpath for this term in a metadata record
		showZeroOccurs - flag that determines whether vocab terms with 0 occurrances will be reported (default is False)
		"""
		self.vocabUrl = vocabUrl
		self.typeName = typeName
		self.vocabXpath = vocabXpath
	
		self.computeFacetList(threshold)
		
	def computeFacetList (self, threshold):
		if threshold is not None:
			self.threshold = threshold
		else:
			self.threshold = self.default_threshold
		
		## self.facetedField = getFacetedField(vocabXpath);
		self.facetedField = self.getFacetedField();
		print "%d facetedField from getFacetedField()" % len (self.facetedField)
		
		# self.facets - list of terms occuring in the METADATA
		self.facets = self.facetedField.facets
		
		# self.xsd_terms - list of terms defined in the SCHEMA
		self.xsd_terms = self.getXsdTerms()
		print "%s xsd defines %d values" % (self.typeName, len(self.xsd_terms))
		
		# if threshold is greater than zero: filter by facet.count
		# if threshold is 0, add facets for vocab terms that have 0 occurrences (and therefore
		# are not represented as facets from DDS search)
		if self.threshold > 0:
			self.facets = filter (lambda x:x.count >= self.threshold, self.facets)
		else:
			self.facets = self.facets + self.getNonFacetedVocabTerms()
		
		self.sortFacets ('count')
		
	def getFacetedField (self):
		"""
		This method exists so it can be overridden in MergingVocabUsageReporter,
		where multipld factedFields must be merged into one FacetedField.
		But here it is pretty simple...
		"""
		return getFacetedField(self.vocabXpath);
		
	def getXsdTerms (self):
		"""
		Return the terms defined by the xsd schema. This method is overridden
		by MerginVocabUsageReporter, which has to merge mulitple xsds
		"""
		xsd = self.getXsd(self.vocabUrl)
		vocabType = xsd.getEnumerationType(self.typeName)
		if not vocabType:
			raise Exception, 'vocabType  not found for "%s"' % self.typeName
		return vocabType.getValues()

		
	def getNonFacetedVocabTerms(self):
		"""
		add a facet with count = 0 for each vocab term that is not
		represented in self.facets
		"""
		nonFaceted=[];add=nonFaceted.append
		print "\ngetNonFacetedVocabTerms()"
		for term in self.xsd_terms:
			if not self.facetedField.getFacet(term):
				add (Facet (term, 0))
				print "- ", term
		print "%d NON-FACETED" % len(nonFaceted)
		return nonFaceted
		
	def filterFacets (self):
		"""
		filters the list of terms by a threshold count
		"""
		# print "filterTerms: threshold = ", self.threshold
		return filter (lambda x:x.count >= self.threshold, self.facetedField.facets)
			
	def sortFacets (self, sortby):
		"""
		sorts provided list of terms (facets) the specified 'sortby' field
		"""
		_cmp = None
		if sortby == 'count':
			_cmp = lambda x, y:cmp (y.count, x.count)  #descending
		if _cmp is not None:
			self.facets.sort(_cmp)
		
	def __len__ (self):
		return len(self.facets)
		
	def getXsd (self, vocabUrl):
		"""
		read the schema file as a VocabXSD instance
		"""
		client = SimpleClient (vocabUrl)
		client.verbose = False
		raw = client.getData()
		return VocabXSD (xml=raw)
		
	def makeReport (self, dest='.'):
		"""
		builds a report and writes to disk
		"""
		print "\ncompiling report  "
		dest = os.path.join(dest, self.getReportFileName())
		recs = [] # start with header
		
		# print 'reporting over %d terms' % len(self.facets)
		
		for i, facet in enumerate(self.facets):
			if i % 50 == 0:
				print '.'
				
			rec = TermUsageRecord(facet.term, facet.count, self)
			rec.inSchema = (rec.term in self.xsd_terms) # boolean s
			recs.append(rec)
			if not facet.term in self.xsd_terms:
				# print 'setting dates for %s' % facet.term
				rec.set_dates()
			
		
				
		sys.stdout.write('\n')
		rows = 	map (lambda x:x.toTabDelimited(), recs)
		rows.insert (0, '\t'.join(term_schema))
		tab_delimited = '\n'.join (rows)
		
		#fp = open (dest, 'w')
		fp = codecs.open (dest, 'w', 'utf-8')
		fp.write (tab_delimited)
		fp.close()
		print "wrote %s report to %s" % (self.typeName, dest)
		
	def getReportFileName (self):
		return '%s_vocab_report_%s.xls' % (self.typeName, self.getTimeStamp())
		
	def getTimeStamp(self):
		"""
		returns a time stamp used to uniquely name a report file
		"""
		fmt = '%Y-%m-%d-%H%M%s'
		return time.strftime(fmt,time.localtime())

def doReport (collection, threshold=None):
	params = collection_params[collection]
	reporter = VocabUsageReporter (params['vocabUrl'], params['typeName'], params['vocab_field'], threshold)

	facets = reporter.facets
	print "\n%d  terms" % len(facets)
	if 1:
		for ft in facets:
			print '%s (%s)' % (ft.term, ft.count)
	
	# reporter.makeReport()
	
if __name__ == '__main__':
	doReport ('instname', 0)
	# doReport ('eventname')
