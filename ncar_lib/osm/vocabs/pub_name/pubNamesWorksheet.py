import string, os, sys, codecs
from xls import WorksheetEntry, XslWorksheet
from dds_pubName_search import PubNameRecordGetterException, PubNameRecordGetter

data_worksheeet_path = "PubNames_ADD_20101202.txt"

class PubNameEntry (WorksheetEntry):
	
	"""
	an entry from the spread sheet
	"""
	
	def __init__ (self, textline, schema):
		WorksheetEntry.__init__(self, textline, schema)
		if 0 and textline.find ("25th Conference on Severe Local Storms") != -1:
			print textline
			self.showChars (textline)
			sys.exit()
			debug = 1
		else:
			debug = 0
		self.term = self['Correct']
		self.badterm = self['Incorrect']
		self.pubType = self['pubType']
		self.addto = []
		buf = self['Add to'].strip()
		
		
		
		if buf:
			# debug = 0
			if debug:
				self.showChars (buf)
				# sys.exit()
			self.addto = map (string.strip, buf.split(chr(10)))
			
		# if self.badterm:
		#	self.findBadPubName()
		
	def showChars (self, buf):
		for ch in buf:
			print "%s %d" % (ch, ord(ch))
		
	def findBadPubName (self):
		"""
		search for osn records having this bad term
		
		eventually, we might call REPLACE pubName on these records ...
		"""
		try:
			dds_client = PubNameRecordGetter (self.badterm)
			if dds_client.results:
				print "%d results found with '%s'" % (len (dds_client.results), self.badterm)
				for result in dds_client.results:
					print ' - ', result.recId
		except PubNameRecordGetterException:
			print sys.exc_info()[1], self.badterm

class PubNamesWorkSheet (XslWorksheet):
	
	# linesep = "\n"
	
	def __init__ (self, path):
		XslWorksheet.__init__ (self,entry_class=PubNameEntry)
		self.read (path)
		print "%d records read" % len(self)
		
	def read_linesOFF (self, path):
		"""
		get lines to be processed.
		this method can be overridden to skip processing of lines if desired
		(e.g., the first n lines)
		"""
		dir, filename = os.path.split (path)
		root, ext = os.path.splitext (filename)
		f = codecs.open(path,'r','utf-8')
		s = f.read()
		lines = s.split(self.linesep)
		f.close()
		return lines
		
	def report(self):
		print "%d records read" % len(ws)
		for rec in ws:
			print "\n************* ", rec.term
			for i in rec.addto:
				print ' - ', i
				
if __name__ == '__main__':
	ws = PubNamesWorkSheet (data_worksheeet_path)
	
