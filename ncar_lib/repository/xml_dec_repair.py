import os, sys, codecs, re

# bog_record = 'H:/tmp/STAFF-000-000-001-490.xml'
bog_record = '/home/ostwald/tmp/STAFF-000-000-001-490.xml'
pat = '<?xml version="1.0" encoding="UTF-8" ?>.*'

decStr = '(<\?xml.*\?>)'
headerStr = decStr + '(.*)<'

decPat = re.compile(decStr)
headerPat = re.compile(headerStr)

dowrites = 1

class DeclarationFixer:
	def __init__ (self, path):
		self.path = path
		self.xml = codecs.open (self.path, 'r', 'utf-8').read()
		self.id = os.path.basename(path)[:-4]
		# print "id: %s" % self.id
		self.declaration = self.getDeclaration()
		# print "declaration: %s" % self.declaration
		m = self.headerMatch()
		
		if m:
			#print "FIXED"
			# print m.group()
			self.fixRecord(m)
		else:
			#print "NOT fixing"
			pass

		
	def getDeclaration (self):
		try:
			return decPat.match (self.xml).group(1)
		except:
			raise Exception, "Declaration not found for %s" % self.id
		
	def headerMatch (self):
		return headerPat.match (self.xml)
		
	def fixRecord (self, m):
		fixed = self.xml.replace (m.group(1)+m.group(2), m.group(1)+'\n')
		
		if dowrites:
			fp = codecs.open (self.path, 'w', 'utf-8')
			fp.write (fixed)
			fp.close()
			print "fixed", self.id
		else:
			print "WOULD've fixed", self.id
		
if __name__ == '__main__':
	DeclarationFixer (bog_record)
	
