import os, sys
from JloXml import RegExUtils
import re

class XmlFormatter:
	
	def __init__ (self, rec):
		self.rec = rec
		
	def getTagPat (self):
		tagPatStr = r"<([A-Za-z-0-9_\-\:]+).*?>"
		return re.compile (tagPatStr, re.DOTALL)

	def isLeaf (self, match):
		"""
		does this element have any children?
		"""
		tagContent = match.group(1)
		m = self.getTagPat().search(tagContent)
		return m is None

	def fixLeaf (self, tagSetMatch):
		content = tagSetMatch.group(1)
		return tagSetMatch.group(0).replace (content, content.strip())

	def pp (self):
		"""
		use 
		"""
		tagPat = self.getTagPat()
		i = 0 # index into the original xml
		s = self.rec.__repr__()
		print "pp processing %d lines" % len (s.split('\n'))
		reps = 0
		buff = ""
		while i <= len(s):
			m = tagPat.search (s,i)
			if m is None:
				buff += s[i:]
				i = len(s)
			#	print 'pattern not found'
				break

			else:
				j = m.start()
				buff += s[i:j]

				# print 'pattern found (%d): "%s"' % (j, m.group(1))
				tag = m.group(1)
				tagSet = RegExUtils.getTagPattern (tag).match(s, j)
				if tagSet:
					# print tagSet.group(1)  # this is the content of this tagSet
					if self.isLeaf (tagSet):
					#	print "%s is a leaf" % tag
						fixedLeaf = self.fixLeaf  (tagSet)
						# print 'fixed leaf: "%s"' % fixedLeaf
						buff += fixedLeaf 
						i=tagSet.end()

					else:
##						print "%s is NOT a leaf" % tag
						buff += s[j]
						i = j + 1
					
				else:
					# we have an empty tag (e.g., <children/>), just add it to buff and continue
					buff += m.group()
					i = j + len(m.group())
						
##				print 'set i to %d' % i

			reps += 1
			if reps % 10 == 0:
				# print dot every once in a while to show progress
				sys.__stderr__.write('.')
				# print "%d/%d" % (i, len(s))
			if reps > 50000:
				print "breaking because limit has been reached!"
				sys.exit()
		
		return '<?xml version="1.0" encoding="UTF-8" ?>\n%s' % buff.strip()
	
def pp (path):
	from JloXml import XmlRecord
	rec = XmlRecord (path=path)
	prettyPrinted = XmlFormatter(rec).pp()
	print prettyPrinted
		
if __name__ == '__main__':
	pp ('soapEnvelope.xml')
	
