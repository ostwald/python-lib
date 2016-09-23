import os, sys, urlparse, cgi, time
from UserDict import UserDict

class TallyItem:
	"""
	line from data file. tab-delimited: url | timestamp
	"""
	def __init__ (self, line):
		splits = map (lambda x: x.strip(), line.split('\t'))
		self.url = splits[0]
		self.timestamp = float(splits[1])
		
		if 0:
			print '\n'
			print 'url: ', self.url
			print 'time: ', self.timestamp
			
		self.params = self.getParamMap()
		self.q = self.getSearchTerm()
		
	def getParamMap (self):
		qtuple = urlparse.urlparse(self.url)
		query = qtuple[4]
		# print 'query: ', query
		return cgi.parse_qs(query)
		
	def getSearchTerm (self):
		if self.params.has_key('q'):
			return self.params['q'][0]

class Tally (UserDict):
	
	verbose = 0
	
	def __init__ (self, path):
		UserDict.__init__ (self)
		self.path = path
		self.startDate = time.time()
		self.endDate = 0
		self.read ()

	def read (self):
		if os.path.isdir(self.path):
			for filename in os.listdir(self.path):
				self.read_file (os.path.join (self.path, filename))
		else:
			self.read_file (self.path)
		
	
			
	def read_file(self, file_path):
		if self.verbose:
			print 'reading', file_path
		s = open(file_path, 'r').read()
		for line in filter (None, s.split('\n')):
			self.tally (TallyItem(line))
			
	def tally (self, item):
		q = item.q
		if not q:
			return
		if self.has_key (q):
			val = self[q]
		else:
			val = []
		val.append (item.timestamp)
		self[q] = val
		self.startDate = min(self.startDate, item.timestamp)
		self.endDate = max(self.endDate, item.timestamp)
		
	def report (self):
		for key in self.keys():
			print '%s (%d)' % (key, len(self[key]))
	
class SortedReportItem:
	
	def __init__ (self, term, cnt):
		self.term = term
		self.cnt = cnt
		
	def __cmp__ (self, other):
		i = cmp(self.cnt, other.cnt)
		if i != 0:
			return -i
		return cmp(self.term.lower(), other.term.lower())
			
class SortedReport:
	
	date_fmt = '%m/%d/%Y %H:%M:%S'
	
	explanation = """  List of unique search terms and occurrences for each.
  Terms are sorted first by occurrences, then alphabetically"""
	
	def __init__ (self, tally):
		sortlist = [];add=sortlist.append
		for key in tally.keys():
			add (SortedReportItem (key, len(tally[key])))
			
		sortlist.sort ()
		header = "Search Term Report (%s - %s)" % (self.getDateStr(tally.startDate), self.getDateStr(tally.endDate))
		print '\n%s\n%s\n%s' % (header, self.explanation, '-'*len(header))
		for item in sortlist:
			print '%s (%d)' % (item.term, item.cnt) 
		
	def getDateStr (self, secs):
		return time.strftime (self.date_fmt, time.localtime(secs))
			
			
if __name__ == '__main__':
	# mypath = 'msp2data/test.log_msp2_data'
	# mypath = 'msp2data/access_log-ncs.log.3_msp2_data'
	mypath = 'msp2data'
	tally = Tally(mypath)
	SortedReport (tally)
