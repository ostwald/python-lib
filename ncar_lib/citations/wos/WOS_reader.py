"""
ultimately want to have enough info to produce "AMS/ASR format (as specified by Pubs) ..."
"""

import sys, os, time, re
from UserList import UserList
from UserDict import UserDict
from misc.titlecase import titlecase
from wos_vs_pubs_fields import wos2pubs_fields
from ncar_lib.citations.Author import WOSAuthor

class WOSXlsReader (UserList):
	"""
	Reads a tab-delimited file of WOS Citation data and produces an unordered list
	of 'WOSRecord' instances
	"""
	schema = None
	records = []
	
	def __init__ (self, path):
		UserList.__init__ (self)
		lines = open (path, 'r').read().split('\r\n') # windows
		print "%d lines read" % len (lines)
		self.schema = lines[0].split('\t')
				
		for line in lines[1:]:
			if line:
				self.append (WOSRecord (line, self.schema))
			
	def report (self, items=None):
		items = items or self.data
		print '\n%d Records' % len(items)
		for rec in items:
			print rec
		
	def showSchema (self):
		for field in self.schema:
			if wos2pubs_fields.has_key (field):
				print "%s -> %s" % (field, wos2pubs_fields[field])
			else:
				print "%s -> NOT FOUND" % field
				
class WOSRecord (UserDict):
	"""
	Record corresponding to one line of a tab-delimited WOSData file
	
	extracts fields corresponding to 'wos2pubs_fields.keys" and discards the rest
	the field names themselves 
	"""
	
	
	
	def __init__ (self, rec_data, schema):
		UserDict.__init__ (self)
		data_fields = rec_data.split('\t')
		for i, wos_header in enumerate (schema):
			# WOS header (e.g., "PT")
			
			if not wos_header in wos2pubs_fields.keys():
				continue
				
			# field is the pubs field  for wos_header (e.g. "Pub Type" for "PT")
			field = wos2pubs_fields[wos_header]
			data = data_fields[i]
			
			# remove surrounding quotes if applicable
			if data and data[0] in ['"', "'"] and data[0] == data[-1]:
				data = data[1:-1]
			self[field] = data
			
	def _getPages (self):
		return "%s-%s" % (self['begin-page'], self['end-page'])
		
	def _getYear (self):
		return self['Pub-Year']
		
		
	def toSmartSentenceCase (self, s):
		"""
		return string with first letter capitalized and any letter following
		a colon capitalized, but all others lower case
		"""
		ret = ""
		doCap = 1
		for i,ch in enumerate(s):
			if doCap and ch != " ":
				ret = ret + ch.upper()
				doCap = 0
			else:
				ret = ret + ch.lower()
				if ch == ':':
					doCap = 1
		return ret
		
	def _getTitle (self):
		# return titlecase(self['Title'].lower())
		return self.toSmartSentenceCase (self['Title'])
		
	funkyNameRe = re.compile("[\S]*\.[\S]")
		
	def _splitname (self, name):
		lastname = initials = ""
		if (name.find(',') != -1):
			lastname = name.split (',')[0].strip()
			try:
				initials = name.split (',')[1]
			except:
				initials = None
		elif (self.funkyNameRe.search (name)):
			lastname = name.split('.')[0].strip()
			try:
				initials = name.split ('.')[1]
			except:
				initials = None
		else:
			lastname = name
			
		lastname = titlecase (lastname.lower())
		return lastname, initials
		
	def _getAuthors (self):
		authors = []
		data = self['authors']
		if not data: return authors
		authororder = 1
		for name in data.split(';'):
			lastname = firstname = middlename = ""
			# lastname = name.split (',')[0].strip()
			# lastname = titlecase (lastname.lower())
			# try:
				# initials = name.split (',')[1]
				# if not initials:
					# print "splitting '%s' by ." % name
					# inititials = name.split ('\.')[1]
			# except:
				# initials = None
			lastname, initials = self._splitname (name)
			if initials:				
				initials = initials.strip()
				if len(initials) == 2:
					# initials = "%s. %s." % (initials[0], initials[1])
					firstname = initials[0]
					middlename = initials[1]
				if len(initials) == 1:
					# initials = "%s." % initials[0]
					firstname = initials[0]
				# authors.append ('%s, %s' % (lastname, initials))
				authors.append (WOSAuthor (lastname=lastname, firstname=firstname, 
										   middlename=middlename, authororder=authororder))
				authororder = authororder + 1
		return authors
		
	def _getPubName (self):
		return titlecase(self['pubname'].lower())
		
	def _getPubStatus (self):
		"""
		all WOS entries are published (this is an 'enum' value in Pubs DB)
		"""
		return "published"
		
	def _getPubType (self):
		"""
		normalize WOS PT field to pubsDB 'type' field
		NOTE: the only values for this field are 'J' and 'C', but all the entries seem to be for
		journals, so for now 'journal' is always returned (this is 'enum' value in PubsDB).
		"""
		# pubtype = self['Pub Type']
		# if pubtype == 'J': return "journal"
		# if pubtype == 'C': return "proceedings"
		# else:
			# raise TypeError, "unknown pub type value: '%s'", pubtype
		return 'journal'
		
	def _getVolume (self):
		"""
		this field holds all part, volume, issue information!
		"""
		ret = ""
		v = self['Volume']
		i = self['Issue']
		p = self['Part Name']

		if v and i:
			ret = "%s(%s)" % (v, i)
		else:
			if v:
				ret = "vol. %s" % v
			if i:
				if ret:
					ret = "%s, i. %s" % (ret, i)
				else:
					ret = "i. %s" % i
		if p:
			if ret:
				ret = "%s, %s" % (ret, p)
			else:
				ret = "%s" % p		
		return ret
		
	def _getPubDate (self):
		"""
		REQUIRE a year, and do the best we can to build a more precise date. 
		
		'Pub-date' is most often something like "27-Feb", but can be simply "Feb" or even blank
		
		we return a value in the same PubsDb format ("2009-10-26")
		"""
		pd = self['Pub-date']
		py = self['Pub-Year']
		if not py:
			raise ValueError, "no pub-year supplied"
			
		splits = pd.split('-')
		day = month = None
		if len(splits) == 2:
			day = splits[0].strip()
			month = splits[1].strip()
		if len(splits) == 1:
			month = splits[0]
		if day:
			try:
				int(day)
			except:
				# print 'bad day: %s' % day
				day = None
		day = day or "1"		 # if day cannot be determined, use 1
		month = month or "Jan"   # if month cannot be determined, use jan
		
		wos_date_format = "%b-%d-%Y"  # OCT-26-2009
		pubs_date_format = "%Y-%m-%d" # 2009-10-26
		
		wos_date_str = "%s-%s-%s" % (titlecase(month.lower()), day, py)
		try:
			dateObj = time.strptime (wos_date_str, wos_date_format)
		except:
			# print ("unable to format wos_date_str: " % wos_date_str)
			dateObj = time.strptime ("Jan-1-%s" % py, wos_date_format)
			
		return time.strftime (pubs_date_format, dateObj)
		
	editorRe = re.compile('([\w^,]+), ([\w]+)')
		
	def _getEditors (self):
		editors = []
		buff = self['editor']
		while 1:
			# print "\n%s" % buff
			m = self.editorRe.search (buff)
			if not m:
				break
			buff = buff[m.end():].strip()
	
			lastname = m.group(1)
			initials = m.group(2)
	
			# print "lastname: %s,  initial: %s" % (lastname, initials)
	
			if len(initials) > 3:
				print 'WARNING: bogus initials (%s) being ignored' % initials
				initials = ""
			else:
				foo = ""
				for ch in initials:
					foo += ch+'.'
				initials = foo
			name = initials+lastname
			editors.append (name)
		return ', '.join (editors)
		
	def report (self):
		# return self['Title'][:80]
		s = [];add=s.append
		add ("title: %s" % self._getTitle())
		add ("year: %s" % self._getYear())
		if self.has_key('editor'):
			add ("editor: %s" % self['editor'])
		
		add ("pubname: %s" % self._getPubName())
		
		add ("volume: %s" % self._getVolume()) # self['volume'])
		add ("pages: %s" % self._getPages())
		add ("pubstatus: %s" % self._getPubStatus())
		add ("statusdate: %s" % self._getPubDate())
		add ("type: %s" % self._getPubType())
		add ("doi: %s" % self['doi'])
		add ("wos_id: %s" % self['wos_id'])
		add ("authors:")
		for author in self._getAuthors():
			add ("\t" + str(author))
		
		return '\n'.join(s) + '\n'
		
	def brief_report (self):
		s = [];add=s.append
		add ("title: %s" % self._getTitle())
		add ("pubname: %s" % self._getPubName())
		add ("authors:")
		for author in self._getAuthors():
			add ("\t" + str(author))
		return '\n'.join(s) + '\n'
			
	def __repr__ (self):
		# return self._getVolume()
		return self.brief_report()
		
