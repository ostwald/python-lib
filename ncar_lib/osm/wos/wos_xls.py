"""
WOS spreadsheet reader
"""
import sys, os, re
from JloXml import XmlUtils
from xls import WorksheetEntry, XslWorksheet
from ncar_lib.osm import OsmRecord, ContributorOrganization, ContributorPerson, Affiliation
from source_xls import SourceXlsReader
from sponsor_xls import SponsorXlsReader
from wos_author import Author, AuthorParseException



class SourceReaderFactory:
	"""
	privides singleton copy of a SourceXlsReader, so we can reuse an existing instance
	instead of doing many costly reads
	
	useage:
		sourceReaderFactory = SourceReaderFactory()
		sourceReader = sourceReaderFactory.getInstance()
	"""
	instance = None
	source_data_path = 'real_data/wosSourceLook-up-2011.txt'
	
	def getInstance ():
		"""
		returns the singleton instance of SourceXlsReader
		"""
		if self.instance is None:
			self.instance = SourceXlsReader(self.source_data_path)
		return self.instance
		
sourceReaderFactory = SourceReaderFactory()

class SponsorReaderFactory:
	"""
	see SourceReaderFactory
	"""
	instance = None
	sponsor_data_path = 'real_data/wosSponsorLook-up-2011.txt'

	def getInstance ():
		if self.instance is None:
			self.instance = SponsorXlsReader(self.sponsor_data_path)
		return self.instance
	
sponsorReaderFactory = SponsorReaderFactory()



