"""
this module faster than mappingValidator
"""
import sys, os, re

handlePat = re.compile ("2200/[0-9]*T")

class Validator:
	
	default_path = None
	
	def __init__ (self, path=None):
		self.path = path or self.default_path
		self.lines = self.readlines()

	def readlines (self):
		lines = open(self.path, 'r').read().split('\r\n')
		lines = filter (lambda x:x.strip(), lines)
		print '%d lines read' % len (lines)
		return lines

	def findMatchingHandles (self):
		handles = []
		linesCnt = len(self.lines)
		for i,line in enumerate(self.lines):
			handle = line.split('\t')[0]
			if handle in handles:
				raise Exception, "dup handle: %s" % handle
			else:
				handles.append(handle)
			if i % 1000 == 0 and i > 0:
				print '%d/%d' % (i, linesCnt)
				
	def findBogusHandles (self):
		bogCount = 0
		linesCnt = len(self.lines)
		for i,line in enumerate(self.lines):
			handle = line.split('\t')[0]
			if not handlePat.match(handle):
				print "BOGUS: %s" % handle
				bogCount += 1
			if i % 1000 == 0 and i > 0:
				print '%d/%d' % (i, linesCnt)
		print "%d bogus handles found" % bogCount

class ResourceValidator (Validator):
				
	default_path = '/home/ostwald/tmp/resourceMappings.txt'
	
	def findMatchingUrls (self):
		urls = []
		linesCnt = len(self.lines)
		for i,line in enumerate(self.lines):
			url = line.split('\t')[1].strip()
			if url in urls:
				raise Exception, "dup url: %s" % url
			else:
				urls.append(url)
			if i % 1000 == 0 and i > 0:
				print '%d/%d' % (i, linesCnt)
				
class MetadataValidator(Validator):
			
	default_path = '/home/ostwald/tmp/metadataMappings.txt'
	
	def findMatchingKeys (self):
		keys = []
		linesCnt = len(self.lines)
		for i,line in enumerate(self.lines):
			splits = map (lambda x:x.strip(), line.split('\t'))
			id = splits[2]
			setspec = splits[1]
			key = id + ' - ' + setspec
			if key in keys:
				# raise Exception, "dup key: %s" % key
				print "dup key: %s" % key
			else:
				keys.append(key)
			if i % 1000 == 0 and i > 0:
				print '%d/%d' % (i, linesCnt)

	def findSetSpecs (self):
		setspecs = []
		linesCnt = len(self.lines)
		for i,line in enumerate(self.lines):
			splits = map (lambda x:x.strip(), line.split('\t'))
			setspec = splits[1]
			if setspec == '1201216476279':
				print line
			if setspec in setspecs:
				pass
			else:
				# print setspec
				setspecs.append(setspec)
			if 0 and i % 1000 == 0 and i > 0:
				print '%d/%d' % (i, linesCnt)
		return setspecs
	
if __name__ == '__main__':
	validator = MetadataValidator()
	# validator = ResourceValidator()
	# validator.findBogusHandles()
	# validator.findMatchingKeys ()
	# validator.findMatchingHandles ()
	sets = validator.findSetSpecs()
	for set in sets:
		print set
		
	if '1201216476279' in sets:
		print 'Collection of Collection Records is HERE!'
	else:
		print 'you are screwed'
	
	
