"""
Fix records where the root element is on the same page as the xml declaration
e.g., <?xml version="1.0" ?><record
"""

import os, sys, codecs, re


# pat = '<?xml version="1.0" encoding="UTF-8" ?>.*'

decStr = '(<\?xml.*\?>)'
# matches a bogus header
bogusHeaderStr = decStr + '(.*?)[\S]+?'

decPat = re.compile(decStr)
bogusHeaderPat = re.compile(bogusHeaderStr)

default_dowrites = 1
default_encoding = 'utf-8'

class DeclarationFixer:
	def __init__ (self, path, dowrites=None, encoding=None):
		self.dowrites = dowrites or default_dowrites
		self.path = path
		self.encoding = encoding or default_encoding
		self.xml = codecs.open (self.path, 'r', self.encoding).read()
		self.id = os.path.basename(path)[:-4]
		# print "id: %s" % self.id
		self.declaration = self.getDeclaration() # throws exception if there isn't a declaration
		# print "declaration: %s" % self.declaration
		
		m = bogusHeaderPat.match (self.xml)
		self.isbogus = 0
		
		if m:
			#print "FIXED"
			# print 'matched on "%s"' % m.group()
			self.isbogus = 1
			self.fixRecord(m)
		else:
			#print "NOT fixing"
			pass

		
	def getDeclaration (self):
		try:
			return decPat.match (self.xml).group(1)
		except:
			raise Exception, "Declaration not found for %s" % self.id
		
	def fixRecord (self, m):
		fixed = self.xml.replace (m.group(1)+m.group(2), m.group(1)+'\n')
		
		if self.dowrites:
			fp = codecs.open (self.path, 'w', self.encoding)
			fp.write (fixed)
			fp.close()
			# print "fixed", self.id
		else:
			print "DeclarationFixer WOULD've fixed", self.id
			# print fixed.encode('utf-8')
		
if __name__ == '__main__':
	bog_record = "/home/ostwald/python-lib/ndr/id_updater/bogus-record.xml"
	fixer = DeclarationFixer (bog_record, 1)
	print 'fixer is bogus? ', fixer.isbogus
	