class WosXlsRecord (WorksheetEntry):
	"""
	Encapsulates on row of the data spreadsheet. Processes field values
	and inserts them in newly created osmRecord
	
	most fields have a method that massages the WOS value, and are named handleField (e.g., handleSource)
	"""
	def __init__ (self, data, schema):
		WorksheetEntry.__init__(self, data, schema)
		
	def makeOsmRecord (self, idNum=None):
		"""
		The main method - produces an OsmRecord instance for this WOS record
		"""
		rec = OsmRecord (path='OSM_RECORD_TEMPLATE.xml')
		rec.id_prefix = "FY11WOS"
		
		if idNum is None:
			idNum = 9999
			
		rec.setId(rec.makeRecordId (rec.id_prefix, idNum))
		
		like_named_mappings = ['title', 'abstract', 'volume', 'issue']
		
		# rec.addIdNumber (self['wos id'], 'WOS')
		try:
			
			map (lambda field:self.handleSimpleMapping(rec, field), like_named_mappings)
			
			self.handleWosId (rec)
			self.handleIssn (rec)
			self.handleIsbn (rec)
			self.handleDoi (rec)
			self.handleArticleNumber (rec)
			
			self.handleSource (rec)
			self.handleConferenceTitle (rec)
			self.handleConferenceDate (rec)
			# self.handleConferenceLocation (rec)
			
			self.handlePageSpan (rec)
			self.handlePublishedDate (rec)
			
			self.handleSponsor(rec)
			
			self.handleAuthors(rec)

		except IOError, exc:
			print self
			raise exc
		return rec
		
	def handleSimpleMapping (self, osmRecord, xlsfield, xmlfield=None):
		"""
		xlsfield - the xls column name - determines the value
		xmlfield - a named xpath for osmRecord - determines the xml field that gets value
		"""
		if xmlfield is None:
			xmlfield = xlsfield
		val = self[xlsfield]
		if val:
			osmRecord.set(xmlfield, val)
		
	def handleWosId (self, osmRecord):
		"""
		WOS numbers in xls are of form WOS:000XXXXX
		chop off the 'WOS:' part (WOS search will accept either form)
		"""
		wos = self['wos id']
		if not wos:
			return
		if wos.startswith("WOS:"):
			wos = wos[4:]
		osmRecord.addIdNumber (wos, 'WOS')
		
	def handleIssn (self, osmRecord):
		"""
		insert issn value as idNumber in osmRecord
		"""
		val = self['issn']
		if val:
			osmRecord.addIdNumber (val, 'ISSN')
		
	def handleIsbn (self, osmRecord):
		"""
		insert isbn value as idNumber in osmRecord
		"""
		val = self['isbn']
		if val:
			osmRecord.addIdNumber (val, 'ISBN')

	def handleDoi (self, osmRecord):
		"""
		insert doi value as idNumber in osmRecord
		"""
		val = self['doi']
		if val:
			osmRecord.addIdNumber (val, 'DOI')
	
	def handleArticleNumber (self, osmRecord):
		"""
		insert 'article number' value as idNumber in osmRecord
		"""

		val = self['article number']
		if val:
			osmRecord.addIdNumber (val, 'Citation/Article')
			
	def handleSource (self, osmRecord):
		"""
		use 'source' field of xls to do a lookup in the 'source' spreadsheet, where
		normalized values are expressed.
		throws exception if a normalized value is not found
		"""
		source_reader = sourceReaderFactory.getInstance()
		pubName = source_reader.getNormalizedPubname(self['source'])
		osmRecord.setPubName (pubName)
		
	def handleConferenceTitle (self, osmRecord):
		"""
		write conference title to osmRecord as eventName
		"""
		self.handleSimpleMapping (osmRecord, 'conference title', 'eventName')
		
	conf_date_pat = re.compile ("([\d]{4}-[\d]{2}-[\d]{2})-([\d]{4}-[\d]{2}-[\d]{2})")
		
	def handleConferenceDate (self, osmRecord):
		"""
		the attribute type is always Meeting; 
		the start and end dates will need to decode FEB 01-05, 2010 into a YYYY-MM-DD format.
		"""
		dateStr = self['conference date']
		if not dateStr:
			return
			
		m = self.conf_date_pat.match(dateStr)
		if not m:
			raise Exception, 'Could not parse "conference date" (%s)' % dateStr
			
		start = m.group(1)
		end = m.group(2)
		
		osmRecord.setDateRange (start, end, 'Meeting')
		
	def handleConferenceLocation (self, osmRecord):
		"""
		/record/coverage/location/@type="Meeting"; 
		/record/coverage/location/@country="??"; 
		/record/coverage/location/@city="??"; 
		/record/coverage/location/@state="??"
		
		the attribute type is always Meeting; the country and city are known but
		the state is not and it is required. The country is not in the correct
		format. Can you use the country schema to look up the 2-letter country
		identifier?
		
		"""
		raise Exception, 'Not yet implemented'
		
	def handleSponsor (self, osmRecord):
		"""
		/record/contributors/organization/@role="Meeting sponsor"; 
		/record/contributors/organization/affliation/instName
		
		ISSUE: are names REALLY are separated by commas?? 
		perform a lookup of the sponsor name to get the correct OSM instName by using
		http://nldr.library.ucar.edu/metadata/osm/1.1/documents/wosSponsorLook-up-2011.xslx
		"""
		sponsor = self['sponsor']
		
		## NOTE - THERE MAY BE MULTIPLE SPONSORS, so we have to do the following for EACH
		
		instName = sponsor_reader.getInstName(sponsor)

		orgEl = XmlUtils.createElement('organization')
		orgEl.setAttribute ('role', 'Meeting sponsor')
		org = ContributorOrganization (orgEl)
		affiliation = org.getAffiliation (instName)
		osmRecord.addContributorInstance (org)
		
	def handleAuthors (self, osmRecord):
		"""
		process the authors in the spreadsheet, and insert them
		into the osmRecord (relying on the ContributorPerson class)
		"""
		authors = self._getAuthors()
		for author in authors:
			person = ContributorPerson (author.asElement())
			osmRecord.addContributorInstance (person)
		
	def handlePublishedDate (self, osmRecord):
		date = self.getPublishedDate()
		osmRecord.setDate (date, 'Published')
	
	def handlePageSpan (self, osmRecord):
		"""
		compute page span from 'beginning page' and 'ending page' xls field
		only add to xml record if there is a value for both start and end
		"""
		start = self['beginning page']
		end = self['ending page']
		if start and end:
			pageSpan = '%s-%s' % (start, end)
			osmRecord.set ('pageSpan', pageSpan)
			
	monthMap = {
		'JAN':1,
		'FEB':2,
		'MAR':3,
		'APR':4,
		'MAY':5,
		'JUN':6,
		'JUL':7,
		'AUG':8,
		'SEP':9,
		'OCT':10,
		'NOV':11,
		'DEC':12 }
			
	def getPublishedDate (self):
		"""
		return a date of form YYYY, YYYY-MM, or YYYY-MM-DD depending on
		available data ('published year' and 'published month-day' fields)
		
		throws Exception of the available data can't be parsed\
		- year must be present and must be a 4 digit string
		- month must be 3-letter abbrev or span (JAN-MAR), in which case we
		  use the latter month (per Katy)
		- day must be an integer
		"""
		year = self['published year']
		
		if not year:
			raise Exception, 'year not found'	
			
		if len(year) != 4:
			raise Exception, 'year must have 4 digits (%s)' % year
			
		try:
			year = int(year)
		except:
			raise Exception, 'year must be 4-digit integer (%s)' % year
		
		# process MONTH-DAY
		month_day = self['published month-day']
		if not month_day:
			return '%d' % year
				
		splits = map(lambda x:x.strip(), month_day.split(' '))

		monthStr = splits[0]
		if monthStr.find('-') != -1:
			# monthStr is of the form 'JAN-FEB', take the latter
			monthStr = monthStr.split('-')[1]
		
		try:
			month = self.monthMap[monthStr]
		except:
			raise Exception, 'unparsable monthStr (%s)' % monthStr
			
		if len(splits) < 2:
			return '%d-%02d' % (year, month)
		
		else:
			day = int(splits[1])
			return '%d-%02d-%02d' % (year, month, day)
	
	def _getAuthors (self):
		authors = []
		data = self['author full name']
		
		if not data: return authors
		
		print "---\n%s\n------" % data
		
		authororder = 1
		for name in data.split(';'):
			# print '\nprocessing: %s' % name
			try:
				authors.append (Author (name, authororder=authororder))
				authororder = authororder + 1
			except AuthorParseException, msg:
				print "AuthorParseException: %s" % msg
		return authors
			
