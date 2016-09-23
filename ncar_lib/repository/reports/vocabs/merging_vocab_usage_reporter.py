from vocab_usage_reporter import VocabUsageReporter
from UserDict import UserDict
from vocab_data import collection_params
from serviceclient import SimpleClient
from faceted_searcher import getFacetedField
from ncar_lib.osm.vocabs import VocabXSD
from ncar_lib.repository.search_summary import FacetedField, Facet

class MergingVocabUsageReporter (VocabUsageReporter):
	
	def __init__ (self, vocab_data, typeName, threshold=None):
		
		if type(vocab_data) != type([]):
			raise Exception, "MergingVocabUsageReporter requires a vocab_data LIST"
		self.vocab_data = vocab_data
		self.typeName = typeName
		
		self.computeFacetList(threshold)
		
		# if threshold is not None:
			# self.threshold = threshold
		# else:
			# self.threshold = self.default_threshold
				# 
		# self.facetedField = self.getFacetedField()
		# 
		# print "self.facetedField has %d facets" % len(self.facetedField)
			# 
		# self.xsd_terms = self.getXsdTerms()
			# 
		# self.terms = self.getSortedTerms ('count')
		# self.filtered_terms = self.filterTerms(self.terms)
		
	def getFacetedField (self):
		"""
		merge multiple FacetedFields into one
		-> as a side effect	set self.vocabXpath, which is needed by self.setDates()
		"""
		# create a FacetedField that merges facets (and occurrences) from each vocab _field
		unique_vocab_xpaths = []
		self.facetedField = FacetedField()
		for params in self.vocab_data:
			xpath = params['vocab_field']
			if not xpath in unique_vocab_xpaths:
				print "getting facetedField for ", xpath
				unique_vocab_xpaths.append(xpath)
				facetedField = getFacetedField(xpath)
				for i, facet in enumerate(facetedField.facets):
					self.add (facet.term, facet.count)
					if i % 100 == 0:
						print "added %d/%d" % (i, len(facetedField.facets))
		self.vocabXpath = unique_vocab_xpaths[0] # needed by setDates
		return self.facetedField
		
	def getXsdTerms(self):
		xsd_terms = []
		for params in self.vocab_data:
			xsd = self.getXsd (params['vocabUrl'])
			vocabType = xsd.getEnumerationType(params['typeName'])
			if not vocabType:
				raise Exception, 'vocabType  not found for "%s"' % self.typeName
			xsd_terms = xsd_terms + vocabType.getValues()
		return xsd_terms
		
	def add (self, term, count):
		facet = None
		if not self.facetedField.getFacet(term):
			self.facetedField[term] = count
			facet = Facet (term, count)
			self.facetedField.facets.append (facet)
		else:
			facet = self.facetedField.getFacet(term)
			facet.count = self.facetedField[term] + count
		self.facetedField.facetMap[term] = facet
			
		# add term to countMap
		terms = []
		if self.facetedField.countMap.has_key(count):
			terms = self.facetedField.countMap[count]
		terms.append (term)
		self.facetedField.countMap[count] = terms	
					
if __name__ == '__main__':
	
	data = collection_params['pubname']
	reporter = MergingVocabUsageReporter (data, 'pubname')
	print 'reporter has %d terms' % len(reporter)
	print 'there are %d filtered items' % (len(reporter.filtered_terms))
	items_to_report = reporter.filtered_terms
	for term in items_to_report:
		print '%s (%s)' % (term.term, term.count)
	reporter.makeReport()
		
	
