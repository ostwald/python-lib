"""
Awstats DataDir - contains database files written by Awstats.

Can we use these files to determine which log files have been processed??
"""
import os, sys, re, time
from jloFS import JloFile, JloDirectory
from jloFS import myglobals

dirDataPath = '/Users/ostwald/devel/NSDL/awstats/DirData'

class AWFile (JloFile):
	
	def __init__ (self, path, level=0):
		JloFile.__init__ (self, path, level)
		self.firstTime = None
		self.lastTime = None
		self.lastLine = None
		self.parseContent()
		
	def parseContent(self):
		self.lines = filter (None, map (lambda x:x.strip(), self.getContent().split('\n')))
		# print '%d lines read' % len(self.lines)
		
		# find the line with "
		general_start = -1
		lines_to_get = -1
		for i, line in enumerate(self.lines):
			if line.startswith ("BEGIN_GENERAL"):
				lines_to_get = int(line.split(' ')[1])
				# print 'BEGIN_GENERAL found (%d)' % lines_to_get
				# print ' i is %d' % i
				general_start = i + 1
				break
				
		general_fields = {}
				
		if general_start > -1 and lines_to_get > 0:
			
			for line in self.lines[general_start:general_start + lines_to_get]:
				# print line
				all_fields = line.split(' ')
				field_name = all_fields[0]
				fields = all_fields[1:]
				# print 'field_name: %s' % field_name
				# print '\t%s' % fields
				general_fields[field_name] = fields
				
		try:
			if general_fields.has_key('FirstTime'):
				aw_timestmp = general_fields['FirstTime'][0]
				self.firstTime = self.aw_timestampToSecs (aw_timestmp)
		except:
			print "could not get first time from '%s'" % general_fields['FirstTime']
			self.firstTime = 0
			
		try:
			if general_fields.has_key('LastTime'):
				aw_timestmp = general_fields['LastTime'][0]
				self.lastTime = self.aw_timestampToSecs (aw_timestmp)
		except:
			print "could not get last time"	
			self.lastTime = 0
			
		try:
			if general_fields.has_key('LastLine'):
				aw_timestmp = general_fields['LastLine'][0]
				self.lastLine = self.aw_timestampToSecs (aw_timestmp)
		except:
			print "could not get last time"	
			self.lastLine = 0
	
	def aw_timestampToSecs (self, awts):
		format = "%Y%m%d%H%M%S"
		t = time.strptime(awts, format) 
		return time.mktime(t	)
	
	def __repr__ (self):
		"""
		Generic string representation for File system objects. 
		Indented by "self.level"
		"""
		# return ("%s %s" % (self.name, self.ppDate (self.modtime)))	
		label = self.name
		if self.islink:
			label = "%s (link)" % label
		if self.isalias:
			label = "%s (alias)" % label
		s = ''
		if 0:
			s = "%s%s (%s)" % (myglobals.getIndent(self.level), 
								   self.compactDate (self.modtime),
								   self.name)
			s += "\n\t%s - "
		s += "%s - %s (%s)" % (self.compactDate(self.firstTime),
								  self.compactDate(self.lastTime),
								  self.compactDate(self.lastLine))
		return s;

class DirData (JloDirectory):
	
	domainPat = re.compile ('awstats[\d]*.([\S]*).(tmp|txt)[\d]*')
	
	def __init__ (self, domain, path, level=0):
		self.domain = domain
		JloDirectory.__init__(self, path, level)
		
	def getFile (self, path):
		return AWFile (path, self.level+1)
		
	def getDomain(self, filename):
		m = self.domainPat.match (filename)
		if m:
			return m.group(1)
		return None
		
	def _accept_file(self, filename):
		no_tmps = False
		if not JloDirectory._accept_file(self, filename):
			return False
		if no_tmps and filename.find('tmp') != -1:
			return False
		## return filename.find(self.domain) != -1
		return self.getDomain(filename) == self.domain
	
def dirDataTester (domain):
	dirData = DirData (domain, dirDataPath)

	for file in dirData.dir (attr="firstTime", ascending=0):
		print file
		
def awFileTester ():
	file = 'awstats112013.strandmaps.nsdl.org.txt'
	path = os.path.join (dirDataPath, file)
	print path
	awFile = AWFile (path)
	awFile.parseContent()
	# print "FirstTime: " + awFile.FirstTime[0]
	# print "firstTime: " + awFile.compactDate(awFile.firstTime)
	# print "lastTime: " + awFile.compactDate(awFile.lastTime)
	# print "lastLine: " + awFile.compactDate(awFile.lastLine)	
	print awFile
		
if __name__ == '__main__':
	domain = 'nsdl.org'
	
	if len(sys.argv) > 0:
		domain = sys.argv[1]
	
	dirDataTester(domain)
	# awFileTester()