def filterByTitle (item):
	findstring = "DETERMINING MAJOR SAR-ARC PROPERTIES FROM A FEW MEASURABLE PARAMETERS"
	title = item._getTitle().lower()
	return title.find (findstring.lower()) != -1
	
funkyAuthorRe = re.compile("[\S]*\.[\S]")
	
def filterByFunkyAuthor (item):
	m = funkyAuthorRe.search (item['authors'])
	if m:
		# print m.group()
		print item['authors']
		return 1
	else:
		return 0
		
def filterByHasEditor (item):
	if item['editor']:
		print item['editor']
		print "--> ", item._getEditors()
		return 1
	else:
		return 0
		
def getAllEditors ():
	dataDir = "WOS_data_files"
	for filename in os.listdir (dataDir):
		path = os.path.join (dataDir, filename)
		print filename
		wos = WOSXlsReader(path)
	
		items = filter (filterByHasEditor, wos)		
		
def editorTester ():
	path = "WOS_data_files/WOS_4501-5000.txt"
	wos = WOSXlsReader(path)
	items = filter (filterByHasEditor, wos)	
	
def recordTester ():
	# path = "WOS_data_files/WOS_4501-5000.txt"
	path = "test-data-8-4.txt"
	wos = WOSXlsReader(path)
	print (wos[9].report())
	
if __name__ == '__main__':
	# getAllEditors()
	recordTester()

		
