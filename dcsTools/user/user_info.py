import os, sys, re
from UserList import UserList
from HyperText.HTML import *


"""
Simple reader for DCS User records (using regular expressions)
"""


## userdir = "C:/Program Files/Apache Software Foundation/Tomcat 5.5/var/dcs_conf/users"
## userdir = "H:/Documents/NSDL/TransitionToLdap/ncs-users-2009-11-02"

# userdir = "H:/Documents/NCAR Library/Transition to UCAS/users"

def findTag (s, tag):
	pat = re.compile ("<%s>(.*?)</%s>" % (tag, tag), re.DOTALL | re.MULTILINE)
	m = pat.search (s)
	if m:
		return m.group(1).strip()
	else:
		return None

class User:
	attrs = ['username', 'firstname', 'lastname', 'department', 'institution', 'email']
	def __init__ (self, path):
		s = open (path, 'r').read()
		
		for attr in self.attrs:
			setattr (self, attr, findTag (s, attr))

	def __repr__ (self):
		s=[];add=s.append
		add ("")
		for attr in self.attrs:
			val = getattr (self, attr)
			if val:
				add ("%s: %s" % (attr, val))
		return '\n'.join (s)

	def tabDelimitedRecord (self):
		s=[];add=s.append
		for attr in self.attrs:
			val = getattr (self, attr)
			add (val or "")
		return '\t'.join (s)
	
			
class Users (UserList):
		
	def __init__ (self, dirname):
		UserList.__init__ (self)
		self.dirname = dirname
		# print "Users dirname: ", self.dirname
		for filename in os.listdir (self.dirname):
			path = os.path.join (self.dirname, filename)
			root, ext = os.path.splitext(filename)
			# print 'ext', ext
			if not ext.lower() == ".xml":
				continue
			self.append( User (path) )
			
	def makeAttrList (self, attr):
		"""
		create java expression defining String array containing a value for each user,
		based on provided attribute
		"""
		print '\tstatic String [] %s = new String[] {' % attr
		vals = []
		for user in self:
			val = getattr (user, attr)
			if val:
				vals.append (val)
				
		for i, val in enumerate (vals):
			line = '\t\t"%s"' % val
			if i < len(vals) -1:
				line += ','
			print line
		print "\t};"

	def toTabDelimited (self):
		s = [];add=s.append
		add ('\t'.join (User.attrs))
		for user in self:
			rec = user.tabDelimitedRecord()
			# print rec
			add(rec)
		return '\n'.join (s)
		
if __name__ == '__main__':
	# userdir = "H:/Documents/NSDL/TransitionToLdap/users-2010_03_03"
	userdir = 'test_users'
	print Users(userdir).toTabDelimited()
