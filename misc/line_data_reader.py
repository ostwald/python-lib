import os, sys
from UserList import UserList

class LineDataReader (UserList):
	"""
	Reads data from a file
	assumes data items are one-per-line
	reads data items into a list
	"""
	def __init__ (self, data_file):
		UserList.__init__ (self)
		self.data_file = data_file
		raw = open(self.data_file, 'r').read()
		lines = raw.split('\n')
		# print len(lines), 'lines read'
		for line in lines:
			if not line.strip(): continue
			if line[0] == '#': continue
			self.append(line.strip())
			
	def sort(self):
		self.data.sort()
		
	def report(self):
		print "%d items" % len(self)
		for item in self:
			print item		
			
	def write(self):
		fp = open(self.data_file, 'w')
		fp.write ('\n'.join(self.data))
		fp.close()
		print 'wrote to ', self.data_file
			
if __name__ == '__main__':
	LineDataReader('input/originalDRMappings.txt').write()
	
