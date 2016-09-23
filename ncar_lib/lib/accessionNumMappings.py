import sys, os, string
from UserDict import UserDict
import globals, webcatUtils

pdfDir = globals.pdf

path = globals.mappingDataPath

class AccessNumMapping (UserDict):
	
	failOnKeyError = True  # fail if there are duplicate accessionNumbers
	failOnValueError = True # fail if there are dup ids
	verbose = False
	
	def __init__ (self, data_path):
		self.data_path = data_path
		UserDict.__init__ (self)
		self._read()
		if self.verbose:
			print "%d records read" % len (self)				
				
	def keys (self):
		"""
		return list of sorted keys
		"""
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def __setitem__ (self, key, value):
		if self.has_key (key):
			msg = "duplicate accessionNum: %s (%s / %s)" % (key, value, self[key])
			if self.failOnKeyError:
				raise KeyError, msg
			elif self.verbose:
				print msg
		if value in self.values():
			msg = "duplicate id: %s (%s)" % (val, key)
			if self.failOnValueError:
				raise ValueError, msg
			elif self.verbose:
				print msg
		self.data[key] = value
			
	def _read (self):
		s = open (self.data_path).read()
		lines = s.splitlines()
		if self.verbose:
			print "%d lines read" % len (lines)
		for line in lines:
			accessionNum, id = map (string.strip, line.split(':'))
			self[accessionNum] = id			

			
if __name__ == '__main__':
	am = AccessNumMapping (path)
	print am['DR000830']
