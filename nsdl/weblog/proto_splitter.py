import os, sys, time
from month_splitter import MonthSplitter
from log_file import LogFileEntry

class ProtoSplitter (MonthSplitter):
	"""
	MonthSpliter splits files into their pieces before writing them to disk
	ProtoSplitter will write to disk in smaller batches. 
	
	Hopothesis - there will be some batch size, maybe depending on the size of
	log file to be processeed, at which it will be faster to write in batches.
	The assumption is that storing very large lists of entries in memory bogs
	the process down by holding so much in memory.
	"""

	dowrites = 1
	write_buffer_size = 500
	verbose = 1
	strict = False
	
	def split(self):
		"""
		write to disk in configurable batch sizes - write_buffer_size
		"""
		current_month = None
		entries = []
		self.current_split_file = None
		self.entry_count = 0

		for i,line in enumerate(open(self.path,'r')):
			if not line.strip():
				break
			try:
				entry = LogFileEntry(line.strip())
			except Exception, e:
				# msg = 'COULD NOT PARSE: %s\nCAUSE: %s' % (line, e)
				msg = 'COULD NOT PARSE line %d' % i
				if self.strict:
					raise Exception, msg
				else:
					print msg 
					continue
			mydate = entry.month
			# print '%d/%d/%d' % (entry.month, entry.timestamp[2], entry.timestamp[0])
			if mydate == current_month:
				entries.append(entry)
			else:
				if entries:
					self.appendEntries (entries)
				self.current_split_file = None
				current_month = mydate
				entries = []

			if i and i % self.report_interval == 0:
				print i
				
			if i and i % self.write_buffer_size == 0:
				self.appendEntries (entries)
				entries = []
				# time.sleep (0.2)
		if entries:
			if self.dowrites:
				self.appendEntries(entries)
			else:
				print 'would have written %d entries with date = %s' % (len(entries), current_month)


	def appendEntries (self, entries):
		if not entries:
			return
		self.entry_count = self.entry_count + len(entries)
		if self.current_split_file is None:
			self.current_split_file = self.initializeSplitFile(entries)
			return
			
		if self.dowrites:
			fp = open(self.current_split_file, 'a')
			fp.write ('\n'.join(map(lambda x:x.data, entries)) + '\n')
			fp.close()
			if self.verbose:
				# print 'wrote to', self.current_split_file
				sys.stdout.write('.')
		else:
			print 'WOULD HAVE written to %s' % self.current_split_file
				
	def initializeSplitFile (self, entries):
		timestamp = entries[0].timestamp
		# filename = '%s-%d%02d01' % (self.baseFilename, timestamp[0], timestamp[1]+1)
		filename = '%s-%s' % (self.baseFilename,self.getDateTag(timestamp))
		destPath = os.path.join (self.destDir, filename)
		if self.dowrites:
			fp = open (destPath, 'w')
			fp.write ('\n'.join(map(lambda x:x.data, entries)) + '\n')
			fp.close()
		else:
			print 'WOULD HAVE initialized and written to %s' % destPath		
		return destPath

if __name__ == '__main__':
	
	# nsdl.org_access_log_10_25_1022'  # rs1
	# nsdl.org_access_log_frag'  # acorn
	filename = 'harvest.nsdl.org_access_log'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		print 'filename', filename

	src = '/Users/ostwald/devel/NSDL/logs/tmp/search_queries.log.20131101'
	dest = '/Users/ostwald/devel/NSDL/logs/splits_output/testerFOO.log'

	log = ProtoSplitter (src, dest)
	print "entries processeed %d" % log.entry_count
	print "write_buffer_size: %d" % log.write_buffer_size
