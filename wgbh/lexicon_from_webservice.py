"""
gets lexicon terms via WGBH_Client.get_term_catalogue_with_id
"""

from rpcclient import WGBH_Client
from UserDict import UserDict
from UserList import UserList

class Lexicon (UserList):
	
	def __init__ (self):
		
		client = WGBH_Client()
		client.verbose = 0
		UserList.__init__ (self, client.get_term_catalogue_with_id())
		print "%d lexicon items read" % len (self)
		
	def reportTermSegments (self):
		lengths = []
		for item in self:
			mylen = len (item[0].split ('::'))
			if not mylen in lengths:
				lengths.append (mylen)
				
		print lengths
	
	def write (self, path):
		fp = open (path, 'w')
		lines = []
		for item in self:
			lines.append (str(item))
		fp.write ('\n'.join(lines))
		fp.close()
		print "write to %s" % path
		
if __name__ == '__main__':
	lex = Lexicon()
	lex.reportTermSegments()
	lex.write ("data/lexicon.txt")
			