class WosXlsReader (XslWorksheet):
	
	verbose = 1
	linesep = '\r\n' # windows
	encoding = 'utf-8'
	
	def __init__ (self, path):
		XslWorksheet.__init__ (self, entry_class=WosXlsRecord)
		self.read (path)
		
def pubNameLookupTester ():
	data_path = 'real_data/wos_ncar-ucar_fy11.txt'
	reader = WosXlsReader(data_path)	
	for item in reader:
		source = item['source']
		try:
			source_reader = sourceReaderFactory.getInstance()
			pubName = source_reader.getNormalizedPubname(source)
		except:
			print 'could not find pubName for "%s"' % source

def instNameLookupTesterISSUE ():
	data_path = 'real_data/wos_ncar-ucar_fy11.txt'
	reader = WosXlsReader(data_path)	
	for item in reader:
		sponsorVal = item['sponsor']
		if not sponsorVal:
			continue
		sponsors = map (lambda x: x.strip(), sponsorVal.split(','))
		for sponsor in sponsors:
			try:
				sponsor_reader = sponsorReaderFactory.getInstance()
				instName = sponsor_reader.getInstName(sponsor)
			except:
				print 'could not find instName for "%s"' % sponsor
	
def instNameLookupTester ():
	data_path = 'real_data/wos_ncar-ucar_fy11.txt'
	reader = WosXlsReader(data_path)	
	for item in reader:
		sponsor = item['sponsor']
		if not sponsor:
			continue
		try:
			sponsor_reader = sponsorReaderFactory.getInstance()
			instName = sponsor_reader.getInstName(sponsor)
		except:
			print 'could not find instName for "%s"' % sponsor
				
if __name__ == '__main__':
	
	data_path = 'real_data/wos_ncar-ucar_fy11.txt'
	reader = WosXlsReader(data_path)
	if 1:
		item = reader[208] # 523
		rec = item.makeOsmRecord()
		print rec
	elif 1:
		item = reader[208] # 523
		authors = item._getAuthors()
		print '%d authors' % len(authors)
		for author in authors:
			print author
	elif 0: # show raw author data
		for item in reader:
			data = item['author full name']
			if data:
				authors = map (lambda x:x.strip(), data.split(';'))
				for author in authors:
					print author
	elif 1: # show sponsors
		for item in reader:
			sponsor = item['sponsor']
			if sponsor:
				print sponsor
				sponsors = map (lambda x: x.strip(), sponsor.split(','))
				for sp in sponsors:
					print ' - "%s"' % sp
