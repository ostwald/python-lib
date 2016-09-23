""" 
Tool to parse catalina.out files. Specially created to try and get a handle
on what record saves and status changes had occurred within a particular log
file
"""
import os, sys, re, time
# logpath = "dcslogs/catalina.out.20090318.190301"
logpath = "dcslogs/catalina.out.20090722.144716" # most recent
foopath = "foo.out"

class CatalinaParser:
	"""
	reqPat finds a request
	statusPat finds a status request
	"""
	
	reqPat = "(?P<timestamp>[\w: ,]+?)AuthorizationFilter:"
	statusPat = "(?P<timestamp>[\w: ,]+?)AuthorizationFilter:.*?status.do"
	
	def __init__ (self, path):
		self.reqEx = re.compile(self.reqPat)
		self.statusEx = re.compile(self.statusPat)
		self.rawdata = open(path).read()
		self.requests = self.parse()
		
	def filterRequests (self, param, value):
		"""
		filter the requests to only include those that have a request paramter having specified value
		"""
		filtered = []
		for request in self.requests:
			if request.params.has_key(param) and request.params[param] == value:
				filtered.append (request)
		return filtered
		
	def parse (self):
		"""
		return 'blobs' that consist of all text between beginning of a status request
		and the start of the next request
		"""
		lines = self.rawdata.split('\n') # 
		collecting = 0
		blobLines = []
		blobs = []
		currentRequest = None
		requests = []
		for line in lines:
			reqMatch = self.reqEx.match (line)	
			if reqMatch and currentRequest:
				currentRequest = None
				
			statusMatch = self.statusEx.match (line)
			if statusMatch:
				currentRequest = Request (statusMatch.group("timestamp"))
				requests.append (currentRequest)
				

			if currentRequest:
				currentRequest.add (line)
		return requests
		
class Request:
	
	paramRegEx = re.compile ("\t(.*?):[ ]+?(.*)")
	
	def __init__ (self, timestamp):
		self.timestamp = timestamp
		self.lines = []
		self.params = {}
	
	def add (self, line):
		self.lines.append (line)
		m = self.paramRegEx.match (line)
		if m:
			self.params[m.group(1)] = m.group(2)
			# print "%s -> %s" % (m.group(1), m.group(2))
			
	def __repr__ (self):
		# return '\n'.join (self.lines)
		s=[];add=s.append
		add (self.lines[0])
		for key in self.params.keys():
			if key in ['status', 'recId', 'command']:
				add ("\t%s: %s" % (key, self.params[key]))
		return '\n'.join (s)

def reporter ():
	"""
	write status changes to tab-delimited file that can be read in xls
	header: timestamp, recId, status
	"""
	
	logdir = "dcslogs"	
	
	## set up the report
	lines=[];add=lines.append
	add ('\t'.join (['timestamp', 'recId', 'status']))
	
	filenames = os.listdir (logdir)
	filenames.sort()
	for filename in filenames:
		logpath = os.path.join (logdir, filename)
		if not os.path.isfile(logpath): continue
		
		parser = CatalinaParser (logpath)
		requests = parser.filterRequests ('command', 'updateStatus')
		print "%s - %d update status requests" % (filename, len(requests))
		
		for r in requests:
			# get rid of the pesky time zone name which for some reason python can
			# parse (MDT, MST)
			ts = r.timestamp.strip()[:-4]
			# print ts
			tup = time.strptime (ts, "%b %d, %Y %I:%M:%S %p")
			# print time.asctime(tup)
			date = time.strftime ("%m/%d/%Y %I:%M:%S %p", tup)
			add ('\t'.join ([date, r.params['recId'], r.params['status']]))
		
	report = '\n'.join (lines)
	outfile = 'report.txt'
	fp = open(outfile, 'w')
	fp.write(report)
	fp.close()
	print "wrote report to " + outfile
	
def tester():
	parser = CatalinaParser (logpath)
	requests = parser.filterRequests ('command', 'updateStatus')
	
	lines=[];add=lines.append
	add ('\t'.join (['timestamp', 'recId', 'status']))
			
	print '%d status requests found' % len(requests)
	for r in requests:
		# print r, '\n----------------'
		add ('\t'.join ([r.timestamp, r.params['recId'], r.params['status']]))
		
	report = '\n'.join (lines)
	# print report
		
	if 1:
		outfile = 'report.txt'
		fp = open(outfile, 'w')
		fp.write(report)
		fp.close()
		print "wrote report to " + outfile
			
if __name__ == '__main__':
	reporter()

