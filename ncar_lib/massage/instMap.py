
import sys, os
import globals
from UserDict import UserDict

class DupKeyException (Exception):
	pass

class InstMap (UserDict):

	delimiter = '\t'
	failOnError = False
	
	def __init__ (self, path):
		self.path = path
		self.name = os.path.splitext (os.path.split(path)[1])[0]
		UserDict.__init__ (self)
		self.schema = None
		self.read()
		
		
	def parseLine (self, line):
		"""
		remove surrounding quotes from each item in list
		"""
		splits = line.split(self.delimiter)
		parsed = []
		for t in splits:
			if not t is None: t = t.strip()
			if t and len (t) > 1:
				if t[0] == t[-1] and t[0] in ['"', "'"]:
					t = t[1:-1]
			parsed.append(t)
		return parsed
		
	def keys(self):
		k = self.data.keys()
		k.sort()
		return k
		
	def getMappingValues (self, field, unique=True):
		s = [];add=s.append
		for rec in self.values():
			value = getattr (rec, field)
			if value and not unique or not value in s:
				add (value)
		s.sort()
		return s		
		
	def getInstNames (self, unique=True):
		return self.getMappingValues ("instName", unique)
		
	def getOriginalNames (self, unique=True):
		return self.getMappingValues ("original", unique)
		
	def getInstDivs (self, unique=True):
		return self.getMappingValues ("instDiv", unique)
		
		
		
	def read (self):
		print "reading from ", self.name
		lines = open (self.path).read().splitlines()
		errors = []
		## print "%d lines read" % len(lines)
		self.schema = self.parseLine(lines[0])
		#  print "schema: ", self.schema
		for line in lines [1:]:
			try:
				rec = Mapping (self.parseLine(line), self.schema)
				key = rec.original
				if not key: continue
				if self.has_key (key):
					raise DupKeyException, key
				self[key] = rec
			except DupKeyException, msg:
				if self.failOnError:
					errors.append("Duplicate Key: '%s'" % msg)
				
		if (errors):
			print "ERRORS"
			for e in errors:
				print '\t', e
			sys.exit()
			
	def reportMappings (self):
		print '"%s" mappings' % self.name
		for key in self.keys():
			print self[key]
			
	def reportMappingValues (self, field, unique=True):
		u = unique and "unique" or "all"
		print '"%s": %s falues (%s)' % (self.name, field, u)
		for name in self.getMappingValues(field, unique):
			print name
			
class Mapping:
	
	def __init__ (self, data, schema):
		self.schema = schema
		for i, field in enumerate (schema):
			value = None
			if len(data) > i:
				value = data[i]
			setattr (self, field, value)
			
	def __repr__ (self):
		s=[];add=s.append
		add ("\n%s" % self.original)
		for field in self.schema[1:]:
			if getattr(self, field):
				add ("\t%s: %s" % (field, getattr(self, field)))
		return '\n'.join (s)
		
	def __cmp__ (self, b):
		for field in self.schema:
			val = cmp (getattr(self, field), getattr(b, field))
			if val != 0: return val
		return 0
		
def getInstMap (name):
	path = os.path.join (globals.instMaps, name+".txt")
	return InstMap (path)	
		
def getKatyMap ():
	return getInstMap ("katy")
	
def getFaithMap ():
	return getInstMap ("faith")

		
if __name__ == "__main__":
	name = "combo"
	im = getInstMap(name)
	im.reportMappingValues("instName", 1)
