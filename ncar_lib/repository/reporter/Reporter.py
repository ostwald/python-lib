import os, sys, re, codecs
from UserList import UserList
from Properties import Properties
from serviceclient import ServiceClient, URL
from JloXml import XmlRecord, XmlUtils
from ncar_lib import RepositorySearcher, SearchResult, unionDateToSecs

"""
Use search service to retrieve and report batch of records. Search and report are configured
in properties file
"""

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
		
		
class ReportResultMixin:
	"""
	define reporting functionality for ReportResult items
	"""
	def asTabDelimited (self, columns):
		return '\t'.join (map (self.getAttr, columns))

	def getAttr (self, attr, baseObj=None):
		baseObj = baseObj or self
		# print ' @%s' % attr
		val = hasattr(baseObj, attr) and getattr(baseObj, attr) or ""
		return unicode(val)
		
class ReportResult (SearchResult, ReportResultMixin):
	"""
	The ReportResult makes it's attributes available as "columns"
	"""

	#default_payload_constructor = XmlRecord 

	def __init__ (self, element, payload_constructor=None):
		SearchResult.__init__ (self, element, payload_constructor)
		
		# define the columns that can be reported
		self.recordID = self.recId
		
class ReportSearcher (RepositorySearcher):
	"""
	reads properties file to parameterize search - see ReportSearcher.get_params
	
	"""

	numToFetch = 20
	batchSize = 400
	searchResult_constructor = ReportResult
	filter_predicate = None
	verbose = 0
	
	def __init__ (self, propsFile):
		self.props = Properties (propsFile)
		baseUrl = self.props.getProperty("baseUrl")
		RepositorySearcher.__init__(self)
			
	def get_params (self, collection, xmlFormat):
		"""
		use params defined in properties file to query the search service
		"""
		
		parms_dict = {
			"verb": "Search",
			"xmlFormat": self.props.getProperty('xmlFormat'),
			"ky": self.props.getProperty('collection'),
			'q' : self.props.getProperty('q'),
			'dcsStatus' : self.props.getProperty('dcsStatus'),
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid','osmDatePublished']
			}
			
		# process params dict from properties
		propertyParams = self.props.params
		if propertyParams:
			if self.verbose:
				print "\nProperty Params"
				for parm in propertyParams:
					print "- %s - %s" % (parm, propertyParams[parm])
			parms_dict.update (propertyParams)
			
		if self.verbose:
			print "\nQuery Params"
			for parm in parms_dict:
				print "- %s - %s" % (parm, parms_dict[parm])
			
		return parms_dict
	
class Reporter:
	"""
	columns are implemented by ReportResult and exposed as attributes
	"""
	default_columns = ['recordID', 'collection', 'title', 'authors', 'pubName']
	searcher_class = ReportSearcher
	verbose = 0
	
	def __init__ (self, propsFile):
		self.props = Properties (propsFile)
		if self.props.hasProperty ('report.columns'):
			self.columns = map (lambda x:x.strip(), self.props.getProperty('report.columns').split(','))
			if self.verbose:
				print 'using CUSTOM COLUMNS (%s)' % self.columns
		else:
			if self.verbose:
				print 'using DEFAULT COLUMNS'
			self.columns = self.default_columns
		self.results = self.searcher_class(propsFile)
		
		self.resultClass = self.results.searchResult_constructor
		try:
			self.verifyColumns()
		except Exception, msg:
			print "could not verify columns: %s" % msg
			# print "first result:", self.results[1]
			sys.exit()
		
	def verifyColumns (self):
		"""
		raises Exception if a configured column is not present in the data
		"""
		if self.results:
			result = self.results[0]
			for col in self.columns:
				if not hasattr (result, col):
					raise KeyError, "attribute does not exist for %s: %s" % (self.resultClass.__name__, col)
		
	def getTabDelimited (self, records=None):
		"""
		return tab-delimited report for the specified records - representing each in tab-delimeted form
		"""
		records = records or self.results
		
		s = [];add=s.append
		# header
		add ('\t'.join (self.columns))
		
		for result in (records):
			add (result.asTabDelimited(self.columns))
			
		return u'\n'.join (s)
					
	def writeTabDelimited (self, records=None, outpath=None):
		"""
		write tab delimeted report to "outpath"
		"""

			
		tabDelimited = self.getTabDelimited(records)
		if outpath is None:
			# outpath = '%s-tab-delimited.txt' % self.__class__.__name__
			outpath = self.props.getProperty('report.file.path')
		## fp = open (outpath, 'w')
		fp = codecs.open(outpath, 'w', "utf-8")
		fp.write (tabDelimited)
		fp.close()
		
		print 'wrote tab-delimited report to ', outpath
			
if __name__ == '__main__':

	props = Properties('myprops.properties')
	
	if 0:
		for key in props.keys():
			print "%s: %s" % (key, props.getProperty(key))
			
	reporter = Reporter ('myprops.properties')
	reporter.writeTabDelimited()
	# for result in reporter.results:
		# print result.toTabDelimited(reporter.columns)
