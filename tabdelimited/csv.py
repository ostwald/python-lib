"""
CSV - subclass of TabDelimitedFile

see /Users/ostwald/devel/python/csv !!
"""

import os, sys, re
from tabdelimited import TabDelimitedFile, TabDelimitedRecord

class CsvRecord (TabDelimitedRecord):
	pass
	
class CsvFile (TabDelimitedFile):
	
	record_constructor = CsvRecord
	
	def __init__ (self, data=[], record_constructor=None):
		if record_constructor is None:
			record_constructor = self.record_constructor
		TabDelimitedFile.__init__(self, data, record_constructor)
	
	def accept (self, item):
		"""
		subclasses may specialize this method to filter records
		"""
		return 1
	
	def preprocess (self, filecontents):
		regex = re.compile (',".*?",', re.M | re.S)
		i=0
		j=0
		processed=''
		
		def flatten (s):
			return s.replace('\n',' ').replace('\r',' ')
		
		while i<len(filecontents):
			# print 'i: %d/%d' % (i,len(filecontents))
			m = regex.search(filecontents, i)
			if m:
				# print 'MATCH'
				start = m.start()
				processed += filecontents[i:start]
				# print '-- added before match'
				# print '-- added before match - %s' % filecontents[i:start]
				processed += flatten(m.group())
				# print '-- added flattened match - %s' % flatten(m.group())
				i = m.end()
			else:
				processed += filecontents[i:]
				# print '-- added unmatched remainder - %s' % filecontents[i:]
				i = len(filecontents)
		# print "PRE-PROCESSED: %s" % processed
		return processed
	
	def preprocessOLD (self, filecontents):
		"""
		we assume there are not quotes in data, so all quotes
		surround field values.
		Here we replace line breaks inside filecontents with chr(13)
		"""
		
		def flatten (match):
			return match.group().replace('\n',' ').replace('\r',' ')
		
		regex = re.compile (',".*?",', re.M | re.S)
		
		# sanity check
		if 1:
			m = regex.search(filecontents)
			if m:
				print "match: " + m.group(0)
			else:
				print "NO match"
		
		if 1:
			m = regex.split(filecontents)
			if m:
				print 'm has %d parts' % len(m)
				for i, part in enumerate(m):
					print '\n- %d - %s' % (i, part)
					pass
		
		processed = regex.sub(flatten, filecontents)
		
		# processed = ''
		# within_field = 0
		# for ch in filecontents:
			# if ch in ['\n', '\r'] and within_field:
				# # ch = chr(13)
				# continue
			# if ch == '"':
				# within_field = not within_field
			# processed += ch
			
		return processed
	
	def splitline (self, line):
		"""
		have to handle cases where there is a comma within the field
		"""
		fields=[];add=fields.append
		current_field = ""
		within_field = 0
		for ch in line:
			if ch in ['\n', '\t', chr(13)]:
				continue
			if ch == ',' and not within_field:
				add (current_field)
				current_field = ""
				continue
			if ch == '"':
				within_field = not within_field
			current_field += ch
			
		if current_field:
			add (current_field)
	
		return fields

if __name__ == '__main__':
	path = 'elevations-2011-sample.csv'
	csvFile = CsvFile (path)
	csvFile.read(path)
	print '%d records read' % len(csvFile)
	print csvFile.schema
