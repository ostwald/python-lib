import sys, os, re
from weblog import LogFile, LogLine

class Msp2Entry (LogLine):
	
	def __init__ (self, line):
		LogLine.__init__ (self, line)
		self.referer = self['referrer']
	
	def getRefererData (self):
		return '\t'.join([self.referer, str(self.timestamp)])

class Msp2logTool (LogFile):
	
	debug = 0
	do_writes = 1
	line_class = Msp2Entry
	
	def getMsp2Lines (self):
		pred = lambda x:x['referrer'] and x['referrer'].find('www.msteacher2.org') != -1
		return self.selectLines(pred)
			
	def showMsp2Referers (self, verbose=0):
		msp2items = self.getMsp2Lines()
		print "MSP2 referers (%d)" % len(msp2items)
		if verbose:
			for item in msp2items:
				print item['referrer']
		
	def getDataFilePath (self):
		srcdir, srcname = os.path.split(self.path)
		destdir = 'msp2data'
		dest = os.path.join (destdir, srcname+'_msp2_data')
		print 'dest: ', dest
		return dest
				
	def writeMsp2Referers (self, path=None):
		
		if path is None:
			path = self.getDataFilePath ()
			
		msp2lines = self.getMsp2Lines()
		content = '\n'.join( map (lambda x:x.getRefererData(), msp2lines))
		print 'writing %d msp2 referer queries' % len (msp2lines)
		
		if not self.do_writes:
			print 'would have written to %s' % path
			print content
			return

		fp = open (path, 'w')
		fp.write (content)
		fp.close()
		print 'wrote msp2lines to %s' % path
			
def tester():
	# path = 'c:/tmp/access_log-ncs.log.2'
	# path = '/home/ostwald/Documents/NSDL/MGR NCS Logs/test.log'
	
	# path = 'test.log'
	path = 'access_log-ncs.log.3'
	
	lf = Msp2logTool(path)
	# lf.showMsp2Referers(1)
	lf.writeMsp2Referers()
	
def processDir (basedir):
	for filename in os.listdir(basedir):
		if not filename.startswith ("access"):
			print 'skipping', filename
			continue
		path = os.path.join (basedir, filename)
		print path
		Msp2logTool(path).writeMsp2Referers()
		
if __name__ == '__main__':

	baseDir = '/home/ostwald/Documents/NSDL/MGR NCS Logs/logs'
	processDir(baseDir)


