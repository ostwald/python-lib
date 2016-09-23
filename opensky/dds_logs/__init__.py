import os, sys, re, time
from weblog import LogLine, LogFile, getDateStr

class DDSLogLine (LogLine):
	
	def parse (self):
		line = self.line.strip()
		self.startField()
		# print line
		i = 0
		while i < len(line):
			# print '\n',s
			ch = line[i]
			# print '"%s"' % ch
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
					self.cur_field = self.cur_field + ch
				
					
			# we're not a start character while we're between fields
			else:  # we're in a field
				if ch == ' ':
					self.endField()
				else:
					self.cur_field = self.cur_field + ch
			i = i + 1

		self.endField()

class DDSLogFile (LogFile):
	debug = 0
	line_class = DDSLogLine
	schema_fields = ['vh', 'IP', 'clientId', 'userId', 'datetime', 'request', 'HTTP status',
		  'size', 'referrer', 'agent']
	
	
	def filter (self, filterfn):
		return filter (None, filter (filterfn, self.data))
	
if __name__ == '__main__':
	# logdir = '/Users/ostwald/devel/opensky2/library-dds-weblogs/'
	logdir = '/Users/ostwald/Documents/Work/OpenSky/nldr_logs/library-dds-weblogs/' # purg
	filename = 'access.log'	
	
	path = os.path.join (logdir, filename)
	lf = DDSLogFile(path)
	# print '%s - %s' % (getDateStr(lf.startDate), getDateStr(lf.endDate))
	# lf.report()
	if 1:
		fname = "TD.txt"
		td = lf.toTabDelimited()
		fp = open(fname, 'w')
		fp.write (td)
		fp.close()
		print 'wrote to',fname
