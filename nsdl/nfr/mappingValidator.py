"""
test mappings files for uniqueness of keys and values
- this implementation is pretty slow compared with validator module
"""
import os, sys
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from UserList import UserList

class UniqueList(UserList):
	
	def append (self, item):
		if item in self.data:
			raise "Exception", 'Duplicate Item: %s' % item
		self.data.append(item)

class ResourceMapping (TabDelimitedRecord):
	
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		# print "%s -> %s" % (self['resourceHandle'], self['resourceUrl'])
		if not self['resourceUrl']:
			sys.exit()
				
class Validator (TabDelimitedFile):
	
	linesep ="\r\n"
	
	def __init__ (self, path):
		TabDelimitedFile.__init__ (self, entry_class=ResourceMapping)
		self.read (path)

	def validate(self):
		print '\nvalidating...'
		handles = UniqueList()
		urls = UniqueList()
		
		for i, mapping in enumerate(self):
			handles.append(mapping['resourceHandle'])
			urls.append(mapping['resourceUrl'])
			
			if i > 0 and i % 1000 == 0:
				print '%d/%d' % (i, len(self))

if __name__ == '__main__':
	path = '/devel/ostwald/tmp/resourceMappings.txt'
	validator = Validator(path)
	print 'validator has %d entries to validate' % len(validator)
	validator.validate()
