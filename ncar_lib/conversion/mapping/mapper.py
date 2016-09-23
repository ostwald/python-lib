import sys, os
from UserDict import UserDict
from ncar_lib.lib import globals
import samples

default_mapping_data = os.path.join (globals.docBase, 'InstNameDiv-mapping/mapping-source.txt')

class Mapper (UserDict):
	
	def __init__ (self, mapping_data=default_mapping_data):
		UserDict.__init__ (self)
		self.read(mapping_data)
		
	def read (self, mapping_data):
		s = open(mapping_data).read()
		splits =  s.split ("\n\n")
		## splits = map (lambda x:x.strip(),splits)
		for s in splits:
			s = s.strip()
			if s:
				# print MapParser (s.strip())
				for m in MapParser(s).mappings:
					key = m.original
					if self.has_key(key):
						msg = "Duplicate Key: '%s'" % key
						if 1: # fail on dups
							raise Exception, msg
						else:
							print msg
							continue
					self[key] = m
						
	def keys (self):
		sorted = self.data.keys()
		sorted.sort
		return sorted
						
	def getMapping (self, key):
		if self.has_key (key):
			return self[key]
		else:
			return None
		
	def getUniqueInstNames (self):
		uniqueInstNames = []
		for key in self.keys():
			mapping = self[key]
			for name in mapping.instNames:
				if not name in uniqueInstNames:
					uniqueInstNames.append (name)
		uniqueInstNames.sort()
		return uniqueInstNames

	def getUniqueInstDivs (self):
		uniqueInstDivs = []
		for key in self.keys():
			mapping = self[key]
			for name in mapping.instDivs:
				if not name in uniqueInstDivs:
					uniqueInstDivs.append (name)
		uniqueInstDivs.sort()
		return uniqueInstDivs
			
	def report (self):
		if 0:
			for key in self.keys():
				print self[key]
				
		print "\nInst Names"
		for name in self.getUniqueInstNames():
			print "\t'%s'" % name
			
		print "\nInst Divisions"
		for name in self.getUniqueInstDivs():
			print "\t'%s'" % name
			
class Mapping:
	
	def __init__ (self, original, instNames, instDivs):
		self.original = original
		self.instNames = instNames
		self.instDivs = instDivs
		self.isIdentity = not (self.instNames or self.instDivs)
		
	def __repr__ (self):
		s=[];add=s.append
		print ("")
		add ("%s" % self.original)
		if self.isIdentity:
			add ("\t IDENTITY mapping")
		else:
			for name in self.instNames:
				add ("\t instName: %s" % name)
			for div in self.instDivs:
				add ("\t instDiv: %s" % div)
		return "\n".join (s)
				
class MapParser:
	
	def __init__ (self, input):
		self.values = []
		self.instNames = []
		self.instDivs = []
		self.identityMapping = False
		self.nullMapping = False
		self.parse (input)
		self.mappings = self._make_mappings()
		
	def _make_mappings (self):
		mappings = []
		if not self.nullMapping:
			for val in self.values:
				mappings.append (Mapping (val, self.instNames, self.instDivs))
		return mappings
		
		
	def parse (self, input):
		pat = "map to:"
		splits = input.split (pat)
		self._parseValues (splits[0])
		if len (splits) == 1:
			self.identityMapping = True
			return
		
		mapping = splits[1].strip()
		if mapping == "null":
			self.nullMapping = True
			return
		
		self._parseMapping (mapping)
	
	def _parseValues (self, data):
		splits = data.split ("\n")
		values = []
		pat = "value:"
		for v in splits:
			v = v.strip()
			if v:
				if v.startswith (pat):
					v = v[len(pat):].strip()
				values.append(v)
		self.values = values
		
	def _parseMapping (self, mapping):

		# print "mapping:", mapping
		for line in mapping.split("\n"):
			parts = line.split(':')
			# print "parts:", parts
			if len(parts) < 2:
				msg = "unparsable mapping line: '%s'" % line
				raise Exception, msg
			parts = map (lambda x:x.strip(),parts)
			if parts[0] == "instName":
				self.instNames.append (':'.join(parts[1:]))
			elif parts[0] == "instDiv":
				self.instDivs.append (':'.join(parts[1:]))
			else:
				msg = "unparsable mapping line: '%s'" % line
				raise Exception, msg
			
	def __repr__ (self):
		s=[];add=s.append
		add ("--------------------\n")

		for val in self.values:
			add ("%s" % val)
		if self.identityMapping:
			add ("\t IDENTITY mapping")
		if self.nullMapping:
			add ("\t NULL Mapping")
		if not (self.identityMapping or self.nullMapping):
			for name in self.instNames:
				add ("\t instName: %s" % name)
			for div in self.instDivs:
				add ("\t instDiv: %s" % div)
		return "\n".join (s)
		
def allSamplesTest ():
	for m in samples.allMappings:
		print "\n", m
		print MapParser (getattr (samples, m))	
if __name__ == "__main__":
	# print MapParser (samples.multiMapping)
	# allSamplesTest()
	m = Mapper()
	m.report()
	# print m.getMapping ("Computing Facility")


