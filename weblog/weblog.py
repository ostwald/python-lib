import sys, os, re, time
from xls import FieldList
from UserList import UserList

date_fmt = '%m/%d/%Y %H:%M:%S'
def getDateStr (secs):
	return time.strftime (date_fmt, time.localtime(secs))

class LogLine (UserList):
	"""
	provides mapping interface to fields in a LogFile line
	fields defined by schema_fields
	"""
	quotePat = re.compile ('"(.*?)"')
	bracketPat = re.compile ('\[(.*?)\]', re.DOTALL)
	blankPat = re.compile('(\-)')
	
	datetime_fmt = "%d/%b/%Y:%H:%M:%S"
	
	field_brackets = {
		' ': ' ',
		'[':']', 
		'"':'"'
		}
		
	start_chars = ['-' ,'[' ,'"']
	schema = None

	def __init__ (self, line):
		self.line = line
		UserList.__init__ (self)
		self.cur_field = ''
		self.infield = 0 # start off collecting field data
		self.start_field_chars = self.field_brackets.keys()
		self.end_char = None
		self.parse()

		try:
			self.timestamp = self.get_timestamp()
		except:
			raise Exception, 'Could NOT parse time for %s' % self['datetime']

	def get_timestamp (self):
		"""
		ignore offset for now
		"""
		datetime, offset = map (lambda x:x.strip(), self['datetime'].split(' -'))
		return time.mktime( time.strptime (datetime, self.datetime_fmt ))
		
	def parse (self):
		line = self.line
		self.startField()
		# print line	
		
		i = 0
		while i < len(line):
			
			ch = line[i]
			if not self.infield:
				
				if ch in self.start_chars:
					# if ch == ' ':  # step through spaces when we're not in a word
						# i = i + 1
						# continue
					# "start_char: %s" % ch
					m = None
					if ch == '"':
						# print '\n looking at a quote - %s' % line[i:i+30]
						m = self.quotePat.match (line, i)
					elif ch == '[':
						m = self.bracketPat.match (line, i)
					elif ch == '-':
						m = self.blankPat.match (line, i)
					if m:
						self.addField (m.group(1))
						i = m.end()
						continue
						
				if ch != ' ':
					self.startField()
					
				
					
			# we're not a start character while we're between fields
			else:
				if ch == ' ':
					self.endField()
				else:
					self.cur_field = self.cur_field + ch
			i = i + 1

		self.endField()


	def __getitem__ (self, field):
		"""
		Provides field-based addressing so that values can be obtained by field name.
		Returns the empty string if the field is not found in the schema
		"""
		index = self.schema.getIndex (field)
		# print '__getitem__() field: %s, index: %d' % (field, index)
		if index > -1:
			try:
				## return self.data[index]
				value = self.data[index]
				if len(value) > 1 and \
				   value[0] == value[-1] == "'" or \
				   value[0] == value[-1] == '"':
					value = value[1:-1]
				return value
			except:
				return ""
		else:
			return ""
		
	def __getitemOFF__ (self, index):
		# print "getItem: %d" % index
		if index > len(self) - 1:
			return "None"
		return self.data.__getitem__(index)
		
	def addField (self, field):
		if field:
			self.append(field)
			# print 'added: %s' % field

	def startField(self, ch=' '):
		# print ' - startField'
		self.infield = 1
		self.end_char = self.field_brackets[ch]

	def endField (self):
		# print ' - endField'
		self.addField (self.cur_field)
		self.cur_field = ''
		self.infield = 0

	def report (self):
		print'\nReport'
		for field in self.schema:
			print '%s: %s' % (field, self[field])

class LogFile (UserList):
	
	debug = 0
	line_class = LogLine
	schema_fields = ['IP', 'clientId', 'userId', 'datetime', 'request', 'HTTP status',
		  'size', 'referrer', 'agent']

	def __init__ (self, path):
		"""
		exposes:
			- path
			- filename
			- startDate, endDate (as secs)
		"""
		UserList.__init__ (self)
		
		self.path = path
		self.schema = FieldList(self.schema_fields)
		self.line_class.schema = self.schema
		self.filename = os.path.basename(self.path)
		self.read()
		self.startDate, self.endDate = self.getTimeExtents()
		self.ips = None
		
	def read (self):
		"""
		read the log file, creating a LogLine instance (self.line_class) for each line
		self.data is populated with LogLine instances
		"""
		s = open(self.path, 'r').read()
	
		lines = s.split ('\n')
		print '%d lines read' % len(lines)
		
		if self.debug:
			self.append(self.line_class(lines[0]))
		else:
			# self.data = map (self.line_class, filter(None, lines))
			for line in filter (None, lines):
				try:
					logLine = self.line_class(line)
					self.data.append(logLine)
				except Exception, msg:
					print "could not parse: %s (%s)" % (line, msg)
			
	def getTimeExtents (self):
		"""
		returns startDate, endDate as time extents (in seconds) for all the records
		read.
		"""
		startDate = time.time()
		endDate = 0
		for item in self:
			startDate = min(startDate, item.timestamp)
			endDate = max(endDate, item.timestamp)
		return startDate, endDate
		
	def getUniqueIps (self):
		if self.ips is None:
			ips=[]
			for item in self:
				ip = item['IP']
				if ip and ip not in ips:
					ips.append(ip)
			self.ips = ips
		return self.ips
			
	def selectLines (self, pred):
		"""
		filters LogLines by provided predicate
		"""
		return filter (pred, self)
			
	def report (self, itemList=None):
		"""
		calls reports on each item in provided itemList (or all lines if itemList is not provided)
		"""
		if itemList is None:
			itemList = self
		for line in itemList:
			line.report()
			
	def toTabDelimited (self):
		headers = ['IP', 'datetime', 'request']
		lines = [];add=lines.append
		add ('\t'.join(headers))
		for logLine in self.data:
			row_data = []
			for field in headers:
				val = logLine[field]
				row_data.append(val)
				print '= ', val
			add ('\t'.join(row_data))
		return '\n'.join (lines)

if __name__ == '__main__':

	
	# path = 'c:/tmp/access_log-ncs.log.2'
	# path = '/home/ostwald/Documents/NSDL/MGR NCS Logs/test.log'
	
	# path = 'test.log'
	# path = 'access_log-ncs.log.3'
	path = '/home/ostwald/Documents/NSDL/Weblogs/cat-logs/cat-1/access_log-cat.log.12'
	lf = LogFile(path)
	print '%s - %s' % (getDateStr(lf.startDate), getDateStr(lf.endDate))
	# lf.report()

